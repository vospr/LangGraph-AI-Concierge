# AWS GenAI Mock Interview - Hard Mode

**Date:** 2026-02-23  
**Use:** Practice adversarial interviewer pushback and senior-level rebuttals.

---

## Hard Mode Rules

1. Answer in 45-60 seconds.
2. Handle 2-3 pushbacks in under 20 seconds each.
3. Defend tradeoffs with metrics, constraints, and risk controls.
4. Never claim "best" without naming assumptions.

---

## 1) Legal RAG: semantic plus exact citations

**Interviewer:** Your legal assistant must support semantic meaning and exact citation precision. Design it.

**Your answer:**  
I would use Bedrock Knowledge Bases with OpenSearch hybrid retrieval, metadata filters, and citation-enforced response templates. Hybrid is required because legal terms need lexical precision while concept matching needs semantic recall. I would tune chunking by section and evaluate retrieval quality on a legal benchmark set.

**Pushback A:** Hybrid retrieval is expensive. Why not vector-only?  
**Rebuttal:** Vector-only lowers exact-match precision on legal citations. I would optimize cost by caching repeated queries and narrowing retrieval candidates with metadata filters.

**Pushback B:** What if citations are still wrong?  
**Rebuttal:** Add a post-generation citation validator that checks cited passage IDs against retrieved context before response finalization.

---

## 2) Token limits, retries, streaming

**Interviewer:** Least-ops architecture for token governance and streaming?

**Your answer:**  
API Gateway plus a thin Lambda policy layer calling Bedrock streaming inference. Lambda enforces token budget, retry with jitter, and timeout policy. CloudWatch tracks token, latency, and retry metrics.

**Pushback A:** Why not direct API Gateway to Bedrock?  
**Rebuttal:** Direct integration reduces policy flexibility for token estimation, custom retry controls, and per-business-unit metering.

**Pushback B:** Lambda adds latency.  
**Rebuttal:** The policy layer is lightweight, and the control benefit outweighs marginal overhead for governed production traffic.

---

## 3) Prompt consistency with non-blocking filter alerts

**Interviewer:** Required prompt fields, fixed output format, but flagged content should alert and not always block.

**Your answer:**  
Use Prompt Management variables and output schema, run through Flows, attach Guardrails in detect mode for selected categories, and route high-risk alerts to EventBridge review workflow.

**Pushback A:** Detect mode can let bad content through.  
**Rebuttal:** Use risk tiers. Critical classes block, medium classes detect-and-escalate, low classes log only.

**Pushback B:** How do you prove consistency?  
**Rebuttal:** CI prompt regression tests and schema validation at runtime.

---

## 4) Source traceability and metadata attribution

**Interviewer:** How do you preserve source lineage across the whole GenAI pipeline?

**Your answer:**  
Register sources in Glue Data Catalog, enforce metadata contracts at ingestion, propagate tags through transforms, and audit access with CloudTrail. This gives document-level attribution and governance evidence.

**Pushback A:** Why not just S3 tags?  
**Rebuttal:** S3 tags alone are not enough for cross-pipeline lineage and standardized schema governance.

**Pushback B:** Metadata quality drifts over time.  
**Rebuttal:** Add contract tests and ingestion reject rules for invalid metadata.

---

## 5) 10k+ concurrent recommendation assistant

**Interviewer:** Low-latency recommendation chat at high concurrency.

**Your answer:**  
Start with Bedrock KB plus OpenSearch retrieval and Lambda/API Gateway orchestration for managed scale. If business KPIs require stronger personalization ranking, add a dedicated ranker endpoint later.

**Pushback A:** Why not build ranker first?  
**Rebuttal:** Start with lowest-operational path and validate KPI gap before introducing ML platform complexity.

**Pushback B:** What metric drives the decision to add ranker?  
**Rebuttal:** Conversion lift and relevance NDCG gap against retrieval-only baseline.

---

## 6) Org-wide model allow-lists and prompt governance

**Interviewer:** Multiple AWS accounts, central control, no policy bypass.

**Your answer:**  
Use SCPs for model allow-lists, IAM conditions and role boundaries to require approved guardrails, and centralized logs for violation monitoring.

**Pushback A:** App teams need fast iteration.  
**Rebuttal:** Use a governed exception path with pre-approved model tiers and automated policy promotion.

**Pushback B:** Why not enforce in app code?  
**Rebuttal:** Org policy controls are authoritative. App-only controls are bypassable.

---

## 7) Scientific corpus RAG inconsistency

**Interviewer:** 25M+ papers, irrelevant citations, similar sections.

