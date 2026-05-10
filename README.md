# Hackathon Genius — Multi-Agent AI System

Aplikacja Multi-Agent do transformacji pomysłu hackathonu w profesjonalny pitch z tech stackiem i timeline'em.

---

## 🔐 Ocena Bezpieczeństwa: **7/10**

### Status: ✅ Dobry dla Demo | ⚠️ Wymaga Upgrade'u na Produkcję

---

## Zaimplementowane Zabezpieczenia

### 1. **Prompt Injection Protection** ✅ (⭐⭐)
- **Co:** Blokuje 22 znane wzorce prompt injection (PL + EN)
- **Gdzie:** `prompt_injection_guard()` callback w `IdeaAgent`
- **Limity:** Max 500 znaków na wejście
- **Score:** +1.5/10

### 2. **Rate Limiting (Token Bucket)** ✅ (⭐⭐)
- **Co:** DoS protection — max 10 żądań/min na użytkownika
- **Gdzie:** `hackathon_genius/security/rate_limiter.py` + callback w `prompt_injection_guard()`
- **Burst:** Do 3 żądań w sekwencji
- **Score:** +1.5/10

### 3. **Tool Argument Validation** ✅ (⭐)
- **Co:** Allowlista narzędzi per agent, walidacja argumentów
- **Blokady:** Path traversal (`../`), iniekcja powłoki (`;|&$`)
- **Gdzie:** `tool_argument_guard()` callback w `IdeaAgent`
- **Score:** +1.0/10

### 4. **Docker Sandbox** ✅ (⭐⭐)
- **Read-only filesystem** — app nie może modyfikować system
- **Unprivileged user** (UID 1001) — brak dostępu root
- **Capability drop** — `cap_drop: ALL`
- **Resource limits** — 1 CPU, 512MB RAM
- **Network isolation** — bridge driver
- **Score:** +2.0/10

### 5. **Boundary-Based Security Model** ✅ (⭐)
- **Gdzie:** Tylko `IdeaAgent` ma callbacki (granica człowiek→system)
- **Czemu:** Wewnętrzna komunikacja agentów przechodzi przez `session.state` bez walidacji
- **Score:** +0.5/10

---

## Luki Bezpieczeństwa (Gaps)

### ⚠️ Brak Centralized Logging (-0.5)
- Logi zapisane tylko lokalnie, brak ELK/Splunk
- **Rekomendacja:** Dodać structured logging do Elasticsearch

### ⚠️ Brak Policy Engine (-0.5)
- Polityki hardcoded w Python, brak OPA/Authz
- **Rekomendacja:** Open Policy Agent dla dynamicznych polityk

### ⚠️ Brak Model Monitoring (-0.5)
- Brak deteksji anomalii w output modelu
- **Rekomendacja:** Implementacja LLM prompt/response filtering

### ⚠️ Brak Secret Rotation (-0.5)
- Secrets w `.env`, brak Vault/Secret Manager
- **Rekomendacja:** HashiCorp Vault lub AWS Secrets Manager

### ⚠️ Brak Audit Trail (-0.5)
- Brak permanentnego rejestru działań
- **Rekomendacja:** Immutable audit log (database + archiving)

---

## Matryca Bezpieczeństwa (8 Warstw)

| Warstwa | Mechanizm | Implementacja | Score |
|---------|-----------|----------------|-------|
| **Input** | Prompt injection detection | 22 pattern signatures | ✅ 1.5/10 |
| **Throttle** | Rate limiting (token bucket) | 10 req/min, burst=3 | ✅ 1.5/10 |
| **Tools** | Argument validation + allowlist | Per-tool constraints | ✅ 1.0/10 |
| **Agent** | Tool isolation | `_AGENT_TOOL_ALLOWLIST` | ✅ 0.5/10 |
| **Container** | Sandbox (read-only, unprivileged) | Docker + compose | ✅ 2.0/10 |
| **Policy** | Authorization engine | ❌ Brak (OPA) | ❌ -0.5/10 |
| **Logging** | Centralized observability | ❌ Brak (ELK) | ❌ -0.5/10 |
| **Monitoring** | Anomaly detection | ❌ Brak | ❌ -0.5/10 |
| | | **RAZEM** | **7.0/10** |

