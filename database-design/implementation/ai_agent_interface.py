#!/usr/bin/env python3
"""
DevDocAI AI Agent Interface
Production-ready interface for AI agents to query the multi-database system
Supports 7 specialized query types with LangChain integration
"""

import os
import json
import asyncio
import hashlib
from typing import List, Dict, Any, Optional, Tuple, Union
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import time
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import yaml
from langchain.schema import Document, BaseRetriever
from langchain.callbacks.manager import CallbackManagerForRetrieverRun
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain.memory import ConversationSummaryBufferMemory
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.tools import Tool, BaseTool
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.agents.openai_tools.base import create_openai_tools_agent
from langchain_core.messages import HumanMessage, AIMessage
import structlog
from tenacity import retry, stop_after_attempt, wait_exponential
import psycopg2
from psycopg2.extras import RealDictCursor
from qdrant_client import QdrantClient
from neo4j import GraphDatabase
import redis
from elasticsearch import Elasticsearch
from prometheus_client import Counter, Histogram, Gauge
from pydantic import BaseModel, Field

# Configure structured logging
logger = structlog.get_logger(__name__)

# Metrics
query_counter = Counter('ai_queries_total', 'Total AI queries', ['query_type', 'status'])
query_duration = Histogram('ai_query_duration_seconds', 'Query duration', ['query_type'])
cache_hit_rate = Gauge('ai_cache_hit_rate', 'Cache hit rate percentage')


class QueryType(Enum):
    """Specialized query types for DevDocAI"""
    SEMANTIC_SEARCH = "semantic_search"
    REQUIREMENT_TRACING = "requirement_tracing"
    MODULE_DEPENDENCIES = "module_dependencies"
    TEST_COVERAGE = "test_coverage"
    IMPLEMENTATION_GUIDES = "implementation_guides"
    CONSISTENCY_CHECKING = "consistency_checking"
    ARCHITECTURE_QUERIES = "architecture_queries"


@dataclass
class QueryResult:
    """Result from a database query"""
    query_type: QueryType
    query: str
    results: List[Dict[str, Any]]
    metadata: Dict[str, Any]
    confidence: float
    sources: List[str]
    execution_time: float


class QueryInput(BaseModel):
    """Input model for AI queries"""
    query: str = Field(description="The user's query")
    query_type: Optional[str] = Field(default=None, description="Specific query type")
    filters: Optional[Dict[str, Any]] = Field(default={}, description="Additional filters")
    limit: int = Field(default=10, description="Maximum number of results")
    include_context: bool = Field(default=True, description="Include additional context")


