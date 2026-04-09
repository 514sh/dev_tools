# Developer Dev Tools - Product Requirements Document

## 1. Problem Statement

Developers often need to run multiple infrastructure services (databases, caches, message queues, automation tools, proxies) across different projects. Managing these services individually per project leads to:

- **Resource duplication**: Multiple PostgreSQL/Redis instances running simultaneously
- **Configuration inconsistency**: Different connection strings, ports, and credentials per project
- **Complexity in networking**: Difficulty exposing services securely while maintaining local accessibility
- **Onboarding friction**: Time spent setting up dev environment for each new project
- **Lack of reusability**: Services configured for one project cannot be easily shared with others

## 2. Goals

### Primary Goals

1. **Centralized Dev Infrastructure**: Provide a single Docker network (`dev-tools`) containing commonly used developer services
2. **Flexible Composition**: Allow any combination of services to run (single, subset, or full stack)
3. **Easy Integration**: Enable other Docker projects to connect to `dev-tools` network with minimal configuration
4. **Production Parity**: Use configurations similar to production deployments for realistic development experience
5. **Isolation & Security**: Keep dev tools isolated from production while allowing controlled exposure when needed

### Secondary Goals

1. **Health Monitoring**: Basic health checks and status visibility for running services
2. **Data Persistence**: Persistent volumes for databases that survive container restarts
3. **Configuration Management**: Centralized environment configuration per tool
4. **Documentation**: Clear usage examples for each service integration

## 3. User Stories

### As a Developer, I can...

| #   | User Story                                                                 | Benefit                           |
| --- | -------------------------------------------------------------------------- | --------------------------------- |
| 1   | **Start only PostgreSQL** when I only need a relational database           | Resource efficiency               |
| 2   | **Start MongoDB** when I need document storage or JSON APIs                | Flexible schema support           |
| 3   | **Start Qdrant** when I need vector similarity search for AI features      | Semantic search capability        |
| 4   | **Start Ollama** when I need local LLM inference                           | Privacy-first AI development      |
| 5   | **Start Meilisearch** when I need full-text search for my application      | Fast, typo-tolerant search        |
| 6   | **Start PostgreSQL + Redis + Celery** when building Python async workflows | Match exact project needs         |
| 7   | **Start the entire stack** when exploring a new project                    | Quick onboarding                  |
| 8   | **Connect my existing project** to `dev-tools` network via Docker Compose  | Seamless integration              |
| 9   | **Access services via localhost** on predefined ports                      | No memorizing port numbers        |
| 10  | **Use rotating Tor proxy** for privacy-sensitive development tasks         | Enhanced privacy with IP rotation |
| 11  | **Persist database data** across container restarts                        | Data durability                   |
| 12  | **View service status** at a glance                                        | Quick troubleshooting             |
| 13  | **Extend the stack** with additional containers                            | Future-proofing                   |

## 4. Scope of Tools

> **Important**: All tools listed below are **100% self-hosted**. We use the open-source software only, not any SaaS/cloud offerings from these providers. All services run locally in Docker containers on the `dev-tools` network.

### Included in v1.0

| Category            | Tool               | Purpose                          | Default Port |
| ------------------- | ------------------ | -------------------------------- | ------------ |
| **Relational DB**   | PostgreSQL         | Relational database              | 5432         |
| **NoSQL DB**        | MongoDB            | Document database                | 27017        |
| **Cache/Queue**     | Redis              | In-memory cache & message broker | 6379         |
| **Vector DB**       | Qdrant             | Vector similarity search engine  | 6333         |
| **AI/ML**           | Ollama             | Local LLM inference              | 11434        |
| **Search**          | Meilisearch        | Full-text search for AI apps     | 7700         |
| **Automation**      | n8n                | Workflow automation platform     | 5678         |
| **Background Jobs** | Celery + Redis     | Python async task queue          | (via Redis)  |
| **Reverse Proxy**   | Traefik            | Reverse proxy with auto-HTTPS    | 80, 443      |
| **Privacy**         | Rotating Tor Proxy | Anonymizing network proxy        | 9050, 8118   |

### Recommended Extensions (v1.x)

| Category           | Tool                 | Purpose               |
| ------------------ | -------------------- | --------------------- |
| **Monitoring**     | Grafana + Prometheus | Metrics & dashboards  |
| **Object Storage** | MinIO                | S3-compatible storage |
| **Message Queue**  | RabbitMQ             | AMQP message broker   |
| **Email Testing**  | MailHog              | Email capture for dev |

### Self-Hosting Commitment

- **PostgreSQL**: Self-hosted PostgreSQL instance (not Neon, Supabase, etc.)
- **MongoDB**: Self-hosted MongoDB instance (not MongoDB Atlas)
- **Qdrant**: Self-hosted Qdrant container (not Qdrant Cloud)
- **Ollama**: Runs entirely local (no Ollama Cloud)
- **Meilisearch**: Self-hosted Meilisearch (not Meilisearch Cloud)
- **n8n**: Self-hosted n8n instance (not n8n Cloud)
- **Traefik**: Self-hosted Traefik proxy

## 5. Architecture

### Network Structure

