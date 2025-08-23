#!/usr/bin/env python3
"""
DevDocAI Document Ingestion Pipeline
Processes and ingests all documentation into the multi-database system
Supports batch processing, idempotency, and real-time synchronization
"""

import os
import hashlib
import json
import asyncio
import time
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

import numpy as np
from tqdm import tqdm
import yaml
import tiktoken
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document as LangChainDocument
from langchain_openai import OpenAIEmbeddings
from sentence_transformers import SentenceTransformer
import structlog
from tenacity import retry, stop_after_attempt, wait_exponential
import psycopg2
from psycopg2.extras import Json, execute_batch
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from neo4j import GraphDatabase
import redis
from elasticsearch import Elasticsearch, helpers
from prometheus_client import Counter, Histogram, Gauge

# Configure structured logging
logger = structlog.get_logger(__name__)

# Metrics
ingestion_counter = Counter('document_ingestion_total', 'Total documents ingested', ['document_type', 'status'])
chunk_counter = Counter('document_chunks_total', 'Total document chunks created', ['document_type'])
embedding_histogram = Histogram('embedding_generation_seconds', 'Time to generate embeddings', ['model'])
ingestion_gauge = Gauge('ingestion_progress', 'Current ingestion progress percentage')


class DocumentType(Enum):
    """Types of DevDocAI documentation"""
    REQUIREMENTS = "requirements"
    ARCHITECTURE = "architecture"
    API = "api"
    MODULE = "module"
    TESTING = "testing"
    DEPLOYMENT = "deployment"
    USER_GUIDE = "user_guide"
    CONTRIBUTING = "contributing"
    SECURITY = "security"
    PERFORMANCE = "performance"
    CONFIGURATION = "configuration"


@dataclass
class DocumentMetadata:
    """Metadata for ingested documents"""
    document_id: str
    title: str
    type: DocumentType
    source_path: str
    version: str
    created_at: datetime
    updated_at: datetime
    author: Optional[str] = None
    tags: List[str] = None
    module_id: Optional[str] = None
    phase: Optional[int] = None
    checksum: Optional[str] = None
    quality_score: Optional[float] = None


@dataclass
class DocumentChunk:
    """Individual chunk of a document"""
    chunk_id: str
    document_id: str
    content: str
    chunk_index: int
    start_char: int
    end_char: int
    metadata: Dict[str, Any]
    embedding: Optional[np.ndarray] = None


