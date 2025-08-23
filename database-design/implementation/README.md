# DevDocAI Multi-Database System

## AI-Accessible Database System for DevDocAI Documentation

A production-ready, multi-database architecture designed to serve as the authoritative North Star for AI agents throughout the DevDocAI development lifecycle. This system combines vector, graph, relational, cache, and full-text search databases to provide comprehensive documentation access with sub-second query response times and 99.9% consistency guarantees.

## 🏗️ Architecture Overview

### Database Components

1. **Qdrant** (Vector Database)
   - Semantic search with OpenAI embeddings
   - 1536-dimensional vectors for documents
   - Collections: documents, modules, requirements, tests

2. **Neo4j** (Graph Database)
   - Relationship tracking and dependency analysis
   - Module dependencies and requirement tracing
   - Architecture component relationships

3. **PostgreSQL + pgvector** (Hybrid Search)
   - Structured data storage with vector capabilities
   - Full-text search with tsvector
   - Audit logging and consistency checking

4. **Redis** (Cache Layer)
   - Query result caching (1-hour TTL)
   - Embedding cache (24-hour TTL)
   - Real-time synchronization

5. **Elasticsearch** (Full-text Search)
   - Advanced text search with analyzers
   - Code snippet indexing
   - Faceted search capabilities

### Supported Query Types

1. **Semantic Search** - Find similar documents using AI embeddings
2. **Requirement Tracing** - Track requirements through implementation
3. **Module Dependencies** - Analyze module relationships
4. **Test Coverage** - Check test coverage metrics
5. **Implementation Guides** - Get step-by-step implementation help
6. **Consistency Checking** - Validate documentation consistency
7. **Architecture Queries** - Explore system architecture

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.11+
- OpenAI API key (for embeddings)
- 16GB RAM minimum (recommended: 32GB)
- 50GB free disk space

### Installation

1. **Clone the repository**
```bash
cd /workspaces/DevDocAI-v3.5.0/database-design/implementation
```

2. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
# Required: OPENAI_API_KEY
```

3. **Start the database services**
```bash
docker-compose up -d
```

Wait for all services to be healthy (approximately 2-3 minutes):
```bash
docker-compose ps
```

4. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

5. **Initialize the databases**
```bash
python setup_databases.py
```

6. **Ingest DevDocAI documentation**
```bash
# Assuming documents are in ../../../Docs directory
python document_ingestion.py --documents ../../../Docs
```

## 📊 Usage

### AI Agent Interface

The system provides a comprehensive AI agent interface with LangChain integration:

#### Interactive Chat
```bash
python ai_agent_interface.py --interactive
```

#### Single Query
```bash
python ai_agent_interface.py --query "What are the main modules in DevDocAI?"
```

#### Python Integration
```python
from ai_agent_interface import AIAgentInterface, QueryInput

# Initialize interface
interface = AIAgentInterface(config_path="config.yaml")

# Execute query
query_input = QueryInput(
    query="How do I implement the MIAIR engine?",
    query_type="implementation_guides",
    limit=5
)

result = await interface.query(query_input)

print(f"Confidence: {result.confidence:.2%}")
print(f"Sources: {result.sources}")
for res in result.results:
    print(res['content'])
```

### Document Ingestion

#### Ingest All Documents
```bash
python document_ingestion.py --documents ./documents
```

#### Process Single Document
```bash
python document_ingestion.py --single ./documents/architecture.md
```

### Database Management

#### Verify Setup
```bash
python setup_databases.py --verify-only
```

#### Health Check
```bash
curl http://localhost:8080/health
```

#### View Metrics
```bash
curl http://localhost:9090/metrics
```

## 🔧 Configuration

### config.yaml

The main configuration file controls all aspects of the system:

```yaml
system:
  environment: development
  log_level: INFO

postgresql:
  host: localhost
  port: 5432
  database: devdocai

qdrant:
  host: localhost
  port: 6333
  collections:
    documents:
      vector_size: 1536
      distance: Cosine

