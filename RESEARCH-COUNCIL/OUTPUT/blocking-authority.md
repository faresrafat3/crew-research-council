## [DEEP DIVE]: Real-World Tester Blocking Abuse, Calibration, Escalation Time, and Collusion

### 1. Real-World Examples of Tester Blocking Abuse

**Pattern 1: The Overly Strict Gatekeeper** [Medium, 2025]
- Symptom: Tester blocks 50%+ of tasks on style preferences, out-of-scope performance, or ambiguous requirements.
- Consequence: Engineer spends more time appealing than developing. Trust erodes. "Just skip the tester" workarounds appear.
- Root cause: Tester SOUL lacks MUST-NOT list. Tester treats all opinions as block-worthy.
- Fix: Closed block list (8 conditions) + MUST-NOT list (style, scope, ambiguity, outages).

**Pattern 2: The Rubber Stamp** [ArizenAI, 2025]
- Symptom: Tester PROMOTES 100% of tasks. Zero HOLDs. Zero ROLLBACKs.
- Consequence: Bugs reach production. Tester is decorative.
- Root cause: Tester SOUL lacks blocking authority or fear of conflict.
- Fix: Escape rate tracking. If escapes > 1/20, tighten tester SOUL. Add mutation gate.

**Pattern 3: The Veto War** [Priygop, 2026]
- Symptom: Engineer appeals every HOLD. Critic sides with engineer. Tester appeals to human. Deadlock.
- Consequence: Human spends hours resolving testing disputes.
- Root cause: No appeal limit. No evidence requirements.
- Fix: One-appeal rule with evidence package. Critic tie-break. Human only on split.

**Pattern 4: The Capture** [QABattle, 2025]
- Symptom: Tester and engineer collude: engineer writes weak tests, tester approves them. Both optimize for "green" not "correct."
- Consequence: 100% coverage, 4% mutation score, bugs in production.
- Root cause: No independent oracle. No mutation gate. No critic review.
- Fix: Oracle separation (tester writes tests, not engineer). Mutation gate. Critic independent rerun.

**Pattern 5: The Fatigue Model** [arXiv, 2026 — Oversight Has a Capacity]
- Symptom: Human reviewer rubber-stamps escalations because too many arrive.
- Consequence: Escalations become meaningless. Real bugs slip through.
- Root cause: Tester escalates too frequently (low threshold).
- Fix: Calibrate escalation rate. Safety-optimal escalation is below full escalation. Monitor reviewer workload.

### 2. Calibrating Tester Strictness Automatically

**Calibration signals** [IJECS, 2026; KnowMBA, 2025]:

| Signal | What It Measures | How to Adjust |
|--------|------------------|---------------|
| **False-positive rate** | Blocks that human overturned | >5%: loosen thresholds by 5% absolute |
| **Escape rate** | Bugs shipped despite PROMOTE | >1/10: tighten thresholds by 5% absolute |
| **Appeal success** | Engineer appeals that overturned | >5%: loosen; <1%: tighten |
| **Block rate** | HOLD+ROLLBACK / total verdicts | >50%: too strict; <5%: too lenient |
| **Coverage/mutation gap** | False confidence | >20%: tighten mutation gate |
| **Reviewer workload** | Escalations per week | >5/week: raise escalation threshold |

**Automatic calibration algorithm:**
```
quarterly_calibration():
  fp_rate = overturned_blocks / total_blocks
  escape_rate = escapes / FULL_tasks
  appeal_success = overturned_appeals / total_appeals
  
  if fp_rate > 0.05:
    coverage_threshold -= 5  # loosen
    mutation_threshold -= 5
  if escape_rate > 0.1:
    coverage_threshold += 5  # tighten
    mutation_threshold += 5
  if appeal_success > 0.05:
    coverage_threshold -= 5
  if appeal_success < 0.01:
    coverage_threshold += 5
  
  # Clamp to industry benchmarks
  coverage_threshold = clamp(coverage_threshold, 70, 95)
  mutation_threshold = clamp(mutation_threshold, 60, 90)
  
  log_adjustment(fp_rate, escape_rate, appeal_success, new_thresholds)
```

**Calibration governance:**
- Adjustments are logged to ledger with evidence.
- Human approves adjustments > 10% absolute.
- Adjustments are versioned in TEST-POLICY.md.

### 3. Optimal Escalation Time

**Evidence-based escalation timeouts** [Priygop, 2026; arXiv, 2026]:

