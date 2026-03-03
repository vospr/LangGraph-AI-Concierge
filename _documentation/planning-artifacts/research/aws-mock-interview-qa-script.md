# AWS GenAI Mock Interview Q&A Script

**Date:** 2026-02-23  
**Use:** Practice spoken answers for senior/staff system design interviews.

---

## Practice Format

- Target answer length: 45-60 seconds.
- Structure: constraints -> architecture -> tradeoff -> mitigation.
- After each main answer, practice the follow-up in 15-25 seconds.

---

## 1) Legal research assistant with semantic + citation precision

**Interviewer:** How would you design legal RAG retrieval that handles semantic meaning and exact legal citations?

**Ideal answer (60s):**  
I would implement hybrid retrieval, not pure vector search. Legal workloads need semantic recall and exact terminology match, so I would use Bedrock Knowledge Bases with OpenSearch hybrid retrieval, strict metadata filters, and citation-enforced response formatting. I would tune chunking for section coherence and run offline relevance tests for legal queries. This gives better precision for citations and reduces misses on statute-like strings. The tradeoff is tuning complexity, mitigated by a benchmark set and periodic retrieval evaluation jobs.

**Follow-up:** Why not vector-only retrieval?  
**Follow-up answer:** Vector-only often misses exact phrase and citation-level matching. Legal search needs lexical precision, so hybrid is safer.

---

## 2) GenAI API with token limits, retries, and streaming

**Interviewer:** What architecture would you use with least operational overhead?

**Ideal answer (60s):**  
I would use API Gateway plus a thin Lambda control layer before Bedrock streaming inference. Lambda enforces token budget policy, adaptive retries with jitter, and timeout control, then calls `InvokeModelWithResponseStream`. This keeps infrastructure fully managed while preserving precise runtime controls. I would emit token, latency, and retry metrics to CloudWatch. Tradeoff is one extra hop; mitigation is lightweight Lambda logic and region-local deployment.

**Follow-up:** Why not direct API Gateway to Bedrock?  
**Follow-up answer:** Direct integration reduces flexibility for custom token governance and retry policies.

---

## 3) Prompt consistency with non-blocking content filter alerts

**Interviewer:** How do you enforce required prompt inputs and response format, but only alert on flagged content?

**Ideal answer (60s):**  
I would define prompts in Bedrock Prompt Management with required variables and output schema, then run through Bedrock Flows with Guardrails configured in detect mode for selected categories. Detect mode lets us alert and audit without hard-blocking every flagged response. I would route high-risk detections to EventBridge for review workflow. Tradeoff is potential unsafe pass-through under detect mode; mitigation is escalation thresholds and category-based blocking for truly critical risks.

**Follow-up:** Why not block all flags?  
**Follow-up answer:** Full blocking can hurt business continuity. Detect-plus-escalate gives safer control with operational flexibility.

---

## 4) Source traceability and metadata attribution

**Interviewer:** How do you keep source attribution through a GenAI pipeline?

**Ideal answer (60s):**  
I would standardize metadata at ingestion and register sources centrally using AWS Glue Data Catalog plus source tags, then enforce propagation through each transformation step. CloudTrail would provide audit visibility on access and changes. This keeps lineage intact for governance and explainability. Tradeoff is schema discipline overhead; mitigation is contract tests and metadata validation in CI/CD.

**Follow-up:** Why not rely only on S3 object tags?  
**Follow-up answer:** Tags alone are not enough for full catalog-level lineage and consistency across pipelines.

---

## 5) 10k+ concurrent recommendation assistant

**Interviewer:** How do you handle low-latency, high-concurrency recommendation conversations?

**Ideal answer (60s):**  
For conversational recommendations over text/reviews, I would use Bedrock KB with OpenSearch vector retrieval and API Gateway plus Lambda orchestration. That gives managed scaling and low-latency retrieval. If strict personalized ranking quality is required, I would augment with a dedicated ranker model endpoint. Tradeoff is additional complexity in hybrid ranking; mitigation is phased rollout starting with managed retrieval and adding ranker only after KPI validation.

**Follow-up:** When would SageMaker be justified here?  
**Follow-up answer:** When custom ranking models clearly outperform prompt/retrieval approaches on business KPIs.

---

## 6) Multi-account model governance

**Interviewer:** How would you enforce approved models and prompt safety controls across accounts?

**Ideal answer (60s):**  
I would enforce model allow-lists via SCPs and require approved guardrail usage through IAM conditions and role boundaries. Governance must be outside prompts, at org policy level. I would also centralize logging and alerting for policy violations. Tradeoff is slower policy change cycles; mitigation is staged policy rollout and policy-as-code.

**Follow-up:** Why not rely on app-level checks only?  
**Follow-up answer:** App-only checks are bypassable. Org-level SCP + IAM controls are authoritative.

---

## 7) Large-scale RAG inconsistency in scientific corpus