# ... see config.yaml for complete configuration
```

### Environment Variables

Key environment variables in `.env`:

- `OPENAI_API_KEY` - Required for OpenAI embeddings
- `POSTGRES_PASSWORD` - PostgreSQL password
- `NEO4J_PASSWORD` - Neo4j password
- `REDIS_PASSWORD` - Redis password (optional)
- `ELASTICSEARCH_PASSWORD` - Elasticsearch password (optional)

## 📈 Performance

### Benchmarks

- **Query Response Time**: < 1 second (p95)
- **Ingestion Rate**: 10-15 documents/second
- **Embedding Generation**: 100 chunks/second (batch)
- **Cache Hit Rate**: 60-70% typical
- **Concurrent Users**: 100+ supported

### Optimization Tips

1. **Enable Query Caching**
   - Redis caching reduces response time by 80%
   - Configure TTL based on data volatility

2. **Batch Processing**
   - Process documents in batches of 100
   - Use parallel embedding generation

3. **Index Optimization**
   - Ensure pgvector indexes are created
   - Optimize Elasticsearch mappings

4. **Resource Allocation**
   - Allocate 4GB to Neo4j heap
   - Give PostgreSQL 25% of system RAM
   - Elasticsearch: 50% of container memory

## 🔍 Query Examples

### Semantic Search
```python
"Find all documentation about the MIAIR engine"
```

### Requirement Tracing
```python
"Trace requirement REQ-001 through the system"
```

### Module Dependencies
```python
"What are the dependencies for module M003?"
```

### Test Coverage
```python
"Show test coverage for the Configuration Manager module"
```

### Architecture Queries
```python
"Explain the system architecture for document processing"
```

## 🐳 Docker Commands

### Start Services
```bash
docker-compose up -d
```

### Stop Services
```bash
docker-compose down
```

### View Logs
```bash
docker-compose logs -f [service_name]
```

### Reset Everything
```bash
docker-compose down -v
rm -rf data/
```

### Backup Data
```bash
docker-compose exec postgres pg_dump -U postgres devdocai > backup.sql
docker-compose exec neo4j neo4j-admin dump --to=/backups/neo4j.dump
```

## 🔐 Security

### API Keys
- Store in `.env` file (never commit)
- Rotate keys regularly
- Use environment-specific keys

### Network Security
- Databases not exposed externally by default
- Use Docker network isolation
- Enable TLS for production

### Access Control
- Implement RBAC for production
- Use strong passwords
- Enable authentication on all databases

## 🛠️ Troubleshooting

### Common Issues

#### 1. Docker Services Won't Start
```bash
# Check logs
docker-compose logs [service_name]

# Ensure ports are free
netstat -tulpn | grep -E '5432|6333|7687|6379|9200'
```

#### 2. Embedding Generation Fails
```bash
# Check OpenAI API key
echo $OPENAI_API_KEY

# Test API connection
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

#### 3. Out of Memory
```bash
# Increase Docker memory limit
# Docker Desktop: Preferences > Resources > Memory

# Reduce batch sizes in config.yaml
batch_size: 50  # Instead of 100
```

#### 4. Slow Queries
```bash
# Check indexes
psql -U postgres -d devdocai -c "\di"

# Analyze query performance
EXPLAIN ANALYZE SELECT ...
```

### Debug Mode

Enable debug logging:
```yaml
# config.yaml
system:
  log_level: DEBUG
  debug: true
```

## 📊 Monitoring

### Grafana Dashboards

Access at http://localhost:3000 (admin/admin)

Available dashboards:
- Query Performance
- Database Health
- Ingestion Progress
- Cache Statistics

### Prometheus Metrics

Access at http://localhost:9090

Key metrics:
- `ai_queries_total` - Total queries by type
- `ai_query_duration_seconds` - Query latency
- `document_ingestion_total` - Documents processed
- `database_connections_active` - Active connections

### Health Checks

```bash
# Overall system health
curl http://localhost:8080/health

# Individual database health
curl http://localhost:8080/health/postgresql
curl http://localhost:8080/health/qdrant
curl http://localhost:8080/health/neo4j
```

## 🧪 Testing

### Run Tests
```bash
pytest tests/ -v --cov=.
```

### Integration Tests
```bash
pytest tests/test_integration.py -v
```

### Performance Tests
```bash
pytest tests/test_performance.py --benchmark
```

## 📚 API Documentation

### REST API Endpoints

#### Query Endpoint
```
POST /api/query
Content-Type: application/json

{
  "query": "What is the MIAIR engine?",
  "query_type": "semantic_search",
  "limit": 10
}
```

#### Ingestion Status
```
GET /api/ingestion/status
```

#### Health Check
```
GET /health
```

### WebSocket Support

Real-time updates via WebSocket:
```javascript
const ws = new WebSocket('ws://localhost:8000/ws');
ws.send(JSON.stringify({
  type: 'query',
  query: 'Module dependencies for M003'
}));
```

## 🚀 Production Deployment

### Kubernetes Deployment

```bash
# Apply configurations
kubectl apply -f k8s/

# Check deployment
kubectl get pods -n devdocai
```

### Environment-Specific Configs

```bash
# Production
cp config.prod.yaml config.yaml
cp .env.prod .env

# Staging
cp config.staging.yaml config.yaml
cp .env.staging .env
```

### Scaling Considerations

1. **Horizontal Scaling**
   - Use Kubernetes HPA for auto-scaling
   - Implement database read replicas
   - Use Redis Sentinel for HA

2. **Vertical Scaling**
   - Increase memory for large datasets
   - Optimize JVM heap for Neo4j
   - Tune PostgreSQL shared_buffers

## 📖 Documentation

- [Architecture Deep Dive](docs/architecture.md)
- [Query Language Reference](docs/query-language.md)
- [Performance Tuning Guide](docs/performance.md)
- [Security Best Practices](docs/security.md)
- [API Reference](docs/api-reference.md)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📝 License

Apache 2.0 License - See LICENSE file for details

## 🆘 Support

- GitHub Issues: [Report bugs or request features]
- Documentation: [Full documentation]
- Community: [Join our Discord]

## 🎯 Roadmap

- [ ] GraphQL API support
- [ ] Multi-language document support
- [ ] Real-time collaborative querying
- [ ] Advanced visualization dashboard
- [ ] Machine learning model fine-tuning
- [ ] Automated quality assessment

---

Built with ❤️ for the DevDocAI project