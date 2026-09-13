# Security and Safety in Multi-Agent Systems

## Executive Summary
Crew v2 agents share a filesystem, can execute arbitrary code, and trust each other's outputs with no inter-agent security boundary — a single compromised agent can exfiltrate data, escalate privileges, or corrupt the entire crew. Multi-agent systems face unique risks: prompt injection between agents, tool misuse, data exfiltration via outputs, and supply chain attacks. This document specifies a defense-in-depth security architecture with ring-based access control, sandboxing, behavioral monitoring, and audit logging, adapted from OWASP AI Agent Security, Microsoft Agent Governance Toolkit, and production patterns (2025-2026).

## Key Findings

- **OWASP AI Agent Security Cheat Sheet (2026)** identifies key risks: prompt injection (direct & indirect), tool abuse & privilege escalation, data exfiltration, sensitive data exposure. Multi-agent systems are explicitly called out for preventing privilege escalation through agent chains [OWASP, 2026].
- **Parallax (arXiv, 2604.12986, 2026)** demonstrates that 40% of AI agent frameworks contain exploitable prompt injection flaws. The reference implementation (OpenParallax) uses process-level separation, canary verification at startup, security tokens for agent-engine authentication, and append-only audit logs with SHA-256 hash chains [Parallax, 2026].
- **Obsidian Security (2026)** reports AI agents move 16x more data than human users. Behavioral deviation from baseline combined with data volume anomalies detects prompt injection more reliably than keyword scanning. Target: detect within 15 minutes, contain within 5 minutes [Obsidian, 2026].
- **Stellar Cyber (2026)** identifies top agentic threats: tool misuse & privilege escalation (the "confused deputy" problem), prompt injection & multi-step manipulation ("salami slicing" attacks), memory poisoning, cascading failures, supply chain attacks. Real incident: attacker tricked agent into exporting 45,000 customer records via crafted regex pattern [Stellar Cyber, 2026].
- **Microsoft Agent Governance Toolkit (2025)** implements ring-based security with breach detection, circuit breakers, and kill switches. Agents start in sandbox (Ring 3) and require consensus to elevate [Microsoft, 2025].
- **Tao An (2025)** describes the "lethal trifecta" for agent vulnerabilities: access to private data + exposure to untrusted content + ability to communicate externally. Defense requires layered implementation: input validation, permission controls, behavioral monitoring, comprehensive audit logging [Tao An, 2025].

## Detailed Analysis

### Current Failure Modes in Crew v2

1. **No inter-agent trust boundary**: Agents trust each other's outputs blindly.
2. **Shared filesystem**: All agents can read/write any file.
3. **Arbitrary code execution**: Engineer can run any terminal command.
4. **No output sanitization**: Agent outputs can contain malicious instructions for downstream agents.
5. **No audit trail**: No structured log of which agent touched which data.
6. **Prompt injection vulnerability**: Researcher fetches web content that could contain injection payloads.

### Threat Model

| Threat | Attacker | Vector | Impact |
|--------|----------|--------|--------|
| Prompt injection | External (web content) | Researcher fetches poisoned page | Agent exfiltrates data |
| Privilege escalation | Compromised agent | Engineer exploits shared credentials | Full system access |
| Data exfiltration | Any agent | Output contains sensitive data | Compliance violation |
| Cascading failure | One failing agent | Timeout or error propagates | Entire task fails |
| Supply chain | External (dependency) | Malicious code in project deps | Persistent backdoor |
| Memory poisoning | Compromised agent | Corrupts shared memory | Repeated failures |

### Security Architecture (Defense-in-Depth)

**Five layers (adapted from OWASP + Parallax):**

```
┌─────────────────────────────────────────────────────────┐
│  LAYER 1: INPUT VALIDATION                              │
│  - Sanitize all external inputs (web content, user)     │
│  - Detect prompt injection patterns                     │
│  - Bound input size (max 10KB per message)              │
├─────────────────────────────────────────────────────────┤
│  LAYER 2: PERMISSION CONTROL                            │
│  - Ring-based access (0-3) per agent                    │
│  - Least privilege: agent only has tools it needs       │
│  - Capability-based tool access tokens                  │
├─────────────────────────────────────────────────────────┤
│  LAYER 3: SANDBOXING & ISOLATION                        │
│  - Per-agent workspace isolation                        │
│  - Filesystem access scoped to task directory           │
│  - Network egress restricted (allowlist)                 │
├─────────────────────────────────────────────────────────┤
│  LAYER 4: BEHAVIORAL MONITORING                         │
│  - Baseline normal agent behavior                       │
│  - Alert on deviation (tool calls, data volume)         │
│  - Circuit breaker on anomaly score ≥ 20                │
├─────────────────────────────────────────────────────────┤
│  LAYER 5: AUDIT LOGGING                                 │
│  - Append-only structured log with hash chain           │
│  - Every tool call, file access, output                 │
│  - Tamper-evident (SHA-256 + Ed25519 signatures)        │
└─────────────────────────────────────────────────────────┘
```

### Ring-Based Access Control

**Four rings (adapted from Microsoft Agent Governance Toolkit):**

| Ring | Level | Tools | Agents |
|------|-------|-------|--------|
| 0 (Root) | System infrastructure | All tools + user management | firstmate (limited), coach |
| 1 (Privileged) | High-trust operations | Read/write + terminal (limited) | architect, critic |
| 2 (Standard) | Default agent operations | Read + write (task dir) | researcher, tester, historian |
| 3 (Sandbox) | New/untested agents | Read-only + sandboxed execution | New agents, razor (constrained) |