**Interviewer:** Users say responses cite irrelevant sections. How do you fix retrieval quality?

**Ideal answer (60s):**  
I would revise chunking strategy first: hierarchical or semantic chunking to preserve paragraph-level context and section continuity, then tune overlap and reranking. In very large corpora, naive fixed chunks cause context fragmentation and retrieval drift. I would also add domain-specific metadata filters. Tradeoff is higher indexing complexity; mitigation is controlled experiments with retrieval quality metrics.

**Follow-up:** Would you jump to fine-tuning first?  
**Follow-up answer:** No. Fix retrieval quality and chunking before model tuning.

---

## 8) Real-time call center copilot

**Interviewer:** Design a managed AWS architecture for live assistant suggestions while customer is speaking.

**Ideal answer (60s):**  
I would stream audio through Amazon Transcribe streaming with partial transcripts, then call Bedrock streaming inference and push incremental suggestions to agent desktop via API Gateway WebSocket. This supports real-time feedback and fully managed services. I would track first-token latency and suggestion usefulness metrics in CloudWatch. Tradeoff is orchestration complexity under burst traffic; mitigation is backpressure, queueing, and autoscaling controls.

**Follow-up:** Why not batch transcription?  
**Follow-up answer:** Batch misses real-time requirements and breaks in-call assist experience.

---

## 9) Fairness evaluation across demographic groups

**Interviewer:** How do you evaluate fairness and alert on >15% discrepancy?

**Ideal answer (60s):**  
I would run a dedicated fairness evaluation pipeline by demographic slices, publish fairness metrics to CloudWatch, and set alarms for threshold breaches. This should be a measurable evaluation workflow, not only guardrails. I would compare prompt variants or model variants against the same evaluation set for controlled results. Tradeoff is evaluation overhead; mitigation is scheduled automation and representative sample management.

**Follow-up:** Why are guardrails alone insufficient?  
**Follow-up answer:** Guardrails are policy filters, not full fairness measurement frameworks.

---

## 10) Prompt inconsistency in clinical summaries

**Interviewer:** How do you diagnose and control prompt quality drift over time?

**Ideal answer (60s):**  
I would treat prompts as versioned artifacts with CI regression tests over complex clinical datasets and quantitative quality metrics. Every prompt change must pass thresholds before promotion. I would track historical performance per version to detect regressions early. Tradeoff is pipeline overhead; mitigation is automated test runs and reusable datasets.

**Follow-up:** Why not choose prompts manually in production?  
**Follow-up answer:** Manual selection is subjective and not stable; regulated domains need repeatable evidence.

---

## 11) Hallucinations plus 40% cost overrun

**Interviewer:** What monitoring architecture would you put in place?

**Ideal answer (60s):**  
I would enable Bedrock invocation logging to S3, activate grounding-related safety checks, and set CloudWatch anomaly detection on token and cost metrics. I would correlate quality and cost metrics in dashboards to identify root causes like retrieval drift or prompt inflation. Tradeoff is monitoring data volume; mitigation is tiered retention and sampled deep analysis.

**Follow-up:** Why not only CloudTrail?  
**Follow-up answer:** CloudTrail is control-plane audit, not enough for response-quality and token-usage diagnostics.

---

## 12) Multilingual RAG with metadata filters

**Interviewer:** 10M embeddings, multilingual search, low latency, low ops. What do you choose?

**Ideal answer (60s):**  
I would use OpenSearch Serverless for vector search with metadata filtering and integrate with Bedrock Knowledge Bases for managed RAG orchestration. This gives scalable retrieval with lower operational burden than self-managed databases. I would validate multilingual retrieval quality using language-balanced test sets. Tradeoff is service-specific tuning limits; mitigation is schema and filter design upfront.

**Follow-up:** Why not pgvector first?  
**Follow-up answer:** For this scale and low-ops requirement, managed vector search is usually better fit.

---

## 13) Agent workflow needing memory + event-driven + synchronous support

**Interviewer:** What is your architecture for scalable reasoning workflows?

**Ideal answer (60s):**  
I would use managed Bedrock agent capabilities for session-aware memory and access control, and expose actions through API Gateway/EventBridge so both sync and async invocations are supported. This reduces custom orchestration while preserving policy and observability. Tradeoff is framework dependency; mitigation is tool abstraction and contract-first APIs.

**Follow-up:** Why not custom ECS orchestrator from day one?  
**Follow-up answer:** It increases operational load without proving incremental value first.

---

## 14) Bedrock observability and retries during peak load

**Interviewer:** How do you prevent transient failures from cascading?

**Ideal answer (60s):**  
I would configure SDK retries with exponential backoff and jitter, use distributed tracing across boundaries, and set anomaly alarms for latency and error bursts. Retry policy must be bounded to avoid retry storms. I would include circuit-breaker logic for downstream protection. Tradeoff is occasional delayed responses; mitigation is graceful degradation paths.

