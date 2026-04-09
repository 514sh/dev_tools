# Connection References - Developer Dev Tools

Quick reference for connecting to each service in the dev-tools stack.

---

## PostgreSQL

| Property | Value                            |
| -------- | -------------------------------- |
| Host     | `postgres`                       |
| Port     | `5432`                           |
| Database | `devtools` (configurable)        |
| Username | `devtools` (configurable)        |
| Password | From `.env`: `POSTGRES_PASSWORD` |

### Connection Strings

**Python (psycopg2)**

```python
postgresql://devtools:<password>@postgres:5432/devtools
```

**Python (async)**

```python
postgresql+asyncpg://devtools:<password>@postgres:5432/devtools
```

**Node.js (pg)**

```javascript
postgres://devtools:<password>@postgres:5432/devtools
```

**JDBC**

```java
jdbc:postgresql://postgres:5432/devtools?user=devtools&password=<password>
```

**CLI**

```bash
psql -h postgres -p 5432 -U devtools -d devtools
```

---

## MongoDB

| Property | Value                                     |
| -------- | ----------------------------------------- |
| Host     | `mongodb`                                 |
| Port     | `27017`                                   |
| Database | `admin` (for auth)                        |
| Username | `devtools` (configurable)                 |
| Password | From `.env`: `MONGO_INITDB_ROOT_PASSWORD` |

### Connection Strings

**Python (pymongo)**

```python
mongodb://devtools:<password>@mongodb:27017/?authSource=admin
```

**Python (motor - async)**

```python
mongodb://devtools:<password>@mongodb:27017/?authSource=admin
```

**Node.js (mongoose)**

```javascript
mongodb://devtools:<password>@mongodb:27017/devtools?authSource=admin
```

**CLI**

```bash
mongosh "mongodb://devtools:<password>@mongodb:27017/?authSource=admin"
```

---

## Redis

| Property | Value                         |
| -------- | ----------------------------- |
| Host     | `redis`                       |
| Port     | `6379`                        |
| Password | From `.env`: `REDIS_PASSWORD` |
| DB 0     | Celery broker                 |
| DB 1     | Celery results                |

### Connection Strings

**Python (redis-py)**

```python
redis://:devtools_redis_password@redis:6379/0
```

**Python (redis-py, cluster mode)**

```python
redis://:devtools_redis_password@redis:6379
```

**Node.js (ioredis)**

```javascript
redis://:devtools_redis_password@redis:6379
```

**CLI**

```bash
redis-cli -h redis -p 6379 -a <password>
```

---

## Meilisearch

| Property   | Value                           |
| ---------- | ------------------------------- |
| Host       | `meilisearch`                   |
| Port       | `7700`                          |
| Master Key | From `.env`: `MEILI_MASTER_KEY` |

### Connection Strings

**Python**

```python
import meilisearch
client = meilisearch.Client(
    "http://meilisearch:7700",
    "<MEILI_MASTER_KEY>"
)
```

**JavaScript**

```javascript
const { MeiliSearch } = require("meilisearch");
const client = new MeiliSearch({
  host: "http://meilisearch:7700",
  apiKey: "<MEILI_MASTER_KEY>",
});
```

**cURL**

```bash
curl -H "Authorization: Bearer <MEILI_MASTER_KEY>" \
  http://meilisearch:7700/health
```

---

## Qdrant (Vector Database)

| Property  | Value                         |
| --------- | ----------------------------- |
| Host      | `qdrant`                      |
| REST Port | `6333`                        |
| gRPC Port | `6334`                        |
| API Key   | From `.env`: `QDRANT_API_KEY` |

### Connection Strings

**Python (qdrant-client)**

```python
from qdrant_client import QdrantClient
client = QdrantClient(
    host="qdrant",
    port=6333,
    api_key="<QDRANT_API_KEY>"
)
```

**Python (grpc)**

```python
from qdrant_client import QdrantClient
client = QdrantClient(
    host="qdrant",
    port=6334,
    grpc_port=6334,
    api_key="<QDRANT_API_KEY>"
)
```

**JavaScript**

```javascript
const { QdrantClient } = require("@qdrant/js-client-rest");
const client = new QdrantClient({
  url: "http://qdrant:6333",
  apiKey: "<QDRANT_API_KEY>",
});
```