class DevDocAIRetriever(BaseRetriever):
    """
    Custom retriever for DevDocAI multi-database system
    Implements intelligent query routing and result fusion
    """
    
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize the retriever with database connections"""
        self.config = self._load_config(config_path)
        self.connections = {}
        self._initialize_connections()
        self._initialize_embeddings()
        self.query_router = QueryRouter(self.config)
        self.result_fusion = ResultFusion(self.config)
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
    
    def _initialize_connections(self):
        """Initialize all database connections"""
        try:
            # PostgreSQL
            self.connections['postgresql'] = psycopg2.connect(
                host=self.config['postgresql']['host'],
                port=self.config['postgresql']['port'],
                database=self.config['postgresql']['database'],
                user=self.config['postgresql']['username'],
                password=self.config['postgresql']['password'],
                cursor_factory=RealDictCursor
            )
            
            # Qdrant
            self.connections['qdrant'] = QdrantClient(
                host=self.config['qdrant']['host'],
                port=self.config['qdrant']['port'],
                api_key=self.config['qdrant'].get('api_key'),
                https=self.config['qdrant'].get('https', False)
            )
            
            # Neo4j
            self.connections['neo4j'] = GraphDatabase.driver(
                self.config['neo4j']['uri'],
                auth=(
                    self.config['neo4j']['username'],
                    self.config['neo4j']['password']
                )
            )
            
            # Redis
            self.connections['redis'] = redis.Redis(
                host=self.config['redis']['host'],
                port=self.config['redis']['port'],
                password=self.config['redis'].get('password', ''),
                db=self.config['redis']['db'],
                decode_responses=True
            )
            
            # Elasticsearch
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
        """Initialize embedding model for queries"""
        if self.config['embeddings']['provider'] == 'openai':
            self.embeddings = OpenAIEmbeddings(
                openai_api_key=self.config['embeddings']['openai']['api_key'],
                model=self.config['embeddings']['openai']['model']
            )
        else:
            from sentence_transformers import SentenceTransformer
            model_name = self.config['embeddings']['local']['model_name']
            self.embeddings = SentenceTransformer(model_name)
    
    def _get_relevant_documents(
        self,
        query: str,
        *,
        run_manager: Optional[CallbackManagerForRetrieverRun] = None,
    ) -> List[Document]:
        """
        Retrieve relevant documents for a query
        
        Args:
            query: User query
            run_manager: Callback manager for tracking
            
        Returns:
            List of relevant documents
        """
        # Detect query type
        query_type = self.query_router.detect_query_type(query)
        
        # Route to appropriate databases
        databases = self.query_router.select_databases(query_type)
        
        # Execute queries in parallel
        results = []
        with ThreadPoolExecutor(max_workers=len(databases)) as executor:
            futures = []
            for db in databases:
                if db == 'qdrant':
                    futures.append(executor.submit(self._search_qdrant, query))
                elif db == 'neo4j':
                    futures.append(executor.submit(self._search_neo4j, query, query_type))
                elif db == 'elasticsearch':
                    futures.append(executor.submit(self._search_elasticsearch, query))
                elif db == 'postgresql':
                    futures.append(executor.submit(self._search_postgresql, query))
            
            for future in futures:
                try:
                    result = future.result(timeout=30)
                    results.extend(result)
                except Exception as e:
                    logger.error("database_query_failed", error=str(e))
        
        # Fuse results
        fused_results = self.result_fusion.fuse(results, query_type)
        
        # Convert to LangChain documents
        documents = []
        for result in fused_results:
            doc = Document(
                page_content=result.get('content', ''),
                metadata=result.get('metadata', {})
            )
            documents.append(doc)
        
        return documents
    
    def _search_qdrant(self, query: str) -> List[Dict[str, Any]]:
        """Search Qdrant vector database"""
        try:
            # Generate query embedding
            if isinstance(self.embeddings, OpenAIEmbeddings):
                query_embedding = self.embeddings.embed_query(query)
            else:
                query_embedding = self.embeddings.encode(query).tolist()
            
            # Search in documents collection
            client = self.connections['qdrant']
            results = client.search(
                collection_name=self.config['qdrant']['collections']['documents']['name'],
                query_vector=query_embedding,
                limit=10,
                with_payload=True
            )
            
            # Format results
            formatted_results = []
            for result in results:
                formatted_results.append({
                    'content': result.payload.get('content', ''),
                    'metadata': result.payload,
                    'score': result.score,
                    'source': 'qdrant'
                })
            
            return formatted_results
            
        except Exception as e:
            logger.error("qdrant_search_failed", error=str(e))
            return []
    
    def _search_neo4j(self, query: str, query_type: QueryType) -> List[Dict[str, Any]]:
        """Search Neo4j graph database"""
        try:
            driver = self.connections['neo4j']
            results = []
            
            with driver.session() as session:
                if query_type == QueryType.MODULE_DEPENDENCIES:
                    cypher = """
                        MATCH (m:Module)-[r:DEPENDS_ON|REFERENCES]->(m2:Module)
                        WHERE m.id CONTAINS $query OR m2.id CONTAINS $query
                        RETURN m.id as source, type(r) as relationship, m2.id as target, 
                               m.phase as source_phase, m2.phase as target_phase
                        LIMIT 20
                    """
                elif query_type == QueryType.REQUIREMENT_TRACING:
                    cypher = """
                        MATCH path = (r:Requirement)-[*1..3]->(n)
                        WHERE r.id CONTAINS $query OR r.title CONTAINS $query
                        RETURN r.id as requirement, 
                               [node in nodes(path) | node.id] as path_nodes,
                               [rel in relationships(path) | type(rel)] as relationships
                        LIMIT 20
                    """
                elif query_type == QueryType.ARCHITECTURE_QUERIES:
                    cypher = """
                        MATCH (d:Document {type: 'architecture'})-[r]->(n)
                        WHERE d.title CONTAINS $query OR d.content CONTAINS $query
                        RETURN d.id as document, d.title as title, 
                               type(r) as relationship, labels(n) as target_type, n.id as target
                        LIMIT 20
                    """
                else:
                    # Generic graph search
                    cypher = """
                        MATCH (n)-[r]->(m)
                        WHERE n.id CONTAINS $query OR n.title CONTAINS $query
                           OR m.id CONTAINS $query OR m.title CONTAINS $query
                        RETURN n.id as source, type(r) as relationship, m.id as target
                        LIMIT 20
                    """
                
                result = session.run(cypher, query=query)
                
                for record in result:
                    results.append({
                        'content': json.dumps(dict(record)),
                        'metadata': dict(record),
                        'score': 0.8,  # Default relevance score
                        'source': 'neo4j'
                    })
            
            return results
            
        except Exception as e:
            logger.error("neo4j_search_failed", error=str(e))
            return []
    
    def _search_elasticsearch(self, query: str) -> List[Dict[str, Any]]:
        """Search Elasticsearch for full-text results"""
        try:
            es = self.connections['elasticsearch']
            
            # Build search query
            search_body = {
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": ["title^2", "content", "tags"],
                        "type": "best_fields",
                        "fuzziness": "AUTO"
                    }
                },
                "highlight": {
                    "fields": {
                        "content": {"fragment_size": 200, "number_of_fragments": 3}
                    }
                },
                "size": 10
            }
            
            # Search
            response = es.search(
                index=self.config['elasticsearch']['indices']['documents']['name'],
                body=search_body
            )
            
            # Format results
            results = []
            for hit in response['hits']['hits']:
                content = hit['_source'].get('content', '')
                if 'highlight' in hit:
                    content = ' ... '.join(hit['highlight'].get('content', [content]))
                
                results.append({
                    'content': content,
                    'metadata': hit['_source'],
                    'score': hit['_score'],
                    'source': 'elasticsearch'
                })
            
            return results
            
        except Exception as e:
            logger.error("elasticsearch_search_failed", error=str(e))
            return []
    
    def _search_postgresql(self, query: str) -> List[Dict[str, Any]]:
        """Search PostgreSQL with pgvector"""
        try:
            conn = self.connections['postgresql']
            cursor = conn.cursor()
            
            # Generate query embedding
            if isinstance(self.embeddings, OpenAIEmbeddings):
                query_embedding = self.embeddings.embed_query(query)
            else:
                query_embedding = self.embeddings.encode(query).tolist()
            
            # Hybrid search with vector similarity and full-text
            sql = """
                WITH vector_search AS (
                    SELECT 
                        document_id,
                        title,
                        content,
                        1 - (embedding <=> %s::vector) as vector_score
                    FROM documents
                    WHERE embedding IS NOT NULL
                    ORDER BY embedding <=> %s::vector
                    LIMIT 20
                ),
                text_search AS (
                    SELECT 
                        document_id,
                        title,
                        content,
                        ts_rank(search_vector, plainto_tsquery('english', %s)) as text_score
                    FROM documents
                    WHERE search_vector @@ plainto_tsquery('english', %s)
                    LIMIT 20
                )
                SELECT 
                    COALESCE(v.document_id, t.document_id) as document_id,
                    COALESCE(v.title, t.title) as title,
                    COALESCE(v.content, t.content) as content,
                    COALESCE(v.vector_score, 0) * 0.7 + COALESCE(t.text_score, 0) * 0.3 as combined_score
                FROM vector_search v
                FULL OUTER JOIN text_search t ON v.document_id = t.document_id
                ORDER BY combined_score DESC
                LIMIT 10
            """
            
            cursor.execute(sql, (query_embedding, query_embedding, query, query))
            rows = cursor.fetchall()
            
            # Format results
            results = []
            for row in rows:
                results.append({
                    'content': row['content'],
                    'metadata': {
                        'document_id': row['document_id'],
                        'title': row['title']
                    },
                    'score': row['combined_score'],
                    'source': 'postgresql'
                })
            
            return results
            
        except Exception as e:
            logger.error("postgresql_search_failed", error=str(e))
            return []


class QueryRouter:
    """Routes queries to appropriate databases based on query type"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.query_patterns = self._initialize_patterns()
    
    def _initialize_patterns(self) -> Dict[QueryType, List[str]]:
        """Initialize patterns for query type detection"""
        return {
            QueryType.SEMANTIC_SEARCH: [
                "search", "find", "look for", "similar", "related"
            ],
            QueryType.REQUIREMENT_TRACING: [
                "requirement", "trace", "implement", "fulfill", "satisfy"
            ],
            QueryType.MODULE_DEPENDENCIES: [
                "depend", "module", "import", "reference", "use"
            ],
            QueryType.TEST_COVERAGE: [
                "test", "coverage", "unit test", "integration", "verify"
            ],
            QueryType.IMPLEMENTATION_GUIDES: [
                "how to", "implement", "build", "create", "develop"
            ],
            QueryType.CONSISTENCY_CHECKING: [
                "consistent", "conflict", "mismatch", "validate", "check"
            ],
            QueryType.ARCHITECTURE_QUERIES: [
                "architecture", "design", "structure", "component", "system"
            ]
        }
    
    def detect_query_type(self, query: str) -> QueryType:
        """
        Detect the type of query based on keywords and patterns
        
        Args:
            query: User query
            
        Returns:
            Detected query type
        """
        query_lower = query.lower()
        
        # Check each pattern
        scores = {}
        for query_type, patterns in self.query_patterns.items():
            score = sum(1 for pattern in patterns if pattern in query_lower)
            scores[query_type] = score
        
        # Return highest scoring type, default to semantic search
        if max(scores.values()) > 0:
            return max(scores, key=scores.get)
        else:
            return QueryType.SEMANTIC_SEARCH
    
    def select_databases(self, query_type: QueryType) -> List[str]:
        """
        Select appropriate databases for a query type
        
        Args:
            query_type: Type of query
            
        Returns:
            List of database names to query
        """
        database_map = {
            QueryType.SEMANTIC_SEARCH: ['qdrant', 'postgresql'],
            QueryType.REQUIREMENT_TRACING: ['neo4j', 'postgresql'],
            QueryType.MODULE_DEPENDENCIES: ['neo4j'],
            QueryType.TEST_COVERAGE: ['neo4j', 'postgresql'],
            QueryType.IMPLEMENTATION_GUIDES: ['elasticsearch', 'qdrant'],
            QueryType.CONSISTENCY_CHECKING: ['neo4j', 'postgresql', 'elasticsearch'],
            QueryType.ARCHITECTURE_QUERIES: ['neo4j', 'elasticsearch']
        }
        
        return database_map.get(query_type, ['qdrant', 'elasticsearch'])