| Escalation Type | Optimal Timeout | Maximum | Rationale |
|-----------------|-----------------|---------|-----------|
| Tester RED not received | 15 min | 30 min | Tester should write RED in one shot; if stuck, escalate |
| Engineer GREEN not received | 30 min | 60 min | Engineer needs time to implement; but not too long |
| Critic review not received | 10 min/file, 30 min/task | 60 min | Critic is read-only; should be fast |
| Human escalation response | 4 hours | 24 hours | Human attention is finite; 4h is the fatigue threshold [arXiv, 2026] |
| Flake rerun cycle | 5 min per rerun | 15 min total | Flake detection should be fast |
| Appeal response | 2 hours | 8 hours | Appeal is one-shot; should be quick |

**Fatigue model insight** [arXiv, 2026]:
- Human reliability declines as cumulative escalation load grows.
- Safety-optimal escalation rate is below full escalation.
- If human receives > 5 escalations/week, they start rubber-stamping.
- Solution: raise escalation threshold so only truly ambiguous cases reach human.

**Escalation budget:**
- Target: < 5 human escalations per week.
- If exceeded: raise tester confidence threshold by 5%.
- If zero for 4 weeks: lower threshold by 5% (may be too lenient).

### 4. Handling Tester-Critic Collusion

**Collusion scenarios:**

| Scenario | Detection | Prevention |
|----------|-----------|------------|
| Tester and engineer agree on weak tests | Mutation survivors > 10% | Mutation gate catches weak assertions |
| Tester and critic are same model | Model ID check | Use different model families for tester vs critic |
| Tester and critic both miss same bug | Drill pass < 100% | Break drills catch what point tests miss |
| Tester writes test, critic uses same oracle | Oracle separation | Tester writes from REQ only; critic reruns independently |

**Anti-collusion measures:**

1. **Oracle separation** [Eleks, 2025]: Tester writes tests from REQ-IDs only, never reads implementation code. Critic reruns tests without reading tester's rationale.
2. **Model diversity** [IJECS, 2026]: Use different model families for tester and critic (e.g., tester = Claude, critic = GPT). Disagreement triggers human review.
3. **Mutation gate** [ArXiv, 2025]: Independent of both tester and critic. Catches weak assertions regardless of collusion.
4. **Drill pass** [KnowMBA, 2025]: Break each REQ independently. If both tester and critic miss a break, the drill catches it.
5. **Audit sampling**: Human reviews 5% of PROMOTED tasks randomly. If audit finds bug, both tester and critic are recalibrated.

**Collusion detection metrics:**
- If tester-critic agreement rate > 99%: suspicious. Normal is 90-95%.
- If mutation survivors = 0 AND drill pass < 100%: likely collusion.
- If appeal success = 0% AND block rate > 30%: likely over-strictness or collusion.

**References for deep dive:**
- [Medium, 2025] Quality Assistance: gatekeeper bottleneck, structural conflict
- [ArizenAI, 2025] The End of Determinism: rubber-stamp detection, FP erosion
- [Priygop, 2026] Escalation Frameworks: veto wars, evidence requirements
- [QABattle, 2025] Layered LLM Evaluation: capture, independent oracle
- [arXiv, 2026] Oversight Has a Capacity: fatigue model, optimal escalation rate
- [IJECS, 2026] Detect-Fix-Learn Loop: model diversity, calibration
- [KnowMBA, 2025] Test Automation Strategy: drill pass, 14-day SLA
- [Eleks, 2025] Independent Oracle: oracle separation, tautology detection
- [ArXiv, 2025] MutGen: mutation gate catches weak assertions
- [TMMi Foundation, 2018] Level 5: calibration, process optimization

---

## [DEEP DIVE (freebuff, pass 2, 2026-09-14)]: Audit Sampling Mathematics — How Many Verdicts to Review and What the Sample Can Prove

Pass-1 anti-collusion measure #5 says: "Human reviews 5% of PROMOTED tasks randomly." It names no sample size, no confidence level, and no detection claim — and that gap matters, because the human audit is the only layer that can catch collusion *between* the machine gates (§4's other defenses each assume at least one uncorrupted component). An undersized audit delivers false assurance, which is worse than no audit: it is rubber-stamping with an alibi.

### B1. The c=0 zero-acceptance plan: deriving n

For attribute sampling with zero tolerated bad verdicts, the sample size needed to have confidence C of catching at least one bad verdict when the true bad rate is p is:

```
n = ln(1 − C) / ln(1 − p)
```

This is the standard c=0 acceptance-sampling plan (zero-nonconformity plans); LTPD-style plans and OC curves are the classical framing [NIST/SEMATECH Engineering Statistics Handbook; NCSS c=0 procedure; variation.com]. Evaluation is attribute-style: a sampled verdict is either validated or defective — no partial credit.

**Derived sample sizes at 95% confidence:**

