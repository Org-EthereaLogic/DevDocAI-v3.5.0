#!/usr/bin/env python3
"""
DevDocAI Database System Main Entry Point
Orchestrates all components of the multi-database documentation system
"""

import os
import sys
import asyncio
import argparse
import logging
from pathlib import Path
from typing import Optional
import yaml

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from pydantic import BaseModel
from prometheus_client import make_asgi_app

# Import system components
from setup_databases import DatabaseSetup
from document_ingestion import DocumentIngestionPipeline
from ai_agent_interface import AIAgentInterface, QueryInput, QueryResult

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="DevDocAI Database System",
    description="Multi-database documentation system with AI agent interface",
    version="3.5.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add Prometheus metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Global instances
db_setup: Optional[DatabaseSetup] = None
ingestion_pipeline: Optional[DocumentIngestionPipeline] = None
ai_interface: Optional[AIAgentInterface] = None


class SystemStatus(BaseModel):
    """System status response model"""
    status: str
    databases: dict
    ingestion: dict
    ai_interface: bool
    version: str


class QueryRequest(BaseModel):
    """Query request model"""
    query: str
    query_type: Optional[str] = None
    limit: int = 10
    filters: dict = {}


class QueryResponse(BaseModel):
    """Query response model"""
    success: bool
    query_type: str
    confidence: float
    results: list
    sources: list
    execution_time: float
    error: Optional[str] = None


class IngestionRequest(BaseModel):
    """Document ingestion request"""
    directory: str
    single_file: Optional[str] = None


