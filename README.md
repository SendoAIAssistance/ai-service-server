<div align="center">

# Sendo AI TechSupport Agent

**Enterprise-grade AI assistance for Sendo operations, onboarding, and daily technical support.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-0.3%2B-121212?logo=chainlink&logoColor=white)](https://www.langchain.com/)
[![Hugging Face](https://img.shields.io/badge/Hugging%20Face-Models-FFD21E?logo=huggingface&logoColor=black)](https://huggingface.co/)
[![PyTorch](https://img.shields.io/badge/PyTorch-GPU%20ready-EE4C2C?logo=pytorch&logoColor=white)](https://pytorch.org/)
[![CUDA](https://img.shields.io/badge/CUDA-12.x-76B900?logo=nvidia&logoColor=white)](https://developer.nvidia.com/cuda-zone)
[![Ollama](https://img.shields.io/badge/Ollama-Compatible-000000?logo=ollama&logoColor=white)](https://ollama.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-47A248?logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Prometheus](https://img.shields.io/badge/Prometheus-%2Fmetrics-E6522C?logo=prometheus&logoColor=white)](https://prometheus.io/)
[![Pydantic](https://img.shields.io/badge/Pydantic-v2-3776AB?logo=pydantic&logoColor=white)](https://docs.pydantic.dev/)
[![Uvicorn](https://img.shields.io/badge/Uvicorn-ASGI-111111?logo=uvicorn&logoColor=white)](https://www.uvicorn.org/)
[![pytest](https://img.shields.io/badge/pytest-tested-0A9EDC?logo=pytest&logoColor=white)](https://pytest.org/)

</div>

---

## Introduction

Welcome to the **Sendo AI TechSupport Agent** repository. This project delivers a backend AI service that understands Sendo’s workflows, policies, and systems well enough to act as a **co-pilot for technical support teams**—from first-day onboarding questions to complex troubleshooting across business domains.

This project is an AI Agent that has deep knowledge of Sendo's entire business operations. It acts as an intelligent coordinator and assistant for all system users and especially provides specialized onboarding and daily support for new techsupport staff joining the company.

Whether you are a **developer** integrating the API, an **ML engineer** tuning models, or a **non-technical tech support teammate** validating answers, this README is structured so you can jump to the sections that matter most.

### Who this documentation is for

| Audience | What you will find most useful |
|----------|--------------------------------|
| **New tech support staff** | Purpose, Quick Start, Features (plain-language notes), and Contact |
| **Backend / full-stack engineers** | Installation, Architecture, API examples, troubleshooting |
| **ML / data scientists** | Trained Models, Project Structure (`data/`, `fine_tuning/`, `models/`) |
| **DevOps / SRE** | Installation (GPU/Docker), metrics endpoint, operational guidance |

<details>
<summary><strong>Glossary (terms used throughout this README)</strong></summary>

| Term | Meaning |
|------|---------|
| **Agent** | The overall system behavior: routing, tools, models, and policies working together—not a single neural network by itself. |
| **Orchestration** | Logic that decides *which* component runs next (classifier vs basic vs expert, tools, retrieval). |
| **Streaming** | Returning partial tokens/events over time (often SSE) so clients can render responses progressively. |
| **RAG** | Retrieval-augmented generation: fetch relevant documents/snippets before answering. |
| **Grounding** | Anchoring answers to trusted sources (docs, DB fields) to reduce unsupported claims. |
| **Intent** | A high-level label for what the user is trying to do (e.g., “how-to”, “escalation”, “policy lookup”). |

</details>

---

## Purpose of the Project

| Goal | What it means in practice |
|------|---------------------------|
| **Operational clarity** | Surface accurate, context-aware guidance about Sendo processes, tools, and expectations—reducing time spent searching internal docs. |
| **Onboarding acceleration** | Give new tech support hires a consistent “first responder” that explains systems, escalation paths, and day-to-day routines. |
| **Daily assistance** | Support recurring ticket patterns, clarifications, and cross-team coordination with a unified conversational interface. |
| **Safe coordination** | Route queries intelligently (classification + orchestration) so simpler questions do not overload expert pathways—and complex cases get the right depth. |
| **Measurable operations** | Expose standard API and observability hooks (e.g., metrics) suitable for staging and production monitoring. |

> **Note for stakeholders:** The agent is designed to **assist**, not replace, human judgment—especially for customer-impacting decisions, compliance-sensitive topics, and anything requiring verified live system state.

### Outcomes we optimize for

| Outcome | Indicator (examples) |
|---------|------------------------|
| **Faster onboarding** | Time-to-first-successful-ticket, reduced repeated questions |
| **Consistent guidance** | Fewer contradictory answers for the same policy question |
| **Controlled cost** | Lower average model spend per conversation via routing |
| **Operational trust** | Traceable logs/metrics and reviewable failure modes |

<details>
<summary><strong>Boundaries & responsible use (read once)</strong></summary>

- Treat model outputs as **draft guidance** unless your workflow explicitly marks them as verified.
- Do not paste **secrets** (passwords, tokens, private customer data) into prompts unless your security review approves it.
- Prefer **internal documentation links** and **ticket system procedures** for authoritative policy.

</details>

---

## Trained Models

This stack is built around **multiple specialized models**, each tuned for a distinct responsibility in the agent pipeline. Together they enable **fast routing**, **reliable general support**, and **deep domain reasoning** when the business context demands it.

### Model lineup

| Model key | Base architecture | Primary role |
|-----------|-------------------|----------------|
| **`classifier_model`** | Fine-tuned from **Llama 3** | Intelligent query classification and routing |
| **`basic_model`** | Fine-tuned from **Llama 3.1** | General conversational support and standard ticket handling |
| **`expert_model`** | Fine-tuned from **Qwen 3.5** | Expert-level domain knowledge and complex Sendo business scenarios |

### Comparison at a glance

| Dimension | `classifier_model` | `basic_model` | `expert_model` |
|-----------|-------------------|---------------|----------------|
| **Primary objective** | Route/label | Helpful resolution | Deep domain reasoning |
| **Typical latency target** | Lowest | Medium | Higher (acceptable) |
| **Best for** | Intent + triage | Routine tickets | Exceptions + cross-domain |
| **Risk if misused** | Wrong routing | Overconfidence on edge cases | Higher cost without uplift |

### What each model does (detailed)

#### `classifier_model` (Llama 3–based)

The classifier is the **front door** of the system. It ingests user messages (and lightweight context such as recent turns or metadata when available) and predicts **intent**, **urgency**, and the **downstream handling strategy**.

- **Routing:** Decides whether a request should be answered by lightweight tooling, the general conversational model, or escalated toward expert reasoning.
- **Stability:** Trained to be robust to noisy phrasing—common in real support chats—so the pipeline does not thrash between paths.
- **Efficiency:** Keeps latency and cost predictable by preventing unnecessary expert calls for straightforward intents.

#### `basic_model` (Llama 3.1–based)

The basic model is the **workhorse** for most day-to-day interactions: clarifying procedures, summarizing known policies, suggesting next steps for standard tickets, and maintaining a helpful, consistent tone.

- **Conversational support:** Handles multi-turn dialogue for routine questions and ticket triage guidance.
- **Standard ticket handling:** Supports repeatable workflows (checklists, common resolutions, documentation pointers) without requiring deep domain specialization.
- **Quality bar:** Fine-tuning on Llama 3.1 emphasizes balanced instruction-following and generalization across varied user styles.

#### `expert_model` (Qwen 3.5–based)

The expert model is invoked when the business context is **non-trivial**: cross-domain dependencies, nuanced Sendo operational rules, exception paths, or scenarios that require **high recall** of domain specifics.

- **Complex Sendo scenarios:** Better equipped for multi-constraint problems where multiple internal policies interact.
- **Depth over speed:** Prioritizes correctness and thoroughness for high-stakes answers; orchestration should still shield it from trivial traffic.
- **Expert-level domain knowledge:** Complements the basic model by reducing hallucination risk in specialized areas—especially when paired with retrieval and tool use in the application layer.

<details>
<summary><strong>How the models work together (typical flow)</strong></summary>

1. **Classify** with `classifier_model` to determine intent and route.
2. **Resolve** most interactions with `basic_model` for speed and coverage.
3. **Escalate** selectively to `expert_model` when classification signals complexity, risk, or domain depth.

This pattern is standard in multi-model agents: **a small/fast routing brain**, a **general responder**, and a **heavyweight specialist** for the long tail.

</details>

### Model lifecycle & ownership (recommended)

| Stage | Recommended practice |
|------|-----------------------|
| **Data** | Store sanitized corpora under `data/` with clear licensing and retention rules. |
| **Training** | Version configs in `fine_tuning/`; record dataset hashes and base model IDs. |
| **Evaluation** | Maintain golden questions for routing, basic answers, and expert edge cases. |
| **Packaging** | Publish artifacts to Hugging Face (or internal registry) with model cards. |
| **Serving** | Map logical names (`classifier_model`, `basic_model`, `expert_model`) to runtime endpoints. |
| **Rollback** | Keep N−1 weights available for quick revert if quality regresses. |

<details>
<summary><strong>Model risk notes (production teams)</strong></summary>

- **Routing drift:** If the classifier degrades, you may see unnecessary expert calls (cost) or under-escalation (risk). Monitor route distribution over time.
- **Expert overuse:** Even strong models can be wrong on rare policies—pair expert outputs with retrieval and escalation rules.
- **Latency budgets:** Streaming improves perceived speed; still set timeouts for each hop (API → orchestrator → model).

</details>

---

## Project Structure

The layout below reflects a **mature multi-model LLM agent** codebase: API surface, orchestration, model artifacts, data lifecycle, and operational tooling. Some paths are **repository-specific**; others are **recommended** for teams scaling training and deployment.

```text
sendo-ai-techsupport-agent/
├── README.md                      # Project overview (this file)
├── LICENSE                        # License terms
├── Makefile                       # Convenience targets (serve, install, dev helpers)
├── Dockerfile                     # Container image definition (customize for your deployment)
├── docker-compose.yml             # Optional local stack (add if you use compose)
├── pyproject.toml                 # Python packaging metadata (project name, deps)
├── requirements.txt               # Pinned/runtime dependencies for pip installs
├── setup.py                       # Legacy setuptools entry (if used in your workflow)
├── .env.example                   # Example environment variables (copy to .env)
├── .gitignore                     # Ignore rules for secrets, caches, and artifacts
│
├── src/                           # Primary application source
│   ├── main.py                    # FastAPI app entrypoint, middleware, routers, metrics
│   ├── test_api.py                # API-level tests / manual integration checks
│   ├── cases_unsovled.txt         # Optional case logs / QA notes (project-specific)
│   ├── test_cases.txt             # Optional test prompts / scenarios
│   │
│   ├── ai_engine/                 # Core AI engine package
│   │   ├── core/                  # Configuration, logging, shared settings
│   │   │   ├── config.py          # Settings (paths, Mongo URI, model hosts, etc.)
│   │   │   └── server_logging.py# Structured logging + request correlation
│   │   ├── api/                   # HTTP API layer
│   │   │   ├── dependencies.py    # FastAPI dependencies (auth, clients, etc.)
│   │   │   └── routes/
│   │   │       └── chat_routes.py # Chat/agent endpoints
│   │   ├── schemas/               # Pydantic models for request/response validation
│   │   │   ├── chat_schema.py
│   │   │   └── ai_schema.py
│   │   └── services/              # Business + AI orchestration services
│   │       ├── ai_service.py      # High-level AI orchestration entrypoints
│   │       ├── database/
│   │       │   └── mongo_manager.py # MongoDB access patterns (sessions, metadata, etc.)
│   │       ├── agents/            # Multi-agent orchestration
│   │       │   ├── orchestra.py   # Coordinator logic across experts / tools
│   │       │   ├── state.py       # Conversation/agent state containers
│   │       │   └── experts/       # Specialized expert modules + routing floors
│   │       │       ├── dynamic_router/
│   │       │       ├── process_expert.py
│   │       │       ├── table_expert.py
│   │       │       └── tools_expert.py
│   │       └── scripts/
│   │           └── ingest_schema.py # Data/schema ingestion utilities
│   │
│   ├── storage/                   # Local artifacts (large files may be gitignored)
│   │   ├── models/                # Model definitions, Ollama Modelfiles, export stubs
│   │   │   └── custom/            # Custom model packaging (e.g., *.Modelfile)
│   │   └── vector_db/             # Embeddings / dictionary stores (when enabled)
│   │
│   └── tests/                     # Unit/integration tests
│       ├── test_orchestra.py
│       └── llm_test.py
│
├── models/                        # (Recommended) Published weights & checkpoints
│   ├── classifier_model/          # Artifacts for routing model
│   ├── basic_model/               # Artifacts for general support model
│   └── expert_model/              # Artifacts for expert model
│
├── data/                          # (Recommended) Curated datasets & corpora
│   ├── raw/                       # Immutable source dumps (tickets, docs—sanitized)
│   ├── processed/                 # Tokenized / chunked / labeled datasets
│   └── evaluation/                # Benchmarks + golden questions for regression tests
│
├── fine_tuning/                   # (Recommended) Training pipelines & experiment tracking
│   ├── configs/                   # YAML/JSON training configs
│   ├── scripts/                   # launch_train.sh, deepspeed, etc.
│   └── notebooks/                 # Exploratory analysis (optional)
│
├── inference/                     # (Recommended) Serving profiles & load tests
│   ├── ollama/                    # Modelfiles, model cards, runbooks
│   ├── vllm/                      # Alternative high-throughput serving configs
│   └── load_tests/                # k6/Locust scenarios
│
├── api/                           # (Optional) API contracts separate from code
│   └── openapi/                   # Extra OpenAPI snippets / client generation
│
├── frontend/                      # (Optional) Internal chat UI or admin console
│   └── README.md                  # UI-specific setup (if present)
│
├── docs/                          # (Recommended) Architecture notes, ADRs, runbooks
│   ├── architecture/              # Diagrams + deep dives
│   ├── onboarding/                # Playbooks for new engineers and support staff
│   └── security/                # Threat model + data handling guidelines
│
└── scripts/                       # Operational scripts (backup, deploy, smoke tests)
    ├── setup_dev_environment.sh
    └── download_models.sh
```

### Folder guide (what belongs where)

| Path | Purpose |
|------|---------|
| `src/ai_engine/` | **Runtime logic**: API routes, orchestration, database adapters, schemas. |
| `src/storage/` | **Local runtime assets** (vector stores, Modelfiles); keep large binaries out of git when possible. |
| `models/` | **Versioned model weights** (often LFS or downloaded at deploy time). |
| `data/` | **Training/eval data** with clear separation between raw and processed. |
| `fine_tuning/` | **Reproducible training** scripts and configs—your source of truth for model updates. |
| `inference/` | **Serving** tuning: batching, quantization notes, and performance validation. |
| `docs/` | **Human documentation**: onboarding, security reviews, architecture decision records. |
| `scripts/` | **Automation**: bootstrap, downloads, CI helpers—anything runnable by operators. |

### Repository map: what exists today vs recommended additions

| Area | In-repo today (typical) | Recommended next step |
|------|-------------------------|-------------------------|
| **API** | `src/main.py`, `src/ai_engine/api/routes/` | Add integration tests per route contract |
| **Orchestration** | `src/ai_engine/services/agents/` | Centralize routing policy + feature flags |
| **Models** | `src/storage/models/` (Modelfiles, packaging) + optional top-level `models/` | Standardize download scripts in `scripts/` |
| **Docs** | `README.md` | Add `docs/` runbooks for on-call + incident response |
| **Frontend** | Optional / separate repo | Internal chat UI for QA and demos |

<details>
<summary><strong>Where to put large artifacts (weights, caches)</strong></summary>

- Keep **multi‑GB checkpoints** out of git; store in object storage or download at deploy time.
- Add ignore rules for `models/**` checkpoints, `**/.cache/`, and local vector stores unless your team explicitly versions small artifacts.

</details>

---

## Installation

This section is written for **Windows**, **macOS**, and **Linux** (including **WSL2**). Adjust paths if your organization uses a different layout.

### Prerequisites

- **Python** `3.10+` (3.11 recommended for many ML stacks)
- **Git**
- **A NVIDIA GPU** (optional but recommended for local inference/training)
  - Install the **NVIDIA driver** compatible with your CUDA toolkit
  - For PyTorch GPU wheels, follow the official matrix for your CUDA version
- **MongoDB Atlas URI** (if the deployment uses MongoDB features)
- **Ollama** or another compatible LLM runtime (if you serve local models)

<details>
<summary><strong>Windows-specific notes</strong></summary>

- Prefer **Python from python.org** or a managed distribution you standardize on.
- Virtual environments: `python -m venv .venv` then activate with `.venv\Scripts\activate`.
- If you use **WSL2**, follow the Linux steps inside Ubuntu for fewer toolchain surprises.

</details>

### 1) Clone the repository

```bash
git clone git@github.com:SendoAIAssistance/ai-service-server.git
cd ai-service-server
```

### 2) Create and activate a virtual environment

**Linux / macOS / WSL2**

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

**Windows (PowerShell)**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

### 3) Install Python dependencies

```bash
pip install -r requirements.txt
```

If your environment requires editable installs:

```bash
pip install -e .
```

### 4) Configure environment variables

Copy the example file and edit values for your environment:

```bash
cp .env.example .env
```

| Variable (example) | Purpose |
|--------------------|---------|
| `MONGODB_ATLAS_URI` | Connection string for MongoDB Atlas (if used) |
| `OLLAMA_HOST` | Host/port for Ollama or compatible local inference endpoint |
| `WEATHER_API_API_KEY` | Optional tool integration key (if enabled in your deployment) |

> **Security:** Never commit `.env` to git. Rotate keys if they leak.

<details>
<summary><strong>Expanded environment variable reference (common keys)</strong></summary>

| Variable | Type | Example | Notes |
|----------|------|---------|-------|
| `MONGODB_ATLAS_URI` | string | `mongodb+srv://user:pass@cluster/...` | Use least-privilege DB user; rotate regularly |
| `OLLAMA_HOST` | string | `http://127.0.0.1:11434` | Include scheme; match your inference deployment |
| `WEATHER_API_API_KEY` | string | `<token>` | Only if tool integration is enabled |
| `PYTHONPATH` | string | `src` | Sometimes needed for tests/imports in nonstandard layouts |

**Application settings** may also be defined in `src/ai_engine/core/config.py` (for example `PROJECT_NAME`, paths, and defaults). Treat that file as the source of truth for:

- default project metadata
- filesystem paths for dictionaries/vector stores (when used)
- integration points for tools and external services

If you add new secrets, prefer:

1. `.env` for local development
2. secret manager / Kubernetes secrets for staging/production

</details>

<details>
<summary><strong>Example <code>.env</code> skeleton (do not copy secrets)</strong></summary>

```dotenv
# --- Core ---
# MONGODB_ATLAS_URI=mongodb+srv://USER:PASSWORD@cluster.mongodb.net/?retryWrites=true&w=majority
# OLLAMA_HOST=http://127.0.0.1:11434

# --- Optional tool keys ---
# WEATHER_API_API_KEY=replace_me
```

</details>

### 5) Download models from Hugging Face (example workflow)

Your exact model IDs and filenames depend on internal publishing. A typical pattern:

```bash
pip install huggingface_hub

huggingface-cli download <org>/<classifier_model_repo> --local-dir ./models/classifier_model
huggingface-cli download <org>/<basic_model_repo>       --local-dir ./models/basic_model
huggingface-cli download <org>/<expert_model_repo>     --local-dir ./models/expert_model
```

If you use **private** repositories:

```bash
huggingface-cli login
```

<details>
<summary><strong>Optional: Git LFS for large checkpoints</strong></summary>

Some teams store weights via **Git LFS**. If your model repo requires it:

```bash
git lfs install
git clone <your-model-weights-repo>
```

</details>

### 6) GPU setup (PyTorch + CUDA)

This repository’s `requirements.txt` may include a PyTorch CUDA wheel index (verify the CUDA version matches your system). Example install pattern:

```bash
# Example only — use the CUDA build that matches your machine
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

Validate GPU visibility:

```python
import torch
print(torch.cuda.is_available(), torch.cuda.get_device_name(0))
```

### 7) Run the API service (development)

**Uvicorn (recommended for local dev)**

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**Makefile (Linux/macOS/WSL)**

```bash
make install
make serve
```

**Windows note:** If `make` is unavailable, use the `uvicorn` command directly.

### 8) Verify the deployment

- **OpenAPI docs:** `http://localhost:8000/docs`
- **Metrics:** `http://localhost:8000/metrics` (Prometheus instrumentation)

<details>
<summary><strong>Optional: Public tunnel for demos (ngrok)</strong></summary>

If your `Makefile` includes a tunnel target, ensure ngrok is installed and authenticated:

```bash
ngrok config add-authtoken <token>
ngrok http 8000
```

</details>

### 9) Ollama (optional local inference)

If you run models through **Ollama**, install it for your platform and ensure the daemon is reachable.

```bash
# Example: check server (adjust host/port to match your environment)
curl http://localhost:11434/api/tags
```

Set `OLLAMA_HOST` in `.env` if your daemon is not on the default address. Map logical model names used by the app to Ollama tags (e.g., `basic_model:latest`) according to your deployment convention.

<details>
<summary><strong>Modelfiles and custom merges</strong></summary>

Teams often keep **Modelfile** definitions under `src/storage/models/custom/` to document prompts, parameters, and adapter merges. Treat these as **build recipes**: rebuild images/tags when you change them.

</details>

### 10) Docker (optional)

The repository may ship a minimal `Dockerfile`. For production, prefer a multi-stage image that:

- installs only runtime dependencies
- runs as a non-root user
- uses pinned base image digests

Example pattern (adjust to your organization’s base images):

```dockerfile
# Example only — validate versions before production use
FROM python:3.11-slim AS runtime
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src ./src
COPY pyproject.toml .
EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:

```bash
docker build -t sendo-ai-techsupport:dev .
docker run --rm -p 8000:8000 --env-file .env sendo-ai-techsupport:dev
```

<details>
<summary><strong>docker-compose (local stack sketch)</strong></summary>

```yaml
# docker-compose.yml (example — add services you need: MongoDB, Ollama, etc.)
services:
  api:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    # depends_on:
    #   - mongo
```

</details>

### 11) Production readiness checklist (operators)

| Check | Why it matters |
|------|----------------|
| **Secrets** managed via vault/secret manager | Prevents `.env` leakage in images |
| **TLS termination** at ingress | Protects tokens and customer data in transit |
| **Rate limits** / auth on public endpoints | Reduces abuse and cost spikes |
| **Log redaction** | Prevents accidental PII in centralized logs |
| **Backups** for operational DB | Recovery for sessions and audit metadata |
| **Dashboards** | Latency, error rate, route distribution, GPU utilization |

### 12) Troubleshooting

| Symptom | Likely cause | What to try |
|---------|--------------|-------------|
| `torch.cuda.is_available()` is `False` | Driver/CUDA mismatch or CPU-only wheel | Reinstall PyTorch with correct CUDA index; verify `nvidia-smi` |
| Mongo connection errors | Wrong URI, IP allowlist, or credentials | Validate Atlas network access + user/role |
| Slow first token | Cold start / model load | Pre-warm models; keep a warm pool |
| 422 validation errors | Client payload mismatch | Compare request schema in `/docs` |
| SSE stream hangs | Upstream model stall | Set timeouts; inspect orchestrator logs |

<details>
<summary><strong>Deep diagnostics (developers)</strong></summary>

1. Confirm **request IDs** in logs (`X-Request-ID`) and correlate across services.
2. Capture **minimal repro** prompts (sanitized) for routing issues.
3. Compare **route distribution** before/after classifier updates.
4. For GPU OOM, reduce batch size, enable quantization, or move larger models to dedicated workers.

</details>

<details>
<summary><strong>Windows development tips (PowerShell)</strong></summary>

If script execution policy blocks activation:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

If you need to bind to all interfaces during LAN testing:

```powershell
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Firewall prompts may appear the first time—approve only on trusted networks.

</details>

<details>
<summary><strong>Version pinning strategy</strong></summary>

- Pin **major/minor** versions for frameworks (`fastapi`, `pydantic`, `langchain*`) to avoid surprise breaking changes.
- Pin **CUDA/PyTorch** combinations explicitly for GPU environments.
- Re-run your **golden tests** after dependency upgrades—especially when upgrading LangChain.

</details>

---

## Quick Start

1. **Install** dependencies and configure `.env`.
2. **Start** the API with Uvicorn (see Installation).
3. **Open** Swagger UI at `/docs` and run a sample chat request against the documented endpoint.
4. **Watch** logs for request IDs (useful when correlating support cases with engineering).

**Minimal mental model:** *Classify → route → respond (basic) → escalate (expert) when needed.*

### Call the chat endpoint (curl)

The chat route is implemented as **multipart form data** and returns a **streaming** response (`text/event-stream`). Example:

```bash
curl -N -X POST "http://localhost:8000/api/v1/chat" \
  -H "Accept: text/event-stream" \
  -F "conversationId=demo-thread-001" \
  -F "message=Hello from Quick Start"
```

> **Note:** If your deployment uses a different `APP_PREFIX`, adjust the prefix accordingly (see `src/ai_engine/core/config.py` and `src/main.py`).

<details>
<summary><strong>Python example (streaming consumer sketch)</strong></summary>

```python
import requests

url = "http://localhost:8000/api/v1/chat"
files = {
    "conversationId": (None, "demo-thread-001"),
    "message": (None, "Hello from Python"),
}
with requests.post(url, files=files, stream=True, timeout=300) as resp:
    resp.raise_for_status()
    for chunk in resp.iter_content(chunk_size=None):
        if chunk:
            print(chunk.decode("utf-8", errors="ignore"), end="")
```

</details>

<details>
<summary><strong>FAQ (quick answers)</strong></summary>

**Q: Where is OpenAPI documentation?**  
A: `http://localhost:8000/docs` (Swagger UI).

**Q: Where are Prometheus metrics?**  
A: `http://localhost:8000/metrics`.

**Q: Do I need a GPU?**  
A: Not strictly for API development, but recommended for local inference/training throughput.

**Q: Can I use only one model?**  
A: You can wire a simplified deployment, but you lose the cost/latency benefits of routing and specialization.

**Q: How do I report a bad answer?**  
A: Capture the **request ID**, timestamp, sanitized prompt, and expected policy—open an issue internally per your process.

</details>

### API conventions (practical)

| Topic | Convention |
|------|------------|
| **Base path** | Typically `/api/v1` (see `src/main.py` and settings) |
| **Chat transport** | `POST` with `multipart/form-data` fields |
| **Streaming** | `text/event-stream` (SSE) consumer should handle partial chunks |
| **Correlation** | Send/propagate `X-Request-ID` for support escalations |

<details>
<summary><strong>Client integration checklist</strong></summary>

- **Timeouts:** streaming calls need generous read timeouts; add client-side cancel on navigation.
- **Retries:** use idempotency keys only if your backend supports them; chat may not be idempotent.
- **Uploads:** validate file types/size limits at the gateway before hitting the API.
- **Localization:** if you support Vietnamese + English, pass the user language as metadata when you add that field.

</details>

---

## Features

| Feature | Benefit |
|---------|---------|
| **Multi-model orchestration** | Optimizes cost/latency by routing simple work to lighter paths. |
| **Tech support–focused onboarding** | Helps new staff learn processes faster with consistent guidance. |
| **FastAPI + OpenAPI** | Fast integration for internal tools and automated clients. |
| **Structured schemas** | Predictable request/response contracts via Pydantic models. |
| **Observability hooks** | Prometheus metrics endpoint for production monitoring. |
| **MongoDB integration** | Persistent/session patterns suitable for operational data (as configured). |
| **Extensible experts** | Modular “expert” components for domain-specific behaviors. |
| **Streaming responses** | SSE-friendly streaming for responsive UX in chat UIs |
| **Request correlation** | Request ID middleware helps debug multi-step agent flows |

<details>
<summary><strong>Feature details for support staff (non-technical)</strong></summary>

- You can think of the agent as a **smart internal search + coach**: it helps you find the right procedure and asks clarifying questions when needed.
- For anything that could affect a customer’s account, billing, or compliance, **confirm with your lead** and follow your team’s escalation policy.

</details>

<details>
<summary><strong>Capability matrix (what to expect)</strong></summary>

| Capability | Supported well | Notes |
|-------------|----------------|-------|
| **Explaining internal procedures** | ✅ | Best when grounded with internal docs/retrieval |
| **Ticket triage suggestions** | ✅ | Pair with your ticket taxonomy and SLAs |
| **Live production debugging** | ⚠️ | Requires tools/telemetry; do not assume live access |
| **Legal/compliance determinations** | ❌ | Human review required |

</details>

<details>
<summary><strong>Security & privacy features (recommended practices)</strong></summary>

- **Minimize PII** in prompts; use internal IDs where possible.
- **Redact** customer details in logs.
- **Separate** staging and production keys and databases.
- **Audit** model upgrades with regression suites for routing and safety.

</details>

---

## Architecture Overview

### High-level description

The system follows a **layered architecture**:

1. **API layer (FastAPI):** Validates inputs, attaches request IDs, exposes OpenAPI docs and metrics.
2. **Orchestration layer:** Coordinates agents/experts, decides tool usage, and manages conversation state.
3. **Model layer:** Executes `classifier_model`, `basic_model`, and `expert_model` according to routing policy.
4. **Data layer:** Connects to databases (e.g., MongoDB) and optional retrieval/vector stores for grounded answers.

### Component responsibilities (C4-style, brief)

| Component | Responsibility | Primary interfaces |
|-----------|----------------|--------------------|
| **FastAPI app** | HTTP, validation, middleware, CORS | REST/SSE |
| **Chat routes** | Agent entrypoints for chat flows | `multipart/form-data` |
| **AIService / agents** | Orchestration, tools, streaming | Internal service calls |
| **Mongo manager** | Persistence/session patterns (as configured) | MongoDB wire protocol |
| **Model runtimes** | `classifier_model`, `basic_model`, `expert_model` | Local inference (HTTP/gRPC) |

### Mermaid diagram (conceptual)

```mermaid
flowchart LR
  U[Users / Internal Tools] -->|HTTPS JSON| API[FastAPI /api/v1]
  API --> OR[Orchestrator / Agents]
  OR --> C[classifier_model\nLlama 3]
  OR --> B[basic_model\nLlama 3.1]
  OR --> E[expert_model\nQwen 3.5]
  OR --> DB[(MongoDB Atlas)]
  OR --> VS[(Vector / Dictionary\noptional)]
  API --> M[/Prometheus /metrics/]
```

### Mermaid sequence (request lifecycle)

```mermaid
sequenceDiagram
  participant Client
  participant API as FastAPI
  participant Orc as Orchestrator
  participant Clf as classifier_model
  participant Bas as basic_model
  participant Exp as expert_model

  Client->>API: Chat request + metadata
  API->>Orc: Dispatch conversation turn
  Orc->>Clf: Classify intent / route
  alt Standard handling
    Orc->>Bas: Generate response
    Bas-->>Orc: Answer + rationale (optional)
  else Expert path
    Orc->>Exp: Deep reasoning / domain answer
    Exp-->>Orc: Answer + citations/tools (optional)
  end
  Orc-->>API: Final response payload
  API-->>Client: JSON result
```

### Deployment view (conceptual)

```mermaid
flowchart TB
  Internet[Clients / Internal Apps]
  LB[Load Balancer / API Gateway]
  API1[FastAPI Instance 1]
  API2[FastAPI Instance 2]
  INF[Model Inference Layer\n(Ollama / vLLM / Triton)]
  DB[(MongoDB Atlas)]
  PROM[Prometheus / Grafana]

  Internet --> LB --> API1
  LB --> API2
  API1 --> INF
  API2 --> INF
  API1 --> DB
  API2 --> DB
  API1 --> PROM
  API2 --> PROM
```

<details>
<summary><strong>Scaling notes</strong></summary>

- **Scale API** horizontally once inference is separated.
- **Isolate** heavy expert workloads on dedicated GPU nodes if latency spikes.
- **Cache** retrieval results when safe (short TTL) to reduce repeated DB/vector lookups.

</details>

### Data flow (retrieval + generation, conceptual)

```mermaid
flowchart TD
  Q[User question] --> R[Retrieve context\n(vector DB / docs)]
  Q --> C[classifier_model]
  C -->|simple| B[basic_model]
  C -->|complex| E[expert_model]
  R --> B
  R --> E
  B --> A[Answer stream]
  E --> A
```

This diagram is **illustrative**: your deployment may omit retrieval for some routes, or always retrieve for policy-heavy questions.

<details>
<summary><strong>Failure modes to design for</strong></summary>

| Failure | User-visible symptom | Mitigation |
|---------|----------------------|----------|
| Retrieval empty | Generic or overly confident answer | Fallback clarifying questions; “not found” policy |
| Classifier wrong path | Wrong tone/depth | Monitoring + periodic golden tests |
| Expert timeout | Stalled stream | Timeouts + graceful degradation to basic + disclaimer |
| DB outage | Missing session context | Read-only mode or degraded features |

</details>

<details>
<summary><strong>Operational considerations</strong></summary>

- **Latency:** Keep the classifier lightweight; cache stable routing decisions when safe.
- **Safety:** Combine models with **policy checks** and **human review** for sensitive categories.
- **Grounding:** Prefer retrieval-augmented answers for fast-changing operational facts.

</details>

<details>
<summary><strong>Performance & cost knobs (engineering)</strong></summary>

| Knob | Effect | Tradeoff |
|------|--------|----------|
| **Route more to basic** | Lower cost | May miss nuanced answers |
| **Raise expert threshold** | Lower expert spend | Risk under-escalation |
| **Quantization (INT8/INT4)** | Higher throughput / lower VRAM | Possible quality loss |
| **Smaller context windows** | Faster prefill | May drop needed history |
| **Caching retrieval** | Fewer DB/vector queries | Stale answers if docs change often |

Always validate changes with **offline eval** and a **canary** release when possible.

</details>

<details>
<summary><strong>Reliability patterns</strong></summary>

- **Circuit breakers** around inference dependencies
- **Bulkheads** separating interactive chat from batch jobs
- **Graceful degradation**: if expert is unavailable, return a safe basic response + escalation guidance

</details>

<details>
<summary><strong>Observability reference (what to monitor)</strong></summary>

| Signal | Why it matters |
|--------|----------------|
| **p95 latency** (end-to-end) | User experience and SLA tracking |
| **5xx rate** | Stability regressions |
| **Model error rate** | Upstream inference health |
| **Tokens/sec** (if available) | Throughput planning |
| **Route mix** (basic vs expert) | Cost + quality drift detection |
| **DB latency** | Data layer bottlenecks |

Pair metrics with **structured logs** that include request IDs and high-level route decisions (without sensitive content).

</details>

---

## Contributing

We welcome contributions that improve reliability, documentation, and operational clarity.

### How to contribute

1. **Fork** the repository and create a feature branch from `main`.
2. **Discuss** larger changes via an issue first (architecture, new endpoints, model swaps).
3. **Develop** with tests where applicable (`src/tests/`).
4. **Run** formatting/linting if the project adopts them (add scripts if missing).
5. **Open a Pull Request** with:
   - A clear description of the problem and solution
   - Risk notes (API compatibility, data handling)
   - Screenshots or logs for user-visible behavior changes

### Code review values

- **Small diffs** that are easy to review
- **No secrets** in commits
- **Backward compatibility** unless explicitly versioning APIs

### Branching & commits (suggested)

| Practice | Guidance |
|----------|----------|
| **Branch names** | `feat/`, `fix/`, `chore/`, `docs/` prefixes |
| **Commits** | Imperative subject line; explain *why* in the body when non-obvious |
| **Tests** | Add/extend tests for orchestration changes and schema changes |
| **Model changes** | Document dataset/version deltas in the PR description |

<details>
<summary><strong>Security disclosure (contributors)</strong></summary>

If you discover a vulnerability, **do not** open a public issue with exploit details. Contact the maintainers via the organization’s security channel (or email the project contact) and include steps to reproduce with minimal impact.

</details>

### Local testing (pytest)

Install optional test dependencies if your workflow uses them:

```bash
pip install -e ".[test]"
```

Run tests:

```bash
pytest -q
```

<details>
<summary><strong>What to test for agent changes</strong></summary>

- **Routing:** classifier decisions on representative prompts (golden set)
- **Schemas:** request/response validation for API compatibility
- **Streaming:** end-to-end smoke test for SSE clients (timeouts, cancellation)
- **Persistence:** Mongo-dependent flows (use a disposable database or mocks)

</details>

<details>
<summary><strong>Release checklist (maintainers)</strong></summary>

- [ ] Update version strings consistently (`pyproject.toml`, app metadata if applicable)
- [ ] Refresh `requirements.txt` / lockfiles with explicit rationale in the PR
- [ ] Run tests locally and in CI
- [ ] Validate OpenAPI diff for breaking changes
- [ ] Update README sections if endpoints/env vars changed
- [ ] Document model artifact versions and evaluation deltas

</details>

---

## License

This project is licensed under the **MIT License**—see the `LICENSE` file for details.

<details>
<summary><strong>MIT License (short summary)</strong></summary>

The MIT License generally permits **use, modification, and distribution** with minimal restrictions, provided the license and copyright notice are included in copies. **Disclaimer:** this summary is not legal advice; read the full `LICENSE` text for authoritative terms.

</details>

---

## Acknowledgments

- **Sendo** teams and subject-matter experts who shaped domain requirements and operational constraints.
- **Open-source communities** behind FastAPI, LangChain, PyTorch, Hugging Face, and the broader LLM tooling ecosystem.
- **Base model creators and fine-tuning teams** contributing to robust instruction-tuned foundations.
- **Llama** and **Qwen** families and their ecosystems for strong foundations and tooling.
- **Observability** projects (Prometheus ecosystem) that make production operations measurable.

<details>
<summary><strong>Third-party notices (general guidance)</strong></summary>

When you ship derived models or combine weights/adapters, **follow the license terms** of each base model and dataset. Keep records of:

- base model IDs and versions
- training data sources and retention
- evaluation results for major releases

</details>

### Documentation conventions used in this README

- **Collapsible sections** hide optional depth (operators, security, long tables).
- **Tables** summarize decisions quickly; use them in PRs and runbooks too.
- **Mermaid** diagrams are best viewed on GitHub or Markdown renderers that support Mermaid.

If you print or export documentation, expand collapsible sections first so readers do not miss critical operational guidance.

---

## Contact / Support

| Channel | Usage |
|---------|-------|
| **Repository Issues** | Bug reports, feature requests, and documentation fixes |
| **Internal team channel** | Escalations for access, credentials, and production incidents (org-specific) |
| **Email / on-call** | Follow your team’s operational handbook |

**Maintainer / project contact (as configured in the codebase):** FPT Sendo OJT2026-01 Team — `khoile54642005@gmail.com`

### Support expectations (typical)

| Severity | Examples | Target response (example SLA) |
|----------|----------|--------------------------------|
| **S1** | Production outage, auth bypass, data leak risk | Immediate paging per your org |
| **S2** | Major degradation, partial outage | Same business day |
| **S3** | Minor bug, doc fix | Best effort / next sprint |

> Replace the table above with your **official** SLA if your organization publishes one.

<details>
<summary><strong>Information to include when reporting an issue</strong></summary>

- **Environment:** OS, Python version, GPU model, CUDA version (if relevant)
- **Version:** git commit hash or release tag
- **Repro steps:** minimal sequence to trigger the behavior
- **Logs:** include `X-Request-ID` when available (redact secrets)
- **Expected vs actual:** one paragraph each

</details>

<details>
<summary><strong>Enterprise procurement / compliance questions</strong></summary>

For questions about data processing agreements, residency, retention, or vendor assessments, route the request through your **internal compliance** team. Engineering maintainers can help answer technical controls (encryption in transit, access patterns), but legal terms are organization-specific.

</details>

### Status page / incident communication (optional)

If your organization maintains a **status page** or an internal incident channel, link it here when available:

- **Status page URL:** `https://status.example.com` *(replace with your org)*
- **Incident comms policy:** follow your ITIL / SRE process

During incidents, prioritize **customer impact**, **data safety**, and **clear stakeholder updates** over non-urgent feature work.

Keep a **post-incident review** note for model/routing regressions so improvements compound over time.

---

<div align="center">

**Built with care for Sendo’s tech support teams and the engineers who support them.**

</div>