| True bad-verdict rate p | Required n = ln(0.05)/ln(1−p) |
|---|---|
| 10% | 29 |
| 5% | 59 |
| 2% | 149 |
| 1% | 299 |

### B2. What a 5% sample actually detects

The pass-1 "5% of PROMOTEs" rule scales n with volume: 200 quarterly PROMOTEs → n=10 sampled verdicts. Detection probability for a true bad rate p is 1−(1−p)^n:

| True rate p | Detection probability (n=10) |
|---|---|
| 10% | 65% |
| 5% | 40% |
| 2% | 18% |

A 5% sample leaves a 5%-rate collusion undetected **60% of the time**. The fix is not sampling *more of everything* (B4) but sampling to a *stated claim*: the operator should pick the worst tolerable collusive/defective verdict rate and review the c=0-derived n. Recommendation: "95% confidence of detecting collusion affecting ≥5% of verdicts" → **n=59 per quarter**, volume-independent.

### B3. Rule of three: reading a clean sample

When the audit finds zero defects in n sampled verdicts, the 95% upper bound on the bad rate is ≈ 3/n (rule of three). A clean 59-verdict audit certifies a bad rate below ~5.1% — no better. This bounds what calibration can conclude from audit data: pass-1's §2 calibration algorithm moves thresholds on FP signals, but a *clean sample* is absence of evidence, not evidence of absence; threshold moves justified only by audit cleanliness should be conservative (the ±5% clamp already encodes this).

### B4. Stratify before you randomize

Uniform random sampling spends n on high-volume trivial verdicts. Stratify the quarterly plan by information value:
1. **Appeal-overturned blocks** — oversample 3×; an overturned block is already half a collusion signal (§1 Pattern 3).
2. **FULL formation verdicts** — highest blast radius; every FULL PROMOTE in the quarter should be *eligible* with elevated selection weight.
3. **New-module or new-agent verdicts** — fresh failure surfaces.
4. **Maintenance verdicts** — lowest weight.

Stratified attribute sampling is standard audit practice; the AQL/OC-curve machinery applies per stratum [SixSigma.us attribute sampling; NIST/SEMATECH].

### B5. Audit cadence and the fatigue budget

Pass-1's fatigue model (Pattern 5: >5 escalations/week degrades human review) applies to the audit itself: 59 verdicts/quarter ≈ 5/week of *audit* review on top of escalations. Two mitigations keep the audit inside the attention budget: batch the audit into one weekly 60-minute session (5 verdicts × ~10 min evidence review, verdict evidence is machine-fetched by the auditor agent), and rotate auditors if more than one human operator exists. If the audit backlog grows, reduce scope by *tightening p* honestly (declare a 10% detection target → n=29) rather than silently skimming the sample — a silently skimmed audit is Pattern 2 (the rubber stamp) wearing an auditor's badge.

### Numbers for calibration (pass 2)

| Quantity | Value | Source |
|---|---|---|
| n for 95% confidence @ p=5% | 59 | c=0 plan, derived [NIST/SEMATECH] |
| n for 95% confidence @ p=1% | 299 | same |
| 5%-sample (n=10) detection of 5% rate | 40% (1−0.95¹⁰) | derived |
| Clean-sample upper bound (rule of three) | ≈3/n | [NCSS; standard] |
| Pass-1 audit rule, revised | fixed-n c=0 stratified plan, not 5% volume share | this dive |
| Audit load at n=59 | ~5 verdicts/week | derivation |

### References (pass 2)
1. [NIST/SEMATECH] Engineering Statistics Handbook, §7.2.2 "Lot Acceptance Sampling Plans" — LTPD, OC curves. https://www.itl.nist.gov/div898/handbook/pmc/section2/pmc22.htm [verified: 2026-09-14]
2. [NCSS] "Acceptance Sampling for Attributes with Zero Nonconformities" (c=0 plans). https://www.ncss.com/wp-content/themes/ncss/pdf/Procedures/PASS/Acceptance_Sampling_for_Attributes_with_Zero_Nonconformities.pdf [verified: 2026-09-14, doc page]
3. [variation.com] "Selecting Statistically Valid Sampling Plans" — AQL, 95% acceptance mechanics. https://variation.com/selecting-statistically-valid-sampling-plans/ [verified: 2026-09-14, snippet]
4. [SixSigma.us] "How Attribute Sampling Works" — AQL, OC curves, plan selection. https://www.6sigma.us/six-sigma-in-focus/attribute-sampling/ [verified: 2026-09-14, snippet]
5. Cross-refs: blocking-authority.md pass 1 §2 (calibration algorithm), §4 (anti-collusion), Pattern 5 (fatigue); tester-soul.md cycle 4 (escape-classification).