**Your answer:**  
I would switch to hierarchical or semantic chunking, tune overlap and reranking, and apply domain metadata filters. The primary issue is context fragmentation, not model intelligence alone.

**Pushback A:** Why not fine-tune model first?  
**Rebuttal:** Retrieval quality should be fixed before tuning because bad context in means bad output out.

**Pushback B:** How do you validate improvement?  
**Rebuttal:** Retrieval precision-at-k and grounded-answer accuracy on domain test sets.

---

## 8) Real-time call-center copilot

**Interviewer:** Live transcription plus incremental suggestions while customer is speaking.

**Your answer:**  
Use Transcribe streaming partials, feed to Bedrock streaming inference, return suggestions over API Gateway WebSocket to agent desktop. Add backpressure and autoscaling guardrails.

**Pushback A:** What if latency spikes under load?  
**Rebuttal:** Degrade gracefully to concise hints, prioritize active calls, and enforce timeout budgets.

**Pushback B:** How do you measure user value?  
**Rebuttal:** Track assist acceptance rate, average handling time reduction, and first-token latency.

---

## 9) Fairness evaluation with alert thresholds

**Interviewer:** Need fairness discrepancy detection above 15% between groups.

**Your answer:**  
Use a dedicated fairness evaluation pipeline by demographic slice, publish metrics to CloudWatch, and set threshold alerts. Compare prompt variants against the same evaluation datasets.

**Pushback A:** Can guardrails do fairness?  
**Rebuttal:** Guardrails are policy filters, not full fairness analytics.

**Pushback B:** How do you avoid false alarms?  
**Rebuttal:** Use minimum sample-size gates and confidence intervals before alerting.

---

## 10) Clinical summary inconsistency and prompt drift

**Interviewer:** Complex docs fail while simple docs pass. What now?

**Your answer:**  
Treat prompts as code: version, test, and promote via CI gates on complex clinical datasets with quantitative metrics. Keep historical performance by version.

**Pushback A:** Why not human QA only?  
**Rebuttal:** Human-only QA does not scale and is inconsistent for release gating.

**Pushback B:** Which metrics matter?  
**Rebuttal:** Factual consistency, omission rate, compliance pass rate, and variance across document complexity tiers.

---

## 11) Hallucinations and 40% cost overrun

**Interviewer:** Give me monitoring with minimal custom maintenance.

**Your answer:**  
Enable Bedrock invocation logging to S3, add grounding checks, and configure CloudWatch anomaly alarms for token and cost drift. Correlate quality and spend metrics in one dashboard.

**Pushback A:** Why not CloudTrail only?  
**Rebuttal:** CloudTrail is control-plane audit and lacks deep response-quality telemetry.

**Pushback B:** How do you find root cause quickly?  
**Rebuttal:** Slice by model, prompt version, retrieval source, and traffic segment.

---

## 12) Multilingual RAG with metadata filters

**Interviewer:** 10M embeddings, low-latency, minimal ops overhead.

**Your answer:**  
Use OpenSearch Serverless with metadata filtering integrated with Bedrock KB. It balances scale and low ops for multilingual retrieval.

**Pushback A:** Why not pgvector in Aurora?  
**Rebuttal:** At this scale and ops constraint, managed vector search is usually more operationally efficient.

**Pushback B:** How do you validate multilingual parity?  
**Rebuttal:** Language-balanced evaluation sets and per-language recall/precision tracking.

---

## 13) Agent workflows with memory and event-driven invocation

**Interviewer:** Must support sync and async, session control, memory.

**Your answer:**  
Use managed Bedrock agent capabilities for session-aware memory and expose tools via API Gateway and EventBridge for sync and async paths.

**Pushback A:** Why not ECS custom orchestrator now?  
**Rebuttal:** Higher ops cost upfront without proof of incremental business value.

**Pushback B:** What if we outgrow managed features?  
**Rebuttal:** Keep tool contracts and orchestration interfaces portable so migration is controlled.

---

## 14) Observability and retries under peak traffic

**Interviewer:** Prevent cascading failures on transient model errors.

**Your answer:**  
Use bounded retries with exponential backoff and jitter, add tracing IDs across services, and enforce circuit breakers plus fallback behavior.

**Pushback A:** Why not fixed 1-second retry delay?  
**Rebuttal:** Fixed delay synchronizes retries and amplifies traffic spikes.

**Pushback B:** What fallback would you use?  
**Rebuttal:** Smaller model fallback or deterministic response path for critical intents.

---

## 15) Event-driven post-call analysis

