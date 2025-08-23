-- DevDocAI PostgreSQL Initialization Script
-- Creates database schema with pgvector extension

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS btree_gin;

-- Create schema
CREATE SCHEMA IF NOT EXISTS devdocai;
SET search_path TO devdocai, public;

-- Documents table with vector embeddings
CREATE TABLE IF NOT EXISTS documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    document_id VARCHAR(255) UNIQUE NOT NULL,
    title VARCHAR(500) NOT NULL,
    content TEXT NOT NULL,
    document_type VARCHAR(100) NOT NULL,
    source_path VARCHAR(500),
    metadata JSONB DEFAULT '{}',
    embedding vector(1536),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    version INTEGER DEFAULT 1,
    checksum VARCHAR(64),
    is_active BOOLEAN DEFAULT true,
    tags TEXT[] DEFAULT '{}',
    search_vector tsvector GENERATED ALWAYS AS (
        setweight(to_tsvector('english', coalesce(title, '')), 'A') ||
        setweight(to_tsvector('english', coalesce(content, '')), 'B')
    ) STORED
);

-- Modules table
CREATE TABLE IF NOT EXISTS modules (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    module_id VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    phase INTEGER NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    dependencies JSONB DEFAULT '[]',
    metadata JSONB DEFAULT '{}',
    embedding vector(1536),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    implementation_status VARCHAR(50) DEFAULT 'not_started',
    complexity_score DECIMAL(3,2),
    priority INTEGER DEFAULT 5,
    CHECK (phase BETWEEN 1 AND 4),
    CHECK (priority BETWEEN 1 AND 10)
);

-- Requirements table
CREATE TABLE IF NOT EXISTS requirements (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    requirement_id VARCHAR(100) UNIQUE NOT NULL,
    title VARCHAR(500) NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(100) NOT NULL,
    priority VARCHAR(20) NOT NULL,
    status VARCHAR(50) DEFAULT 'draft',
    module_id VARCHAR(50) REFERENCES modules(module_id),
    parent_id UUID REFERENCES requirements(id),
    metadata JSONB DEFAULT '{}',
    embedding vector(1536),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    acceptance_criteria JSONB DEFAULT '[]',
    verification_method VARCHAR(100),
    CHECK (priority IN ('critical', 'high', 'medium', 'low'))
);

-- Tests table
CREATE TABLE IF NOT EXISTS tests (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    test_id VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(500) NOT NULL,
    description TEXT,
    test_type VARCHAR(50) NOT NULL,
    module_id VARCHAR(50) REFERENCES modules(module_id),
    requirement_id VARCHAR(100) REFERENCES requirements(requirement_id),
    test_data JSONB DEFAULT '{}',
    expected_result TEXT,
    actual_result TEXT,
    status VARCHAR(50) DEFAULT 'pending',
    metadata JSONB DEFAULT '{}',
    embedding vector(1536),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    execution_time_ms INTEGER,
    coverage_percentage DECIMAL(5,2),
    CHECK (test_type IN ('unit', 'integration', 'e2e', 'performance', 'security'))
);

-- Audit log table
CREATE TABLE IF NOT EXISTS audit_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    entity_type VARCHAR(50) NOT NULL,
    entity_id VARCHAR(255) NOT NULL,
    action VARCHAR(50) NOT NULL,
    user_id VARCHAR(255),
    changes JSONB DEFAULT '{}',
    metadata JSONB DEFAULT '{}',
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Embeddings cache table
CREATE TABLE IF NOT EXISTS embeddings_cache (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    content_hash VARCHAR(64) UNIQUE NOT NULL,
    model_name VARCHAR(100) NOT NULL,
    embedding vector(1536),
    dimension INTEGER NOT NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    accessed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    access_count INTEGER DEFAULT 1
);

-- Document chunks table for better retrieval
CREATE TABLE IF NOT EXISTS document_chunks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    document_id VARCHAR(255) REFERENCES documents(document_id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,
    embedding vector(1536),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(document_id, chunk_index)
);

-- Relationships table for cross-references
CREATE TABLE IF NOT EXISTS relationships (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_type VARCHAR(50) NOT NULL,
    source_id VARCHAR(255) NOT NULL,
    target_type VARCHAR(50) NOT NULL,
    target_id VARCHAR(255) NOT NULL,
    relationship_type VARCHAR(100) NOT NULL,
    strength DECIMAL(3,2) DEFAULT 1.0,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(source_type, source_id, target_type, target_id, relationship_type),
    CHECK (strength BETWEEN 0 AND 1)
);

-- Query cache table
CREATE TABLE IF NOT EXISTS query_cache (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    query_hash VARCHAR(64) UNIQUE NOT NULL,
    query_type VARCHAR(50) NOT NULL,
    query_params JSONB NOT NULL,
    results JSONB NOT NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    hit_count INTEGER DEFAULT 0
);

-- Create indexes for better performance
CREATE INDEX idx_documents_embedding ON documents USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
CREATE INDEX idx_documents_search ON documents USING GIN (search_vector);
CREATE INDEX idx_documents_metadata ON documents USING GIN (metadata);
CREATE INDEX idx_documents_type ON documents (document_type);
CREATE INDEX idx_documents_created ON documents (created_at DESC);
CREATE INDEX idx_documents_tags ON documents USING GIN (tags);