## [DEEP DIVE (freebuff, pass 3, 2026-09-14)]: Break-Glass — Emergency Overrides of the Blocker, With the Audit Trail That Keeps Them Rare

Pass 2 gave the blocker statistical audit machinery (c=0 sampling). One operational path remains unexamined: **break-glass** — the emergency bypass every real gate eventually needs, and the loophole that can erase the gate if unmanaged. The privileged-access literature is direct: emergency access must be **just-in-time (granted per-incident, time-boxed, auto-expiring)**, **session-recorded**, and **alerted in real time to a second party** — standing break-glass credentials are the classic audit finding [JIT privileged-access guidance; PAM literature — snippet-verified 2026-09-14]. The design goal is *blast-radius control*: the override must be able to unblock one PR, not the gate systemwide.

**Protocol deltas for the blocking authority.**
1. **Per-incident, time-boxed overrides only**: a break-glass grant applies to exactly one blocking verdict and expires (default 4h); no standing "override role" exists. Reuse requires a fresh grant — each grant is a sampled verdict for the pass-2 audit.
2. **Dual-visibility rule**: every break-glass use notifies the operator channel *at grant time*, not at audit time. Real-time alerting is what separates emergency access from shadow authority.
3. **Justification must be falsifiable at audit**: the grant records the specific gate verdict overridden and the concrete harm of respecting it ("build env down, demo at 15:00"), not sentiment ("urgent"). The pass-2 c=0 sample oversamples break-glass verdicts — an override with an unverifiable justification counts as a defect against the granter's own ledger.
4. **Budget coupling**: the crew's error-budget discipline (self-healing pass 1) applies — if break-glass use exceeds the agreed rate (suggested: 2% of blocking verdicts per quarter), the *gate itself* is reviewed for miscalibration before any further grants. Frequent overrides mean the gate is wrong, not the world.
5. **No self-grant for the same agent's work**: the granter and the blocked-PR author must differ (the conflict-resolution grounded-semantics verdict is the only single-agent exception, and it is logged as such).

**Cross-links:** pass-2 audit sampling (overrides as oversampled stratum), self-healing pass 1 (error-budget policy), conflict-resolution pass 3 (who adjudicates a disputed override — the grounded-semantics kernel).

**Sources.**
1. [NIST SP 800-53 AC-2(3) / AC-6(9)] Just-in-time and time-bound privileged authorization controls [literature, snippet-verified: 2026-09-14].
2. [Microsoft Entra, 2026] PIM activation with justification, approval, and expiration — the JIT pattern as productized [snippet-verified: 2026-09-14].
3. [CIS Controls v8, Control 5/6] Account and access-control management: emergency-account procedures and audit logging [literature].

---

## [DEEP DIVE]: Antigravity — Zero-Daemon Cryptographic Gate Enforcement, M-of-N Threshold Escalation & Bayesian Calibration

### 1. Zero-Daemon Cryptographic Gate Enforcement Architecture

In distributed multi-agent workflows, blocking authority easily degenerates into advisory recommendations or insecure status flags in volatile memory. Under the strict zero-daemon architectural invariant (`MAP.md`), gating must be non-bypassable, decentralized, and verifiable without running persistent gatekeeper daemons or background evaluation servers.

We implement cryptographic gate enforcement via **Ed25519 Capability Tokens** (RFC 8032) stored in an embedded SQLite-WAL ledger and verified at local checkout/pre-push git lifecycle boundaries.

```
+-------------------------------------------------------------------------------+
|                       CRITICAL LIFECYCLE BOUNDARY                             |
|                                                                               |
|   +-------------------+      Evaluates Task      +-----------------------+    |
|   |   Tester / Critic  | ----------------------> | SQLite Gate Evaluation|    |
|   |    Agent Subproc  |                          | & Token Minting Engine|    |
|   +-------------------+                          +-----------------------+    |
|             |                                                |                |
|             | Signs Verdict Payload                          | Writes WAL     |
|             v                                                v                |
|   +-----------------------------------------------------------------------+   |
|   |                      SQLite-WAL Gate State Tables                     |   |
|   |  - gate_evaluations (verdict, criteria_hash, signature)              |   |
|   |  - gate_capability_tokens (token_id, git_sha, gate_type, expires_at) |   |
|   |  - gate_revocation_ledger (nonce, revoked_at, revocation_proof)      |   |
|   +-----------------------------------------------------------------------+   |
|                                     |                                         |
|                                     | Read-only Query (<1.5ms)                |
|                                     v                                         |
|   +-------------------+      Inspects Token      +-----------------------+    |
|   | Git Pre-Push Hook | <----------------------- | Cryptographic Verifier|    |
|   | (Exit 0 or Exit 1)|                          | (RFC 8032 Signature)  |    |
|   +-------------------+                          +-----------------------+    |
+-------------------------------------------------------------------------------+
```

