# Technical Specifications - Developer Dev Tools

## Overview

These specs define the technical implementation for a **global, modular Docker-based dev tools stack**. The primary use case is:

- **Turn on/off** any combination of services independently
- **Connect external projects** to the `dev-tools` network seamlessly
- All services are **self-hosted** locally

---

## Spec 1: Network Setup

### Files

- Created: `docker-compose.yml` (networks section)
- No new files needed

### Function Signature

```
Network Name: dev-tools
Type: bridge
External: false (can be changed to true after initial creation)
```

### API Contract

- Network created automatically on `docker compose up`
- Other projects reference via: `external: true, name: dev-tools`

### Data Model

- Network ID format: `dev-tools`

### Test Scenarios

1. `docker network ls` shows `dev-tools` network
2. Network persists when no containers running
3. External containers can join network

---

## Spec 2: Environment Configuration

### Files

- Created: `.env.example`

### Function Signature

```
Environment Variables (key=value):
- DEVTOOLS_NETWORK=dev-tools
- POSTGRES_VERSION=15
- POSTGRES_USER=devtools
- POSTGRES_PASSWORD=<secret>
- POSTGRES_DB=devtools
- POSTGRES_PORT=5432
- MONGODB_VERSION=7
- MONGO_INITDB_ROOT_USERNAME=devtools
- MONGO_INITDB_ROOT_PASSWORD=<secret>
- MONGODB_PORT=27017
- REDIS_VERSION=7
- REDIS_PASSWORD=<secret>
- REDIS_PORT=6379
- MEILISEARCH_VERSION=1.6
- MEILI_MASTER_KEY=<secret>
- MEILISEARCH_PORT=7700
- QDRANT_VERSION=1.7
- QDRANT_API_KEY=<secret>
- QDRANT_PORT=6333
- QDRANT_GRPC_PORT=6334
- OLLAMA_VERSION=0.1
- OLLAMA_HOST=0.0.0.0:11434
- OLLAMA_PORT=11434
- N8N_VERSION=1.14
- N8N_BASIC_AUTH_USER=admin
- N8N_BASIC_AUTH_PASSWORD=<secret>
- N8N_PORT=5678
- TRAEFIK_VERSION=3.0
- TRAEFIK_HTTP_PORT=80
- TRAEFIK_HTTPS_PORT=443
- TRAEFIK_DASHBOARD_PORT=8090
- TOR_VERSION=2024
- TOR_CONTROL_PASSWORD=<secret>
- TOR_SOCKS_PORT=9050
- TOR_CONTROL_PORT=9051
- TOR_HTTP_PORT=8118
```

### API Contract

- Copy `.env.example` to `.env`
- All services read from environment variables
- No hardcoded credentials

### Test Scenarios

1. `.env` file can be created from `.env.example`
2. All services start without hardcoded values
3. Credentials are not committed to git

---

## Spec 3: PostgreSQL Service

### Files

- Created: `docker-compose.yml` (postgres service)

### Function Signature

```
Container: devtools_postgres
Image: postgres:15-alpine
Ports: 5432:5432
Volumes: devtools_postgres_data:/var/lib/postgresql/data
Environment: POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB
Healthcheck: pg_isready
Profiles: minimal, data, ai, full
```

### API Contract

**Inputs:**

- `POSTGRES_USER` (default: devtools)
- `POSTGRES_PASSWORD` (required)
- `POSTGRES_DB` (default: devtools)

**Outputs:**

- Port 5432 exposed
- Database `devtools` created by default

**Error Cases:**

- Port 5432 already in use → fails with clear error

**Connection String:**

```
postgresql://devtools:<password>@localhost:5432/devtools
```

### Data Model

- Volume: `devtools_postgres_data`
- Default database name matches `POSTGRES_DB`

### Test Scenarios

1. `docker compose --profile minimal up postgres` starts successfully
2. `psql` connects with correct credentials
3. Data persists after `docker compose down && up`
4. Healthcheck passes after startup

---

## Spec 4: MongoDB Service

### Files

- Created: `docker-compose.yml` (mongodb service)

### Function Signature

```
Container: devtools_mongodb
Image: mongo:7
Ports: 27017:27017
Volumes: devtools_mongodb_data:/data/db
Environment: MONGO_INITDB_ROOT_USERNAME, MONGO_INITDB_ROOT_PASSWORD
Healthcheck: mongosh ping
Profiles: data, full
```

### API Contract

**Inputs:**

- `MONGO_INITDB_ROOT_USERNAME` (default: devtools)
- `MONGO_INITDB_ROOT_PASSWORD` (required)

**Outputs:**

- Port 27017 exposed
- Admin user created

**Connection String:**

