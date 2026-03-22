# Sendo AI TechSupport Agent — User Guide & Usage Documentation

**Document type:** Internal user guide  
**Audience:** Tech Support staff (new hires through senior), team leads, and internal integrators  
**Classification:** Internal use — follow your department’s data-handling policy  

---

## Table of contents

1. [Introduction](#1-introduction)  
2. [Who Should Use This Guide](#2-who-should-use-this-guide)  
3. [System Requirements & Access](#3-system-requirements--access)  
4. [How to Log In / Start the Agent](#4-how-to-log-in--start-the-agent)  
5. [Understanding the 3 Models & Automatic Routing](#5-understanding-the-3-models--automatic-routing)  
6. [Core Features & How to Use Them](#6-core-features--how-to-use-them)  
7. [Detailed Usage Examples](#7-detailed-usage-examples)  
8. [Advanced Features](#8-advanced-features)  
9. [Best Practices & Tips for Maximum Performance](#9-best-practices--tips-for-maximum-performance)  
10. [Troubleshooting Guide](#10-troubleshooting-guide)  
11. [FAQ](#11-faq)  
12. [Glossary of Sendo-Specific Terms](#12-glossary-of-sendo-specific-terms)  
13. [Version History & Changelog](#13-version-history--changelog)  
14. [Appendix](#14-appendix)  

---

## 1. Introduction

### 1.1 What this system is

The **Sendo AI TechSupport Agent** is an internal AI assistant with deep knowledge of **Sendo business operations**. It is designed to help technical support staff work faster and more consistently by:

- Answering process questions (how things work, where to look, what to do next)  
- Supporting **daily ticket handling** for common scenarios  
- Helping **new employees onboard** with guided explanations and checklists  
- Assisting with **complex business scenarios** by combining retrieval (knowledge lookup) with expert reasoning  

> **Important:** This agent is an **assistant**, not an authority. For customer-impacting actions, refunds, policy exceptions, fraud, or legal/compliance questions, follow your team’s escalation rules and verify in official systems.

### 1.2 How it relates to the three models

The platform is built around three trained models (conceptual names used in documentation and planning):

| Documentation name | Typical role |
|--------------------|--------------|
| **`classifier_model`** (fine-tuned from **Llama 3**) | Decides how to route your question |
| **`basic_model`** (fine-tuned from **Llama 3.1**) | General conversation and standard support responses |
| **`expert_model`** (fine-tuned from **Qwen 3.5**) | Expert reasoning for complex Sendo scenarios |

> **Note:** In the current backend implementation, Ollama model tags may look like `tech_support_classifier_model:latest`, `tech_support_basic_model:latest`, and `tech_support_order_expert:latest`. Your IT team maps these to the documentation names above.

### 1.3 What “success” looks like on day one

You can consider day one successful if you can:

1. Open the agent through your approved channel (web portal, API client, or internal tool).  
2. Start a conversation with a stable **conversation ID**.  
3. Read streaming responses and distinguish **status/planning** messages from the final answer.  
4. Know when to **escalate to a human** instead of trusting the model alone.  

---

## 2. Who Should Use This Guide

### 2.1 Primary readers

| Role | What you will learn |
|------|---------------------|
| **New Tech Support hires** | How to ask good questions, avoid mistakes, and escalate safely |
| **Experienced agents** | How to use the agent for speed without sacrificing accuracy |
| **Team leads / QA** | How to review conversations and spot routing or quality issues |
| **Internal developers** | How end users are expected to interact with APIs and UIs |

### 2.2 What this guide is not

- **Not a replacement** for Sendo’s official policy manuals, HR documents, or legal guidance.  
- **Not a guarantee** that every answer is correct for every edge case.  
- **Not permission** to share secrets, credentials, or unmasked customer PII in prompts.  

### 2.3 How to read this document

- If you are **non-technical**, focus on Sections **1–7** and **9–12**.  
- If you integrate systems, read **4**, **8**, and **14** carefully.  

---

## 3. System Requirements & Access

### 3.1 What you need on your side

| Requirement | Details |
|-------------|---------|
| **Network access** | Access to the internal URL or API gateway your IT team provides |
| **Browser** | Latest stable Chrome/Edge/Firefox (for web UI deployments) |
| **Account** | SSO / VPN / internal auth as required by Sendo IT |
| **Headset (optional)** | If you dictate messages—keep dictation professional and avoid reading sensitive data aloud in public spaces |

### 3.2 Roles and permissions (typical)

> **Tip:** Exact role names depend on your organization. Replace examples with your internal IAM labels.

| Permission | Typical meaning |
|------------|-----------------|
| **Chat user** | Can use the agent in approved channels |
| **Power user** | May access advanced settings where enabled |
| **Integrator** | May call APIs from approved systems |
| **Admin** | Configures models, keys, and endpoints (IT/Platform only) |

### 3.3 Data you should never paste into the agent

> **Warning (data protection)**  
> Do **not** paste: passwords, API keys, full payment card numbers, government IDs, or unmasked customer phone/email unless your security team explicitly approved a workflow.

**Safer alternatives:**

- Use **internal ticket IDs** and **order IDs** as references.  
- Describe issues in **generic terms** when possible (“seller reported late delivery,” not full address dumps).  

### 3.4 Supported languages

The agent may respond in **Vietnamese** and/or **English** depending on configuration and your prompt. If your team standardizes a language for customer-facing text, mirror that standard in internal drafts you copy out of the agent.

---

## 4. How to Log In / Start the Agent

This section covers the **common ways** teams deploy AI assistants. Your organization may offer **one or more** of these. If something is not deployed yet, treat it as **planned** and use the API path that IT confirms.

### 4.1 Web UI (internal portal)

**Typical flow:**

1. Connect to VPN / corporate network if required.  
2. Open the internal portal URL (example): `https://techsupport-ai.sendo.internal`  
3. Sign in with your corporate account (SSO).  
4. Click **“TechSupport Agent”** (name may differ).  

**Screenshot placeholder (replace with real asset):**

![Login screen for internal TechSupport Agent portal](images/login.png)

**Screenshot placeholder — chat workspace:**

![Main chat screen showing conversation, input box, and streaming response](images/chat_workspace.png)

> **Tip:** If you don’t see the menu item, request access via your manager or IT helpdesk ticket template **“AI Tool Access”**.

### 4.2 CLI (command-line) via API

If you have `curl` and permission to reach the API host, you can start a session by sending a chat message. The service exposes a streaming chat endpoint.

**Base URL examples:**

- Local development: `http://localhost:8000`  
- Staging/production: provided by platform team (HTTPS recommended)  

**Health check (quick “is it up?”):**

```bash
curl -s http://localhost:8000/
```

You should see JSON with fields like `status`, `project`, and `mode`.

**Start a streaming chat (multipart form):**

```bash
curl -N -X POST "http://localhost:8000/api/v1/chat" ^
  -H "Accept: text/event-stream" ^
  -H "X-Request-ID: cli-demo-0001" ^
  -F "conversationId=onboarding-day1-user-12345" ^
  -F "message=Chào bạn, hôm nay tôi cần checklist xử lý ticket đơn hàng chậm."
```

> **Note (Windows PowerShell):** Use backtick `` ` `` for line continuation, or put the command on one line. On Linux/macOS, use `\` line breaks as shown in internal developer docs.

**Screenshot placeholder — terminal streaming output:**

![Terminal window showing curl streaming SSE events from the chat endpoint](images/cli_streaming.png)

### 4.3 API (programmatic usage)

**OpenAPI docs:** `GET /docs` on the service host (Swagger UI).  

**Primary chat endpoint (as implemented in this project):**

| Item | Value |
|------|-------|
| **Method** | `POST` |
| **Path** | `/api/v1/chat` (prefix may vary if `APP_PREFIX` is customized) |
| **Content type** | `multipart/form-data` |
| **Fields** | `conversationId` (required), `message` (optional default exists), `files` (optional upload) |
| **Response** | `text/event-stream` (streaming chunks) |

**Non-streaming note:** The endpoint is implemented as streaming. Clients should consume incrementally.

### 4.4 VS Code / editor extension workflow (typical pattern)

Many teams integrate HTTP APIs using:

- **REST Client** (`.http` files)  
- **Thunder Client**  
- **Postman** collections  

**Example `.http` snippet (adjust host):**

```http
### Health
GET http://localhost:8000/

### Chat stream (REST Client may display streaming partially depending on settings)
POST http://localhost:8000/api/v1/chat
Accept: text/event-stream
X-Request-ID: vscode-demo-0002
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary

------WebKitFormBoundary
Content-Disposition: form-data; name="conversationId"

vscode-thread-001
------WebKitFormBoundary
Content-Disposition: form-data; name="message"

Explain the escalation path for a seller dispute about shipping delays.
------WebKitFormBoundary--
```

> **Warning:** Multipart formatting in `.http` files can be fiddly. Many teams prefer `curl` or Postman for multipart streaming.

**Screenshot placeholder — VS Code REST Client:**

![VS Code window with .http file sending a request to the chat API](images/vscode_rest_client.png)

### 4.5 Understanding streaming output (SSE-style)

The backend streams lines like:

```text
data: {"type":"reasoning","content":"Planning...","status":"IN_PROGRESS"}
```

Your UI or terminal may show:

- **`reasoning` events** — planning / intermediate status  
- **token/content events** — answer text chunks (depends on model/tooling)  
- **`error` events** — something failed  
- **`done`** — end of turn  

**Screenshot placeholder — network tab showing event stream:**

![Browser developer tools Network tab listing EventStream frames](images/network_eventstream.png)

---

## 5. Understanding the 3 Models & Automatic Routing

### 5.1 The three models (documentation view)

| Model | Base | Primary purpose |
|------|------|-----------------|
| **`classifier_model`** | Fine-tuned **Llama 3** | Intent classification and routing |
| **`basic_model`** | Fine-tuned **Llama 3.1** | General conversational support and standard ticket handling |
| **`expert_model`** | Fine-tuned **Qwen 3.5** | Expert-level domain knowledge and complex Sendo business scenarios |

### 5.2 How the classifier decides which model to use (conceptual + implementation-aligned)

In the current orchestration logic, the classifier distinguishes at a high level between:

- **`small_talk`**: greetings, casual chat, non-technical chatter  
- **`technical`**: system/order issues, order lookups, troubleshooting, operational questions  

**What happens next:**

| Classifier result | Typical path |
|-------------------|--------------|
| **`small_talk`** | Routed to the **basic** conversational agent |
| **`technical`** | Retrieves similar past cases/knowledge (RAG) when available, then routes to the **expert/reasoning** agent |

> **Tip:** Even if you are “just chatting,” keep work questions in **clear technical wording** if you want the expert path. For example, add: “This is a technical ticket about order X.”

**Diagram placeholder:**

![Flowchart showing classifier to basic vs expert paths](images/routing_flowchart.png)

### 5.3 When to “force” a specific model

**Default:** End users should rely on **automatic routing** for consistency and cost control.

**Practical ways to influence routing without admin access:**

| Goal | What to do |
|------|------------|
| Prefer **expert depth** | Ask a **technical** question with order IDs, error symptoms, and expected vs actual behavior |
| Prefer **basic style** | Keep prompts social/light (not recommended for work-critical answers) |
| Avoid wrong path | Remove ambiguous jokes; start with a one-line **intent**: “Technical issue: …” |

**Admin-only mechanisms (typical in enterprises):**

- Feature flags / configuration in the orchestration service  
- Swapping model tags in the inference server (Ollama/vLLM)  
- Prompt templates in Modelfiles (managed by ML/platform teams)  

> **Warning:** “Forcing” the wrong model can increase hallucination risk (e.g., expert path without needed context). If you believe routing is systematically wrong, report it with examples (Section 10).

---

## 6. Core Features & How to Use Them

### 6.1 Daily ticket support

**What it helps with:**

- Triaging ticket types (shipping, seller, buyer, payment, account)  
- Suggesting next diagnostic steps  
- Summarizing what the customer likely needs  

**How to prompt effectively:**

1. Provide **ticket ID** (if allowed) and **category**.  
2. Include **timeline** (“since yesterday”, “after promotion change”).  
3. State **what you already checked** (reduces repetitive advice).  

**Template:**

```text
Technical issue — Ticket #____
Category: (shipping / seller / payment / account / other)
Customer symptom:
Steps already taken:
Question: What should I verify next, and what is the escalation rule?
```

### 6.2 Complex business scenario solving

Use this for multi-step Sendo scenarios: promotions, seller penalties, order lifecycle edge cases, cross-team dependencies.

**Best practice:** Ask the agent for:

- A **structured plan** (steps)  
- **Checks** against policy (then verify in official docs)  
- **Risks** (what could go wrong if you act too early)  

> **Warning:** For money movement, account bans, or legal disputes, you must follow **authorized workflows** in your ticket system—do not rely on AI alone.

### 6.3 Onboarding & training new staff

**Recommended onboarding prompts:**

- “Give me a day-1 checklist for new tech support at Sendo.”  
- “Explain how we classify ticket severity and SLAs in plain language.”  
- “Quiz me: ask 10 questions about order states and I’ll answer; then correct me.”  

**Screenshot placeholder — onboarding quiz in chat UI:**

![Chat UI showing a quiz-style interaction for training](images/onboarding_quiz.png)

### 6.4 Task coordination & workflow automation

The agent can help **draft**:

- Internal messages to sellers/buyers (you review before sending)  
- Handoff notes for L2/L3  
- Checklists for incident bridges  

**Automation boundary:**

- The agent may **suggest** automation; actual automation requires integrations (Section 8).  

### 6.5 Knowledge base querying

For technical queries, the system may retrieve similar historical cases/context to ground responses.

**How to improve retrieval quality:**

- Use **specific nouns**: order code, error text, feature name.  
- Paste **short** error snippets (redact secrets).  
- Ask: “What are the top 3 likely causes and how to confirm each?”  

---

## 7. Detailed Usage Examples

Each example includes **input → expected output shape** (not verbatim text, since models vary) and a **screenshot description** you can replace with real captures.

> **Note:** Expected outputs describe **structure and intent**, not guaranteed wording.

### Example 1 — Greeting / small talk (routes to basic)

- **Input:** `Chào team, hôm nay mình làm việc với ca sáng, có tip nào giữ tốc độ không?`  
- **Expected output:** Friendly short guidance + asks what you’re working on; may propose a workflow tip.  
- **Screenshot:** ![Small talk greeting response in chat bubble](images/ex01_small_talk.png)  

### Example 2 — Technical: delayed shipment inquiry

- **Input:** `Technical issue — Đơn SO123456789 bị trễ giao 3 ngày, khách hỏi hoàn. Mình cần checklist xác minh trước khi escalate.`  
- **Expected output:** Stepwise verification checklist + questions to confirm carrier status + escalation criteria.  
- **Screenshot:** ![Checklist response with numbered steps](images/ex02_delayed_shipment.png)  

### Example 3 — Seller dispute: wrong item received

- **Input:** `Technical: Seller báo gửi đúng SKU nhưng buyer claim nhận sai. Mình cần các bước thu thập bằng chứng và team liên quan.`  
- **Expected output:** Evidence list (photos, packing, weight), timeline questions, internal routing suggestions.  
- **Screenshot:** ![Evidence checklist message](images/ex03_wrong_item.png)  

### Example 4 — Payment / refund ambiguity

- **Input:** `Technical: Thanh toán hiển thị success nhưng đơn chưa xác nhận. Hướng dẫn mình phân biệt các trạng thái thanh toán và điều tra.`  
- **Expected output:** Distinction between payment states + what to check in systems + escalation triggers.  
- **Screenshot:** ![Payment troubleshooting plan](images/ex04_payment_states.png)  

### Example 5 — New hire asks for SLA overview

- **Input:** `Mình mới vào team. Giải thích SLA theo mức độ ưu tiên và ví dụ ticket mỗi mức.`  
- **Expected output:** SLA framing in plain language + examples + reminder to follow internal tables.  
- **Screenshot:** ![SLA explanation with bullet points](images/ex05_sla_overview.png)  

### Example 6 — Promotion / campaign confusion

- **Input:** `Technical: Khách hỏi tại sao mã giảm giá không áp dụng cho sản phẩm flash sale. Cần các bước kiểm tra điều kiện áp dụng.`  
- **Expected output:** Checks for eligibility rules, time windows, product exclusions, known edge cases.  
- **Screenshot:** ![Promotion eligibility checklist](images/ex06_promotion.png)  

### Example 7 — Account access / login issues

- **Input:** `Technical: Buyer không đăng nhập được app, báo lỗi session. Mình cần flow xử lý từ cơ bản đến escalate.`  
- **Expected output:** Basic troubleshooting ladder + what info to collect + when to escalate security.  
- **Screenshot:** ![Login troubleshooting flow](images/ex07_login_issue.png)  

### Example 8 — Bulk orders / B2B-ish complexity (if applicable)

- **Input:** `Technical: Đơn số lượng lớn, giao từng phần, khách muốn đổi địa chỉ giữa chừng. Mình cần rủi ro và quy trình.`  
- **Expected output:** Risk summary + required validations + stakeholder touchpoints.  
- **Screenshot:** ![Partial delivery address change scenario](images/ex08_bulk_order.png)  

### Example 9 — Internal handoff note drafting

- **Input:** `Draft handoff note to L2: order SO..., symptoms..., logs checked..., suspected root cause..., ask L2 to verify X.`  
- **Expected output:** Concise internal memo with headings + open questions.  
- **Screenshot:** ![Handoff note draft in chat](images/ex09_handoff_draft.png)  

### Example 10 — Knowledge retrieval: “what did we do for similar cases?”

- **Input:** `Technical: Tra cứu các case tương tự lỗi đồng bộ trạng thái đơn sau khi đổi kho. Tóm tắt pattern và cách xác minh.`  
- **Expected output:** Summarized patterns + verification steps; may cite retrieved internal case text if RAG hits exist.  
- **Screenshot:** ![RAG-style response referencing internal knowledge snippets](images/ex10_similar_cases.png)  

### Example 11 — Language switching (optional)

- **Input:** `Answer in English: what should I check first for a missing pickup scan?`  
- **Expected output:** English checklist aligned with internal processes.  
- **Screenshot:** ![English response in bilingual UI](images/ex11_language.png)  

### Example 12 — File upload scenario (if enabled)

- **Input:** (Upload screenshot of error) + `Technical: Lỗi như ảnh khi mở chi tiết đơn.`  
- **Expected output:** Interpretation attempt + what additional data is needed; may vary by OCR/vision availability.  
- **Screenshot:** ![Chat with attached image thumbnail and analysis](images/ex12_upload.png)  

---

## 8. Advanced Features

### 8.1 Custom instructions / system prompts

**Who can change these:** typically **ML/Platform admins**, not frontline agents.

**What exists in many deployments:**

- **Modelfiles** (Ollama) defining persona, tone, and safety boundaries  
- **Orchestrator prompts** for classification and RAG injection  

**What you can do as an agent:**

- Use consistent **user-side templates** (Section 6) to mimic “custom instructions” without changing system prompts.  

### 8.2 Batch processing

If your team needs batch evaluation (many tickets at once), standard practice is:

- Build an internal script that calls `/api/v1/chat` with **unique `conversationId` per ticket**  
- Rate-limit requests to avoid overloading inference  
- Store outputs in your ticket tool as **draft notes** for human review  

**Sketch (Python, synchronous streaming with `requests`):**

```python
import requests

def ask_stream(base_url: str, conversation_id: str, message: str) -> None:
    files = {
        "conversationId": (None, conversation_id),
        "message": (None, message),
    }
    with requests.post(
        f"{base_url}/api/v1/chat",
        files=files,
        stream=True,
        timeout=300,
        headers={"Accept": "text/event-stream"},
    ) as resp:
        resp.raise_for_status()
        for line in resp.iter_lines(decode_unicode=True):
            if line and line.startswith("data:"):
                print(line)

if __name__ == "__main__":
    ask_stream("http://localhost:8000", "batch-0001", "Technical: summarize checks for ...")
```

> **Note:** For high-throughput async batch jobs, your platform team may provide `httpx`/`aiohttp` clients with concurrency limits.

> **Warning:** Batch jobs can spike GPU/CPU usage. Coordinate with platform teams.

### 8.3 Integration with Sendo internal tools (CRM, ticket system, etc.)

**Typical integration patterns:**

| Pattern | Description |
|---------|-------------|
| **Deep links** | Ticket UI links to an agent workspace with prefilled context |
| **Webhook → draft** | Ticket update triggers a draft suggestion stored as internal note |
| **Read-only lookups** | Agent queries allowed APIs for order/ticket facts (requires engineering) |

> **Tip:** Treat integrations as **internal projects** with security review. Do not connect production databases to experimental scripts.

### 8.4 API usage — endpoints + examples

#### 8.4.1 Root health

```http
GET /
```

**Example response shape:**

```json
{
  "statusCode": 200,
  "status": "Online",
  "project": "Tech Support Agent",
  "mode": "Orchestra of Agents",
  "message": "Welcome to Tech Support Agent AI Engine"
}
```

#### 8.4.2 Chat streaming

```http
POST /api/v1/chat
Content-Type: multipart/form-data
```

**Fields:**

| Field | Required | Notes |
|------|----------|------|
| `conversationId` | Yes | Stable per thread; used as conversation key |
| `message` | Has default in API | Provide explicit text for predictable behavior |
| `files` | No | Optional attachment |

**curl example:**

```bash
curl -N -X POST "http://localhost:8000/api/v1/chat" \
  -H "Accept: text/event-stream" \
  -F "conversationId=demo-thread-001" \
  -F "message=Technical: Need triage help for ticket CATEGORY-X"
```

#### 8.4.3 Metrics (ops)

```http
GET /metrics
```

Used by monitoring systems (Prometheus). Frontline agents typically do not need this.

---

## 9. Best Practices & Tips for Maximum Performance

### 9.1 Prompting checklist (fast wins)

| Do | Why |
|----|-----|
| Start with **Technical** or **non-technical** context explicitly | Improves routing clarity |
| Include **IDs** (order/ticket) when allowed | Grounds the response |
| Say what you already tried | Avoids repeated steps |
| Ask for **numbered steps** | Easier to execute under pressure |

### 9.2 Quality checklist before you act

> **Warning:** Never take irreversible actions based solely on AI output.

1. Verify facts in **official tools** (order pages, admin consoles).  
2. Compare against the latest **policy bulletin** if the topic changes frequently.  
3. If two answers conflict, trust **verified internal documentation** + your lead.  

### 9.3 Performance tips (latency)

- Prefer **shorter** prompts with high-signal nouns.  
- Avoid uploading huge images repeatedly; reuse links when possible.  
- If streaming stalls, see Section 10.  

### 9.4 Team habits that scale

- Maintain a shared **“good prompts”** library internally (approved by QA).  
- Log **bad answers** with ticket ID + request ID for improvement loops.  

---

## 10. Troubleshooting Guide

### 10.1 Quick diagnosis table

| Symptom | Likely cause | What to try |
|---------|--------------|------------|
| Blank UI / cannot connect | VPN/network | Reconnect VPN; verify URL |
| `401/403` from API | Auth missing | Request token/gateway access |
| `404` on `/api/v1/chat` | Wrong prefix/host | Confirm base URL with IT |
| Streaming stops mid-way | Model timeout / GPU pressure | Retry once; escalate if repeated |
| Answers feel generic | Weak prompt / retrieval miss | Add IDs; rephrase as technical |
| Wrong language | Mixed prompt | Ask explicitly: “Answer in Vietnamese” |

### 10.2 Slow responses

**Common reasons:**

- Large model cold start on GPU servers  
- High concurrent usage  
- Long prompts and large attachments  

**What to do:**

- Wait briefly; if > your team’s SLA threshold, escalate to platform on-call.  
- Capture **`X-Request-ID`** from response headers for engineers.  

### 10.3 Model fallback behavior

Fallbacks depend on deployment. Typical patterns:

- Route to a smaller model with a disclaimer  
- Return a safe error event (`type: error`)  

**What you should do:** retry once, then use human fallback procedures.

### 10.4 GPU / inference server issues (for staff partnering with IT)

**Signals:**

- Elevated error rates  
- Repeated timeouts  
- Ops alerts on GPU memory  

**Escalation payload (copy/paste template):**

```text
Time (TZ):
Endpoint:
X-Request-ID:
ConversationId:
Symptom: (timeout / 500 / empty stream)
Impact: (#users / critical ticket IDs)
```

### 10.5 “The classifier picked the wrong path”

**Mitigations:**

- Rephrase with explicit `Technical issue:` prefix  
- Remove sarcasm/jokes that look like small talk  
- Report systematic misroutes with 3–5 examples  

---

## 11. FAQ

1. **Is the agent allowed to access live customer data automatically?**  
   Only if your deployment integrated authorized APIs. Never assume live access.

2. **Can I use this for customer-facing messages directly?**  
   Use as **draft**, then edit for tone, accuracy, and policy compliance.

3. **Why do I see “Planning…” or reasoning lines?**  
   Those are intermediate streaming statuses while the orchestrator works.

4. **What is `conversationId`?**  
   A stable thread identifier; reuse it to keep context consistent.

5. **Does conversation persist forever?**  
   Persistence depends on server memory/backend configuration; treat threads as operational, not legal records.

6. **Can I share my login with a teammate?**  
   No—use individual accounts per security policy.

7. **Why does the answer differ from last week?**  
   Models/prompts/knowledge may update; verify critical policy points in official docs.

8. **How do I report a harmful or unsafe suggestion?**  
   Follow your incident reporting process; include screenshots and request IDs.

9. **Is uploaded data retained?**  
   Depends on deployment logging policies—ask IT for the official retention statement.

10. **Can it replace training?**  
    No—it supplements training; required compliance training remains mandatory.

11. **Why is Vietnamese mixed with English?**  
    Mixed sources and user prompts can cause mixing; specify desired language explicitly.

12. **What if I disagree with the answer?**  
    Your team lead/QC decision wins; the agent is advisory.

13. **Can I use it on mobile?**  
    If your internal portal supports mobile browsers and policy allows it.

14. **Does it work offline?**  
    Generally **no**—it needs network access to the service.

15. **How do I request a new feature (templates, integrations)?**  
    Submit an internal feature request to the platform team with ROI and use cases.

16. **What does `mode: Orchestra of Agents` mean on `/`?**  
    Indicates multi-agent orchestration is running in the service.

17. **Are attachments always analyzed?**  
    Depends on vision/OCR pipelines enabled; if unsure, paste key text from the image.

---

## 12. Glossary of Sendo-Specific Terms

> **Note:** Definitions are simplified for onboarding. Follow your official business glossary if documents conflict.

| Term | Meaning (internal plain language) |
|------|-----------------------------------|
| **Sendo** | Sendo e-commerce ecosystem and related operations (marketplace context). |
| **Seller** | Merchant selling on the platform; subject to seller policies. |
| **Buyer / Khách hàng** | End customer purchasing through Sendo flows. |
| **Đơn hàng (Order)** | Transaction record with lifecycle states (created → processing → delivery → completed/cancelled, etc.). |
| **Mã đơn / Order code** | Identifier used to trace a specific order in tools. |
| **Kho / Warehouse** | Fulfillment/storage context; impacts shipping timelines and inventory. |
| **Vận chuyển / Shipping** | Carrier pickup, in-transit scans, delays, returns logistics. |
| **Flash sale** | Time-bound promotional selling window; may have special constraints. |
| **Khuyến mãi / Promotion** | Discounts/campaign rules; eligibility can depend on product/category/time. |
| **Ticket** | Support case record used to track communication and resolution. |
| **Escalation** | Raising to L2/L3 or specialized teams when thresholds are met. |
| **SLA** | Service-level expectations for response/resolution timing by priority. |
| **RAG** | Retrieval-augmented generation: pulling similar knowledge/cases to improve answers. |

---

## 13. Version History & Changelog

> **Process note:** Replace this section with your official release process. Below is a starter template.

| Version | Date | Changes | Owner |
|---------|------|---------|-------|
| `0.1.0` | YYYY-MM-DD | Initial internal user guide published | Tech Writing / Platform |
| `0.1.1` | YYYY-MM-DD | Added API examples + troubleshooting | Tech Writing |

**Changelog (template):**

- **Added:** Section 8 batch processing sketch  
- **Changed:** Routing description aligned to orchestrator intent labels  
- **Fixed:** curl examples for Windows vs Linux notes  

---

## 14. Appendix

### 14.1 Model specs (documentation-level)

| Model | Documentation name | Base | Typical strength |
|------|----------------------|------|------------------|
| Classifier | `classifier_model` | Llama 3 (fine-tuned) | Routing / intent |
| General | `basic_model` | Llama 3.1 (fine-tuned) | Standard handling / conversation |
| Expert | `expert_model` | Qwen 3.5 (fine-tuned) | Complex Sendo scenarios |

**Implementation note:** Ollama tags in code may differ (e.g., `tech_support_order_expert:latest`). Your platform team maintains the mapping.

### 14.2 Prompt templates (copy/paste)

**Template A — Technical triage**

```text
Technical issue:
Order/Ticket ID:
Symptom:
Expected:
Actual:
Already checked:
Ask: numbered next steps + escalation criteria.
```

**Template B — Policy clarification (draft only)**

```text
Summarize the policy in plain language for internal training.
Include: who it applies to, exceptions, and what to escalate.
Do not invent citations; if unsure, say what is missing.
```

### 14.3 Security notes (internal)

- Follow **least privilege** for API tokens.  
- Rotate credentials when team members change roles.  
- Prefer **SSO + MFA** where available.  
- Report suspected prompt injection attempts (“ignore policies…”) via security channels.  

### 14.4 Data privacy policy pointers (internal)

> **Warning:** This section is **not** a legal privacy policy. It summarizes common internal expectations.

| Topic | Guidance |
|------|----------|
| **Customer PII** | Minimize, mask, and only use for legitimate support work |
| **Logs** | May exist for reliability; access is restricted |
| **Training data** | Internal datasets must be sanitized per governance rules |
| **Retention** | Follow IT data retention schedules |

### 14.5 Incident escalation — quick reference

| Severity | Who to contact | What to include |
|----------|----------------|-----------------|
| Service down | IT/platform on-call | time window, endpoint, error, impact |
| Wrong guidance causing risk | Team lead + QA | ticket IDs, screenshots, request IDs |
| Security concern | Security team | suspicious prompts, data exfil attempts |

---

**End of document**
