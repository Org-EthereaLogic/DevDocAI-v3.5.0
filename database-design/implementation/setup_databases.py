#!/usr/bin/env python3
"""
DevDocAI Multi-Database System Setup Script
Production-ready initialization and configuration for hybrid database architecture
Supports vector, graph, relational, cache, and full-text search databases
"""

import os
import sys
import yaml
import json
import asyncio
import logging
import hashlib
import re
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.extras import RealDictCursor
import asyncpg
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance, VectorParams, PointStruct, 
    CollectionStatus, OptimizersConfigDiff,
    HnswConfigDiff, Filter, FieldCondition, MatchValue
)
from neo4j import GraphDatabase, AsyncGraphDatabase
import redis
from redis.sentinel import Sentinel
from elasticsearch import Elasticsearch, AsyncElasticsearch
from elasticsearch.helpers import bulk
import numpy as np
from tqdm import tqdm
from tenacity import retry, stop_after_attempt, wait_exponential
from dotenv import load_dotenv
import structlog
from prometheus_client import Counter, Histogram, Gauge, start_http_server

# Load environment variables
load_dotenv()

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger(__name__)

# Prometheus metrics
setup_counter = Counter('database_setup_total', 'Total database setup attempts', ['database', 'status'])
setup_duration = Histogram('database_setup_duration_seconds', 'Database setup duration', ['database'])
connection_gauge = Gauge('database_connections_active', 'Active database connections', ['database'])