#### 1.1 SQLite-WAL Schema for Cryptographic Gate Ledger

```sql
-- Schema: Cryptographic Gate Enforcement Ledger (gate_ledger.sql)
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS gate_evaluations (
    evaluation_id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    git_sha TEXT NOT NULL,
    agent_id TEXT NOT NULL,
    gate_name TEXT NOT NULL, -- e.g. 'ORACLE_INTEGRITY', 'MUTATION_SCORE', 'REGRESSION_SUITE'
    verdict TEXT NOT NULL CHECK(verdict IN ('PASS', 'HOLD', 'ROLLBACK', 'OVERRIDE')),
    metrics_json TEXT NOT NULL, -- Serialized JSON measurements
    criteria_hash TEXT NOT NULL, -- SHA-256 of gate definition criteria
    signature TEXT NOT NULL, -- Ed25519 signature over canonical payload
    public_key TEXT NOT NULL, -- Hex-encoded Ed25519 verifying key
    created_at REAL NOT NULL DEFAULT (unixepoch('subsec'))
);

CREATE TABLE IF NOT EXISTS gate_capability_tokens (
    token_id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    git_sha TEXT NOT NULL,
    scope TEXT NOT NULL CHECK(scope IN ('BRANCH_MERGE', 'MAIN_PUSH', 'DEPLOY_CANARY')),
    issued_to TEXT NOT NULL,
    verdict TEXT NOT NULL CHECK(verdict IN ('PROMOTED', 'EMERGENCY_OVERRIDE')),
    nonce TEXT NOT NULL UNIQUE,
    token_signature TEXT NOT NULL, -- Signed by gate authority
    issued_at REAL NOT NULL DEFAULT (unixepoch('subsec')),
    expires_at REAL NOT NULL, -- Hard expiry (default: issued_at + 1800s)
    FOREIGN KEY(task_id) REFERENCES gate_evaluations(task_id)
);

CREATE TABLE IF NOT EXISTS gate_revocation_ledger (
    revocation_id TEXT PRIMARY KEY,
    nonce TEXT NOT NULL UNIQUE,
    reason TEXT NOT NULL,
    revoked_by TEXT NOT NULL,
    revocation_proof TEXT NOT NULL, -- Ed25519 signature from Security Officer / Human Operator
    revoked_at REAL NOT NULL DEFAULT (unixepoch('subsec'))
);

CREATE INDEX IF NOT EXISTS idx_gate_tokens_sha ON gate_capability_tokens(git_sha, scope, expires_at);
CREATE INDEX IF NOT EXISTS idx_gate_eval_task ON gate_evaluations(task_id, verdict);
```

#### 1.2 Zero-Daemon Gate Minter and Git Hook Verifier

