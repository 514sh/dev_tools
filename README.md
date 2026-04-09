# Developer Dev Tools

A modular, self-hosted Docker-based dev tools stack for developers. Turn on/off services as needed and easily connect other projects to the shared network.

## Features

- **PostgreSQL** - Relational database
- **MongoDB** - Document database
- **Redis** - Cache & message broker
- **Meilisearch** - Full-text search engine
- **Qdrant** - Vector database for AI applications
- **Ollama** - Local LLM inference
- **n8n** - Workflow automation
- **Celery** - Python async task queue
- **Traefik** - Reverse proxy
- **Tor Proxy** - Privacy/anonymity

## Quick Start

```bash
# 1. Clone and setup
cd dev_tools
cp .env.example .env

# 2. Start services (choose one)
docker compose --profile minimal up    # postgres + redis
docker compose --profile data up       # + mongodb, meilisearch
docker compose --profile ai up         # + qdrant, ollama
docker compose --profile full up       # all services

# 3. Or start specific services
docker compose up postgres redis
```

## Profiles

| Profile   | Services                                       |
| --------- | ---------------------------------------------- |
| `minimal` | PostgreSQL, Redis                              |
| `data`    | PostgreSQL, MongoDB, Redis, Meilisearch        |
| `ai`      | PostgreSQL, Redis, Qdrant, Ollama, Meilisearch |
| `full`    | All services                                   |

## Connecting External Projects

Add to your project's `docker-compose.yml`:

```yaml
networks:
  default:
    external: true
    name: dev-tools
```

Then use service hostnames: `postgres`, `redis`, `mongodb`, etc.

See [docs/INTEGRATION.md](docs/INTEGRATION.md) for full guide.

## Ports

Default ports (change in `.env` if you have local services on same ports):

| Service           | Default | Alternate |
| ----------------- | ------- | --------- |
| PostgreSQL        | 5432    | 15432     |
| MongoDB           | 27017   | 27018     |
| Redis             | 6379    | 16379     |
| Meilisearch       | 7700    | 17700     |
| Qdrant            | 6333    | 16333     |
| Ollama            | 11434   | 11435     |
| n8n               | 5678    | 15678     |
| Traefik HTTP      | 80      | 8080      |
| Traefik HTTPS     | 443     | 8443      |
| Traefik Dashboard | 8090    | 18090     |
| Tor SOCKS         | 9050    | 19050     |
| Privoxy HTTP      | 8118    | 18118     |

### Port Conflicts

If you have local services (e.g., local PostgreSQL at 5432), change Docker ports in `.env`:

```bash
# Add to your .env
POSTGRES_PORT=15432
REDIS_PORT=16379
```

Your local services stay at original ports. Docker services use alternate ports.

## Documentation

- [Product Requirements](docs/PRD.md)
- [Feature List](docs/FEATURES.md)
- [Technical Specs](docs/SPEC.md)
- [Integration Guide](docs/INTEGRATION.md)
- [Connection References](docs/CONNECTION_REFS.md)

## License

MIT