**Interviewer:** S3 recording lands, then summarize and sentiment in structured output.

**Your answer:**  
Trigger Step Functions via EventBridge on object creation, transcribe audio, call Bedrock through a prompt-builder Lambda, and persist structured JSON back to S3.

**Pushback A:** Why Step Functions over Lambda chain?  
**Rebuttal:** Native retries, state visibility, error handling, and auditability.

**Pushback B:** How to avoid duplicate processing?  
**Rebuttal:** Idempotency keys from object metadata and execution dedupe checks.

---

## 16) EU data residency and private FM access

**Interviewer:** Strict SCP controls, cross-region profile usage, no compliance break.

**Your answer:**  
Update SCP and IAM conditions to allow only approved EU inference profile paths, verify model access in target regions, and enforce profile-based invocation.

**Pushback A:** Why not grant temporary admin?  
**Rebuttal:** Violates least privilege and weakens governance controls.

**Pushback B:** How to test policy safely?  
**Rebuttal:** Policy simulation plus pre-prod canary account validation.

---

## 17) Token management and proactive alerting at 5k+ RPM

**Interviewer:** Need alerts before token limits and BU-level cost allocation.

**Your answer:**  
Estimate token usage pre-invoke in Lambda, publish per-model and per-BU metrics to CloudWatch, and store per-request usage records for chargeback.

**Pushback A:** API throttling already exists. Enough?  
**Rebuttal:** Throttling is request-rate control, not token-governance and BU attribution.

**Pushback B:** Estimation can be wrong.  
**Rebuttal:** Reconcile estimated versus actual usage logs and calibrate per model.

---

## 18) Layered content filtering before FM

**Interviewer:** Must block offensive, PII, and harmful advice prompts before model call.

**Your answer:**  
Use a staged pre-inference pipeline with safety classification, toxicity checks, and PII detection/redaction. Route flagged items to review queues.

**Pushback A:** Why not post-filter only?  
**Rebuttal:** Post-filtering cannot prevent prompt-side data leakage and harmful prompt execution.

**Pushback B:** This adds latency.  
**Rebuttal:** Parallelize safe-compatible checks and keep strict SLA budgets per stage.

---

## 19) Product recommendation hallucinations

**Interviewer:** Recommendations include unavailable or irrelevant products.

**Your answer:**  
Add deterministic catalog validation before final response. Retrieval and generation can suggest, but final output must pass live inventory and relevance constraints.

**Pushback A:** Can prompt engineering alone solve it?  
**Rebuttal:** No deterministic guarantee. Validation layer is needed for correctness.

**Pushback B:** How to keep latency low?  
**Rebuttal:** Use indexed catalog checks and batch validation in one lookup call.

---

## 20) Automated quality evaluation plus targeted human review

**Interviewer:** Need scale automation and expert oversight for financial assistant.

**Your answer:**  
Use automated evaluations for factual and conversational quality, enforce policy checks with guardrails, and route high-risk interactions to A2I human review.

**Pushback A:** Why not review everything manually?  
**Rebuttal:** Does not scale, expensive, and too slow for continuous delivery.

**Pushback B:** How do you choose high-risk cases?  
**Rebuttal:** Low confidence, policy-near-miss, high-value intents, and random audit sampling.

---

## 21) Minimal-change RAG relevance fix

**Interviewer:** Keep architecture mostly unchanged.

**Your answer:**  
Enable metadata-aware filtering in current Bedrock KB and enrich ingestion metadata to reduce irrelevant candidate retrieval.

**Pushback A:** Why not migrate vector database now?  
**Rebuttal:** Migration risk is unnecessary if metadata filtering addresses the main retrieval issue.

---

## 22) Multi-agent healthcare assistant by department

**Interviewer:** Scalable, safe, domain-correct responses across clinical, insurance, scheduling, claims.

**Your answer:**  
Use a supervisor for intent routing and separate domain agents with isolated knowledge bases and clear boundaries. This reduces cross-domain contamination and supports incremental feature onboarding.

**Pushback A:** Why not one general agent?  
**Rebuttal:** Higher risk of domain mixing and weaker control in regulated healthcare contexts.

**Pushback B:** How do agents coordinate safely?  
**Rebuttal:** Contracted handoff schema, trace IDs, and policy checks at each boundary.

---

## 10-Minute Stress Drill

1. Pick any 3 sections.
2. Deliver main answer in 45 seconds each.
3. Answer both pushbacks in under 20 seconds each.
4. End with one line: `Primary risk is X, my mitigation is Y, and my metric is Z.`