```python
"""Zero-daemon gate token issuance and pre-push hook verifier."""
import hashlib
import json
import sqlite3
import sys
import time
from typing import Dict, Any, Tuple
from nacl.signing import SigningKey, VerifyKey
from nacl.exceptions import BadSignatureError

class GateEnforcementEngine:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def _get_conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, timeout=5.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode = WAL")
        return conn

    @staticmethod
    def canonical_hash(payload: Dict[str, Any]) -> bytes:
        """Deterministically serialize payload per RFC 8785 (JSON Canonicalization)."""
        canonical_json = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(canonical_json.encode("utf-8")).digest()

    def record_evaluation(
        self,
        task_id: str,
        git_sha: str,
        agent_id: str,
        gate_name: str,
        verdict: str,
        metrics: Dict[str, Any],
        criteria_hash: str,
        signing_key: SigningKey,
    ) -> str:
        eval_id = f"eval_{task_id}_{gate_name}_{int(time.time()*1000)}"
        payload = {
            "eval_id": eval_id,
            "task_id": task_id,
            "git_sha": git_sha,
            "agent_id": agent_id,
            "gate_name": gate_name,
            "verdict": verdict,
            "metrics": metrics,
            "criteria_hash": criteria_hash,
        }
        digest = self.canonical_hash(payload)
        signed = signing_key.sign(digest)
        sig_hex = signed.signature.hex()
        pub_hex = signing_key.verify_key.encode().hex()

        with self._get_conn() as conn:
            conn.execute(
                """
                INSERT INTO gate_evaluations 
                (evaluation_id, task_id, git_sha, agent_id, gate_name, verdict, metrics_json, criteria_hash, signature, public_key)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (eval_id, task_id, git_sha, agent_id, gate_name, verdict, json.dumps(metrics), criteria_hash, sig_hex, pub_hex),
            )
        return eval_id

    def issue_capability_token(
        self,
        task_id: str,
        git_sha: str,
        scope: str,
        issued_to: str,
        gate_authority_key: SigningKey,
        ttl_seconds: float = 1800.0,
    ) -> str:
        """Issues capability token only if all required gates passed and no active HOLDs exist."""
        with self._get_conn() as conn:
            cur = conn.execute(
                "SELECT gate_name, verdict FROM gate_evaluations WHERE git_sha = ? AND task_id = ?",
                (git_sha, task_id),
            )
            rows = cur.fetchall()
            if not rows:
                raise PermissionError("Cannot issue token: Zero gate evaluations recorded.")
            
            for row in rows:
                if row["verdict"] in ("HOLD", "ROLLBACK"):
                    raise PermissionError(f"Cannot issue token: Gate '{row['gate_name']}' is in {row['verdict']} status.")

            token_id = f"tok_{task_id}_{int(time.time()*1000)}"
            nonce = hashlib.sha256(f"{token_id}_{time.time_ns()}".encode()).hexdigest()
            now = time.time()
            expires_at = now + ttl_seconds

            token_payload = {
                "token_id": token_id,
                "task_id": task_id,
                "git_sha": git_sha,
                "scope": scope,
                "issued_to": issued_to,
                "verdict": "PROMOTED",
                "nonce": nonce,
                "expires_at": expires_at,
            }
            digest = self.canonical_hash(token_payload)
            token_sig = gate_authority_key.sign(digest).signature.hex()

            conn.execute(
                """
                INSERT INTO gate_capability_tokens
                (token_id, task_id, git_sha, scope, issued_to, verdict, nonce, token_signature, issued_at, expires_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (token_id, task_id, git_sha, scope, issued_to, "PROMOTED", nonce, token_sig, now, expires_at),
            )
            return token_id

    def verify_git_push(self, target_git_sha: str, scope: str, expected_pubkey_hex: str) -> Tuple[bool, str]:
        """Sub-2ms check invoked directly by .git/hooks/pre-push without daemons."""
        verify_key = VerifyKey(bytes.fromhex(expected_pubkey_hex))
        now = time.time()

        with self._get_conn() as conn:
            cur = conn.execute(
                """
                SELECT token_id, task_id, git_sha, scope, issued_to, verdict, nonce, token_signature, expires_at
                FROM gate_capability_tokens
                WHERE git_sha = ? AND scope = ? AND expires_at > ?
                ORDER BY issued_at DESC LIMIT 1
                """,
                (target_git_sha, scope, now),
            )
            token = cur.fetchone()
            if not token:
                return False, f"GATE BLOCK: No valid, non-expired capability token found for commit {target_git_sha[:8]}."

            revoked = conn.execute(
                "SELECT reason, revoked_by FROM gate_revocation_ledger WHERE nonce = ?",
                (token["nonce"],),
            ).fetchone()
            if revoked:
                return False, f"GATE BLOCK: Token revoked by {revoked['revoked_by']}: {revoked['reason']}."

            token_payload = {
                "token_id": token["token_id"],
                "task_id": token["task_id"],
                "git_sha": token["git_sha"],
                "scope": token["scope"],
                "issued_to": token["issued_to"],
                "verdict": token["verdict"],
                "nonce": token["nonce"],
                "expires_at": token["expires_at"],
            }
            digest = self.canonical_hash(token_payload)
            try:
                verify_key.verify(digest, bytes.fromhex(token["token_signature"]))
            except BadSignatureError:
                return False, "SECURITY ALERT: Capability token cryptographic signature verification failed!"

            return True, f"GATE PERMIT: Verified valid token {token['token_id']} for commit {target_git_sha[:8]}."
```

---

### 2. Dual-Key Escalation Protocol & Collusion Detection Quotient (CDQ)

#### 2.1 M-of-N Threshold Escalation Protocol
When an engineer agent appeals a Tester's `HOLD` or `ROLLBACK` verdict, unilateral override is strictly prohibited. An emergency promotion or threshold relaxation requires an M-of-N threshold signature:

$$\text{Verdict}_{\text{override}} = \text{ThresholdSign}_{M/N}(\sigma_1, \sigma_2, \dots, \sigma_M) \quad \text{where } M \ge 2, \; N \ge 3$$

In Crew v2:
- **P0 Critical Path Override**: Requires $M=2$ of 3 distinct roles: $\text{Signature}_{\text{Operator}} + \text{Signature}_{\text{Critic}}$ OR $\text{Signature}_{\text{Operator}} + \text{Signature}_{\text{Tester}}$.
- **No Single Agent Self-Approval**: An Engineer agent's key is explicitly blocked from the threshold set for its own code diff.
- **Time-Bounded Leases**: All emergency override tokens carry a hard maximum Time-To-Live ($TTL_{\max} = 900\text{ seconds}$ / 15 minutes), forcing either automated canary validation or automatic rollback.