```
mongodb://devtools:<password>@localhost:27017/?authSource=admin
```

### Test Scenarios

1. `docker compose --profile data up mongodb` starts successfully
2. `mongosh` connects with correct credentials
3. Data persists after restart
4. Healthcheck passes

---

## Spec 5: Redis Service

### Files

- Created: `docker-compose.yml` (redis service)

### Function Signature

```
Container: devtools_redis
Image: redis:7-alpine
Ports: 6379:6379
Volumes: devtools_redis_data:/data
Command: redis-server --requirepass <password>
Healthcheck: redis-cli ping
Profiles: minimal, data, ai, full
```

### API Contract

**Inputs:**

- `REDIS_PASSWORD` (required)
- `REDIS_PORT` (default: 6379)

**Outputs:**

- Port 6379 exposed
- AUTH enabled

**Connection String:**

```
redis://:devtools_redis_password@localhost:6379
```

### Test Scenarios

1. `docker compose up redis` starts successfully
2. `redis-cli -a <password> ping` returns PONG
3. Data persists after restart
4. Healthcheck passes

---

## Spec 6: Meilisearch Service

### Files

- Created: `docker-compose.yml` (meilisearch service)

### Function Signature

```
Container: devtools_meilisearch
Image: getmeili/meilisearch:v1.6
Ports: 7700:7700
Volumes: devtools_meilisearch_data:/meili_data
Environment: MEILI_MASTER_KEY, MEILI_ENV
Healthcheck: wget health endpoint
Profiles: data, ai, full
```

### API Contract

**Inputs:**

- `MEILI_MASTER_KEY` (required)
- `MEILISEARCH_PORT` (default: 7700)

**Outputs:**

- Port 7700 exposed
- REST API available at `http://localhost:7700`

**Connection Info:**

```
http://localhost:7700
Master Key: <MEILI_MASTER_KEY>
```

### Test Scenarios

1. `docker compose --profile data up meilisearch` starts successfully
2. Health endpoint returns OK
3. Search operations work with master key
4. Data persists after restart

---

## Spec 7: Qdrant Service

### Files

- Created: `docker-compose.yml` (qdrant service)

### Function Signature

```
Container: devtools_qdrant
Image: qdrant/qdrant:v1.7
Ports: 6333:6333, 6334:6334
Volumes: devtools_qdrant_data:/qdrant/storage
Environment: QDRANT__SERVICE__API_KEY
Healthcheck: curl readyz endpoint
Profiles: ai, full
```

### API Contract

**Inputs:**

- `QDRANT_API_KEY` (required)
- `QDRANT_PORT` (default: 6333)
- `QDRANT_GRPC_PORT` (default: 6334)

**Outputs:**

- REST API on port 6333
- gRPC API on port 6334

**Connection Info:**

```
http://localhost:6333
API Key: <QDRANT_API_KEY>
```

### Test Scenarios

1. `docker compose --profile ai up qdrant` starts successfully
2. Readyz endpoint returns OK
3. Collections can be created with API key
4. Vector search works

---

## Spec 8: Ollama Service

### Files

- Created: `docker-compose.yml` (ollama service)

### Function Signature

```
Container: devtools_ollama
Image: ollama/ollama:0.1
Ports: 11434:11434
Volumes: devtools_ollama_data:/root/.ollama
Environment: OLLAMA_HOST
Healthcheck: curl api tags endpoint
Profiles: ai, full
```

### API Contract

**Inputs:**

- `OLLAMA_PORT` (default: 11434)

**Outputs:**

- REST API on port 11434
- Model files stored in volume

**Connection Info:**

```
http://localhost:11434
```

**Test Model Command:**

```bash
curl http://localhost:11434/api/pull -d '{"name": "llama2"}'
```

### Test Scenarios

1. `docker compose --profile ai up ollama` starts successfully
2. API responds to tags request
3. Models can be pulled and run
4. Volume persists downloaded models

---

## Spec 9: n8n Service

### Files

- Created: `docker-compose.yml` (n8n service)

### Function Signature

```
Container: devtools_n8n
Image: n8nio/n8n:1.14
Ports: 5678:5678
Volumes: devtools_n8n_data:/home/node/.n8n
Environment: N8N_BASIC_AUTH_USER, N8N_BASIC_AUTH_PASSWORD, DB_* variables
DependsOn: postgres (healthy), redis (healthy)
Healthcheck: wget healthz endpoint
Profiles: automation, full
```

### API Contract

**Inputs:**

- `N8N_BASIC_AUTH_USER` (default: admin)
- `N8N_BASIC_AUTH_PASSWORD` (required)
- `N8N_PROTOCOL` (default: http)
- `N8N_HOST` (default: localhost)