**cURL**

```bash
curl -H "api-key: <QDRANT_API_KEY>" \
  http://qdrant:6333/collections
```

---

## Ollama (Local LLM)

| Property | Value    |
| -------- | -------- |
| Host     | `ollama` |
| Port     | `11434`  |
| API      | REST     |

### Connection Strings

**Python**

```python
import ollama
response = ollama.chat(
    model='llama2',
    messages=[{'role': 'user', 'content': 'Hello'}]
)
```

**JavaScript**

```javascript
const ollama = require("ollama");
const response = await ollama.chat({
  model: "llama2",
  messages: [{ role: "user", content: "Hello" }],
});
```

**cURL**

```bash
curl http://ollama:11434/api/tags
```

**Pull a model**

```bash
curl http://ollama:11434/api/pull -d '{"name": "llama2"}'
```

---

## n8n (Workflow Automation)

| Property | Value                                  |
| -------- | -------------------------------------- |
| Host     | `n8n`                                  |
| Port     | `5678`                                 |
| Protocol | `http`                                 |
| Username | From `.env`: `N8N_BASIC_AUTH_USER`     |
| Password | From `.env`: `N8N_BASIC_AUTH_PASSWORD` |

### Web UI

```
http://localhost:5678
```

### Webhook URL Format

```
http://n8n:5678/webhook/<workflow-path>
```

---

## Traefik (Reverse Proxy)

| Property   | Value     |
| ---------- | --------- |
| Host       | `traefik` |
| HTTP Port  | `80`      |
| HTTPS Port | `443`     |
| Dashboard  | `8090`    |

### Dashboard

```
http://localhost:8090/dashboard/
```

### Example Router Labels

```yaml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.myapp.rule=Host(`myapp.localhost`)"
  - "traefik.http.routers.myapp.entrypoints=web"
  - "traefik.http.services.myapp.loadbalancer.server.port=3000"
```

---

## Tor Proxy

| Property         | Value                               |
| ---------------- | ----------------------------------- |
| Host             | `tor`                               |
| SOCKS Port       | `9050`                              |
| Control Port     | `9051`                              |
| Control Password | From `.env`: `TOR_CONTROL_PASSWORD` |

### HTTP Proxy (via Privoxy)

| Property | Value     |
| -------- | --------- |
| Host     | `privoxy` |
| Port     | `8118`    |

### Usage Examples

**cURL (SOCKS5)**

```bash
curl --socks5 localhost:9050 https://api.ipify.org
```

**cURL (HTTP proxy)**

```bash
curl --proxy localhost:8118 https://api.ipify.org
```

**Python (requests)**

```python
proxies = {
    'http': 'socks5h://localhost:9050',
    'https': 'socks5h://localhost:9050'
}
requests.get('https://api.ipify.org', proxies=proxies)
```

**Python (HTTP)**

```python
proxies = {'http': 'http://localhost:8118', 'https': 'http://localhost:8118'}
requests.get('https://api.ipify.org', proxies=proxies)
```

### Renew Tor Circuit

```bash
# Via control port
echo -e 'AUTHENTICATE "<TOR_CONTROL_PASSWORD>"\r\nsignal NEWNYM\r\n' | nc localhost 9051

# Or via Docker exec
docker exec devtools_tor tor-controlpanel reload
```

---

## Celery Worker

| Property | Value      |
| -------- | ---------- |
| Broker   | Redis DB 0 |
| Backend  | Redis DB 1 |

### Task Definitions

```python
# tasks.py
from celery import Celery

app = Celery("devtools_worker")
app.conf.update(
    broker_url="redis://:devtools_redis_password@redis:6379/0",
    result_backend="redis://:devtools_redis_password@redis:6379/1",
)

@app.task
def process_data(data):
    return {"processed": data}
```

### Calling Tasks

```python
from tasks import process_data

# Submit task (async)
result = process_data.delay("hello")

# Get result (blocking)
result.get(timeout=30)
```

---

## Quick Environment Template

Copy this to your project's `.env`:

```bash
# =============================================================================
# Dev Tools Connection - Copy values from dev_tools/.env
# =============================================================================

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