---

## Architektura Bezpieczeństwa

```
┌─────────────────────────────────────────┐
│           USER INPUT                    │
└────────────┬────────────────────────────┘
             │
             ▼
     ┌───────────────────────────────────┐
     │  [IdeaAgent - Security Layer]     │
     │  ├─ prompt_injection_guard        │
     │  ├─ rate_limiter (token bucket)   │
     │  ├─ tool_argument_guard           │
     │  └─ tool_isolation (allowlist)    │
     └────────┬────────────────────────┘
              │
              ▼  (validated + rate-limited)
     ┌───────────────────────────────────┐
     │  session.state (internal flow)    │
     │  [no callbacks - trusted zone]    │
     └────────┬────────────────────────┘
              │
          ┌───┴────┬──────────┬──────────┐
          ▼        ▼          ▼          ▼
    ┌──────────┐┌────────────┐┌─────────────┐┌─────────────┐
    │TechStack ││ Timeline   ││  Pitch      ││  (other)    │
    │  Agent   ││  Agent     ││  Agent      ││  Agents     │
    └──────────┘└────────────┘└─────────────┘└─────────────┘
```

---

## Deployment Security

### Docker Hardening
```yaml
# docker-compose.yml
read_only: true                          # Immutable filesystem
cap_drop: ALL                            # No Linux capabilities
security_opt: no-new-privileges          # Prevent privilege escalation
user: 1001                               # Unprivileged user
tmpfs:                                   # Selective writable paths
  - /tmp
  - /var/tmp
  - /run
resource_limits:
  cpus: "1.0"
  memory: 512M
```

### Network Isolation
- Bridge network (isolated from host)
- Healthcheck: LM Proxy connectivity + ADK Web endpoint
- No direct access to host services (except via `host.docker.internal`)

---

## Rekomendacje dla Produkcji

### Priority 1 (Critical)
- [ ] Centralized logging + audit trail (ELK/Datadog)
- [ ] Secrets management (Vault/AWS Secrets Manager)
- [ ] Distributed tracing (Jaeger/DataDog)
- [ ] Input/output content filtering (LLM Firewall)

### Priority 2 (Important)
- [ ] Policy engine (OPA/Authz)
- [ ] Rate limiting per endpoint (API Gateway)
- [ ] Model monitoring (prompt/response anomaly detection)
- [ ] RBAC (role-based access control)

### Priority 3 (Nice-to-have)
- [ ] Microservices per agent (separate sandboxes)
- [ ] Load balancing + HA deployment
- [ ] DLP (Data Loss Prevention) policies
- [ ] Encryption at rest + in transit

---

## Uruchamianie

### Development
```bash
python -m venv .venv
source .venv/Scripts/activate  # Windows
pip install -r requirements.txt
```

### Docker (Production-like)
```bash
docker compose up -d hackathon-genius
docker compose logs -f hackathon-genius
```

---

## Struktura Projektu

```
hackathon_genius/
├── agent.py              # Main IdeaAgent + orchestration
├── config/
│   ├── __init__.py
│   └── model_config.py   # LLM provider configuration
├── security/
│   ├── __init__.py       # Public security exports
│   ├── guards.py         # ✅ Prompt injection + tool guards
│   └── rate_limiter.py   # ✅ Token bucket rate limiter
├── sub_agents/
│   ├── tech_stack_agent.py
│   ├── timeline_agent.py
│   └── pitch_agent.py
└── tools/
  └── hackathon_tools.py

docs/
├── ARCHITEKTURA_DEMO_PL.md
└── flowchart-hackathon-genius.mmd

Dockerfile                # 2-stage secure build
docker-compose.yml        # ✅ Hardened container config
requirements.txt
README.md                 # ← Ty jesteś tu
```

---

## Status Security Review

**Ostatnia aktualizacja:** 2026-05-10  
**Oceniający:** Security Module + Rate Limiting Integration  
**Zalecenia:** Uruchomić na demo, upgrade na ELK/OPA przed produkcją