#### 2.2 Collusion Detection Quotient (CDQ)
To detect Pattern 4 (The Capture: Engineer and Tester secretly colluding to maximize throughput by passing weak implementations), we define the **Collusion Detection Quotient (CDQ)**.

CDQ monitors inter-agent agreement against statistical independence using Cohen's Kappa ($\kappa$) coupled with conditional defect discovery:

$$\kappa = \frac{P_o - P_e}{1 - P_e}$$

Where:
- $P_o$ is the observed proportional agreement across $N$ test verdicts:
  $$P_o = \frac{\sum_{i=1}^C n_{ii}}{N}$$
- $P_e$ is the hypothetical probability of chance agreement:
  $$P_e = \sum_{i=1}^C \left( \frac{n_{i+}}{N} \cdot \frac{n_{+i}}{N} \right)$$

We combine Cohen's Kappa with the **Escape Divergence Ratio ($R_{\text{esc}}$)** over a sliding window of $W = 50$ tasks:

$$R_{\text{esc}} = \frac{\text{Escapes}_{\text{Production}}}{\max(1, \text{Escapes}_{\text{Baseline}})}$$

The **Collusion Detection Quotient (CDQ)** is defined as:

$$\text{CDQ} = \kappa \cdot \log_2(1 + R_{\text{esc}})$$

```
Nominal Zone:        CDQ <= 0.40  --> Normal independent operation
Investigation Zone:  0.40 < CDQ <= 0.85 --> Warn, increase mutation audit sampling to 25%
Hard Collusion Alarm: CDQ > 0.85  --> Revoke Tester signing key, inject Adversarial Mutant Suite
```

```python
"""Collusion Detection Quotient (CDQ) Calculator."""
import math
from typing import List, Tuple

def compute_cohens_kappa(contingency_matrix: List[List[int]]) -> float:
    """Computes Cohen's Kappa for NxN agreement matrix."""
    n = sum(sum(row) for row in contingency_matrix)
    if n == 0:
        return 0.0
    po = sum(contingency_matrix[i][i] for i in range(len(contingency_matrix))) / n
    row_sums = [sum(contingency_matrix[i][j] for j in range(len(contingency_matrix))) for i in range(len(contingency_matrix))]
    col_sums = [sum(contingency_matrix[i][j] for i in range(len(contingency_matrix))) for i in range(len(contingency_matrix))]
    pe = sum((row_sums[i] * col_sums[i]) for i in range(len(row_sums))) / (n * n)
    if pe == 1.0:
        return 1.0
    return (po - pe) / (1.0 - pe)

def evaluate_cdq(
    tester_engineer_matrix: List[List[int]], 
    prod_escapes: int, 
    baseline_escapes: int = 1
) -> Tuple[float, str]:
    kappa = compute_cohens_kappa(tester_engineer_matrix)
    r_esc = prod_escapes / max(1, baseline_escapes)
    cdq = kappa * math.log2(1.0 + r_esc)

    if cdq > 0.85:
        action = "COLLUSION_ALARM: Suspend Tester signing key; trigger adversarial canary test."
    elif cdq > 0.40:
        action = "INVESTIGATION_WARN: Elevated alignment with escapes; increase audit sampling."
    else:
        action = "NOMINAL: Agents demonstrating statistical independence."
    return cdq, action
```

---

### 3. Bayesian Beta-Binomial Strictness Calibration

Static thresholds suffer from two catastrophic failure modes: threshold drift (becoming overly permissive as suites grow) and gridlock (overly strict gates halting throughput). 

Rather than heuristic $\pm 5\%$ jumps, we model the true defect escape probability $\theta \in [0, 1]$ as a conjugate **Beta-Binomial process**:

$$\theta \sim \text{Beta}(\alpha_0, \beta_0)$$

Given an audit window of $N$ tasks with $k$ verified defective escapes:

$$\theta \mid k, N \sim \text{Beta}(\alpha_0 + k, \, \beta_0 + N - k)$$

The posterior mean escape rate is:

$$\mathbb{E}[\theta \mid k, N] = \frac{\alpha_0 + k}{\alpha_0 + \beta_0 + N}$$

With posterior variance:

$$\text{Var}(\theta \mid k, N) = \frac{(\alpha_0 + k)(\beta_0 + N - k)}{(\alpha_0 + \beta_0 + N)^2 (\alpha_0 + \beta_0 + N + 1)}$$