**Outputs:**

- Web UI on port 5678
- PostgreSQL for workflow data
- Uses Redis for queue

**Connection Info:**

```
http://localhost:5678
User: <N8N_BASIC_AUTH_USER>
Password: <N8N_BASIC_AUTH_PASSWORD>
```

### Test Scenarios

1. `docker compose --profile automation up n8n` starts successfully
2. Web UI accessible at localhost:5678
3. Login works with basic auth credentials
4. Workflows persist after restart

---

## Spec 10: Celery Worker Example

### Files

- Created: `services/celery_worker/` directory structure

### Function Signature

```
Directory Structure:
services/celery_worker/
├── Dockerfile
├── requirements.txt
├── tasks.py
└── README.md

Container: devtools_celery_worker
Build: ./services/celery_worker
Environment: CELERY_BROKER_URL, CELERY_RESULT_BACKEND
DependsOn: redis (healthy)
Profiles: automation, full
```

### API Contract

**Inputs:**

- `CELERY_BROKER_URL` (default: redis://:<REDIS_PASSWORD>@redis:6379/0)
- `CELERY_RESULT_BACKEND` (default: redis://:<REDIS_PASSWORD>@redis:6379/1)

**Outputs:**

- Worker connects to Redis
- Tasks can be submitted from any container on network

**Task Signatures:**

```python
tasks.process_data(data: str) -> dict
tasks.fetch_url(url: str) -> dict
tasks.generate_report(report_id: str, params: dict) -> dict
tasks.batch_process(items: list) -> dict
```

### Data Model

- Task results stored in Redis DB 1
- Task queue in Redis DB 0

### Test Scenarios

1. Worker container starts without error
2. Worker registers with Redis
3. Tasks can be called from Python shell:
   ```python
   from tasks import process_data
   result = process_data.delay("test")
   result.get(timeout=10)
   ```

---

## Spec 11: Traefik Reverse Proxy

### Files

- Created: `docker-compose.yml` (traefik service)

### Function Signature

```
Container: devtools_traefik
Image: traefik:v3.0
Ports: 80:80, 443:443, 8090:8090
Volumes: /var/run/docker.sock:/var/run/docker.sock:ro
Command: --api.dashboard=true, --providers.docker=true
Profiles: full
```

### API Contract

**Inputs:**

- `TRAEFIK_HTTP_PORT` (default: 80)
- `TRAEFIK_HTTPS_PORT` (default: 443)
- `TRAEFIK_DASHBOARD_PORT` (default: 8090)

**Outputs:**

- HTTP proxy on port 80
- HTTPS proxy on port 443
- Dashboard on port 8090

**Dashboard Access:**

```
http://localhost:8090/dashboard/
```

### Test Scenarios

1. `docker compose --profile full up traefik` starts successfully
2. Dashboard accessible at localhost:8090
3. Container labels route traffic correctly
4. Let's Encrypt can be configured (placeholder)

---

## Spec 12: Rotating Tor Proxy

### Files

- Created: `docker-compose.yml` (tor + privoxy services)

### Function Signature

```
Tor Container: devtools_tor
Image: gallaecio/tor:2024
Ports: 9050:9050, 9051:9051
Volumes: devtools_tor_data:/var/lib/tor
Environment: TOR_CONTROL_PASSWORD
Healthcheck: torify echo test

Privoxy Container: devtools_privoxy
Image: vimagick/privoxy:latest
Ports: 8118:8118
Environment: TOR_HOST=tor, TOR_SOCKS_PORT=9050
DependsOn: tor

Profiles: privacy, full
```

### API Contract

**Tor SOCKS Proxy:**

- Host: localhost
- Port: 9050
- Control Port: 9051

**Privoxy HTTP Proxy:**

- Host: localhost
- Port: 8118
- Forwards HTTP traffic to Tor

**Connection Examples:**

```bash
# SOCKS proxy
curl --socks5 localhost:9050 https://example.com

# HTTP proxy
curl --proxy localhost:8118 https://example.com
```

**Circuit Renewal (via control port):**

```bash
docker exec devtools_tor tor-controlpanel reload
# or
echo 'AUTHENTICATE "<TOR_CONTROL_PASSWORD>"' | nc localhost 9051
signal NEWNYM
```

### Test Scenarios

1. `docker compose --profile privacy up tor` starts successfully
2. SOCKS proxy accepts connections on port 9050
3. HTTP proxy accepts connections on port 8118
4. Multiple requests show different exit IPs

---

## Spec 13: Unified Docker Compose

### Files

- Created: `docker-compose.yml`

### Function Signature

```
Single docker-compose.yml combining all services
Profiles: minimal, data, ai, full
```

### Profile Definitions

| Profile   | Services                                     |
| --------- | -------------------------------------------- |
| `minimal` | postgres, redis                              |
| `data`    | postgres, mongodb, redis, meilisearch        |
| `ai`      | postgres, redis, qdrant, ollama, meilisearch |
| `full`    | all services                                 |

### Usage Commands

```bash
# Start only postgres + redis
docker compose --profile minimal up

# Start data stack
docker compose --profile data up

# Start AI stack
docker compose --profile ai up

# Start everything
docker compose --profile full up

# Start specific services
docker compose up postgres redis
```

### API Contract

- Services can run with or without profiles
- Any subset can be started directly
- Dependencies enforced via `depends_on`

### Test Scenarios

1. `docker compose --profile minimal up` starts only postgres + redis
2. `docker compose --profile data up` starts correct services
3. `docker compose up postgres mongodb` starts only those two
4. Dependencies start in correct order

---

## Spec 14: Documentation & Examples

### Files

- Created: `docs/INTEGRATION.md`

### Function Signature

```
docs/INTEGRATION.md - Guide for connecting external projects
docs/CONNECTION_REFS.md - Connection strings for all services
```

### API Contract - External Project Integration

**Step 1: Connect to dev-tools network**

```yaml
# In external project's docker-compose.yml
networks:
  default:
    external: true
    name: dev-tools
```

**Step 2: Use service hostnames**

```yaml
# External container can reach services via:
# postgres:5432
# mongodb:27017
# redis:6379
# meilisearch:7700
# qdrant:6333
# ollama:11434
# n8n:5678
```

**Step 3: Reference environment variables**

```bash
# .env for external project
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=devtools
POSTGRES_USER=devtools
POSTGRES_PASSWORD=<from dev-tools .env>

REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=<from dev-tools .env>
```

### Test Scenarios

1. External project connects to dev-tools network
2. External project resolves service hostnames
3. External project authenticates with service credentials
4. Documentation includes working examples

---

## Dependency Graph (Revised)

```
                    ┌──────────────┐
                    │   Network    │
                    │   (Spec 1)   │
                    └──────────────┘
                            │
                            ▼
                    ┌──────────────┐
                    │  Environment │
                    │   (Spec 2)   │
                    └──────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  PostgreSQL  │    │   MongoDB    │    │    Redis     │
│   (Spec 3)  │    │   (Spec 4)   │    │   (Spec 5)   │
└──────────────┘    └──────────────┘    └──────────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            ▼
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ Meilisearch  │    │    Qdrant    │    │    Ollama    │
│   (Spec 6)   │    │   (Spec 7)   │    │   (Spec 8)   │
└──────────────┘    └──────────────┘    └──────────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
                            ▼
        ┌───────────────────┴───────────────────┐
        ▼                                       ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│     n8n      │    │   Celery     │    │   Traefik    │
│   (Spec 9)   │    │  (Spec 10)   │    │  (Spec 11)   │
└──────────────┘    └──────────────┘    └──────────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
                            ▼
                    ┌──────────────┐
                    │  Rotating    │
                    │  Tor Proxy   │
                    │  (Spec 12)   │
                    └──────────────┘
                            │
                            ▼
                    ┌──────────────┐
                    │   Unified    │
                    │  Compose     │
                    │  (Spec 13)   │
                    └──────────────┘
                            │
                            ▼
                    ┌──────────────┐
                    │  Documentation│
                    │   (Spec 14)  │
                    └──────────────┘
```

---

## Summary

| Spec | Feature            | File(s)                   | Port(s)          |
| ---- | ------------------ | ------------------------- | ---------------- |
| 1    | Network Setup      | docker-compose.yml        | -                |
| 2    | Environment Config | .env.example              | -                |
| 3    | PostgreSQL         | docker-compose.yml        | 5432             |
| 4    | MongoDB            | docker-compose.yml        | 27017            |
| 5    | Redis              | docker-compose.yml        | 6379             |
| 6    | Meilisearch        | docker-compose.yml        | 7700             |
| 7    | Qdrant             | docker-compose.yml        | 6333, 6334       |
| 8    | Ollama             | docker-compose.yml        | 11434            |
| 9    | n8n                | docker-compose.yml        | 5678             |
| 10   | Celery Worker      | services/celery_worker/\* | -                |
| 11   | Traefik            | docker-compose.yml        | 80, 443, 8090    |
| 12   | Rotating Tor       | docker-compose.yml        | 9050, 9051, 8118 |
| 13   | Unified Compose    | docker-compose.yml        | various          |
| 14   | Documentation      | docs/INTEGRATION.md       | -                |