class DocumentIngestionPipeline:
    """
    Production-ready document ingestion pipeline for DevDocAI
    Handles parsing, chunking, embedding generation, and multi-database storage
    """
    
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize the ingestion pipeline with configuration"""
        self.config = self._load_config(config_path)
        self.connections = {}
        self._initialize_connections()
        self._initialize_embeddings()
        self._initialize_text_splitter()
        self.processed_documents = set()
        self.failed_documents = []
        
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
    
    def _initialize_connections(self):
        """Initialize database connections"""
        try:
            # PostgreSQL connection
            self.connections['postgresql'] = psycopg2.connect(
                host=self.config['postgresql']['host'],
                port=self.config['postgresql']['port'],
                database=self.config['postgresql']['database'],
                user=self.config['postgresql']['username'],
                password=self.config['postgresql']['password']
            )
            
            # Qdrant connection
            self.connections['qdrant'] = QdrantClient(
                host=self.config['qdrant']['host'],
                port=self.config['qdrant']['port'],
                api_key=self.config['qdrant'].get('api_key'),
                https=self.config['qdrant'].get('https', False)
            )
            
            # Neo4j connection
            self.connections['neo4j'] = GraphDatabase.driver(
                self.config['neo4j']['uri'],
                auth=(
                    self.config['neo4j']['username'],
                    self.config['neo4j']['password']
                )
            )
            
            # Redis connection
            self.connections['redis'] = redis.Redis(
                host=self.config['redis']['host'],
                port=self.config['redis']['port'],
                password=self.config['redis'].get('password', ''),
                db=self.config['redis']['db'],
                decode_responses=True
            )
            
            # Elasticsearch connection
            self.connections['elasticsearch'] = Elasticsearch(
                self.config['elasticsearch']['hosts'],
                basic_auth=(
                    self.config['elasticsearch'].get('username'),
                    self.config['elasticsearch'].get('password')
                ) if self.config['elasticsearch'].get('username') else None,
                verify_certs=self.config['elasticsearch'].get('verify_certs', False)
            )
            
            logger.info("database_connections_initialized")
            
        except Exception as e:
            logger.error("database_connection_failed", error=str(e))
            raise
    
    def _initialize_embeddings(self):
        """Initialize embedding models"""
        provider = self.config['embeddings']['provider']
        
        if provider == 'openai':
            self.embeddings = OpenAIEmbeddings(
                openai_api_key=self.config['embeddings']['openai']['api_key'],
                model=self.config['embeddings']['openai']['model']
            )
            self.embedding_dimension = self.config['embeddings']['openai']['dimensions']
        else:
            # Local model fallback
            model_name = self.config['embeddings']['local']['model_name']
            self.embeddings = SentenceTransformer(model_name)
            self.embedding_dimension = self.config['embeddings']['local']['dimensions']
        
        logger.info("embeddings_initialized", provider=provider, dimension=self.embedding_dimension)
    
    def _initialize_text_splitter(self):
        """Initialize text splitter for chunking documents"""
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.config['document_processing']['chunk_size'],
            chunk_overlap=self.config['document_processing']['chunk_overlap'],
            separators=self.config['document_processing']['separators'],
            length_function=len
        )
        
        # Initialize tokenizer for accurate token counting
        self.tokenizer = tiktoken.encoding_for_model("gpt-4")
    
    def _calculate_checksum(self, content: str) -> str:
        """Calculate SHA256 checksum of content"""
        return hashlib.sha256(content.encode()).hexdigest()
    
    def _extract_metadata_from_document(self, file_path: Path, content: str) -> DocumentMetadata:
        """Extract metadata from document content and file path"""
        # Determine document type from path or content
        document_type = self._determine_document_type(file_path, content)
        
        # Extract title from first heading or filename
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else file_path.stem.replace('_', ' ').title()
        
        # Generate document ID
        document_id = f"{document_type.value}_{file_path.stem}_{hashlib.md5(str(file_path).encode()).hexdigest()[:8]}"
        
        # Extract module ID if present
        module_match = re.search(r'M(\d{3})', str(file_path))
        module_id = f"M{module_match.group(1)}" if module_match else None
        
        # Determine phase from module ID
        phase = None
        if module_id:
            module_num = int(module_id[1:])
            if module_num <= 7:
                phase = 1
            elif module_num <= 9:
                phase = 2
            elif module_num <= 12:
                phase = 2
            else:
                phase = 3
        
        # Extract tags from content
        tags = self._extract_tags(content)
        
        # Calculate quality score (placeholder - implement actual quality analysis)
        quality_score = self._calculate_quality_score(content)
        
        return DocumentMetadata(
            document_id=document_id,
            title=title,
            type=document_type,
            source_path=str(file_path),
            version="3.5.0",
            created_at=datetime.fromtimestamp(file_path.stat().st_ctime),
            updated_at=datetime.fromtimestamp(file_path.stat().st_mtime),
            tags=tags,
            module_id=module_id,
            phase=phase,
            checksum=self._calculate_checksum(content),
            quality_score=quality_score
        )
    
    def _determine_document_type(self, file_path: Path, content: str) -> DocumentType:
        """Determine document type from file path and content"""
        path_str = str(file_path).lower()
        content_lower = content.lower()
        
        if 'requirement' in path_str or 'prd' in path_str:
            return DocumentType.REQUIREMENTS
        elif 'architecture' in path_str or 'system-design' in path_str:
            return DocumentType.ARCHITECTURE
        elif 'api' in path_str or 'reference' in path_str:
            return DocumentType.API
        elif re.search(r'M\d{3}', str(file_path)):
            return DocumentType.MODULE
        elif 'test' in path_str:
            return DocumentType.TESTING
        elif 'deploy' in path_str or 'installation' in path_str:
            return DocumentType.DEPLOYMENT
        elif 'user' in path_str or 'guide' in path_str:
            return DocumentType.USER_GUIDE
        elif 'contribut' in path_str:
            return DocumentType.CONTRIBUTING
        elif 'security' in path_str:
            return DocumentType.SECURITY
        elif 'performance' in path_str:
            return DocumentType.PERFORMANCE
        elif 'config' in path_str:
            return DocumentType.CONFIGURATION
        else:
            return DocumentType.USER_GUIDE  # Default
    
    def _extract_tags(self, content: str) -> List[str]:
        """Extract tags from document content"""
        tags = []
        
        # Extract from hashtags
        hashtags = re.findall(r'#(\w+)', content)
        tags.extend(hashtags)
        
        # Extract from keywords section
        keywords_match = re.search(r'keywords?:\s*(.+)$', content, re.MULTILINE | re.IGNORECASE)
        if keywords_match:
            keywords = [k.strip() for k in keywords_match.group(1).split(',')]
            tags.extend(keywords)
        
        # Add common technical terms
        tech_terms = ['AI', 'ML', 'API', 'database', 'vector', 'graph', 'cache', 'search']
        for term in tech_terms:
            if term.lower() in content.lower():
                tags.append(term)
        
        return list(set(tags))[:10]  # Return unique tags, max 10
    
    def _calculate_quality_score(self, content: str) -> float:
        """Calculate document quality score (0-100)"""
        score = 50.0  # Base score
        
        # Check for structure
        if re.search(r'^#{1,3}\s+', content, re.MULTILINE):
            score += 10  # Has headings
        
        # Check for code blocks
        if '```' in content:
            score += 10  # Has code examples
        
        # Check for links/references
        if re.search(r'\[.+\]\(.+\)', content):
            score += 5  # Has links
        
        # Check for tables
        if '|' in content and content.count('|') > 10:
            score += 5  # Has tables
        
        # Check for lists
        if re.search(r'^\s*[-*]\s+', content, re.MULTILINE):
            score += 5  # Has lists
        
        # Length check
        word_count = len(content.split())
        if word_count > 500:
            score += 10
        elif word_count > 200:
            score += 5
        
        # Check for metadata
        if re.search(r'^---\n.*\n---', content, re.MULTILINE | re.DOTALL):
            score += 5  # Has frontmatter
        
        return min(score, 100.0)
    
    def _chunk_document(self, content: str, metadata: DocumentMetadata) -> List[DocumentChunk]:
        """Split document into chunks for processing"""
        chunks = []
        
        # Split content into chunks
        text_chunks = self.text_splitter.split_text(content)
        
        for index, chunk_text in enumerate(text_chunks):
            # Find character positions
            start_char = content.find(chunk_text)
            end_char = start_char + len(chunk_text)
            
            # Generate chunk ID
            chunk_id = f"{metadata.document_id}_chunk_{index:04d}"
            
            # Create chunk metadata
            chunk_metadata = {
                "document_id": metadata.document_id,
                "document_type": metadata.type.value,
                "chunk_index": index,
                "total_chunks": len(text_chunks),
                "title": metadata.title,
                "source_path": metadata.source_path,
                "module_id": metadata.module_id,
                "phase": metadata.phase,
                "tags": metadata.tags
            }
            
            chunk = DocumentChunk(
                chunk_id=chunk_id,
                document_id=metadata.document_id,
                content=chunk_text,
                chunk_index=index,
                start_char=start_char,
                end_char=end_char,
                metadata=chunk_metadata
            )
            
            chunks.append(chunk)
        
        logger.info(
            "document_chunked",
            document_id=metadata.document_id,
            num_chunks=len(chunks),
            avg_chunk_size=np.mean([len(c.content) for c in chunks])
        )
        
        return chunks
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def _generate_embeddings(self, chunks: List[DocumentChunk]) -> List[DocumentChunk]:
        """Generate embeddings for document chunks"""
        start_time = time.time()
        
        try:
            # Batch generate embeddings
            texts = [chunk.content for chunk in chunks]
            
            if isinstance(self.embeddings, OpenAIEmbeddings):
                # OpenAI embeddings
                embeddings = self.embeddings.embed_documents(texts)
            else:
                # Local embeddings
                embeddings = self.embeddings.encode(texts, show_progress_bar=False)
            
            # Assign embeddings to chunks
            for chunk, embedding in zip(chunks, embeddings):
                chunk.embedding = np.array(embedding)
            
            duration = time.time() - start_time
            embedding_histogram.labels(model=self.config['embeddings']['provider']).observe(duration)
            
            logger.info(
                "embeddings_generated",
                num_chunks=len(chunks),
                duration=duration,
                model=self.config['embeddings']['provider']
            )
            
            return chunks
            
        except Exception as e:
            logger.error("embedding_generation_failed", error=str(e))
            raise
    
    def _extract_relationships(self, content: str, metadata: DocumentMetadata) -> List[Dict[str, Any]]:
        """Extract relationships between documents and entities"""
        relationships = []
        
        # Extract module dependencies
        module_refs = re.findall(r'M\d{3}', content)
        for ref in module_refs:
            if ref != metadata.module_id:
                relationships.append({
                    "source_id": metadata.document_id,
                    "source_type": "document",
                    "target_id": ref,
                    "target_type": "module",
                    "relationship_type": "REFERENCES",
                    "strength": 0.8
                })
        
        # Extract requirement references
        req_refs = re.findall(r'REQ-\d+', content)
        for ref in req_refs:
            relationships.append({
                "source_id": metadata.document_id,
                "source_type": "document",
                "target_id": ref,
                "target_type": "requirement",
                "relationship_type": "IMPLEMENTS",
                "strength": 0.9
            })
        
        # Extract test references
        test_refs = re.findall(r'TEST-\d+', content)
        for ref in test_refs:
            relationships.append({
                "source_id": metadata.document_id,
                "source_type": "document",
                "target_id": ref,
                "target_type": "test",
                "relationship_type": "TESTS",
                "strength": 0.85
            })
        
        # Extract API references
        api_refs = re.findall(r'/api/[a-z0-9\-/]+', content)
        for ref in api_refs:
            relationships.append({
                "source_id": metadata.document_id,
                "source_type": "document",
                "target_id": ref,
                "target_type": "api_endpoint",
                "relationship_type": "DEFINES",
                "strength": 0.75
            })
        
        return relationships
    
    async def _store_in_postgresql(self, metadata: DocumentMetadata, chunks: List[DocumentChunk]):
        """Store document and chunks in PostgreSQL"""
        conn = self.connections['postgresql']
        cursor = conn.cursor()
        
        try:
            # Insert document metadata
            insert_doc = """
                INSERT INTO documents (
                    document_id, title, content, document_type, source_path,
                    metadata, created_at, updated_at, version, checksum, tags
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (document_id) DO UPDATE SET
                    updated_at = EXCLUDED.updated_at,
                    checksum = EXCLUDED.checksum
            """
            
            # Combine all chunks for full content
            full_content = "\n\n".join([chunk.content for chunk in chunks])
            
            cursor.execute(insert_doc, (
                metadata.document_id,
                metadata.title,
                full_content,
                metadata.type.value,
                metadata.source_path,
                Json(asdict(metadata)),
                metadata.created_at,
                metadata.updated_at,
                metadata.version,
                metadata.checksum,
                metadata.tags
            ))
            
            # Insert chunks
            insert_chunk = """
                INSERT INTO document_chunks (
                    document_id, chunk_index, content, embedding, metadata
                ) VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (document_id, chunk_index) DO UPDATE SET
                    content = EXCLUDED.content,
                    embedding = EXCLUDED.embedding
            """
            
            chunk_data = [
                (
                    chunk.document_id,
                    chunk.chunk_index,
                    chunk.content,
                    chunk.embedding.tolist() if chunk.embedding is not None else None,
                    Json(chunk.metadata)
                )
                for chunk in chunks
            ]
            
            execute_batch(cursor, insert_chunk, chunk_data)
            
            conn.commit()
            logger.info("postgresql_storage_complete", document_id=metadata.document_id)
            
        except Exception as e:
            conn.rollback()
            logger.error("postgresql_storage_failed", error=str(e))
            raise
    
    async def _store_in_qdrant(self, metadata: DocumentMetadata, chunks: List[DocumentChunk]):
        """Store embeddings in Qdrant vector database"""
        client = self.connections['qdrant']
        
        try:
            # Determine collection based on document type
            collection_map = {
                DocumentType.MODULE: "modules",
                DocumentType.REQUIREMENTS: "requirements",
                DocumentType.TESTING: "tests",
            }
            collection_name = self.config['qdrant']['collections'].get(
                collection_map.get(metadata.type, "documents"),
                {}
            ).get('name', 'devdocai_documents')
            
            # Prepare points for insertion
            points = []
            for chunk in chunks:
                if chunk.embedding is not None:
                    point = PointStruct(
                        id=hashlib.md5(chunk.chunk_id.encode()).hexdigest(),
                        vector=chunk.embedding.tolist(),
                        payload={
                            **chunk.metadata,
                            "chunk_id": chunk.chunk_id,
                            "content": chunk.content[:1000],  # Store first 1000 chars
                            "document_id": metadata.document_id,
                            "quality_score": metadata.quality_score
                        }
                    )
                    points.append(point)
            
            # Batch upsert points
            if points:
                client.upsert(
                    collection_name=collection_name,
                    points=points,
                    wait=True
                )
                logger.info(
                    "qdrant_storage_complete",
                    document_id=metadata.document_id,
                    collection=collection_name,
                    num_points=len(points)
                )
            
        except Exception as e:
            logger.error("qdrant_storage_failed", error=str(e))
            raise
    
    async def _store_in_neo4j(self, metadata: DocumentMetadata, relationships: List[Dict[str, Any]]):
        """Store document nodes and relationships in Neo4j"""
        driver = self.connections['neo4j']
        
        try:
            with driver.session() as session:
                # Create document node
                create_doc = """
                    MERGE (d:Document {id: $doc_id})
                    SET d.title = $title,
                        d.type = $doc_type,
                        d.source_path = $source_path,
                        d.version = $version,
                        d.module_id = $module_id,
                        d.phase = $phase,
                        d.quality_score = $quality_score,
                        d.created_at = $created_at,
                        d.updated_at = $updated_at,
                        d.tags = $tags
                """
                
                session.run(create_doc, {
                    "doc_id": metadata.document_id,
                    "title": metadata.title,
                    "doc_type": metadata.type.value,
                    "source_path": metadata.source_path,
                    "version": metadata.version,
                    "module_id": metadata.module_id,
                    "phase": metadata.phase,
                    "quality_score": metadata.quality_score,
                    "created_at": metadata.created_at.isoformat(),
                    "updated_at": metadata.updated_at.isoformat(),
                    "tags": metadata.tags
                })
                
                # Create module node if applicable
                if metadata.module_id:
                    create_module = """
                        MERGE (m:Module {id: $module_id})
                        SET m.phase = $phase
                        WITH m
                        MATCH (d:Document {id: $doc_id})
                        MERGE (d)-[:BELONGS_TO]->(m)
                    """
                    session.run(create_module, {
                        "module_id": metadata.module_id,
                        "phase": metadata.phase,
                        "doc_id": metadata.document_id
                    })
                
                # Create relationships
                for rel in relationships:
                    create_rel = f"""
                        MERGE (source:{rel['source_type'].title()} {{id: $source_id}})
                        MERGE (target:{rel['target_type'].title()} {{id: $target_id}})
                        MERGE (source)-[r:{rel['relationship_type']}]->(target)
                        SET r.strength = $strength
                    """
                    session.run(create_rel, {
                        "source_id": rel['source_id'],
                        "target_id": rel['target_id'],
                        "strength": rel['strength']
                    })
                
                logger.info(
                    "neo4j_storage_complete",
                    document_id=metadata.document_id,
                    num_relationships=len(relationships)
                )
                
        except Exception as e:
            logger.error("neo4j_storage_failed", error=str(e))
            raise
    
    async def _store_in_elasticsearch(self, metadata: DocumentMetadata, chunks: List[DocumentChunk]):
        """Store document in Elasticsearch for full-text search"""
        es = self.connections['elasticsearch']
        
        try:
            # Determine index based on document type
            index_map = {
                DocumentType.MODULE: "modules",
                DocumentType.REQUIREMENTS: "requirements",
            }
            index_name = self.config['elasticsearch']['indices'].get(
                index_map.get(metadata.type, "documents"),
                {}
            ).get('name', 'devdocai-documents')
            
            # Prepare documents for bulk indexing
            actions = []
            
            # Index main document
            doc = {
                "_index": index_name,
                "_id": metadata.document_id,
                "_source": {
                    "document_id": metadata.document_id,
                    "title": metadata.title,
                    "content": "\n\n".join([chunk.content for chunk in chunks]),
                    "document_type": metadata.type.value,
                    "source_path": metadata.source_path,
                    "module_id": metadata.module_id,
                    "phase": metadata.phase,
                    "tags": metadata.tags,
                    "quality_score": metadata.quality_score,
                    "created_at": metadata.created_at.isoformat(),
                    "updated_at": metadata.updated_at.isoformat(),
                    "version": metadata.version
                }
            }
            actions.append(doc)
            
            # Index chunks separately for better search granularity
            for chunk in chunks:
                chunk_doc = {
                    "_index": f"{index_name}-chunks",
                    "_id": chunk.chunk_id,
                    "_source": {
                        "chunk_id": chunk.chunk_id,
                        "document_id": metadata.document_id,
                        "content": chunk.content,
                        "chunk_index": chunk.chunk_index,
                        **chunk.metadata
                    }
                }
                actions.append(chunk_doc)
            
            # Bulk index
            success, failed = helpers.bulk(es, actions, raise_on_error=False)
            
            if failed:
                logger.warning(
                    "elasticsearch_partial_failure",
                    document_id=metadata.document_id,
                    success=success,
                    failed=len(failed)
                )
            else:
                logger.info(
                    "elasticsearch_storage_complete",
                    document_id=metadata.document_id,
                    index=index_name,
                    num_docs=len(actions)
                )
                
        except Exception as e:
            logger.error("elasticsearch_storage_failed", error=str(e))
            raise
    
    async def _cache_in_redis(self, metadata: DocumentMetadata, chunks: List[DocumentChunk]):
        """Cache frequently accessed data in Redis"""
        redis_client = self.connections['redis']
        
        try:
            # Cache document metadata
            metadata_key = f"doc:{metadata.document_id}:metadata"
            redis_client.hset(
                metadata_key,
                mapping={
                    "title": metadata.title,
                    "type": metadata.type.value,
                    "source_path": metadata.source_path,
                    "module_id": metadata.module_id or "",
                    "phase": str(metadata.phase) if metadata.phase else "",
                    "quality_score": str(metadata.quality_score),
                    "checksum": metadata.checksum
                }
            )
            redis_client.expire(metadata_key, 86400)  # 24 hours TTL
            
            # Cache chunk embeddings for fast retrieval
            for chunk in chunks:
                if chunk.embedding is not None:
                    embedding_key = f"embed:{chunk.chunk_id}"
                    redis_client.set(
                        embedding_key,
                        json.dumps(chunk.embedding.tolist()),
                        ex=86400  # 24 hours TTL
                    )
            
            # Add to document index
            redis_client.sadd(f"docs:{metadata.type.value}", metadata.document_id)
            
            # Update ingestion timestamp
            redis_client.set(
                f"doc:{metadata.document_id}:ingested_at",
                datetime.now().isoformat(),
                ex=86400
            )
            
            logger.info("redis_caching_complete", document_id=metadata.document_id)
            
        except Exception as e:
            logger.error("redis_caching_failed", error=str(e))
            # Non-critical failure, continue processing
    
    async def process_document(self, file_path: Path) -> bool:
        """
        Process a single document through the entire pipeline
        
        Args:
            file_path: Path to the document file
            
        Returns:
            Boolean indicating success
        """
        try:
            # Check if already processed
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            checksum = self._calculate_checksum(content)
            
            # Check Redis for existing checksum
            redis_client = self.connections['redis']
            existing_checksum = redis_client.get(f"checksum:{file_path.stem}")
            
            if existing_checksum and existing_checksum == checksum:
                logger.info("document_already_processed", file=str(file_path))
                return True
            
            # Extract metadata
            metadata = self._extract_metadata_from_document(file_path, content)
            
            # Chunk document
            chunks = self._chunk_document(content, metadata)
            
            # Generate embeddings
            chunks = self._generate_embeddings(chunks)
            
            # Extract relationships
            relationships = self._extract_relationships(content, metadata)
            
            # Store in all databases (parallel execution)
            tasks = [
                self._store_in_postgresql(metadata, chunks),
                self._store_in_qdrant(metadata, chunks),
                self._store_in_neo4j(metadata, relationships),
                self._store_in_elasticsearch(metadata, chunks),
                self._cache_in_redis(metadata, chunks)
            ]
            
            await asyncio.gather(*tasks, return_exceptions=True)
            
            # Update checksum in Redis
            redis_client.set(f"checksum:{file_path.stem}", checksum, ex=604800)  # 7 days
            
            # Update metrics
            ingestion_counter.labels(
                document_type=metadata.type.value,
                status="success"
            ).inc()
            chunk_counter.labels(document_type=metadata.type.value).inc(len(chunks))
            
            self.processed_documents.add(metadata.document_id)
            
            logger.info(
                "document_processed_successfully",
                document_id=metadata.document_id,
                chunks=len(chunks),
                relationships=len(relationships)
            )
            
            return True
            
        except Exception as e:
            logger.error(
                "document_processing_failed",
                file=str(file_path),
                error=str(e)
            )
            ingestion_counter.labels(
                document_type="unknown",
                status="failed"
            ).inc()
            self.failed_documents.append(str(file_path))
            return False
    
    async def ingest_all_documents(self, documents_dir: str = "./documents"):
        """
        Ingest all DevDocAI documentation files
        
        Args:
            documents_dir: Directory containing documentation files
        """
        start_time = time.time()
        documents_path = Path(documents_dir)
        
        # Find all markdown files
        document_files = list(documents_path.rglob("*.md"))
        
        logger.info(
            "starting_document_ingestion",
            num_documents=len(document_files),
            directory=documents_dir
        )
        
        # Process documents in batches
        batch_size = self.config['performance']['batch_processing']['batch_size']
        
        for i in range(0, len(document_files), batch_size):
            batch = document_files[i:i+batch_size]
            
            # Process batch concurrently
            tasks = [self.process_document(file_path) for file_path in batch]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Update progress
            progress = ((i + len(batch)) / len(document_files)) * 100
            ingestion_gauge.set(progress)
            
            logger.info(
                "batch_processed",
                batch_num=i // batch_size + 1,
                processed=len([r for r in results if r is True]),
                failed=len([r for r in results if r is False]),
                progress=f"{progress:.1f}%"
            )
        
        # Final statistics
        duration = time.time() - start_time
        
        logger.info(
            "ingestion_complete",
            total_documents=len(document_files),
            processed=len(self.processed_documents),
            failed=len(self.failed_documents),
            duration=f"{duration:.2f}s",
            documents_per_second=len(self.processed_documents) / duration if duration > 0 else 0
        )
        
        # Print failed documents if any
        if self.failed_documents:
            logger.warning(
                "failed_documents",
                files=self.failed_documents
            )
        
        return {
            "total": len(document_files),
            "processed": len(self.processed_documents),
            "failed": len(self.failed_documents),
            "duration": duration
        }
    
    def cleanup(self):
        """Clean up database connections"""
        if 'postgresql' in self.connections:
            self.connections['postgresql'].close()
        
        if 'neo4j' in self.connections:
            self.connections['neo4j'].close()
        
        logger.info("connections_cleaned_up")


async def main():
    """Main entry point for document ingestion"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Ingest DevDocAI documentation into multi-database system"
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
        help="Path to documents directory"
    )
    parser.add_argument(
        "--single",
        type=str,
        help="Process a single document file"
    )
    
    args = parser.parse_args()
    
    # Initialize pipeline
    pipeline = DocumentIngestionPipeline(config_path=args.config)
    
    try:
        if args.single:
            # Process single document
            result = await pipeline.process_document(Path(args.single))
            print(f"Document processed: {'✅' if result else '❌'}")
        else:
            # Process all documents
            results = await pipeline.ingest_all_documents(args.documents)
            print(f"\n📊 Ingestion Results:")
            print(f"  Total Documents: {results['total']}")
            print(f"  Successfully Processed: {results['processed']} ✅")
            print(f"  Failed: {results['failed']} ❌")
            print(f"  Duration: {results['duration']:.2f} seconds")
            print(f"  Rate: {results['processed'] / results['duration']:.2f} docs/second")
    
    finally:
        pipeline.cleanup()


if __name__ == "__main__":
    # Run async main
    asyncio.run(main())