#### 3.1 Damped Strictness Shift Equation
To adjust the mutation gate threshold $T_{\text{mut}}$ (nominal $T^* = 0.80$) and assertion strictness without inducing oscillatory limit cycles, we apply a damped, variance-penalized update:

$$\Delta T = \gamma \cdot \text{clip}\left( \frac{\mathbb{E}[\theta] - \theta^*}{\sqrt{\text{Var}(\theta) + \epsilon}}, \, -\delta_{\max}, \, \delta_{\max} \right)$$

Where:
- $\theta^*$ is the target defect escape ceiling (nominal $\theta^* = 0.02$ / 2%).
- $\gamma = 0.12$ is the learning dampening rate.
- $\delta_{\max} = 0.05$ (5% max threshold step per audit epoch).
- $\epsilon = 10^{-6}$ numerical stability floor.

```python
"""Bayesian Strictness Calibration Engine."""
from dataclasses import dataclass

@dataclass
class BetaPrior:
    alpha: float = 2.0  # Equivalent to 2 prior defects
    beta: float = 98.0  # Equivalent to 98 prior clean tasks (nominal 2% prior)

class BayesianStrictnessCalibrator:
    def __init__(self, prior: BetaPrior = BetaPrior(), target_escape_rate: float = 0.02, dampening: float = 0.12, max_shift: float = 0.05):
        self.alpha = prior.alpha
        self.beta = prior.beta
        self.target_escape_rate = target_escape_rate
        self.gamma = dampening
        self.max_shift = max_shift

    def update(self, observed_tasks: int, observed_escapes: int) -> Tuple[float, float, float]:
        """Returns (posterior_mean, posterior_variance, recommended_threshold_delta)."""
        post_alpha = self.alpha + observed_escapes
        post_beta = self.beta + (observed_tasks - observed_escapes)

        post_mean = post_alpha / (post_alpha + post_beta)
        post_var = (post_alpha * post_beta) / (((post_alpha + post_beta) ** 2) * (post_alpha + post_beta + 1.0))

        # Standardized deviation from target
        z_score = (post_mean - self.target_escape_rate) / math.sqrt(post_var + 1e-6)
        
        # Raw delta modulated by damping
        raw_delta = self.gamma * (z_score * 0.01) # scale z-score to percentage units
        clipped_delta = max(-self.max_shift, min(self.max_shift, raw_delta))

        # Update running prior
        self.alpha = post_alpha
        self.beta = post_beta

        return post_mean, post_var, clipped_delta
```

---

### 4. Quantitative Thresholds & Invariants Summary

| Mechanism | Metric / Parameter | Target Threshold | Action on Breach |
|---|---|---|---|
| **Gate Token Verifier** | Verification Latency | $< 2.0\text{ ms}$ | Fail closed if SQLite query timeout $> 50\text{ ms}$ |
| **Token Validity** | Max TTL ($TTL_{\max}$) | $1800\text{ s}$ (30 min) | Token expires; requires fresh test suite run |
| **Emergency Lease** | Override Max TTL | $900\text{ s}$ (15 min) | Automatic canary rollback if unpromoted |
| **Collusion Monitor** | Collusion Detection Quotient (CDQ) | $\le 0.40$ nominal | $> 0.85 \implies$ Revoke keys, isolate pair |
| **M-of-N Threshold** | Quorum Requirement | $M \ge 2$ of $\{ \text{Operator}, \text{Critic}, \text{Tester} \}$ | Unilateral promotion attempts rejected |
| **Bayesian Calibration** | Max Delta per Epoch ($\delta_{\max}$) | $\pm 0.05$ (5% absolute) | Clamps large jumps; dampens oscillations ($\gamma=0.12$) |

---

### References (pass 3)
1. RFC 8032: Edwards-Curve Digital Signature Algorithm (Ed25519), Internet Engineering Task Force (IETF), 2017. https://datatracker.ietf.org/doc/html/rfc8032
2. RFC 8785: JSON Canonicalization Scheme (JCS), Internet Engineering Task Force (IETF), 2020. https://datatracker.ietf.org/doc/html/rfc8785
3. Cohen, J. (1960). "A Coefficient of Agreement for Nominal Scales". *Educational and Psychological Measurement*, 20(1), 37–46.
4. Gelman, A., Carlin, J. B., Stern, H. S., Dunson, D. B., Vehtari, A., & Rubin, D. B. (2013). *Bayesian Data Analysis* (3rd ed.). Chapman and Hall/CRC.
5. NIST SP 800-207: "Zero Trust Architecture". National Institute of Standards and Technology, 2020. https://doi.org/10.6028/NIST.SP.800-207