class DatabaseStatus(Enum):
    """Database setup status enumeration"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    VERIFIED = "verified"


@dataclass
class DatabaseConfig:
    """Configuration for database connections"""
    postgresql: Dict[str, Any]
    qdrant: Dict[str, Any]
    neo4j: Dict[str, Any]
    redis: Dict[str, Any]
    elasticsearch: Dict[str, Any]
    embeddings: Dict[str, Any]
    monitoring: Dict[str, Any]
    performance: Dict[str, Any]


class DatabaseSetup:
    """
    Production-ready orchestrator for multi-database system setup
    Handles initialization, configuration, and verification of all database components
    """
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize database setup with configuration
        
        Args:
            config_path: Path to YAML configuration file
        """
        self.config_path = config_path
        self.config = self._load_config()
        self.connections = {}
        self.async_connections = {}
        self.setup_status = {
            "postgresql": DatabaseStatus.NOT_STARTED,
            "qdrant": DatabaseStatus.NOT_STARTED,
            "neo4j": DatabaseStatus.NOT_STARTED,
            "redis": DatabaseStatus.NOT_STARTED,
            "elasticsearch": DatabaseStatus.NOT_STARTED
        }
        self.executor = ThreadPoolExecutor(max_workers=5)
        self._setup_monitoring()
    
    def _load_config(self) -> DatabaseConfig:
        """
        Load configuration from YAML file with environment variable substitution
        
        Returns:
            DatabaseConfig object with all settings
        """
        config_file = Path(self.config_path)
        
        if config_file.exists():
            with open(config_file, 'r') as f:
                raw_config = yaml.safe_load(f)
            
            # Substitute environment variables
            config_str = yaml.dump(raw_config)
            for match in set(re.findall(r'\${([^}]+)}', config_str)):
                parts = match.split(':')
                env_var = parts[0]
                default = parts[1] if len(parts) > 1 else ''
                value = os.getenv(env_var, default)
                config_str = config_str.replace(f'${{{match}}}', str(value))
            
            config = yaml.safe_load(config_str)
        else:
            # Fallback to environment variables
            config = {
                "postgresql": {
                    "host": os.getenv("POSTGRES_HOST", "localhost"),
                    "port": int(os.getenv("POSTGRES_PORT", "5432")),
                    "database": os.getenv("POSTGRES_DB", "devdocai"),
                    "username": os.getenv("POSTGRES_USER", "postgres"),
                    "password": os.getenv("POSTGRES_PASSWORD", "password"),
                    "sslmode": os.getenv("POSTGRES_SSLMODE", "prefer"),
                    "pool": {
                        "min_size": 5,
                        "max_size": 20
                    }
                },
                "qdrant": {
                    "host": os.getenv("QDRANT_HOST", "localhost"),
                    "port": int(os.getenv("QDRANT_PORT", "6333")),
                    "grpc_port": int(os.getenv("QDRANT_GRPC_PORT", "6334")),
                    "api_key": os.getenv("QDRANT_API_KEY", ""),
                    "https": os.getenv("QDRANT_HTTPS", "false").lower() == "true",
                    "collections": {
                        "documents": {
                            "name": "devdocai_documents",
                            "vector_size": 1536,
                            "distance": "Cosine"
                        },
                        "modules": {
                            "name": "devdocai_modules",
                            "vector_size": 1536,
                            "distance": "Cosine"
                        },
                        "requirements": {
                            "name": "devdocai_requirements",
                            "vector_size": 1536,
                            "distance": "Cosine"
                        },
                        "tests": {
                            "name": "devdocai_tests",
                            "vector_size": 768,
                            "distance": "Cosine"
                        }
                    }
                },
                "neo4j": {
                    "uri": os.getenv("NEO4J_URI", "bolt://localhost:7687"),
                    "username": os.getenv("NEO4J_USERNAME", "neo4j"),
                    "password": os.getenv("NEO4J_PASSWORD", "password"),
                    "database": os.getenv("NEO4J_DATABASE", "neo4j"),
                    "max_connection_lifetime": 3600,
                    "max_connection_pool_size": 50
                },
                "redis": {
                    "host": os.getenv("REDIS_HOST", "localhost"),
                    "port": int(os.getenv("REDIS_PORT", "6379")),
                    "password": os.getenv("REDIS_PASSWORD", ""),
                    "db": int(os.getenv("REDIS_DB", "0")),
                    "decode_responses": True,
                    "connection_pool": {
                        "max_connections": 50
                    }
                },
                "elasticsearch": {
                    "hosts": [os.getenv("ELASTICSEARCH_HOST", "http://localhost:9200")],
                    "username": os.getenv("ELASTICSEARCH_USERNAME", ""),
                    "password": os.getenv("ELASTICSEARCH_PASSWORD", ""),
                    "verify_certs": False,
                    "indices": {
                        "documents": {
                            "name": "devdocai-documents",
                            "shards": 2,
                            "replicas": 1
                        },
                        "modules": {
                            "name": "devdocai-modules",
                            "shards": 1,
                            "replicas": 1
                        },
                        "requirements": {
                            "name": "devdocai-requirements",
                            "shards": 1,
                            "replicas": 1
                        }
                    }
                },
                "embeddings": {
                    "provider": os.getenv("EMBEDDING_PROVIDER", "openai"),
                    "openai": {
                        "api_key": os.getenv("OPENAI_API_KEY", ""),
                        "model": "text-embedding-ada-002",
                        "dimensions": 1536
                    },
                    "local": {
                        "model_name": "sentence-transformers/all-MiniLM-L6-v2",
                        "dimensions": 768
                    }
                },
                "monitoring": {
                    "enabled": True,
                    "metrics": {
                        "port": int(os.getenv("METRICS_PORT", "9090"))
                    }
                },
                "performance": {
                    "max_workers": int(os.getenv("MAX_WORKERS", "10")),
                    "batch_size": 100,
                    "async_enabled": True
                }
            }
        
        return DatabaseConfig(**config)
    
    def _setup_monitoring(self):
        """Initialize monitoring and metrics collection"""
        if self.config.monitoring.get("enabled", True):
            metrics_port = self.config.monitoring.get("metrics", {}).get("port", 9090)
            try:
                start_http_server(metrics_port)
                logger.info("metrics_server_started", port=metrics_port)
            except Exception as e:
                logger.warning("metrics_server_failed", error=str(e))
    
    def setup_postgresql(self) -> bool:
        """Set up PostgreSQL with pgvector extension"""
        try:
            logger.info("Setting up PostgreSQL...")
            
            # Connect to PostgreSQL
            conn = psycopg2.connect(
                host=self.config["postgresql"]["host"],
                port=self.config["postgresql"]["port"],
                database="postgres",
                user=self.config["postgresql"]["user"],
                password=self.config["postgresql"]["password"]
            )
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = conn.cursor()
            
            # Create database if not exists
            db_name = self.config["postgresql"]["database"]
            cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
            if not cur.fetchone():
                cur.execute(f"CREATE DATABASE {db_name}")
                logger.info(f"Created database: {db_name}")
            
            cur.close()
            conn.close()
            
            # Connect to the DevDocAI database
            conn = psycopg2.connect(
                host=self.config["postgresql"]["host"],
                port=self.config["postgresql"]["port"],
                database=db_name,
                user=self.config["postgresql"]["user"],
                password=self.config["postgresql"]["password"]
            )
            cur = conn.cursor()
            
            # Enable pgvector extension
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
            
            # Create tables
            sql_schema = """
            -- Documents table
            CREATE TABLE IF NOT EXISTS documents (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                doc_type VARCHAR(50) NOT NULL,
                title VARCHAR(255) NOT NULL,
                version VARCHAR(20) NOT NULL,
                content TEXT,
                content_hash VARCHAR(64),
                status VARCHAR(50),
                phase INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                quality_score DECIMAL(5,2),
                embeddings_generated BOOLEAN DEFAULT FALSE
            );
            
            -- Document sections table
            CREATE TABLE IF NOT EXISTS document_sections (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
                section_number VARCHAR(20),
                title VARCHAR(255),
                content TEXT,
                level INTEGER,
                parent_section_id UUID REFERENCES document_sections(id),
                vector_id VARCHAR(100)
            );
            
            -- Requirements mapping table
            CREATE TABLE IF NOT EXISTS requirements_mapping (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                requirement_id VARCHAR(50) UNIQUE,
                user_story_id VARCHAR(50),
                document_id UUID REFERENCES documents(id),
                module_id VARCHAR(50),
                test_case_id VARCHAR(50),
                implementation_status VARCHAR(50)
            );
            
            -- AI queries table for learning
            CREATE TABLE IF NOT EXISTS ai_queries (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                query TEXT NOT NULL,
                query_embedding VECTOR(768),
                response TEXT,
                sources JSONB,
                confidence DECIMAL(3,2),
                execution_time_ms INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            -- Document relationships table
            CREATE TABLE IF NOT EXISTS document_relationships (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                source_doc_id UUID REFERENCES documents(id),
                target_doc_id UUID REFERENCES documents(id),
                relationship_type VARCHAR(50),
                strength DECIMAL(3,2),
                metadata JSONB
            );
            
            -- Create indexes
            CREATE INDEX IF NOT EXISTS idx_doc_type ON documents(doc_type);
            CREATE INDEX IF NOT EXISTS idx_doc_sections ON document_sections(document_id, section_number);
            CREATE INDEX IF NOT EXISTS idx_req_mapping ON requirements_mapping(requirement_id, user_story_id);
            CREATE INDEX IF NOT EXISTS idx_query_time ON ai_queries(created_at DESC);
            """
            
            cur.execute(sql_schema)
            conn.commit()
            
            logger.info("PostgreSQL setup completed successfully")
            self.connections["postgresql"] = conn
            self.setup_status["postgresql"] = True
            return True
            
        except Exception as e:
            logger.error(f"PostgreSQL setup failed: {e}")
            return False
    
    def setup_qdrant(self) -> bool:
        """Set up Qdrant vector database collections"""
        try:
            logger.info("Setting up Qdrant...")
            
            # Connect to Qdrant
            client = QdrantClient(
                host=self.config["qdrant"]["host"],
                port=self.config["qdrant"]["port"]
            )
            
            # Create main knowledge collection
            collections = [
                {
                    "name": "devdocai_knowledge",
                    "vector_size": 768,
                    "distance": Distance.COSINE
                },
                {
                    "name": "implementation_patterns",
                    "vector_size": 768,
                    "distance": Distance.COSINE
                },
                {
                    "name": "requirement_embeddings",
                    "vector_size": 768,
                    "distance": Distance.COSINE
                }
            ]
            
            for collection in collections:
                # Check if collection exists
                try:
                    client.get_collection(collection["name"])
                    logger.info(f"Collection {collection['name']} already exists")
                except:
                    # Create collection
                    client.create_collection(
                        collection_name=collection["name"],
                        vectors_config=VectorParams(
                            size=collection["vector_size"],
                            distance=collection["distance"]
                        )
                    )
                    logger.info(f"Created collection: {collection['name']}")
            
            self.connections["qdrant"] = client
            self.setup_status["qdrant"] = True
            logger.info("Qdrant setup completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Qdrant setup failed: {e}")
            return False
    
    def setup_neo4j(self) -> bool:
        """Set up Neo4j graph database schema"""
        try:
            logger.info("Setting up Neo4j...")
            
            # Connect to Neo4j
            driver = GraphDatabase.driver(
                self.config["neo4j"]["uri"],
                auth=(
                    self.config["neo4j"]["user"],
                    self.config["neo4j"]["password"]
                )
            )
            
            with driver.session() as session:
                # Create constraints and indexes
                constraints = [
                    "CREATE CONSTRAINT doc_id IF NOT EXISTS FOR (d:Document) REQUIRE d.id IS UNIQUE",
                    "CREATE CONSTRAINT req_id IF NOT EXISTS FOR (r:Requirement) REQUIRE r.id IS UNIQUE",
                    "CREATE CONSTRAINT story_id IF NOT EXISTS FOR (s:UserStory) REQUIRE s.id IS UNIQUE",
                    "CREATE CONSTRAINT module_id IF NOT EXISTS FOR (m:Module) REQUIRE m.id IS UNIQUE",
                    "CREATE CONSTRAINT test_id IF NOT EXISTS FOR (t:TestCase) REQUIRE t.id IS UNIQUE"
                ]
                
                indexes = [
                    "CREATE INDEX doc_type IF NOT EXISTS FOR (d:Document) ON (d.type)",
                    "CREATE INDEX doc_status IF NOT EXISTS FOR (d:Document) ON (d.status)",
                    "CREATE INDEX req_type IF NOT EXISTS FOR (r:Requirement) ON (r.type)",
                    "CREATE INDEX story_epic IF NOT EXISTS FOR (s:UserStory) ON (s.epic)",
                    "CREATE INDEX module_phase IF NOT EXISTS FOR (m:Module) ON (m.phase)"
                ]
                
                for constraint in constraints:
                    try:
                        session.run(constraint)
                        logger.info(f"Created constraint: {constraint.split(' ')[2]}")
                    except Exception as e:
                        if "already exists" not in str(e).lower():
                            raise
                
                for index in indexes:
                    try:
                        session.run(index)
                        logger.info(f"Created index: {index.split(' ')[2]}")
                    except Exception as e:
                        if "already exists" not in str(e).lower():
                            raise
            
            self.connections["neo4j"] = driver
            self.setup_status["neo4j"] = True
            logger.info("Neo4j setup completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Neo4j setup failed: {e}")
            return False
    
    def setup_redis(self) -> bool:
        """Set up Redis for caching"""
        try:
            logger.info("Setting up Redis...")
            
            # Connect to Redis
            r = redis.Redis(
                host=self.config["redis"]["host"],
                port=self.config["redis"]["port"],
                db=self.config["redis"]["db"],
                decode_responses=True
            )
            
            # Test connection
            r.ping()
            
            # Set initial configuration
            cache_config = {
                "semantic_search_ttl": 3600,
                "graph_traversal_ttl": 7200,
                "requirement_trace_ttl": 1800,
                "static_content_ttl": 86400
            }
            
            for key, value in cache_config.items():
                r.set(f"config:{key}", value)
            
            self.connections["redis"] = r
            self.setup_status["redis"] = True
            logger.info("Redis setup completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Redis setup failed: {e}")
            return False
    
    def setup_elasticsearch(self) -> bool:
        """Set up Elasticsearch for full-text search"""
        try:
            logger.info("Setting up Elasticsearch...")
            
            # Connect to Elasticsearch
            es = Elasticsearch(self.config["elasticsearch"]["hosts"])
            
            # Check connection
            if not es.ping():
                raise Exception("Cannot connect to Elasticsearch")
            
            # Create index for documents
            index_settings = {
                "settings": {
                    "number_of_shards": 1,
                    "number_of_replicas": 0,
                    "analysis": {
                        "analyzer": {
                            "code_analyzer": {
                                "type": "custom",
                                "tokenizer": "standard",
                                "filter": ["lowercase", "stop", "snowball"]
                            }
                        }
                    }
                },
                "mappings": {
                    "properties": {
                        "doc_id": {"type": "keyword"},
                        "doc_type": {"type": "keyword"},
                        "title": {"type": "text", "analyzer": "standard"},
                        "content": {"type": "text", "analyzer": "code_analyzer"},
                        "section": {"type": "keyword"},
                        "requirements": {"type": "keyword"},
                        "user_stories": {"type": "keyword"},
                        "modules": {"type": "keyword"},
                        "timestamp": {"type": "date"}
                    }
                }
            }
            
            # Create index if not exists
            if not es.indices.exists(index="devdocai_docs"):
                es.indices.create(index="devdocai_docs", body=index_settings)
                logger.info("Created Elasticsearch index: devdocai_docs")
            
            self.connections["elasticsearch"] = es
            self.setup_status["elasticsearch"] = True
            logger.info("Elasticsearch setup completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Elasticsearch setup failed: {e}")
            return False
    
    def verify_setup(self) -> Dict[str, bool]:
        """Verify all databases are properly set up"""
        logger.info("Verifying database setup...")
        
        verification_results = {}
        
        # Verify PostgreSQL
        try:
            conn = self.connections.get("postgresql")
            if conn:
                cur = conn.cursor()
                cur.execute("SELECT COUNT(*) FROM documents")
                verification_results["postgresql"] = True
        except:
            verification_results["postgresql"] = False
        
        # Verify Qdrant
        try:
            client = self.connections.get("qdrant")
            if client:
                client.get_collection("devdocai_knowledge")
                verification_results["qdrant"] = True
        except:
            verification_results["qdrant"] = False
        
        # Verify Neo4j
        try:
            driver = self.connections.get("neo4j")
            if driver:
                with driver.session() as session:
                    session.run("MATCH (n) RETURN COUNT(n) LIMIT 1")
                verification_results["neo4j"] = True
        except:
            verification_results["neo4j"] = False
        
        # Verify Redis
        try:
            r = self.connections.get("redis")
            if r:
                r.ping()
                verification_results["redis"] = True
        except:
            verification_results["redis"] = False
        
        # Verify Elasticsearch
        try:
            es = self.connections.get("elasticsearch")
            if es:
                es.ping()
                verification_results["elasticsearch"] = True
        except:
            verification_results["elasticsearch"] = False
        
        return verification_results
    
    async def run_setup(self):
        """Run complete database setup"""
        logger.info("Starting DevDocAI Knowledge Base setup...")
        
        # Setup databases in sequence
        setup_functions = [
            self.setup_postgresql,
            self.setup_qdrant,
            self.setup_neo4j,
            self.setup_redis,
            self.setup_elasticsearch
        ]
        
        for setup_func in setup_functions:
            if not setup_func():
                logger.error(f"Setup failed at: {setup_func.__name__}")
                return False
        
        # Verify setup
        verification = self.verify_setup()
        
        logger.info("Setup Status:")
        for db, status in verification.items():
            status_emoji = "✅" if status else "❌"
            logger.info(f"  {status_emoji} {db}: {'Ready' if status else 'Failed'}")
        
        if all(verification.values()):
            logger.info("🎉 All databases set up successfully!")
            return True
        else:
            logger.error("Some databases failed to set up properly")
            return False
    
    def cleanup(self):
        """Close all database connections"""
        logger.info("Cleaning up connections...")
        
        if "postgresql" in self.connections:
            self.connections["postgresql"].close()
        
        if "neo4j" in self.connections:
            self.connections["neo4j"].close()
        
        logger.info("Cleanup completed")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Set up DevDocAI Knowledge Base databases"
    )
    parser.add_argument(
        "--config",
        type=str,
        help="Path to configuration file"
    )
    parser.add_argument(
        "--verify-only",
        action="store_true",
        help="Only verify existing setup"
    )
    
    args = parser.parse_args()
    
    # Create setup instance
    setup = DatabaseSetup(config_path=args.config)
    
    if args.verify_only:
        # Just verify existing setup
        verification = setup.verify_setup()
        for db, status in verification.items():
            print(f"{db}: {'✅ Ready' if status else '❌ Not Ready'}")
    else:
        # Run full setup
        asyncio.run(setup.run_setup())
    
    setup.cleanup()


if __name__ == "__main__":
    main()