**Follow-up:** Why fixed retry delay is weak?  
**Follow-up answer:** Fixed delays synchronize retries and can amplify traffic spikes.

---

## 15) S3 upload to post-call summary and sentiment output

**Interviewer:** Describe an event-driven implementation.

**Ideal answer (60s):**  
I would trigger Step Functions via EventBridge on S3 object creation, run Transcribe, validate completion, then invoke Bedrock through Lambda prompt builder for structured JSON output, and store results back to S3. This gives observable, retryable workflow orchestration and clear failure handling. Tradeoff is state-machine complexity; mitigation is modular states and shared libraries.

**Follow-up:** Why Step Functions over ad hoc Lambda chaining?  
**Follow-up answer:** Better reliability, visibility, and native retry/state semantics.

---

## 16) EU data residency and private model access

**Interviewer:** How do you satisfy strict regional controls with Bedrock?

**Ideal answer (60s):**  
I would align SCP and IAM permissions to approved EU inference profile paths, ensure model access in required regions, and route calls through compliant profile endpoints only. This preserves governance while enabling availability options within policy boundaries. Tradeoff is policy complexity; mitigation is policy-as-code and automated access tests.

**Follow-up:** Why not grant broad admin temporarily?  
**Follow-up answer:** It violates least privilege and weakens compliance posture.

---

## 17) Token governance at >5,000 requests/min and BU chargeback

**Interviewer:** What architecture gives proactive alerts and cost allocation?

**Ideal answer (60s):**  
I would estimate tokens pre-invocation in Lambda, emit per-model and per-business-unit metrics to CloudWatch, trigger threshold alarms, and persist granular usage records in DynamoDB for chargeback. This gives proactive control and financial attribution. Tradeoff is token estimation error; mitigation is periodic reconciliation with actual usage logs.

**Follow-up:** Why API throttling alone is insufficient?  
**Follow-up answer:** Throttling controls request rate, not model-specific token consumption and chargeback accuracy.

---

## 18) Layered pre-LLM content filtering

**Interviewer:** How do you prevent unsafe content before model invocation?

**Ideal answer (60s):**  
I would implement a multi-stage pre-processing pipeline: safety intent classification, toxicity checks, and PII detection/redaction before any Bedrock invocation. Flagged items route to human review through EventBridge. This enforces policy before generation, reducing downstream risk. Tradeoff is extra latency; mitigation is parallelizable checks where policy allows.

**Follow-up:** Why not run filters after generation only?  
**Follow-up answer:** Post-filtering is too late for prompt-side risk and data-leak prevention.

---

## 19) Product recommendations hallucinating unavailable items

**Interviewer:** How do you reduce recommendation hallucinations fast?

**Ideal answer (60s):**  
I would add a catalog-grounding validation layer: every recommended item must be verified against live product catalog availability and relevance constraints before response finalization. Retrieval grounding plus deterministic validation is stronger than prompt-only controls. Tradeoff is extra lookup latency; mitigation is fast indexed catalog checks and batching.

**Follow-up:** Why not just improve prompting?  
**Follow-up answer:** Prompting helps but cannot guarantee inventory correctness.

---

## 20) Automated quality evaluation with selective human review

**Interviewer:** How would you combine scale automation with expert oversight?

**Ideal answer (60s):**  
I would run automated Bedrock evaluations for factuality and response quality, enforce compliance controls with guardrails/policy checks, and route only critical or uncertain cases to A2I human review. This keeps broad coverage with targeted expert attention. Tradeoff is labeling cost; mitigation is risk-based sampling and threshold tuning.

**Follow-up:** Why not 100% manual review?  
**Follow-up answer:** It does not scale and introduces high latency and cost.

---

## 21) Minimal-change RAG relevance improvement

**Interviewer:** Users get irrelevant retrieval due to broad vector search scope. Minimal changes only.

**Ideal answer (60s):**  
I would enable metadata-aware filtering in the existing Bedrock Knowledge Base by indexing source metadata such as content type and time window. That narrows candidate documents without redesigning the architecture. Tradeoff is metadata curation effort; mitigation is automated metadata enrichment at ingestion.

---

## 22) Multi-agent healthcare assistant by domain

**Interviewer:** How do you architect domain-safe multi-agent healthcare support?

**Ideal answer (60s):**  
I would use a supervisor agent for intent routing and separate domain agents with isolated knowledge bases for clinical, insurance, scheduling, and claims. This improves correctness, safety boundaries, and onboarding of new capabilities. Tradeoff is coordination complexity; mitigation is shared schemas, tracing, and explicit handoff contracts.

---

## Final Drill Script (Daily)

1. Pick 5 random questions from this file.  
2. Answer each in 60 seconds without notes.  
3. Repeat each with a 20-second follow-up response.  
4. End by summarizing tradeoffs and governance controls in one minute.