CREATE INDEX idx_modules_embedding ON modules USING ivfflat (embedding vector_cosine_ops) WITH (lists = 50);
CREATE INDEX idx_modules_status ON modules (status);
CREATE INDEX idx_modules_phase ON modules (phase);
CREATE INDEX idx_modules_priority ON modules (priority DESC);

CREATE INDEX idx_requirements_embedding ON requirements USING ivfflat (embedding vector_cosine_ops) WITH (lists = 50);
CREATE INDEX idx_requirements_category ON requirements (category);
CREATE INDEX idx_requirements_priority ON requirements (priority);
CREATE INDEX idx_requirements_status ON requirements (status);
CREATE INDEX idx_requirements_module ON requirements (module_id);

CREATE INDEX idx_tests_embedding ON tests USING ivfflat (embedding vector_cosine_ops) WITH (lists = 50);
CREATE INDEX idx_tests_type ON tests (test_type);
CREATE INDEX idx_tests_status ON tests (status);
CREATE INDEX idx_tests_module ON tests (module_id);
CREATE INDEX idx_tests_requirement ON tests (requirement_id);

CREATE INDEX idx_audit_entity ON audit_log (entity_type, entity_id);
CREATE INDEX idx_audit_created ON audit_log (created_at DESC);
CREATE INDEX idx_audit_user ON audit_log (user_id);

CREATE INDEX idx_embeddings_cache_hash ON embeddings_cache (content_hash);
CREATE INDEX idx_embeddings_cache_model ON embeddings_cache (model_name);

CREATE INDEX idx_chunks_document ON document_chunks (document_id);
CREATE INDEX idx_chunks_embedding ON document_chunks USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

CREATE INDEX idx_relationships_source ON relationships (source_type, source_id);
CREATE INDEX idx_relationships_target ON relationships (target_type, target_id);
CREATE INDEX idx_relationships_type ON relationships (relationship_type);

CREATE INDEX idx_query_cache_hash ON query_cache (query_hash);
CREATE INDEX idx_query_cache_expires ON query_cache (expires_at);

-- Create triggers for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_documents_updated_at BEFORE UPDATE ON documents
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_modules_updated_at BEFORE UPDATE ON modules
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_requirements_updated_at BEFORE UPDATE ON requirements
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_tests_updated_at BEFORE UPDATE ON tests
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Create function for semantic search
CREATE OR REPLACE FUNCTION semantic_search(
    query_embedding vector(1536),
    search_type VARCHAR,
    limit_count INTEGER DEFAULT 10
)
RETURNS TABLE (
    id UUID,
    content TEXT,
    similarity FLOAT,
    metadata JSONB
) AS $$
BEGIN
    IF search_type = 'documents' THEN
        RETURN QUERY
        SELECT d.id, d.content, 1 - (d.embedding <=> query_embedding) as similarity, d.metadata
        FROM documents d
        WHERE d.is_active = true
        ORDER BY d.embedding <=> query_embedding
        LIMIT limit_count;
    ELSIF search_type = 'modules' THEN
        RETURN QUERY
        SELECT m.id, m.description, 1 - (m.embedding <=> query_embedding) as similarity, m.metadata
        FROM modules m
        ORDER BY m.embedding <=> query_embedding
        LIMIT limit_count;
    ELSIF search_type = 'requirements' THEN
        RETURN QUERY
        SELECT r.id, r.description, 1 - (r.embedding <=> query_embedding) as similarity, r.metadata
        FROM requirements r
        ORDER BY r.embedding <=> query_embedding
        LIMIT limit_count;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Create materialized view for document statistics
CREATE MATERIALIZED VIEW IF NOT EXISTS document_stats AS
SELECT
    document_type,
    COUNT(*) as document_count,
    AVG(LENGTH(content)) as avg_content_length,
    MAX(updated_at) as last_updated,
    COUNT(DISTINCT tags) as unique_tags
FROM documents
WHERE is_active = true
GROUP BY document_type;

CREATE INDEX idx_document_stats_type ON document_stats (document_type);

-- Create view for test coverage
CREATE OR REPLACE VIEW test_coverage AS
SELECT
    m.module_id,
    m.name as module_name,
    COUNT(DISTINCT r.id) as total_requirements,
    COUNT(DISTINCT t.id) as total_tests,
    AVG(t.coverage_percentage) as avg_coverage,
    COUNT(DISTINCT CASE WHEN t.status = 'passed' THEN t.id END) as passed_tests,
    COUNT(DISTINCT CASE WHEN t.status = 'failed' THEN t.id END) as failed_tests
FROM modules m
LEFT JOIN requirements r ON m.module_id = r.module_id
LEFT JOIN tests t ON r.requirement_id = t.requirement_id
GROUP BY m.module_id, m.name;

-- Grant permissions (adjust as needed)
GRANT ALL PRIVILEGES ON SCHEMA devdocai TO postgres;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA devdocai TO postgres;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA devdocai TO postgres;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA devdocai TO postgres;