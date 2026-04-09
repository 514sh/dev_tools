# Feature List - Developer Dev Tools

## Overview

Each feature is atomic, independently deployable, and completable in one focused coding session. Features should be implemented in order as later features may depend on earlier ones.

> **Important**: All tools are **100% self-hosted**. We run open-source software in Docker containers locally. No SaaS/cloud versions are used.

---

## Features

### Infrastructure

1. **Network Setup**
   - Create `dev-tools` Docker network
   - Network type: bridge
   - Enable external connectivity for other projects

2. **Environment Configuration**
   - Create `.env` template with all service variables
   - PostgreSQL: POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB
   - MongoDB: MONGO_INITDB_ROOT_USERNAME, MONGO_INITDB_ROOT_PASSWORD
   - Redis: REDIS_PASSWORD
   - n8n: N8N_BASIC_AUTH_USER, N8N_BASIC_AUTH_PASSWORD
   - Qdrant: QDRANT_API_KEY
   - Ollama: OLLAMA_HOST, OLLAMA_MODELS
   - Meilisearch: MEILI_MASTER_KEY
   - Tor: TOR_CONTROL_PASSWORD, TOR_SOCKS_PORT, TOR_HTTP_PORT

### Relational & Document Databases

3. **PostgreSQL Service**
   - Docker Compose service for PostgreSQL 15
   - Persistent volume for data
   - Default database: devtools
   - Port: 5432
   - Health check configured

4. **MongoDB Service**
   - Docker Compose service for MongoDB 7
   - Persistent volume for data
   - Port: 27017
   - Authentication enabled
   - Health check configured

### Cache, Queue & Search

5. **Redis Service**
   - Docker Compose service for Redis 7
   - Persistent volume for data
   - Port: 6379
   - Password authentication enabled
   - Health check configured

6. **Meilisearch Service**
   - Docker Compose service for Meilisearch
   - Persistent volume for data
   - Port: 7700
   - Master key authentication
   - Health check configured

### AI/ML Services

7. **Qdrant Vector Database Service**
   - Docker Compose service for Qdrant
   - Persistent volume for data
   - Port: 6333 (GRPC), 6334 (REST)
   - API key authentication
   - Health check configured

8. **Ollama Service**
   - Docker Compose service for Ollama
   - Volume for models
   - Port: 11434
   - GPU support (optional)
   - Health check configured

### Automation & Workers

9. **n8n Service**
   - Docker Compose service for n8n (latest)
   - Connects to PostgreSQL for workflow data
   - Connects to Redis for queue
   - Port: 5678
   - Persistent volume for workflows
   - Basic auth enabled

10. **Celery Worker Example**
    - Example Python service demonstrating Celery usage
    - Connects to Redis queue
    - Shows task processing pattern
    - Can be used as template for real workers
    - Includes requirements.txt example

### Proxy Services

11. **Traefik Reverse Proxy**
    - Docker Compose service for Traefik
    - Docker provider enabled (auto-discover containers)
    - Dashboard on port 8090
    - HTTP (80) and HTTPS (443) ports
    - Let's Encrypt ready (placeholder config)

12. **Rotating Tor Proxy Service**
    - Docker Compose service using Privoxy + Tor
    - SOCKS proxy on port 9050
    - HTTP proxy on port 8118 (Privoxy forwarding to Tor)
    - Control port on 9051 with password
    - Auto-renewal of Tor circuit (configurable)
    - Health check configured

### Integration

13. **Unified Docker Compose**
    - Single `docker-compose.yml` combining all services
    - Profile support: `minimal`, `data`, `ai`, `full`
    - `minimal`: postgres, redis
    - `data`: postgres, mongodb, redis, meilisearch
    - `ai`: postgres, redis, qdrant, ollama, meilisearch
    - `full`: all services
    - Clear dependency ordering

14. **Documentation & Examples**
    - Integration guide for external projects
    - Connection string reference for each service
    - Example Docker Compose snippet for client projects
    - Python Celery integration example
    - RAG application example (Qdrant + Ollama + Meilisearch)
    - Troubleshooting section

---

## Feature Dependency Graph

```
        ┌─────────────────────────────────────────────────────────────┐
        │                     1. Network Setup                        │
        └─────────────────────────────────────────────────────────────┘
                                  │
        ┌─────────────────────────┼─────────────────────────┐
        ▼                         ▼                         ▼
 ┌─────────────┐           ┌─────────────┐           ┌─────────────┐
 │  2. Env     │           │  3. Postgres│           │  4. MongoDB │
 │   Config    │           └─────────────┘           └─────────────┘
 └─────────────┘                 │                         │
        │                        └─────────┬───────────────┘
        │                                  │
        │              ┌──────────────────┼──────────────────┐
        ▼              ▼                  ▼                  ▼
 ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
 │  5. Redis   │ │  6. Meilisearch│ │  7. Qdrant  │ │  8. Ollama  │
 └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘
        │                │                │                │
        └────────────────┼────────────────┼────────────────┘
                         │                │
                         ▼                ▼
                  ┌─────────────┐  ┌─────────────┐
                  │   9. n8n    │  │ 10. Celery  │
                  └─────────────┘  └─────────────┘
                         │                │
                         └────────┬───────┘
                                  │
                                  ▼
                         ┌─────────────┐
                         │ 11. Traefik  │
                         └─────────────┘
                                  │
                                  ▼
                         ┌─────────────┐
                         │12. Rotating  │
                         │  Tor Proxy   │
                         └─────────────┘
                                  │
                                  ▼
                         ┌─────────────┐
                         │13. Unified   │
                         │docker-compose│
                         └─────────────┘
                                  │
                                  ▼
                         ┌─────────────┐
                         │14. Docs &   │
                         │  Examples   │
                         └─────────────┘
```

---

## Implementation Notes

- Each database/search service should be implemented as a separate Docker Compose service
- Use consistent naming convention: `devtools_<service>`
- All services should have health checks
- Volumes should be prefixed with `devtools_`
- Ports should not conflict with host services
- Celery worker example should include working Python code with Redis
- Rotating Tor should demonstrate circuit renewal