**Ring transition rules:**
- Agents start in Ring 3 (sandbox).
- Elevation to Ring 2 requires operator approval.
- Elevation to Ring 1 requires operator approval + peer consensus (2 agents).
- Elevation to Ring 0 requires human operator approval only.
- Elevation is temporary (max 1 hour) unless explicitly renewed.

### Prompt Injection Prevention

**Input validation rules:**
1. **External content sanitization**: All web content fetched by researcher is passed through a sanitization filter that strips instructions (e.g., "ignore previous", "you are now", "system:").
2. **Inter-agent message validation**: Messages between agents are checked for injection patterns. If detected, message is quarantined and operator alerted.
3. **Output filtering**: Agent outputs that contain PII, credentials, or system instructions are redacted before passing to next agent.
4. **Context boundary markers**: System prompts are wrapped in delimiters that agents are instructed never to override.

**Detection patterns (Obsidian Security):**
- Behavioral deviation from baseline (tool calls never executed before).
- Data volume spike (sudden increase in records accessed per session).
- Instruction override patterns in content.

### Sandboxing

**Per-agent workspace (Parallax pattern):**
```python
class AgentSandbox:
    agent_id: str
    workspace_path: str  # /workspace/{task_id}/{agent_id}
    allowed_tools: list[str]
    network_allowlist: list[str]  # Domains agent can access
    max_file_size_mb: int = 100
    max_execution_time_s: int = 300
    
    def validate_tool_call(self, tool, args):
        if tool not in self.allowed_tools:
            raise PermissionError(f"Tool {tool} not allowed for {self.agent_id}")
        # Additional validation per tool type
```

**Canary verification (Parallax):**
- At agent startup, run self-contained probes that should fail under correct sandboxing:
  - Write to host filesystem outside workspace.
  - Read known host file (e.g., /etc/passwd).
  - Open network connection to unauthorized address.
- If any probe succeeds: sandbox is misconfigured, refuse to start.

### Audit Logging

**Log structure (adapted from Parallax):**
```python
class AuditEvent:
    event_id: str
    timestamp: datetime
    agent_id: str
    task_id: str
    event_type: str  # "tool_call", "file_access", "message", "ring_change"
    action: str
    target: str  # File path, tool name, agent ID
    outcome: str  # "success", "failure", "blocked"
    input_hash: str  # SHA-256 of input
    output_hash: str  # SHA-256 of output
    prev_hash: str  # SHA-256 of previous event (chain)
    signature: str  # Ed25519 signature
```

**Log retention:**
- Active logs: 90 days in SQLite.
- Archive: indefinite in append-only file with hash chain.
- EU AI Act compliance: high-risk systems must retain logs for regulatory review.

## Practical Recommendations

| Recommendation | Implementation | Tools | Threshold |
|----------------|----------------|-------|-----------|
| Input validation | Sanitize all external inputs | Custom filter + LLM-based classifier | All external content |
| Ring-based access | 4-ring model per agent | Custom policy engine | Start Ring 3 |
| Sandboxing | Per-agent workspace isolation | Filesystem + network scoping | All agents |
| Prompt injection detection | Behavioral deviation monitoring | Custom baseline + alerts | Deviation > 2σ |
| Audit logging | Append-only log with hash chain | SQLite + SHA-256 chain | All actions |
| Output sanitization | PII/credential redaction | Regex + LLM classifier | All inter-agent messages |
| Circuit breaker | Per-agent state machine | Custom | Anomaly score ≥ 20 |
| Kill switch | Immediate agent stop | Microsoft-style circuit breaker | Behavioral drift detected |

## Metrics Catalog

| Metric | Definition | How to Measure | Target | Warning |
|--------|-----------|----------------|--------|---------|
| Injection attempts | Detected injection patterns | Counter | 0 | >0 alert operator |
| Ring violations | Unauthorized elevation attempts | Counter | 0 | >0 alert operator |
| Sandbox escapes | Agents accessing outside workspace | Counter | 0 | >0 immediate kill |
| Audit coverage | Actions logged / total actions | Log audit | 100% | <100% fix logging |
| Mean time to detect | Injection to detection | Timestamp diff | <15 min | >30 min review |
| Mean time to contain | Detection to containment | Timestamp diff | <5 min | >15 min review |
| Data exfiltration events | Sensitive data in outputs | DLP scan | 0 | >0 immediate kill |

## References

1. [OWASP, 2026] AI Agent Security Cheat Sheet. cheatsheetseries.owasp.org.
2. [Parallax, 2026] Parallax: Why AI Agents That Think Must Never Act. arXiv:2604.12986.
3. [Obsidian Security, 2026] Prompt Injection Attacks on AI Agents. obsidiansecurity.com/blog.
4. [Stellar Cyber, 2026] Top Agentic AI Security Threats in Late 2026. stellarcyber.ai/learn.
5. [Microsoft, 2025] Agent Governance Toolkit: Kill Switch and Rate Limiting. github.com/microsoft/agent-governance-toolkit.
6. [Tao An, 2025] Agent Security Boundaries: From Prompt Injection to Tool Misuse. Medium.
7. [Palo Alto Unit 42, 2026] Persistent Prompt Injection in A2A Systems.
8. [Tao An, 2025] The Lethal Trifecta for Agent Vulnerabilities. Medium.
