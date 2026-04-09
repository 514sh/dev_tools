# Integration Guide - Connecting External Projects to Dev Tools

This guide explains how to connect your existing Docker projects to the `dev-tools` network so they can use the shared services.

---

## Quick Start

### Step 1: Start Dev Tools

```bash
# Clone or navigate to dev_tools directory
cd /path/to/dev_tools

# Copy environment file
cp .env.example .env

# Start services (choose one)
docker compose --profile minimal up          # postgres + redis only
docker compose --profile data up             # + mongodb, meilisearch
docker compose --profile ai up               # + qdrant, ollama, meilisearch
docker compose --profile full up             # all services

# Or start specific services
docker compose up postgres redis
```

### Step 2: Connect Your Project

Add the following to your project's `docker-compose.yml`:

```yaml
networks:
  default:
    external: true
    name: dev-tools
```

### Step 3: Configure Your Application

Use the service hostnames and credentials from the dev tools `.env` file.

---

## Network Configuration

### Option A: Use External Network (Recommended)

In your project's `docker-compose.yml`:

```yaml
version: "3.8"

services:
  your-app:
    build: .
    networks:
      - default
      - dev-tools-external

networks:
  default:
    # Your project's default network
  dev-tools-external:
    external: true
    name: dev-tools
```

### Option B: Join Network After Creation

```bash
# Start dev tools first
docker compose -f /path/to/dev_tools/docker-compose.yml up -d

# Your containers can join the network
docker network connect dev-tools your-container
```

---

## Service Discovery

All services are available via DNS on the `dev-tools` network:

| Service        | Hostname      | Port    |
| -------------- | ------------- | ------- |
| PostgreSQL     | `postgres`    | 5432    |
| MongoDB        | `mongodb`     | 27017   |
| Redis          | `redis`       | 6379    |
| Meilisearch    | `meilisearch` | 7700    |
| Qdrant         | `qdrant`      | 6333    |
| Ollama         | `ollama`      | 11434   |
| n8n            | `n8n`         | 5678    |
| Traefik        | `traefik`     | 80, 443 |
| Tor (SOCKS)    | `tor`         | 9050    |
| Privoxy (HTTP) | `privoxy`     | 8118    |

---

## Environment Variables for External Projects

Create a `.env` file in your project with the credentials from dev_tools:

```bash
# PostgreSQL
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=devtools
POSTGRES_USER=devtools
POSTGRES_PASSWORD=<from dev_tools/.env>

# MongoDB
MONGO_HOST=mongodb
MONGO_PORT=27017
MONGO_USER=devtools
MONGO_PASSWORD=<from dev_tools/.env>

# Redis
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=<from dev_tools/.env>

# Meilisearch
MEILISEARCH_HOST=meilisearch
MEILISEARCH_PORT=7700
MEILISEARCH_KEY=<from dev_tools/.env>

# Qdrant
QDRANT_HOST=qdrant
QDRANT_PORT=6333
QDRANT_API_KEY=<from dev_tools/.env>

# Ollama
OLLAMA_HOST=ollama
OLLAMA_PORT=11434
```

---

## Language-Specific Examples

### Python (psycopg2, redis-py, pymongo)

```python
# PostgreSQL
import psycopg2
conn = psycopg2.connect(
    host="postgres",
    port=5432,
    database="devtools",
    user="devtools",
    password="your_password"
)

# Redis
import redis
r = redis.Redis(
    host="redis",
    port=6379,
    password="your_password",
    decode_responses=True
)

# MongoDB
from pymongo import MongoClient
client = MongoClient(
    "mongodb://devtools:your_password@mongodb:27017/?authSource=admin"
)
```

### Python (Celery)

```python
from celery import Celery

app = Celery("my_app")
app.conf.update(
    broker_url="redis://:your_password@redis:6379/0",
    result_backend="redis://:your_password@redis:6379/1",
)
```

### Node.js

```javascript
// PostgreSQL
const { Pool } = require("pg");
const pool = new Pool({
  host: "postgres",
  port: 5432,
  database: "devtools",
  user: "devtools",
  password: "your_password",
});

// Redis
const redis = require("redis");
const client = redis.createClient({
  socket: {
    host: "redis",
    port: 6379,
  },
  password: "your_password",
});

// MongoDB
const { MongoClient } = require("mongodb");
const client = new MongoClient(
  "mongodb://devtools:your_password@mongodb:27017/?authSource=admin",
);
```

### Go

```go
// PostgreSQL
import (
    "github.com/jackc/pgx/v5"
)
conn, _ := pgx.Connect(ctx, "postgres://devtools:password@postgres:5432/devtools")

// Redis
import "github.com/redis/go-redis/v9"
rdb := redis.NewClient(&redis.Options{
    Addr:     "redis:6379",
    Password: "your_password",
    DB:       0,
})
```

---

## Using Tor Proxy for Privacy

### From Python

```python
import requests

proxies = {
    'http': 'socks5h://localhost:9050',
    'https': 'socks5h://localhost:9050'
}
response = requests.get('https://api.ipify.org', proxies=proxies)
print(response.text)  # Shows different IP on each request
```

### From Node.js

```javascript
const axios = require("axios");
const https = require("https");
const { SocksProxyAgent } = require("socks-proxy-agent");

const agent = new SocksProxyAgent("socks5://localhost:9050");
const response = await axios.get("https://api.ipify.org", {
  httpsAgent: agent,
});
```

### Rotating Tor Circuit

```bash
# Renew Tor circuit to get new exit IP
docker exec devtools_tor tor-controlpanel reload

# Or via netcat
echo -e 'AUTHENTICATE "your_tor_password"\r\nsignal NEWNYM\r\n' | nc localhost 9051
```

---

## Using Traefik as Reverse Proxy

If you have Traefik running in dev-tools, you can route traffic through it:

```yaml
# In your service
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.myapp.rule=Host(`myapp.localhost`)"
  - "traefik.http.routers.myapp.entrypoints=web"
  - "traefik.http.services.myapp.loadbalancer.server.port=3000"
```

Then access your app at `http://myapp.localhost`

---

## Troubleshooting

### "Network dev-tools declared as external"

The network already exists. Either:

1. Use `external: true` in your compose file
2. Or remove the network from dev-tools and recreate

### "Connection refused"

Make sure the service is running:

```bash
docker compose ps
docker compose logs <service-name>
```

### "Authentication failed"

Verify credentials match your dev_tools `.env`:

```bash
cat /path/to/dev_tools/.env
```

### "Name or service not known"

Make sure you're on the same Docker network:

```bash
docker network inspect dev-tools
```

---

## Best Practices

1. **Don't commit credentials**: Use `.env` files and add to `.gitignore`
2. **Use profiles**: Start only what you need to save resources
3. **Health checks**: Wait for services to be healthy before connecting
4. **Volume persistence**: Data survives restarts but not `docker compose down -v`
5. **Cleanup**: Use `docker compose down` (not `-v`) to keep data