class ResultFusion:
    """Fuses results from multiple databases into unified response"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
    
    def fuse(self, results: List[Dict[str, Any]], query_type: QueryType) -> List[Dict[str, Any]]:
        """
        Fuse results from multiple sources
        
        Args:
            results: Raw results from databases
            query_type: Type of query for context
            
        Returns:
            Fused and ranked results
        """
        if not results:
            return []
        
        # Normalize scores
        normalized_results = self._normalize_scores(results)
        
        # Remove duplicates
        deduplicated = self._deduplicate(normalized_results)
        
        # Apply query-specific ranking
        ranked = self._rank_by_query_type(deduplicated, query_type)
        
        # Sort by final score
        ranked.sort(key=lambda x: x.get('score', 0), reverse=True)
        
        # Limit results
        return ranked[:self.config.get('query', {}).get('default_limit', 10)]
    
    def _normalize_scores(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Normalize scores across different databases"""
        # Group by source
        by_source = {}
        for result in results:
            source = result.get('source', 'unknown')
            if source not in by_source:
                by_source[source] = []
            by_source[source].append(result)
        
        # Normalize within each source
        normalized = []
        for source, source_results in by_source.items():
            if not source_results:
                continue
            
            scores = [r.get('score', 0) for r in source_results]
            max_score = max(scores) if scores else 1
            min_score = min(scores) if scores else 0
            range_score = max_score - min_score if max_score != min_score else 1
            
            for result in source_results:
                result['normalized_score'] = (result.get('score', 0) - min_score) / range_score
                normalized.append(result)
        
        return normalized
    
    def _deduplicate(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate results based on content similarity"""
        seen_hashes = set()
        deduplicated = []
        
        for result in results:
            # Create content hash
            content = result.get('content', '')
            content_hash = hashlib.md5(content[:500].encode()).hexdigest()
            
            if content_hash not in seen_hashes:
                seen_hashes.add(content_hash)
                deduplicated.append(result)
            else:
                # Merge metadata if duplicate
                for existing in deduplicated:
                    existing_hash = hashlib.md5(existing.get('content', '')[:500].encode()).hexdigest()
                    if existing_hash == content_hash:
                        # Keep higher score
                        if result.get('normalized_score', 0) > existing.get('normalized_score', 0):
                            existing['normalized_score'] = result['normalized_score']
                        # Merge sources
                        existing_sources = existing.get('metadata', {}).get('sources', [])
                        new_source = result.get('source')
                        if new_source and new_source not in existing_sources:
                            existing_sources.append(new_source)
                            existing.setdefault('metadata', {})['sources'] = existing_sources
                        break
        
        return deduplicated
    
    def _rank_by_query_type(self, results: List[Dict[str, Any]], query_type: QueryType) -> List[Dict[str, Any]]:
        """Apply query-specific ranking adjustments"""
        # Define source preferences by query type
        source_weights = {
            QueryType.SEMANTIC_SEARCH: {'qdrant': 1.2, 'postgresql': 1.0, 'elasticsearch': 0.8},
            QueryType.REQUIREMENT_TRACING: {'neo4j': 1.3, 'postgresql': 0.9},
            QueryType.MODULE_DEPENDENCIES: {'neo4j': 1.5},
            QueryType.TEST_COVERAGE: {'neo4j': 1.2, 'postgresql': 1.0},
            QueryType.IMPLEMENTATION_GUIDES: {'elasticsearch': 1.2, 'qdrant': 1.0},
            QueryType.CONSISTENCY_CHECKING: {'neo4j': 1.1, 'postgresql': 1.0, 'elasticsearch': 0.9},
            QueryType.ARCHITECTURE_QUERIES: {'neo4j': 1.3, 'elasticsearch': 1.0}
        }
        
        weights = source_weights.get(query_type, {})
        
        for result in results:
            source = result.get('source', 'unknown')
            weight = weights.get(source, 1.0)
            result['score'] = result.get('normalized_score', 0) * weight
        
        return results


class AIAgentInterface:
    """
    Main interface for AI agents to interact with DevDocAI database system
    Provides high-level query capabilities and LangChain integration
    """
    
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize the AI agent interface"""
        self.config = self._load_config(config_path)
        self.retriever = DevDocAIRetriever(config_path)
        self.llm = self._initialize_llm()
        self.memory = self._initialize_memory()
        self.chains = self._initialize_chains()
        self.tools = self._initialize_tools()
        self.agent = self._initialize_agent()
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
    
    def _initialize_llm(self):
        """Initialize the language model"""
        return ChatOpenAI(
            openai_api_key=self.config['embeddings']['openai']['api_key'],
            model_name="gpt-4",
            temperature=0.7,
            max_tokens=2000
        )
    
    def _initialize_memory(self):
        """Initialize conversation memory"""
        return ConversationSummaryBufferMemory(
            llm=self.llm,
            max_token_limit=2000,
            return_messages=True
        )
    
    def _initialize_chains(self):
        """Initialize LangChain chains for different query types"""
        chains = {}
        
        # Retrieval QA chain for general queries
        qa_prompt = PromptTemplate(
            template="""You are an AI assistant for DevDocAI, a comprehensive documentation system.
            Use the following pieces of context to answer the question at the end.
            If you don't know the answer, just say that you don't know, don't try to make up an answer.
            Always cite the sources of your information.
            
            Context: {context}
            
            Question: {question}
            
            Answer:""",
            input_variables=["context", "question"]
        )
        
        chains['retrieval_qa'] = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.retriever,
            chain_type_kwargs={"prompt": qa_prompt}
        )
        
        # Conversational chain for interactive sessions
        chains['conversational'] = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.retriever,
            memory=self.memory,
            verbose=True
        )
        
        return chains
    
    def _initialize_tools(self):
        """Initialize tools for the agent"""
        tools = []
        
        # Semantic search tool
        semantic_search_tool = Tool(
            name="semantic_search",
            func=lambda q: self._execute_semantic_search(q),
            description="Search for documents using semantic similarity. Input should be a search query."
        )
        tools.append(semantic_search_tool)
        
        # Requirement tracing tool
        requirement_tool = Tool(
            name="trace_requirements",
            func=lambda q: self._trace_requirements(q),
            description="Trace requirements through the system. Input should be a requirement ID or description."
        )
        tools.append(requirement_tool)
        
        # Module dependency tool
        module_tool = Tool(
            name="analyze_dependencies",
            func=lambda q: self._analyze_module_dependencies(q),
            description="Analyze module dependencies. Input should be a module ID (e.g., M001)."
        )
        tools.append(module_tool)
        
        # Test coverage tool
        test_tool = Tool(
            name="check_test_coverage",
            func=lambda q: self._check_test_coverage(q),
            description="Check test coverage for modules or requirements. Input should be a module or requirement ID."
        )
        tools.append(test_tool)
        
        # Consistency checking tool
        consistency_tool = Tool(
            name="check_consistency",
            func=lambda q: self._check_consistency(q),
            description="Check for consistency issues in documentation. Input should be a topic or module."
        )
        tools.append(consistency_tool)
        
        return tools
    
    def _initialize_agent(self):
        """Initialize the LangChain agent"""
        # Create agent with tools
        from langchain.agents import initialize_agent, AgentType
        
        agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.OPENAI_FUNCTIONS,
            memory=self.memory,
            verbose=True,
            handle_parsing_errors=True
        )
        
        return agent
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def query(self, query_input: QueryInput) -> QueryResult:
        """
        Execute a query against the multi-database system
        
        Args:
            query_input: Query input parameters
            
        Returns:
            Query result with documents and metadata
        """
        start_time = time.time()
        
        try:
            # Detect or use specified query type
            if query_input.query_type:
                query_type = QueryType(query_input.query_type)
            else:
                query_type = self.retriever.query_router.detect_query_type(query_input.query)
            
            # Check cache first
            cache_key = f"query:{hashlib.md5(f'{query_input.query}:{query_type.value}'.encode()).hexdigest()}"
            cached_result = self._check_cache(cache_key)
            
            if cached_result:
                cache_hit_rate.set(100)
                return cached_result
            
            # Execute query based on type
            if query_type == QueryType.SEMANTIC_SEARCH:
                results = await self._execute_semantic_search_async(query_input)
            elif query_type == QueryType.REQUIREMENT_TRACING:
                results = await self._trace_requirements_async(query_input)
            elif query_type == QueryType.MODULE_DEPENDENCIES:
                results = await self._analyze_module_dependencies_async(query_input)
            elif query_type == QueryType.TEST_COVERAGE:
                results = await self._check_test_coverage_async(query_input)
            elif query_type == QueryType.IMPLEMENTATION_GUIDES:
                results = await self._get_implementation_guides_async(query_input)
            elif query_type == QueryType.CONSISTENCY_CHECKING:
                results = await self._check_consistency_async(query_input)
            elif query_type == QueryType.ARCHITECTURE_QUERIES:
                results = await self._query_architecture_async(query_input)
            else:
                results = await self._execute_semantic_search_async(query_input)
            
            # Calculate execution time
            execution_time = time.time() - start_time
            
            # Create query result
            query_result = QueryResult(
                query_type=query_type,
                query=query_input.query,
                results=results,
                metadata={
                    'filters': query_input.filters,
                    'limit': query_input.limit,
                    'timestamp': datetime.now().isoformat()
                },
                confidence=self._calculate_confidence(results),
                sources=self._extract_sources(results),
                execution_time=execution_time
            )
            
            # Cache result
            self._cache_result(cache_key, query_result)
            
            # Update metrics
            query_counter.labels(query_type=query_type.value, status='success').inc()
            query_duration.labels(query_type=query_type.value).observe(execution_time)
            
            logger.info(
                "query_executed",
                query_type=query_type.value,
                execution_time=execution_time,
                num_results=len(results)
            )
            
            return query_result
            
        except Exception as e:
            query_counter.labels(query_type='unknown', status='failed').inc()
            logger.error("query_execution_failed", error=str(e))
            raise
    
    def _execute_semantic_search(self, query: str) -> str:
        """Execute semantic search"""
        result = self.chains['retrieval_qa'].run(query)
        return result
    
    def _trace_requirements(self, query: str) -> str:
        """Trace requirements through the system"""
        # Use Neo4j to trace requirements
        driver = self.retriever.connections['neo4j']
        
        with driver.session() as session:
            cypher = """
                MATCH path = (r:Requirement)-[*1..5]->(n)
                WHERE r.id = $query OR r.title CONTAINS $query
                RETURN r.id as requirement,
                       r.title as title,
                       [node in nodes(path) | {id: node.id, type: labels(node)[0]}] as trace
                LIMIT 10
            """
            result = session.run(cypher, query=query)
            
            traces = []
            for record in result:
                traces.append({
                    'requirement': record['requirement'],
                    'title': record['title'],
                    'trace': record['trace']
                })
            
            return json.dumps(traces, indent=2)
    
    def _analyze_module_dependencies(self, query: str) -> str:
        """Analyze module dependencies"""
        driver = self.retriever.connections['neo4j']
        
        with driver.session() as session:
            cypher = """
                MATCH (m:Module {id: $query})-[r:DEPENDS_ON|REFERENCES|IMPORTS]->(m2:Module)
                RETURN m.id as module,
                       type(r) as relationship,
                       collect(m2.id) as dependencies
            """
            result = session.run(cypher, query=query)
            
            dependencies = []
            for record in result:
                dependencies.append({
                    'module': record['module'],
                    'relationship': record['relationship'],
                    'dependencies': record['dependencies']
                })
            
            return json.dumps(dependencies, indent=2)
    
    def _check_test_coverage(self, query: str) -> str:
        """Check test coverage for modules or requirements"""
        conn = self.retriever.connections['postgresql']
        cursor = conn.cursor()
        
        sql = """
            SELECT 
                m.module_id,
                m.name,
                COUNT(DISTINCT r.id) as total_requirements,
                COUNT(DISTINCT t.id) as total_tests,
                AVG(t.coverage_percentage) as avg_coverage
            FROM modules m
            LEFT JOIN requirements r ON m.module_id = r.module_id
            LEFT JOIN tests t ON r.requirement_id = t.requirement_id
            WHERE m.module_id = %s OR m.name ILIKE %s
            GROUP BY m.module_id, m.name
        """
        
        cursor.execute(sql, (query, f'%{query}%'))
        results = cursor.fetchall()
        
        coverage = []
        for row in results:
            coverage.append({
                'module': row['module_id'],
                'name': row['name'],
                'requirements': row['total_requirements'],
                'tests': row['total_tests'],
                'coverage': float(row['avg_coverage']) if row['avg_coverage'] else 0
            })
        
        return json.dumps(coverage, indent=2)
    
    def _check_consistency(self, query: str) -> str:
        """Check for consistency issues"""
        # Check multiple databases for conflicting information
        issues = []
        
        # Check for orphaned documents
        conn = self.retriever.connections['postgresql']
        cursor = conn.cursor()
        
        sql = """
            SELECT d.document_id, d.title
            FROM documents d
            LEFT JOIN document_chunks dc ON d.document_id = dc.document_id
            WHERE dc.id IS NULL
        """
        cursor.execute(sql)
        orphaned = cursor.fetchall()
        
        if orphaned:
            issues.append({
                'type': 'orphaned_documents',
                'description': 'Documents without chunks',
                'items': [{'id': r['document_id'], 'title': r['title']} for r in orphaned]
            })
        
        # Check for missing embeddings
        sql = """
            SELECT document_id, title
            FROM documents
            WHERE document_id NOT IN (
                SELECT DISTINCT document_id FROM document_chunks WHERE embedding IS NOT NULL
            )
        """
        cursor.execute(sql)
        missing_embeddings = cursor.fetchall()
        
        if missing_embeddings:
            issues.append({
                'type': 'missing_embeddings',
                'description': 'Documents without embeddings',
                'items': [{'id': r['document_id'], 'title': r['title']} for r in missing_embeddings]
            })
        
        return json.dumps(issues, indent=2)
    
    async def _execute_semantic_search_async(self, query_input: QueryInput) -> List[Dict[str, Any]]:
        """Async semantic search execution"""
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, self._execute_semantic_search, query_input.query)
        return [{'content': result, 'type': 'semantic_search'}]
    
    async def _trace_requirements_async(self, query_input: QueryInput) -> List[Dict[str, Any]]:
        """Async requirement tracing"""
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, self._trace_requirements, query_input.query)
        return [{'content': result, 'type': 'requirement_trace'}]
    
    async def _analyze_module_dependencies_async(self, query_input: QueryInput) -> List[Dict[str, Any]]:
        """Async module dependency analysis"""
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, self._analyze_module_dependencies, query_input.query)
        return [{'content': result, 'type': 'module_dependencies'}]
    
    async def _check_test_coverage_async(self, query_input: QueryInput) -> List[Dict[str, Any]]:
        """Async test coverage check"""
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, self._check_test_coverage, query_input.query)
        return [{'content': result, 'type': 'test_coverage'}]
    
    async def _get_implementation_guides_async(self, query_input: QueryInput) -> List[Dict[str, Any]]:
        """Get implementation guides"""
        # Use retrieval QA chain for implementation guides
        result = self.chains['retrieval_qa'].run(f"How to implement {query_input.query}?")
        return [{'content': result, 'type': 'implementation_guide'}]
    
    async def _check_consistency_async(self, query_input: QueryInput) -> List[Dict[str, Any]]:
        """Async consistency checking"""
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, self._check_consistency, query_input.query)
        return [{'content': result, 'type': 'consistency_check'}]
    
    async def _query_architecture_async(self, query_input: QueryInput) -> List[Dict[str, Any]]:
        """Query architecture information"""
        # Use conversational chain for architecture queries
        result = self.chains['conversational'].run(query_input.query)
        return [{'content': result, 'type': 'architecture_query'}]
    
    def _check_cache(self, cache_key: str) -> Optional[QueryResult]:
        """Check Redis cache for query result"""
        try:
            redis_client = self.retriever.connections['redis']
            cached = redis_client.get(cache_key)
            if cached:
                return QueryResult(**json.loads(cached))
        except Exception as e:
            logger.warning("cache_check_failed", error=str(e))
        return None
    
    def _cache_result(self, cache_key: str, result: QueryResult):
        """Cache query result in Redis"""
        try:
            redis_client = self.retriever.connections['redis']
            redis_client.set(
                cache_key,
                json.dumps(asdict(result), default=str),
                ex=3600  # 1 hour TTL
            )
        except Exception as e:
            logger.warning("cache_write_failed", error=str(e))
    
    def _calculate_confidence(self, results: List[Dict[str, Any]]) -> float:
        """Calculate confidence score for results"""
        if not results:
            return 0.0
        
        # Average score of top results
        scores = [r.get('score', 0) for r in results[:5] if 'score' in r]
        return sum(scores) / len(scores) if scores else 0.5
    
    def _extract_sources(self, results: List[Dict[str, Any]]) -> List[str]:
        """Extract unique sources from results"""
        sources = set()
        for result in results:
            if 'metadata' in result:
                if 'source_path' in result['metadata']:
                    sources.add(result['metadata']['source_path'])
                elif 'document_id' in result['metadata']:
                    sources.add(result['metadata']['document_id'])
        return list(sources)
    
    def chat(self, message: str) -> str:
        """
        Interactive chat interface using the agent
        
        Args:
            message: User message
            
        Returns:
            Agent response
        """
        try:
            response = self.agent.run(message)
            return response
        except Exception as e:
            logger.error("chat_failed", error=str(e))
            return f"I encountered an error processing your request: {str(e)}"
    
    def cleanup(self):
        """Clean up connections"""
        if hasattr(self.retriever, 'connections'):
            for conn_name, conn in self.retriever.connections.items():
                try:
                    if conn_name == 'postgresql':
                        conn.close()
                    elif conn_name == 'neo4j':
                        conn.close()
                except Exception as e:
                    logger.warning(f"cleanup_failed_{conn_name}", error=str(e))