```
┌─────────────────────────────────────────────────────────────────────┐
│                         dev-tools network                            │
│                                                                      │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐   │
│  │ PostgreSQL │  │   Redis    │  │    n8n     │  │  Meilisearch│  │
│  └────────────┘  └────────────┘  └────────────┘  └────────────┘   │
│       │               │               │               │              │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐   │
│  │  MongoDB   │  │   Ollama   │  │   Qdrant   │  │  Traefik   │   │
│  └────────────┘  └────────────┘  └────────────┘  └────────────┘   │
│                           │                                        │
│                     ┌────────────┐                                 │
│                     │    Celery   │                                 │
│                     │   Workers   │                                 │
│                     └────────────┘                                 │
│                                                                      │
│  ┌────────────┐                                                    │
│  │ Rotating   │                                                    │
│  │  Tor Proxy │                                                    │
│  └────────────┘                                                    │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              │
                              ▼
┌─────────────────────────────────────┐
│       Other Docker Projects          │
│       (app containers)              │
└─────────────────────────────────────┘
```

### Connection Pattern

External projects connect via:

```yaml
# In project's docker-compose.yml
networks:
  default:
    external: true
    name: dev-tools
```

## 6. Acceptance Criteria

### Functional Criteria

| ID  | Criterion                                                           | Test Scenario                                                   |
| --- | ------------------------------------------------------------------- | --------------------------------------------------------------- |
| F1  | PostgreSQL starts and accepts connections                           | `docker compose up postgres` → `psql` connects                  |
| F2  | MongoDB starts and accepts connections                              | `docker compose up mongodb` → `mongosh` connects                |
| F3  | Redis starts and responds to PING                                   | `docker compose up redis` → `redis-cli ping` returns PONG       |
| F4  | Qdrant starts and serves vector queries                             | `docker compose up qdrant` → Qdrant dashboard loads             |
| F5  | Ollama serves LLM inference requests                                | `docker compose up ollama` → API responds to generation request |
| F6  | Meilisearch starts and indexes documents                            | `docker compose up meilisearch` → search returns results        |
| F7  | n8n starts and is accessible via browser                            | `docker compose up n8n` → http://localhost:5678 loads           |
| F8  | Celery workers process async tasks                                  | Task sent to Redis queue is processed by worker                 |
| F9  | Any subset of services can run together                             | `docker compose up postgres redis` runs without error           |
| F10 | All services run together                                           | `docker compose up` starts all services                         |
| F11 | Services are reachable from other containers on `dev-tools` network | External container can connect to `postgres:5432`               |
| F12 | Data persists across restarts                                       | Data written to PostgreSQL survives `docker compose down && up` |
| F13 | Traefik routes traffic to named services                            | Requests to `http://traefik.localhost` route correctly          |
| F14 | Rotating Tor proxy routes traffic anonymously and rotates exits     | HTTP traffic shows different exit IPs on successive requests    |

### Non-Functional Criteria

| ID  | Criterion                  | Target                                  |
| --- | -------------------------- | --------------------------------------- |
| NF1 | Start time for full stack  | < 60 seconds                            |
| NF2 | Memory usage (idle stack)  | < 2GB RAM                               |
| NF3 | Documentation completeness | Every service has usage example         |
| NF4 | Configuration externalized | No hardcoded credentials in Dockerfiles |

## 7. Use Cases

### Use Case 1: Minimal API Development

**Scenario**: Developer building a simple REST API
**Services**: PostgreSQL only
**Flow**:

1. `docker compose up postgres`
2. API connects to `postgres:5432`
3. No resource waste from unused services

### Use Case 2: Python Async Background Jobs

**Scenario**: Developer building a Python application with Celery background processing
**Services**: PostgreSQL + Redis + Celery workers
**Flow**:

1. `docker compose up postgres redis`
2. Python app connects to PostgreSQL and Redis
3. Celery workers process async tasks from Redis queue

### Use Case 3: AI/ML Application with RAG

**Scenario**: Developer building a RAG (Retrieval-Augmented Generation) application
**Services**: PostgreSQL + Qdrant + Ollama + Meilisearch
**Flow**:

1. `docker compose up postgres qdrant ollama meilisearch`
2. App stores embeddings in Qdrant, documents in Meilisearch
3. Ollama provides LLM inference for generated responses

### Use Case 4: Document-Based Application

**Scenario**: Developer building an application with flexible schema needs
**Services**: MongoDB + Redis
**Flow**:

1. `docker compose up mongodb redis`
2. App stores documents in MongoDB
3. Redis caches frequently accessed data

### Use Case 5: Privacy-Sensitive Development

**Scenario**: Developer testing services that should not reveal IP
**Services**: PostgreSQL + Rotating Tor Proxy
**Flow**:

1. `docker compose up postgres tor`
2. Application routes outbound traffic through rotating Tor
3. External services see rotating Tor exit node IPs

### Use Case 6: Full Stack Exploration

**Scenario**: Developer exploring a new project
**Services**: All services (postgres, mongodb, redis, qdrant, ollama, meilisearch, n8n, traefik, tor)
**Flow**:

1. `docker compose up`
2. All services available immediately
3. No setup time required

---

## 8. Out of Scope (v1.0)

- Authentication/authorization for services (assumes trusted local network)
- Automated backups (future enhancement)
- High availability / clustering
- Cloud deployment configurations
- Windows container support
- Service scaling beyond single instance

## 9. Assumptions & Constraints

- Users have Docker and Docker Compose installed
- Users have basic Docker networking knowledge
- Sufficient RAM (4GB minimum recommended for full stack)
- Linux/macOS development environment (Windows: WSL2 recommended)