@app.on_event("startup")
async def startup_event():
    """Initialize system components on startup"""
    global db_setup, ingestion_pipeline, ai_interface
    
    try:
        logger.info("Initializing DevDocAI Database System...")
        
        # Load configuration
        config_path = os.getenv("CONFIG_PATH", "config.yaml")
        
        # Initialize database setup
        db_setup = DatabaseSetup(config_path)
        
        # Initialize ingestion pipeline
        ingestion_pipeline = DocumentIngestionPipeline(config_path)
        
        # Initialize AI interface
        ai_interface = AIAgentInterface(config_path)
        
        logger.info("System initialization complete")
        
    except Exception as e:
        logger.error(f"Failed to initialize system: {e}")
        sys.exit(1)


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up on shutdown"""
    global db_setup, ingestion_pipeline, ai_interface
    
    try:
        if db_setup:
            db_setup.cleanup()
        
        if ingestion_pipeline:
            ingestion_pipeline.cleanup()
        
        if ai_interface:
            ai_interface.cleanup()
        
        logger.info("System shutdown complete")
        
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "DevDocAI Database System",
        "version": "3.5.0",
        "status": "running",
        "documentation": "/docs",
        "health": "/health",
        "metrics": "/metrics"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check database connections
        verification = db_setup.verify_setup() if db_setup else {}
        
        all_healthy = all(verification.values()) if verification else False
        
        return {
            "status": "healthy" if all_healthy else "degraded",
            "databases": verification,
            "timestamp": asyncio.get_event_loop().time()
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "error": str(e)}
        )


@app.get("/status", response_model=SystemStatus)
async def get_status():
    """Get system status"""
    try:
        # Database status
        db_status = db_setup.verify_setup() if db_setup else {}
        
        # Ingestion status
        ingestion_status = {
            "processed": len(ingestion_pipeline.processed_documents) if ingestion_pipeline else 0,
            "failed": len(ingestion_pipeline.failed_documents) if ingestion_pipeline else 0
        }
        
        # AI interface status
        ai_status = ai_interface is not None
        
        return SystemStatus(
            status="operational",
            databases=db_status,
            ingestion=ingestion_status,
            ai_interface=ai_status,
            version="3.5.0"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/query", response_model=QueryResponse)
async def execute_query(request: QueryRequest):
    """Execute a query against the database system"""
    try:
        if not ai_interface:
            raise HTTPException(status_code=503, detail="AI interface not initialized")
        
        # Create query input
        query_input = QueryInput(
            query=request.query,
            query_type=request.query_type,
            limit=request.limit,
            filters=request.filters
        )
        
        # Execute query
        result = await ai_interface.query(query_input)
        
        return QueryResponse(
            success=True,
            query_type=result.query_type.value,
            confidence=result.confidence,
            results=result.results,
            sources=result.sources,
            execution_time=result.execution_time
        )
        
    except Exception as e:
        logger.error(f"Query execution failed: {e}")
        return QueryResponse(
            success=False,
            query_type="unknown",
            confidence=0.0,
            results=[],
            sources=[],
            execution_time=0.0,
            error=str(e)
        )


@app.post("/api/chat")
async def chat(message: str):
    """Interactive chat endpoint"""
    try:
        if not ai_interface:
            raise HTTPException(status_code=503, detail="AI interface not initialized")
        
        response = ai_interface.chat(message)
        
        return {
            "success": True,
            "message": message,
            "response": response
        }
        
    except Exception as e:
        logger.error(f"Chat failed: {e}")
        return {
            "success": False,
            "message": message,
            "response": f"Error: {str(e)}"
        }


@app.post("/api/ingest")
async def ingest_documents(
    request: IngestionRequest,
    background_tasks: BackgroundTasks
):
    """Ingest documents into the database system"""
    try:
        if not ingestion_pipeline:
            raise HTTPException(status_code=503, detail="Ingestion pipeline not initialized")
        
        # Add ingestion to background tasks
        if request.single_file:
            background_tasks.add_task(
                ingestion_pipeline.process_document,
                Path(request.single_file)
            )
            return {
                "success": True,
                "message": f"Processing single document: {request.single_file}",
                "status": "queued"
            }
        else:
            background_tasks.add_task(
                ingestion_pipeline.ingest_all_documents,
                request.directory
            )
            return {
                "success": True,
                "message": f"Ingesting documents from: {request.directory}",
                "status": "queued"
            }
        
    except Exception as e:
        logger.error(f"Ingestion failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/ingestion/status")
async def get_ingestion_status():
    """Get ingestion pipeline status"""
    try:
        if not ingestion_pipeline:
            raise HTTPException(status_code=503, detail="Ingestion pipeline not initialized")
        
        return {
            "processed": list(ingestion_pipeline.processed_documents),
            "failed": ingestion_pipeline.failed_documents,
            "total_processed": len(ingestion_pipeline.processed_documents),
            "total_failed": len(ingestion_pipeline.failed_documents)
        }
        
    except Exception as e:
        logger.error(f"Failed to get ingestion status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/setup/databases")
async def setup_databases(background_tasks: BackgroundTasks):
    """Initialize database setup"""
    try:
        if not db_setup:
            raise HTTPException(status_code=503, detail="Database setup not initialized")
        
        background_tasks.add_task(db_setup.run_setup)
        
        return {
            "success": True,
            "message": "Database setup initiated",
            "status": "running"
        }
        
    except Exception as e:
        logger.error(f"Database setup failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def run_cli():
    """Run command-line interface"""
    parser = argparse.ArgumentParser(
        description="DevDocAI Database System CLI"
    )
    
    parser.add_argument(
        "command",
        choices=["setup", "ingest", "query", "server", "test"],
        help="Command to execute"
    )
    
    parser.add_argument(
        "--config",
        type=str,
        default="config.yaml",
        help="Path to configuration file"
    )
    
    parser.add_argument(
        "--documents",
        type=str,
        default="./documents",
        help="Path to documents directory (for ingest command)"
    )
    
    parser.add_argument(
        "--query",
        type=str,
        help="Query string (for query command)"
    )
    
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Server port (for server command)"
    )
    
    parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="Server host (for server command)"
    )
    
    args = parser.parse_args()
    
    if args.command == "setup":
        # Run database setup
        logger.info("Running database setup...")
        setup = DatabaseSetup(args.config)
        asyncio.run(setup.run_setup())
        setup.cleanup()
        
    elif args.command == "ingest":
        # Run document ingestion
        logger.info(f"Ingesting documents from {args.documents}...")
        pipeline = DocumentIngestionPipeline(args.config)
        results = asyncio.run(pipeline.ingest_all_documents(args.documents))
        
        print(f"\n📊 Ingestion Results:")
        print(f"  Total Documents: {results['total']}")
        print(f"  Successfully Processed: {results['processed']}")
        print(f"  Failed: {results['failed']}")
        print(f"  Duration: {results['duration']:.2f} seconds")
        
        pipeline.cleanup()
        
    elif args.command == "query":
        # Execute query
        if not args.query:
            print("Error: --query argument required")
            sys.exit(1)
        
        logger.info(f"Executing query: {args.query}")
        interface = AIAgentInterface(args.config)
        
        query_input = QueryInput(query=args.query)
        result = asyncio.run(interface.query(query_input))
        
        print(f"\n📊 Query Results:")
        print(f"  Query Type: {result.query_type.value}")
        print(f"  Confidence: {result.confidence:.2%}")
        print(f"  Execution Time: {result.execution_time:.2f}s")
        print(f"  Sources: {', '.join(result.sources[:3])}")
        print(f"\n📝 Results:")
        for i, res in enumerate(result.results[:3], 1):
            print(f"\n  {i}. {res.get('content', '')[:200]}...")
        
        interface.cleanup()
        
    elif args.command == "server":
        # Run FastAPI server
        logger.info(f"Starting server on {args.host}:{args.port}")
        uvicorn.run(
            "main:app",
            host=args.host,
            port=args.port,
            reload=True,
            log_level="info"
        )
        
    elif args.command == "test":
        # Run system tests
        logger.info("Running system tests...")
        
        # Test database setup
        setup = DatabaseSetup(args.config)
        verification = setup.verify_setup()
        
        print("\n🧪 System Test Results:")
        print("\n📊 Database Status:")
        for db, status in verification.items():
            status_emoji = "✅" if status else "❌"
            print(f"  {status_emoji} {db}: {'Ready' if status else 'Failed'}")
        
        # Test AI interface
        try:
            interface = AIAgentInterface(args.config)
            test_query = QueryInput(query="Test query")
            result = asyncio.run(interface.query(test_query))
            print(f"\n  ✅ AI Interface: Ready (Response time: {result.execution_time:.2f}s)")
            interface.cleanup()
        except Exception as e:
            print(f"\n  ❌ AI Interface: Failed ({str(e)})")
        
        setup.cleanup()


def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        # Run CLI if arguments provided
        run_cli()
    else:
        # Start server by default
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )


if __name__ == "__main__":
    main()