async def main():
    """Main entry point for testing the AI agent interface"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="DevDocAI AI Agent Interface"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="config.yaml",
        help="Path to configuration file"
    )
    parser.add_argument(
        "--query",
        type=str,
        help="Execute a single query"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Start interactive chat session"
    )
    
    args = parser.parse_args()
    
    # Initialize interface
    interface = AIAgentInterface(config_path=args.config)
    
    try:
        if args.query:
            # Execute single query
            query_input = QueryInput(query=args.query)
            result = await interface.query(query_input)
            
            print(f"\n📊 Query Results:")
            print(f"  Query Type: {result.query_type.value}")
            print(f"  Confidence: {result.confidence:.2%}")
            print(f"  Execution Time: {result.execution_time:.2f}s")
            print(f"  Sources: {', '.join(result.sources[:3])}")
            print(f"\n📝 Results:")
            for i, res in enumerate(result.results[:3], 1):
                print(f"\n  {i}. {res.get('content', '')[:200]}...")
        
        elif args.interactive:
            # Interactive chat session
            print("🤖 DevDocAI Interactive Chat")
            print("Type 'exit' to quit\n")
            
            while True:
                message = input("You: ")
                if message.lower() == 'exit':
                    break
                
                response = interface.chat(message)
                print(f"\nAI: {response}\n")
        
        else:
            # Run example queries
            example_queries = [
                "What are the main modules in DevDocAI?",
                "How do I implement the MIAIR engine?",
                "What are the dependencies for module M003?",
                "Show test coverage for the system",
                "Check consistency of documentation"
            ]
            
            print("🧪 Running Example Queries:\n")
            
            for query in example_queries:
                print(f"Query: {query}")
                query_input = QueryInput(query=query)
                result = await interface.query(query_input)
                print(f"  Type: {result.query_type.value}")
                print(f"  Confidence: {result.confidence:.2%}")
                print(f"  Time: {result.execution_time:.2f}s")
                print()
    
    finally:
        interface.cleanup()


if __name__ == "__main__":
    # Run async main
    asyncio.run(main())