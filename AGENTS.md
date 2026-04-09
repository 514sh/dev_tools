# AGENTS.md - Developer Dev Tools

## Project Type

Docker Compose-based dev tools stack (no compilation/build). All services are pre-built Docker images.

## Key Commands

```bash
# Setup
cp .env.example .env

# Start by profile
docker compose --profile <minimal|data|ai|full> up

# Start specific services
docker compose up <service1> <service2>

# Stop
docker compose down

# Validate config (no .env required for validation)
docker compose config --quiet
```

## Profiles

| Profile   | Services                                     |
| --------- | -------------------------------------------- |
| `minimal` | postgres, redis                              |
| `data`    | postgres, mongodb, redis, meilisearch        |
| `ai`      | postgres, redis, qdrant, ollama, meilisearch |
| `full`    | all services                                 |

## Connecting External Projects

External projects join via:

```yaml
networks:
  default:
    external: true
    name: dev-tools
```

Service hostnames: `postgres`, `redis`, `mongodb`, `meilisearch`, `qdrant`, `ollama`, `n8n`

## Service Hostnames & Ports

| Service      | Hostname      | Port  |
| ------------ | ------------- | ----- |
| PostgreSQL   | `postgres`    | 5432  |
| MongoDB      | `mongodb`     | 27017 |
| Redis        | `redis`       | 6379  |
| Meilisearch  | `meilisearch` | 7700  |
| Qdrant       | `qdrant`      | 6333  |
| Ollama       | `ollama`      | 11434 |
| n8n          | `n8n`         | 5678  |
| Tor SOCKS    | `tor`         | 9050  |
| Privoxy HTTP | `privoxy`     | 8118  |

## Port Conflicts

If you have local services using the same ports, override in `.env`:

```bash
# Example: add +10000 to standard ports
POSTGRES_PORT=15432
REDIS_PORT=16379
MONGODB_PORT=27018
```

External projects always connect via container hostname + internal port (not host port).

## Important Notes

- All tools are **self-hosted** only (no SaaS/cloud variants)
- Credentials come from `.env` - never hardcode
- Data persists via named volumes (`devtools_*`)
- Celery worker example is in `services/celery_worker/`
- No build step - images pulled from Docker Hub
- Ports are configurable via `.env` - defaults in `docker-compose.yml`
