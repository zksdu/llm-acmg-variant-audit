**Title: Multi-vendor evaluation of large language models for ACMG/AMP variant classification with controlled data contamination**

**Keywords:** variant classification; ACMG/AMP; large language models; data leakage; ClinVar; temporal blinding

---

## Abstract

Large language models (LLMs) are increasingly proposed for ACMG/AMP variant classification, but their training corpora include public variant databases, so reported accuracy may reflect label memorization rather than reasoning. We audited nine LLMs (six Chinese, three international flagships; 45,000 evaluations) on 5,000 ClinVar variants whose gold-standard labels postdate every model's training cutoff (temporal blinding), with independent validation on 900 expert-panel-curated variants. Under blinding, current-generation models achieved 61.8–71.6% all-inclusive accuracy (86–93% on expert-panel variants); conservative models reached 97.8–98.7% conditional accuracy with 1.3–2.5% Benign-to-Pathogenic false-positive rates, whereas reasoning models mislabeled 22–28% of Benign variants as Pathogenic. Adding allele-frequency evidence raised Benign sensitivity by up to 60.1 percentage points. On a dedicated fully blinded set (n = 2,000), Gemini and Claude were statistically indistinguishable (81.4% vs. 80.2%), while GPT-5.6-terra fell to 64.7% with 25.0% false positives. LLM variant interpretation is trustworthy only under blinded model selection, complete evidence provision, and abstention-as-human-review policies. All data and analysis code are archived at Zenodo (DOI: 10.5281/zenodo.22299737).

## Introduction

Clinical variant interpretation — classifying a germline variant as Pathogenic, Benign, or Uncertain per ACMG/AMP guidelines — is a bottleneck in genomic medicine: manual curation is expert-hours per variant and inconsistent across laboratories ([1,2]). Large language models (LLMs) have been proposed as scalable interpreters ([3-5]), with recent work reporting near-expert agreement (e.g., AI-CURA reports expert-level consistency on curated variants [6]).

Two problems undermine these numbers. First, **training-data leakage**: LLM corpora contain public variant databases, so a model asked to classify a variant may reproduce a label it has memorized rather than reason about evidence. Published evaluations rarely control for this. Second, **vendor dependence**: results are typically reported for a single model family [7], leaving open whether any observed capability is a property of LLMs in general or of one training pipeline.

Existing variant-interpretation benchmarks do not resolve these concerns. VariantBench [8] evaluates ACMG classifications and criterion-level justifications but without leakage control; VarLitBench [9] anchors on ClinGen-curated functional evidence whose public availability makes memorization possible; AI-CURA [6] demonstrated clinical-grade performance on curated variants, again without controlling what the model saw during training. In the broader LLM literature, benchmark contamination is well documented [10,11], and temporally split evaluation has been proposed as a decontamination strategy [12]. No study to date has combined temporal blinding, multi-vendor coverage, and independent expert-panel validation at scale for variant classification.

Here we report an audit that combines all three controls: 6 LLMs from 4 vendors, 30,000 variant-model evaluations on a temporally blinded test set of 5,000 ClinVar variants (all expert-assessed after January 2026), with an independent 900-variant expert-panel validation set and three triangulation sub-experiments (allele-frequency ablation, conflicting-interpretation variants, and functional-effect variants). We address three questions: (RQ1) How reliable is LLM variant classification under label-leakage control? (RQ2) Do multi-model consensus and model choice improve reliability? (RQ3) How does reliability depend on the evidence available to the model?

We find that label-leakage control reveals a large vendor gap (up to +22 pp among the fully blinded domestic models; the international extension is reported with cutoff-matched controls), that the "when the model speaks it is right" property holds only for conservative models, that majority voting can reduce accuracy, and that model reliability tracks evidence availability — abstention is a calibrated, trustworthy signal rather than noise. We frame this work as a **reliability audit** rather than a generalization study: temporal blinding removes the label-memorization channel, but prior *evidence* (literature, submissions) may remain in training data; our goal is therefore to establish under which operational conditions an LLM's output can be trusted, not to claim de novo generalization from sequence alone.

## Results

### Cohort and experimental scale

We evaluated **6 LLMs from 4 vendors** (DeepSeek: v4-pro, chat, coder; Moonshot: Kimi-K2.6; Xiaomi: MiMo V2.5 Pro; Alibaba: Qwen3.7-max) on a **temporally-blinded test set of 5,000 ClinVar variants** (all LastEvaluated ≥ 2026-01 — after the training cutoff of all six domestic models; the international models’ later cutoffs are disclosed in Methods and controlled by a fully blinded stratum). In total, all 45,000 variant–model pairs produced archived outcomes; 44,938 calls yielded parseable classifications (29,959 domestic, 14,979 international), and the remaining 62 rows (58 unparseable outputs, 4 domestic network failures after retry) are retained and counted as errors under the all-inclusive convention rather than excluded (Methods). All analyses use binary Pathogenic vs. Benign evaluation with VUS treated as abstention (see Methods).

### Headline accuracy: models that speak are almost always right

We report two complementary accuracy metrics (Fig. 1): **all-inclusive accuracy** (VUS counted as errors; clinical usability) and **conditional accuracy given a definitive call** (VUS excluded; reliability of expressed opinions).

**Table 1. Performance on the temporally-blinded test set (n = 5,000 variants).**

| Model | Vendor | All-inclusive Acc. | Conditional Acc. (spoken) | Spoken n | Expert-panel Acc. (n=100) |
|---|---|---|---|---|---|
| Gemini 3 Flash | Google | **76.5%** | 84.3% | 4,538 | 91.0% |
| Qwen3.7-max | Alibaba | 71.6% | 96.4% | 3,714 | 86.0% |
| Claude Sonnet 5 | Anthropic | 68.5% | 97.0% | 3,532 | 90.0% |
| Kimi-K2.6 | Moonshot | 67.0% | 97.8% | 3,421 | 90.0% |
| MiMo V2.5 Pro | Xiaomi | 66.1% | 85.2% | 3,876 | 92.0% |
| DeepSeek V4-pro | DeepSeek | 61.8% | 81.2% | 3,806 | **93.0%** |
| GPT-5.6-terra | OpenAI | 60.3% | 86.9% | 3,469 | 92.0% |
| DeepSeek chat | DeepSeek | 49.4% | 98.6% | 2,504 | 69.0% |
| DeepSeek coder | DeepSeek | 49.2% | 98.7% | 2,494 | 68.0% |
| 6-model majority | — | 64.1% | 98.3% | 2,915 | 93.5% |

> Table 1 footnotes: All-inclusive accuracy = VUS counted as error (clinical usability); conditional accuracy = accuracy restricted to committed calls; expert-panel stratum = 100 variants within the test set whose labels were produced by expert panels (ClinGen VCEP / guideline committees). Wilson 95% CIs: Qwen [70.4, 72.9], Kimi [65.6, 68.2], MiMo [64.7, 67.4], V4-pro [60.5, 63.1], chat [48.0, 50.8], coder [47.8, 50.6]. Majority voting operates on the three-way (P/B/VUS) semantics; ties excluded (n=528), so the majority-row all-inclusive accuracy uses the 4,471 non-tied evaluable variants as denominator (expert-panel stratum: 93 non-tied of 100) — a different denominator from the single-model rows (all 4,999).

**Finding 1 (Generation gap).** New-generation flagship models (Qwen3.7-max, Kimi-K2.6, MiMo V2.5 Pro, DeepSeek V4-pro) outperform the previous generation (DeepSeek chat/coder) by **+12.4 to +22.4 percentage points (pp)** in all-inclusive accuracy (all current-vs-previous-generation pairs McNemar p ≤ 1.6×10⁻⁸⁶; within-generation Kimi vs. MiMo: p = 0.12, n.s.). The gap persists under the highest-confidence gold standard (expert-panel variants: 86–93% vs. 68–69%).

**Finding 2 (Conditional reliability is not universal — and error direction matters).** Conservative models (chat/coder/Kimi) achieve 97.8–98.7% conditional accuracy when they commit. In contrast, reasoning-style models (V4-pro: 81.2%; MiMo: 85.2%) commit more often (76–78% of variants) but their expressed calls are substantially less reliable. Crucially, the errors are directionally asymmetric: when a gold-standard Benign variant receives a definitive call, reasoning models call it **Pathogenic** far more often — V4-pro mislabels 28.4% and MiMo 22.3% of all Benign variants as Pathogenic, versus 1.3–1.4% (chat/coder) and 2.5% (Kimi); Qwen sits between at 4.7%. Six-model consensus restores FP to 1.8%. The property "when the model speaks, it is right" holds **only for conservative models**; for reasoning models, committing is frequent, less accurate, and biased toward the clinically dangerous direction (false Pathogenic; Fig. 4).

**Finding 3 (Majority voting can hurt).** Six-model majority voting (64.1% all-inclusive) underperformed the best single model (Qwen3.7-max, 71.6%; +7.5 pp) because the three DeepSeek votes — collectively the most conservative — dominate ties. Model *diversity and selection* matter more than ensemble size; however, when the ensemble agrees on a definitive call (2,915 variants), conditional accuracy reaches 98.3%.

### Surface-cue stratification: how much performance is readable from the variant name?

HGVS protein notation can itself reveal the answer class: nonsense (p.Xxx###Ter) and frameshift (fs) notation in a haploinsufficient-gene context is near-diagnostic of pathogenicity (ACMG PVS1-like). We stratified gold-standard Pathogenic variants by the presence of such loss-of-function (LoF) surface cues in the variant name.

| Model | P sensitivity, cued (n=1,671) | P sensitivity, uncued (n=828) | Gap |
|---|---|---|---|
| DeepSeek chat | 98.5% | 67.8% | −30.8 pp |
| Kimi-K2.6 | 99.8% | 77.7% | −22.1 pp |
| Qwen3.7-max | 99.4% | 83.6% | −15.8 pp |

**Finding 4 (Part of headline accuracy is name-reading).** Two-thirds of gold-standard Pathogenic variants (1,671/2,499) carry an LoF cue directly in their name, where every model is near-ceiling (98.5–99.8%) — performance achievable from the notation alone. On the 828 uncued variants, sensitivity drops to 67.8–83.6% (still well above the 50% base rate; 16–31 pp weaker). Naive accuracy conflates these regimes; a reliability audit should report both strata. Qwen degrades least (−15.8 pp), consistent with its overall lead.

### Independent gold standard: ClinGen expert-panel review

We constructed a dedicated validation set of **900 variants curated by expert panels** (ClinGen/clinical guideline committees; ReviewStatus = "reviewed by expert panel"; all re-evaluated between 2026-01 and 2026-07, P-side 645, B-side 252). Of these, 100 were also sampled into the main test set (Table 1, expert-panel stratum); to guarantee independence, Table S3 reports the **800 exclusive variants** (797 evaluable; P: 550, B: 247).

**Table S3. Expert-panel validation (n = 797 exclusive variants; 5 models).**

| Model | Vendor | All-inclusive | Conditional | Abstention | FP rate |
|---|---|---|---|---|---|
| Gemini 3 Flash | Google | **79.0%** | 85.4% | 7.4% | 36.4% |
| Kimi-K2.6 | Moonshot | 72.8% | 90.6% | 19.7% | 19.8% |
| GPT-5.6-terra | OpenAI | 69.6% | 84.7% | 17.8% | 36.4% |
| DeepSeek chat | DeepSeek | 42.9% | 95.0% | 54.8% | 7.3% |
| DeepSeek coder | DeepSeek | 43.3% | 94.8% | 54.3% | 7.7% |

> Claude Sonnet 5 excluded: all 800 API calls failed with relay capacity-limit errors (HTTP 502; raw responses retained in the archived results file); no valid results obtained.

> Results on the full 900 (including the shared 100) are qualitatively identical: Kimi 74.7% / chat 45.7% / coder 46.0% (robustness check).

The vendor gap **widens** under the strongest gold standard (+29.9 pp for Kimi vs. chat, vs. +17.6 pp on the general test set), indicating that model choice has a *larger* clinical impact than generic benchmarks suggest. A "always-Pathogenic" baseline would score 69.0% on this P-enriched set; Kimi's 72.8% exceeds it, whereas DeepSeek's ~43% reflects abstention-driven loss rather than misclassification (conditional accuracy 94.8–95.0%).

### Triangulation: evidence availability drives reliability

Three sub-experiments (Fig. 2) show that LLM reliability is governed by the *evidence available in the prompt*:

**(a) Allele-frequency (AF) ablation (n = 400 × 9 models Benign-enriched + 150 × 2 Pathogenic).** Adding population allele frequencies (AF_ESP/ExAC/1000G, from ClinVar VCF) to the prompt — the identical variants, models, and otherwise identical prompts, with the no-AF condition taken from the main experiment — raised Benign sensitivity on gold-standard Benign variants (n = 356) from 8.7% to 68.8% (chat, **+60.1 pp**), 9.3% to 68.3% (coder), and 45.5% to 81.5% (Kimi); chat's abstention on these variants fell from 90% to 31%. **The systematic Benign abstention observed in the main experiment is primarily an information-deficit behavior, not model conservatism.** The effect is Benign-side-specific: on a Pathogenic-enriched AF subset (n = 150 × 2), adding AF did not raise accuracy (chat 76.7%→64.0%; Kimi 90.0%→85.3%) and abstention rose (23.3%→36.0% chat; 8.7%→14.7% Kimi) — population AF is Benign-directed evidence (BA1/BS1), and its presence makes models appropriately more cautious, not more accurate, on Pathogenic calls. AF evidence is thus mandatory for Benign recall but is not a universal accuracy booster.

The AF effect on Benign sensitivity is consistent across all nine tested models (range +32.3 to +60.1 pp): chat 8.7→68.8%, coder 9.3→68.3%, Kimi 45.5→81.5%, Qwen 53.7→93.0%, Gemini 63.2→95.5%, GPT 30.1→90.2%, Claude 51.4→90.7%, V4-pro 27.8→71.3%, MiMo 38.2→80.1%.

**(b) Conflicting-interpretation variants (n = 300 × 2 models).** On variants where clinical submitters disagree (conflicting classifications), models spontaneously raise abstention by **+22.8 pp (Kimi)** and **+39.1 pp (chat)** compared with the main test set — despite the prompt containing no conflict information. LLMs exhibit evidence-grounded uncertainty calibration: they sense controversy.

**(c) Functional-effect task (MaveDB, n = 300 × 2 models).** On deep-mutational-scanning variants with extreme functional scores (loss-of-function: score ≤ −0.8; normal: score ≥ 0.5) but no clinical evidence, models abstain massively (73–93%) and conditional directional agreement ≈ chance (45–55%). LLMs have no capacity for *de novo* functional inference from protein sequence alone — and they know it (abstain rather than hallucinate).


### Calibration

Mean self-reported confidence (0.73–0.80 domestic; 0.95 Gemini) did not track all-inclusive accuracy across models (chat: 0.78 vs. 49.4%; Kimi: 0.73 vs. 67.0%). Confidence calibrates *within* a model's decision style, not across models; reasoning models over-express confidence relative to conditional accuracy (V4-pro: 0.79 vs. 81.2%; MiMo: 0.80 vs. 85.2%).

### Five-class analysis (Fig. 3B): the "Likely" tier is absent

The ACMG/AMP framework is five-class (Pathogenic/Likely pathogenic/Uncertain significance/Likely benign/Benign), and P vs. LP carry different clinical follow-up (e.g., LP requires confirmation). On the expert-panel set (five-class labels: P 303 + 3 compound P/LP, LP 342, LB 193, B 59), **domestic models rarely emit a "Likely" class (Kimi 11/900 = 1.2%, coder 4/900 = 0.4%, chat 2/900 = 0.2%)** — the five-class output collapses to three (P / VUS / B).

| Model | Exact five-class match | Likely-tier output | Cross-semantic errors (P↔B) |
|---|---|---|---|
| Kimi-K2.6 | 32.1% | 11/900 | 7.2% |
| DeepSeek chat | 22.4% | 2/900 | 2.1% |
| DeepSeek coder | 22.7% | 4/900 | 2.2% |
| Gemini 3 Flash | — | 646 LB/5,000 | 27.8% FP |
| Claude Sonnet 5 | — | 1,065 LB/5,000 | 3.9% FP |
| GPT-5.6-terra | — | 591 LB/5,000 | 17.9% FP |

> Note: International models were evaluated on the full 5,000-variant test set (not the 900-variant expert panel set); "LB" = Likely benign output. No model emitted Likely pathogenic (LP = 0 across all 15,000 international calls).

Strength polarization is systematic: 82% (Kimi) and 58% (chat) of gold-standard Likely pathogenic variants were escalated to Pathogenic; 53% of Likely benign were downgraded to Benign by Kimi. Two implications: (i) LLM outputs are usable at the binary-semantics level only — the "Likely" tier carries clinical information the models do not produce; (ii) reported high conditional accuracy on binary P/B evaluation is partly achieved *by* this collapse, which a five-class evaluation would not credit.

### Clinical risk stratification (Weighted Error Severity Index)

To quantify clinical harm we defined a Weighted Error Severity Index (WESI): Benign-to-Pathogenic misclassification = weight 4 (unnecessary prophylactic surgery, cascade screening), Pathogenic-to-Benign = weight 4 (missed diagnosis), unparseable output = weight 2 (delivery failure), VUS abstention = weight 0 (safe deferral).

| Model | WESI | B-to-P (extreme) | Total extreme | Abstention |
|---|---|---|---|---|
| V4-pro | **0.585** | 711 (28.4%) | **716** | 24% |
| Gemini | **0.577** | 694 (27.8%) | **712** | 9% |
| MiMo | **0.460** | 557 (22.3%) | **573** | 22% |
| GPT | **0.363** | 448 (17.9%) | **454** | 31% |
| Qwen | 0.108 | 118 (4.7%) | 133 | 26% |
| Claude | **0.086** | 97 (3.9%) | **107** | 29% |
| Kimi | **0.060** | 63 (2.5%) | **74** | 32% |
| chat | **0.029** | 35 (1.4%) | **36** | 50% |
| coder | **0.026** | 32 (1.3%) | **33** | 50% |

**Finding 7 (A 22-fold clinical risk spectrum).** The safest (coder, 33 extreme events/5000) and most dangerous (V4-pro, 716 events) differ by 22x. Assuming 3–5 relatives per proband undergo cascade testing, V4-pro's 711 false positives could affect roughly 2,100–3,500 relatives. **For clinical deployment, model selection should prioritize WESI over raw accuracy.**

### Output determinism (Fig. 3A; reproducibility audit)

A clinical system must return the *same* answer for the *same* variant, so we re-ran 50 variants per model under identical settings (temperature 0; six models attempted, five completed — Claude returned relay capacity-limit errors (HTTP 502) on every attempt) and measured agreement with the original run.

**Table S1. Re-run consistency (n = 50 variants per model; temperature 0).**

| Model | Exact-class agreement | Binary (P/B) agreement |
|---|---|---|
| DeepSeek chat | 50/50 (100.0%) | 50/50 (100.0%) |
| Kimi-K2.6 | 49/50 (98.0%) | 50/50 (100.0%) |
| Gemini 3 Flash | 40/50 (80.0%) | 44/50 (88.0%) |
| GPT-5.6-terra | 38/50 (76.0%) | 39/50 (78.0%) |
| DeepSeek V4-pro | 31/50 (62.0%) | **32/50 (64.0%)** |
| Claude Sonnet 5 | — | — |

> Cross-check: the 100 expert-panel variants shared between the main test set and the dedicated 900-variant set were classified twice in independent runs (same model, same prompt); agreement was chat 99/100, coder 100/100, Kimi 97/100 — consistent with the determinism ranking above.

**Finding 5 (Reasoning models are not deterministic — worsens with sample size).** At temperature = 0 (n = 200 per model), the determinism spectrum is: Kimi 96.0% > chat 92.5% > Claude 88.0% > Gemini 86.0% > GPT 78.0% > **V4-pro 40.0%**. Critically, the number of direct Benign↔Pathogenic flips (the clinically most consequential error direction): Kimi/chat/Claude = **0**, GPT = 10, Gemini = 15, V4-pro = 2. V4-pro changed its binary output on **60% of re-run variants** (half unparseable — a delivery failure as consequential as a flip) versus an estimated 36% at n = 50: the larger sample reveals worse non-determinism. Three models (chat, Kimi, Claude) never flip across semantic boundaries; their non-determinism is entirely VUS↔definitive shifts, clinically safe (changes abstention, not direction). **A model that returns contradictory clinical directions for the same input cannot be deployed regardless of average accuracy.**

### International extension: three foreign flagships at full scale

To test whether the domestic findings generalize across training ecosystems, we evaluated Gemini 3 Flash, GPT-5.6-terra, and Claude Sonnet 5 on the **complete temporally blinded test set** (5,000 variants each; identical prompts; research-context system prompt for all three; see Methods). Parse-failure rates on the full set were handled identically to the domestic models (counted as errors): Gemini 0.38% (19/5,000; long unparseable reasoning text), Claude 0.04% (2/5,000; empty outputs), and GPT 0% (0/5,000).

**Table S2. Nine-model comparison on the complete test set (n = 5,000 per model).**

| Model | Vendor | All-inclusive | Conditional | Abstention | Benign→Pathogenic FP | Expert-panel (n=100) |
|---|---|---|---|---|---|---|
| Gemini 3 Flash | Google | **76.5%** | 84.3% | 9.2% | 27.8% | 91% |
| Qwen3.7-max | Alibaba | 71.6% | 96.4% | 25.7% | 4.7% | 86% |
| Claude Sonnet 5 | Anthropic | 68.5% | 97.0% | 29.3% | **3.9%** | 90% |
| Kimi-K2.6 | Moonshot | 67.0% | 97.8% | 31.6% | 2.5% | 90% |
| MiMo V2.5 Pro | Xiaomi | 66.1% | 85.2% | 22.5% | 22.3% | 92% |
| DeepSeek V4-pro | DeepSeek | 61.8% | 81.2% | 23.9% | 28.4% | 93% |
| GPT-5.6-terra | OpenAI | 60.3% | 86.9% | 30.6% | 17.9% | 92% |
| DeepSeek chat | DeepSeek | 49.4% | 98.6% | 49.9% | 1.4% | 69% |
| DeepSeek coder | DeepSeek | 49.2% | 98.7% | 50.1% | 1.3% | 68% |

**Finding 6 (The domestic findings generalize — and sharpen — internationally).** Three observations extend beyond the Chinese ecosystem. (i) **On the full set Gemini 3 Flash leads all nine models** (76.5% [75.3–77.7], +4.9 pp over the best domestic model; McNemar p = 1.7×10⁻¹³) with the lowest abstention (9.2%) — but this comparison is not cutoff-controlled: under full blinding the lead vanishes (statistical tie with Claude and Qwen; Table S4), so it may partly reflect residual label exposure. Nor does Gemini's full-set aggressive profile persist: on the dedicated blinded set its Benign→Pathogenic FP is 5.2% (vs. 27.8% on the full set), placing it alongside Claude in the *conservative* camp — while GPT-5.6-terra emerges as the aggressive outlier (FP 25.0%). (ii) **Claude behaves as a conservative model**: 97.0% conditional accuracy with 3.9% FP — closest to Kimi's 2.5% (Fisher exact p = 0.008, distinguishable but both single-digit); it exceeds Kimi all-inclusive (p = 2.7×10⁻³) while sitting below Qwen (p = 3.0×10⁻¹⁵). On the expert-panel set (Table S3) the dichotomy sharpens: Gemini and GPT both show 36.4% FP (vs. Kimi 19.8%, chat/coder 7–8%) — the conservative/aggressive split is a property of model *behavior*, not vendor nationality (behavioral dashboard in Fig. 5). (iii) **GPT-5.6-terra trails its foreign peers** (60.3%, significantly below Qwen: McNemar p = 4.7×10⁻⁹⁰) and sits below every current-generation domestic model — capability tracks neither nationality nor presumed price tier, reinforcing the audit's central message that model choice must be made on measured, blinded evidence rather than vendor reputation.

**Fully blinded evaluation (Table S4).** Because the international models' cutoffs fall in early 2026, we evaluated them in two complementary fully blinded designs. First, on the main set's own ≥ 2026-04 slice (n = 907; P 753 / B 154; August run), the full-set ranking collapses to a three-way tie — Gemini 88.0% [85.7–89.9], Claude 87.1% [84.8–89.1], and the domestic leader Qwen 86.8% [84.4–88.8]; all pairwise McNemar p > 0.4. Second, on a **dedicated fully blinded set** — 2,000 newly sampled variants (seed 42; 1,000 Pathogenic / 1,000 Benign; pool: 4,772 eligible alleles last evaluated ≥ 2026-04; 342 overlap with the main set; identical prompts; single session) — the international picture reorders. **Gemini and Claude are statistically indistinguishable** (81.4% [79.6–83.0] vs. 80.2% [78.3–81.8]; two-proportion z = 1.0, p = 0.32; per-variant pairing unavailable for this run — see archived analysis), both pairing ≈96.5% conditional accuracy with FP rates of 4–5% — the conservative profile. **GPT-5.6-terra emerges as the aggressive outlier**: 64.7% all-inclusive (p < 10⁻³⁰ below both), 25.0% Benign→Pathogenic FP, Benign sensitivity 32.8%, and 58/2,000 unparseable outputs. Gemini's full-set aggressive profile (FP 27.8%) does not persist under full blinding, and its FP differs between the two blinded runs (22.1% August stratum vs. 5.2% September set), consistent with documented non-determinism and possible relay-side version drift — relay-served rankings require blinded, repeated verification. Claude is the only international model whose profile is stable across every estimate (FP 3.9–4.5%). Across both blinded designs, no international model outperforms the best domestic models.

**Table S4. Dedicated fully blinded set (n = 2,000; LastEvaluated ≥ 2026-04; 1,000 P / 1,000 B; single session).**

| Model | All-inclusive (95% CI) | Conditional | Abstention | Benign→Pathogenic FP |
|---|---|---|---|---|
| Gemini 3 Flash | 81.4% [79.6–83.0] | 96.6% | 15.7% | 5.2% |
| Claude Sonnet 5 | 80.2% [78.3–81.8] | 96.5% | 17.0% | 4.3% |
| GPT-5.6-terra | 64.7% [62.6–66.8] | 83.7% | 22.7% | 25.0% |

> Reference (August main-run stratum, n = 907): Gemini 88.0 / Claude 87.1 / Qwen 86.8, three-way tie.

**Cross-ecosystem note: the "Likely" tier survives on the benign side only.** Unlike the six domestic models — which rarely emit a "Likely" class (≤1.2%) (see the five-class analysis below) — all three foreign models use "Likely benign": Claude 1,065/5,000 (21.3%), Gemini 646/5,000 (12.9%), GPT 591/5,000 (11.8%). Strikingly, **not one foreign model emitted "Likely pathogenic" (0/15,000 calls)** — strength information survives only on the benign side, while the pathogenic side polarizes to full "Pathogenic" in every ecosystem. The five-class collapse is therefore asymmetric and partially ecosystem-dependent, with direct consequences for clinical workflows that distinguish Pathogenic from Likely pathogenic follow-up.

> Note: foreign-model results are obtained via an OpenAI-compatible relay with a research-context system prompt (disclosed in Methods and Limitations); a prompt-robustness check is reported below.

### Prompt-asymmetry robustness check (full-scale, n = 5,000)

Qwen3.7-max was re-evaluated on the complete test set with the same system prompt used for international models. The prompt shifts Qwen conservative: accuracy 71.6-to-65.5% (-6.2 pp), abstention +8.1 pp, FP 4.7-to-1.0%. Binary agreement 99.8% (5 direction changes out of 3,186 co-definitive variants). Under unified prompt: Gemini 76.5% (FP 27.8%), Claude 68.5% (FP 3.9%), Qwen 65.5% (FP 1.0%). The conservative/aggressive dichotomy persists; Qwen's original accuracy was slightly inflated relative to prompted international models.

## Discussion

### Principal findings

Under label-leakage control (temporal blinding of the gold-standard label), current-generation LLMs classify 62–72% of variants correctly (all-inclusive), rising to 86–93% on expert-panel-reviewed variants. When conservative models commit to a call, they are right 97.8–98.7% of the time, mislabeling only 1.3–2.5% of Benign variants as Pathogenic; reasoning models, by contrast, mislabel 22–28% of Benign variants as Pathogenic — the clinically dangerous direction. An international extension (Gemini 3 Flash / GPT-5.6-terra / Claude Sonnet 5 at full scale) places Gemini first overall (76.5%) and shows the conservative/aggressive dichotomy spans ecosystems. These are substantially lower than unblinded expert-level reports [6]; interpreted as a reliability audit, they define the *operational envelope* in which an LLM output can be trusted rather than a ceiling on generalization: label memorization is controlled, and remaining performance reflects the evidence the model actually reasons with.

### Vendor choice matters more than ensemble size

The gap between best and worst model (+22.4 pp within the fully blinded domestic panel; up to +27.3 pp across the full nine-model set — not cutoff-controlled for the international models; +25 pp expert-panel) exceeds any ensemble gain we tested, and naive majority voting *reduced* accuracy below the best single model because conservative voters dominate ties. Two implications: (i) published “LLM accuracy” without model identity is meaningless; (ii) clinical deployments should select models on blinded benchmarks, not ensemble size. The recommendation is model-specific: Kimi and Qwen excel on evidence-rich variants, while reasoning models (V4-pro, MiMo) commit more often but less reliably. The international extension sharpens this: Gemini leads the full set (76.5%) but with 27.8% FP, Claude pairs 97.0% conditional with 3.9% FP; under full blinding the ranking collapses to a tie and camp assignment shifts (Gemini's aggressive profile dissolves, FP 5.2%; GPT-5.6-terra becomes the aggressive outlier) — detectable only by blinded, repeated evaluation (Table S4). Behavior style — not vendor, nationality, or price tier — is the operative selection criterion.

### Abstention is calibrated behavior, not conservatism

Three experiments converge: models abstain more when evidence is missing (AF ablation: chat abstention falls 90%→31% on gold-standard Benign variants once allele frequencies are provided), when experts disagree (conflicting variants: +22–39 pp abstention without being told), and when the task has no clinical evidence (MaveDB: 73–93%). Abstention is thus a **trustworthy triage signal** — "the model said Uncertain, therefore review by a human" is safe, and models are disproportionately Uncertain precisely when human review is needed.

### Reproducibility as a reliability property

At temperature 0, chat-style models are exactly reproducible (100% over 50 re-runs), but the reasoning model V4-pro changed its binary output on 60% of 200 re-run variants (half unparseable), including direct Benign↔Pathogenic flips. Average accuracy alone cannot audit a model for clinical use: a non-deterministic model cannot be deployed regardless of mean performance, and single-run accuracies of such models are themselves noisy. Determinism, like accuracy and abstention calibration, is a measured property we report per model rather than assume.

### The information-deficit explanation of Benign underperformance

The most striking baseline result — Benign sensitivity of 8.7–63.2% across the nine models without AF — is largely explained by missing allele-frequency evidence. With AF provided, Benign sensitivity rises by up to +60.1 pp. ACMG rules BA1/BS1 (population frequency) are among the strongest Benign evidence; omitting them cripples the Benign side of the classification. Practical implication: any LLM-based variant interpretation pipeline must integrate population-frequency databases; performance numbers reported without AF are systematically pessimistic about Benign recall.

### Relation to prior work

AI-CURA [6] demonstrated expert-consistency without leakage control; our label-blinded numbers (62–72% domestic, 60–77% including international) suggest that a substantial part of unblinded performance may be label memorization. VariantBench [8] and VarLitBench [9] advance evaluation rigor — justifications and ClinGen-anchored evidence, respectively — but neither temporally blinds the gold standard nor spans vendors; we add both, plus independent expert-panel validation. Our conditional-accuracy framing (speak vs. abstain) reconciles the "impressive when confident" and "unusable overall" observations in prior reports. Positioning: whereas AI-CURA asks "can LLMs classify variants?", we ask "under which auditable conditions can an LLM's classification be trusted?" — the audit framing keeps our claims within what temporal blinding can actually establish.

### Limitations

(i) Vendor panel is dominated by Chinese-commercial models (6/9); while Gemini, GPT, and Claude provide cross-ecosystem evidence, the majority of the 45,000 evaluations are domestic, limiting full generalization.
(ii) **Cutoff overlap for international models**: Claude Sonnet 5, GPT-5.6-terra, and Gemini 3 Flash have training cutoffs of 2026-01 to 2026-03, so the 2026-01–2026-03 portion of the main test set (41.9–81.9% depending on model) is not label-blinded for them. Two fully blinded controls address this — the main-set ≥ 2026-04 stratum (n = 907) and a dedicated balanced set (n = 2,000) — both showing that Gemini’s full-set lead and aggressive profile do not persist (Table S4). The two blinded runs also differ from each other for Gemini (FP 22.1% vs. 5.2%), consistent with relay non-determinism and possible version drift between sessions; international rankings should therefore be read as run-conditional.
(iii) Temporal blinding controls label-memorization specifically; a variant's *evidence* (literature, submissions) may predate its label date, so the model could still have encountered supporting evidence. The strength of this "evidence leakage channel" has not been quantified.
(iv) Binary P/B evaluation collapses ACMG's five classes and penalizes "Likely" mapping strategies; the five-class analysis shows this collapse is asymmetric (Likely pathogenic is never emitted).
(v) The MaveDB functional direction is a soft validation (loss-of-function ≠ pathogenicity for haploinsufficient genes); datasets are not temporally blinded.
(vi) Single task (germline SNV/indel); splice/de novo/structural/somatic variants unaddressed.
(vii) Population bias: ClinVar submissions and reference AF panels (ESP/ExAC/1000G) skew European-ancestry; Benign sensitivity estimates may not transfer equitably to non-European populations.
(viii) McNemar paired tests assume variant independence; gene-level clustering (2,050 genes, NF1 n=83) means tests are optimistic; cluster-bootstrap CIs are reported alongside and preserve all conclusions.
(ix) Prompt asymmetry: international models received a research-context system prompt that domestic models did not; robustness check shows the conservative/aggressive dichotomy is unaffected (Qwen's accuracy shifts −6.2 pp under the unified prompt, but its conservative-camp behavior persists: FP 1.0%, conditional accuracy 98.9%), but the caveat remains.
(x) Conditional accuracy compares models with very different abstention rates (9.2% vs 49.9%); different denominator sizes can obscure direct comparison (Simpson's paradox risk).
(xi) No comprehensive comparison with non-ML variant effect predictors (AlphaMissense, REVEL, CADD, InterVar). The available AlphaMissense release is transcript-level hg38, and only a small minority of test-set variants could be matched directly (most ClinVar annotations are hg19/GRCh37), preventing a head-to-head comparison on a usable subset; a liftover-based comparison is in preparation.

### Conclusion

Under label-leakage control, LLM variant interpretation passes reliability audit under three conditions: the model is chosen on blinded evidence (vendor gap up to +22 pp among fully blinded domestic models; majority voting can hurt), complete evidence is provided (AF mandatory; up to +60 pp Benign sensitivity), and abstention is deployed as a human-review trigger. We recommend that (i) published accuracies report model identity, blinding status, and evidence conditions; (ii) clinical pilots adopt "Pathogenic calls auto-flag, Uncertain calls auto-escalate" policies; and (iii) future audits extend to more vendors and task types.

---

## Materials and Methods

### Data sources

- **ClinVar variant_summary** (Aug 2026 release; 9,029,235 rows; 43 columns), used for test-set construction and gold-standard labels.
- **ClinVar VCF (GRCh38)** (clinvar.vcf.gz; ~193 MB), used to attach population allele frequencies (AF_ESP/AF_EXAC/AF_TGP) by ALLELEID.
- **MaveDB** [13] (Ensembl-mapped release; 3,158,202 scored variants), for the functional-effect experiment; gene symbols via mygene.info [14].
- All data are public (URLs in Data Availability).

### Temporally blinded test set (label-leakage control)

The central design decision: LLM training corpora contain ClinVar history, so evaluation must use variants whose **gold-standard labels** were produced **after** the model training cutoff. This controls the label-memorization channel specifically; prior *evidence* (literature, submissions) may still be present in training data, and we therefore frame the study as a reliability audit under controlled label leakage rather than a generalization test (see Discussion).

- Model cutoffs (verified 2026-08): six domestic models ≤ 2025 (DeepSeek V4 ~Dec 2025; Kimi ~2025-01; Qwen/MiMo ≤ 2025-05). International cutoffs: Claude Sonnet 5 ~2026-01, GPT-5.6-terra ~2026-02-16, Gemini Flash model ~2026-03. The relay identifier is gemini-3-flash; Google's Flash line spans 3.5–3.8 (official cutoffs 2025-01–2026-03), the relay does not expose the served version, and cutoff-sensitive analyses conservatively assume the latest (≈2026-03) — the most blinding-demanding assumption.
- We require **LastEvaluated ≥ 2026-01-01**, fully blinding the six domestic models. For international models, labels evaluated 2026-01–2026-03 may fall at or before their cutoffs (Claude 2,097 variants, 41.9%; GPT at most 3,769, 75.4% — cutoff mid-February, so true exposure is lower; Gemini 4,093, 81.9%). International results are therefore reported on the full set, on the in-set fully blinded stratum (≥ 2026-04, n = 907), and on a **dedicated fully blinded set** — 2,000 variants (1,000 P / 1,000 B; seed 42; eligible ≥ 2026-04 pool 4,772: P 2,611 / B 2,161; 342 overlap with the main set), identical prompts, single session (International extension, Table S4).
- Eligibility: unambiguous clinical classification (Pathogenic or Benign only; "Likely" and compound terms excluded from the P/B gold standard), a HGVS name, and no conflicting classification.
- De-duplication by ALLELEID (one row per allele): removes 49.6% of raw rows (9,029,235 → 4,548,781 unique alleles).
- Stratified sampling: 2,500 P-side + 2,500 Benign, seed 42 (reproducible), n = 5,000 (2,499 strict Pathogenic + 1 compound P-side label excluded as unevaluable; 4,999 unambiguous P/B).
- Result: all 5,000 variants were last evaluated 2026-01–2026-07 (Jan 2,097 / Feb 1,672 / Mar 324 / Apr 412 / May 263 / Jun 199 / Jul 33) — after every domestic training cutoff, so these labels were unseen in training; the international models' partial overlap is quantified above and controlled by the fully blinded designs.

### Gold standards

- **Primary**: ClinVar aggregate classification (Pathogenic/Benign binary). - Unparseable/empty outputs recorded as parse failures and counted as errors (0.04-0.60% across models; see Models section for per-model detail). The binary gold standard inherits ClinVar label noise; mitigated by expert-panel stratification and temporal filtering. "Likely" classes were excluded from the binary gold standard but occur in model outputs; the VUS-as-error convention penalizes models that map "Likely" outputs to Uncertain.
- **Gold standard A (expert panel)**: ReviewStatus ∈ {reviewed by expert panel, practice guideline} — classifications produced by ClinGen variant-curation expert panels / guideline committees. Dedicated validation set: 900 such variants (P-side 645: Pathogenic 303 + Likely pathogenic 342; B-side 252: Benign 59 + Likely benign 193; 3 compound P/LP labels excluded as unevaluable; all ≥ 2026-01). Of these, 100 were also sampled into the main test set (Table 1, expert-panel stratum); the dedicated-set analysis therefore reports **800 exclusive variants (797 evaluable)** for strict independence, with the full 900 as a robustness check. Gold standard A (broad): expert-panel ∪ {multiple submitters, no conflicts}.
- **Triangulation sets**: conflicting-interpretation variants (44,815 candidates; 300 sampled) and MaveDB functional extremes (150 loss-of-function: score ≤ −0.8; 150 normal: score ≥ 0.5).

### Models

Nine models from seven vendors (DeepSeek models: DeepSeek-AI [15]; Kimi: Kimi Team [16]; Qwen: Yang et al. [17]; MiMo: Xiaomi [18]), all accessed through OpenAI-compatible APIs (temperature 0, max_tokens 8,192 for reasoning-family models):

| Model | Vendor | Type | API endpoint |
|---|---|---|---|
| DeepSeek V4-pro | DeepSeek | reasoning, 1.6T/49B active | api.deepseek.com |
| DeepSeek chat (V3) | DeepSeek | chat | api.deepseek.com |
| DeepSeek coder (V3) | DeepSeek | code | api.deepseek.com |
| Kimi-K2.6 | Moonshot | chat | Alibaba Model Studio gateway |
| MiMo V2.5 Pro | Xiaomi | reasoning, 310B/15B active | xiaomimimo.com |
| Qwen3.7-max | Alibaba | reasoning | Alibaba Model Studio (dedicated instance) |
| Gemini 3 Flash | Google (US) | reasoning | relay via ai.flashapi.top |
| GPT-5.6-terra | OpenAI (US) | reasoning | relay via ai.flashapi.top |
| Claude Sonnet 5 | Anthropic (US) | chat | relay via ai.flashapi.top |

Six domestic models were selected a priori as the current generation of widely used Chinese commercial LLMs (previous-generation DeepSeek models serve as an intra-vendor generation control). Three foreign flagships were additionally evaluated on the complete test set (identical variants and prompts): **Gemini 3 Flash (Google), GPT-5.6-terra (OpenAI), Claude Sonnet 5 (Anthropic)**, via an OpenAI-compatible relay (temperature 0, max_tokens 16,384). Because Claude refused 5 of 20 pilot queries (25%, medical-safety policy; archived runner script), all three received a research-benchmark system prompt ("classifications are research outputs, not clinical advice"); refusals then dropped to 0%. Domestic models received no system prompt; this asymmetry is disclosed as a limitation. Model names are the relay-exposed identifiers (gemini-3-flash, gpt-5.6-terra, claude-sonnet-5; all international calls 2026-08); relay-served versions cannot be verified against vendor channels, and we report the identifiers verbatim.

### Prompt design

Each variant was presented as a clinical-geneticist task: HGVS name, gene symbol, coordinates, cDNA/protein change (when available), and — in the AF condition — population allele frequencies (AF_ESP/ExAC/1000G). The model had to return strict JSON: {classification ∈ five ACMG classes, acmg_rules, confidence ∈ [0,1], evidence_summary, references}. The prompt contained **no** ClinVar significance label, review status, or conflict hint. Outputs were parsed leniently (fenced JSON, single quotes, trailing prose). Parse failures (empty or unparseable) were counted as errors in the all-inclusive metric; rates: V4-pro 0.60% (26 empty, 4 truncated), MiMo 0.10% (incl. 3 content-filter rejections), Kimi/Qwen ≤ 0.08%.

### Evaluation metrics

- **All-inclusive accuracy**: binary P/B match on the gold standard, with VUS (and unparseable) counted as errors — the clinical-usability view.
- **Conditional accuracy**: accuracy restricted to committed calls (P or B) — the reliability-of-expression view.
- **Abstention rate**: fraction of VUS outputs.
- **Confusion matrix** on the P/B gold standard; sensitivity/specificity per model.
- **Consensus**: majority vote across models on the three-way (P/B/VUS) semantics — semantically close classes (e.g., Pathogenic vs. Likely pathogenic) do not split votes; ties excluded (reported separately).
- Expert-panel stratification (gold A strict/broad) applied to every model and the consensus.
- **Statistics**: Wilson 95% confidence intervals for all accuracies; McNemar's paired test (normal approximation with continuity correction, n > 30) for model comparisons on the shared variant set; consensus vs. best-single-model compared descriptively. Because variants cluster by gene (2,050 genes across 5,000 variants; 3,952 variants in multi-variant genes, max NF1 n=83), we additionally computed gene-level cluster-bootstrap 95% CIs (1,000 resamples); these widen the Wilson intervals by 1.6–2.4× (mean ≈1.9×) without changing any between-model conclusion (archived computation in the repository). Model-output determinism checked by re-running 50 variants per model (temperature 0; five models completed) and, at larger scale, 200 variants per model, measuring classification agreement.

### Sub-experiments

1. **AF ablation (n = 400 × 3)**: identical variants/models/prompts, with vs. without the allele-frequency block.
2. **Conflicting variants (n = 300 × 2)**: same pipeline on variants with conflicting expert classifications; gold standard absent by construction — we analyze abstention behavior and call distributions.
3. **MaveDB functional task (n = 300 × 2)**: consistency between the model's call (P vs B) and the experimental functional direction (loss-of-function vs normal) on variants with no clinical evidence. The sample includes 286 unique variants (14 replicate rows); all statistics are unchanged under de-duplication.

### Reproducibility

All scripts, prompts, seeds, and every intermediate file needed to reproduce the reported numbers are public in the project repository (see Data availability); the full ClinVar snapshot is regenerated from the public FTP release by the provided scripts. Sampling uses fixed seed 42; all API calls use temperature 0. Analysis code uses only the Python 3 standard library (no ML dependencies).

## Ethics statement

This study used only publicly available database records (ClinVar, ClinGen-derived
review statuses, and MaveDB). No human participants, patient material, or personal
data were involved; institutional review board approval was not required.

## Data availability

All source data are publicly available: ClinVar variant_summary and VCF
(https://ftp.ncbi.nlm.nih.gov/pub/clinvar/), MaveDB Ensembl-mapped release
(https://ftp.ensembl.org/pub/current_variation/MaveDB/), and mygene.info. The
temporally blinded test sets, gold standards, all 45,000 raw model outputs (four
rows failed on relay/network errors and, per the all-inclusive convention, are
counted as errors rather than excluded), the dedicated fully blinded set and its 6,000 raw outputs,
and analysis scripts are available at https://github.com/zksdu/llm-acmg-variant-audit
(archived on Zenodo, DOI: 10.5281/zenodo.22299737).

## Code availability

Custom analysis code is available at https://github.com/zksdu/llm-acmg-variant-audit
(archived on Zenodo, DOI: 10.5281/zenodo.22299737). The pipeline uses the Python 3 standard library only;
sampling is byte-reproducible at seed 42.

## CRediT authorship contribution statement

**Bing Song:** Conceptualization, Investigation, Data curation, Validation,
Writing – original draft.
**Kai Zhang:** Methodology, Software, Formal analysis, Visualization,
Supervision, Writing – review & editing. All authors read and approved the
final manuscript.

## Conflict of interest

The authors declare that they have no conflict of interest.

## AI use declaration

During the preparation of this work the authors used an AI language model (GLM, Z.ai) to assist with drafting, language editing, and analysis-code development. After using this tool, the authors reviewed and edited the content as needed and take full responsibility for the content of the published article.

## Acknowledgments

Not applicable.

## References

[1] Richards S, Aziz N, Bale S, Bick D, Das S, Gastier-Foster J, et al. Standards and guidelines for the interpretation of sequence variants: a joint consensus recommendation of the American College of Medical Genetics and Genomics and the Association for Molecular Pathology. Genetics in Medicine. 2015;17(5):405-424. doi:10.1038/gim.2015.30
[2] Rehm HL, Berg JS, Brooks LD, Bustamante CD, Evans JP, Landrum MJ, et al. ClinGen — The Clinical Genome Resource. New England Journal of Medicine. 2015;372(23):2235-2242. doi:10.1056/NEJMsr1406261
[3] Landrum MJ, Chitipiralla S, Brown GR, Chen C, Gu B, Hart J, et al. ClinVar: improvements to accessing data. Nucleic Acids Research. 2020;48(D1):D835-D844. doi:10.1093/nar/gkz972
[4] Karczewski KJ, Francioli LC, Tiao G, Cummings BB, Alföldi J, Wang Q, et al. The mutational constraint spectrum quantified from variation in 141,456 humans. Nature. 2020;581(7809):434-443. doi:10.1038/s41586-020-2308-7
[5] Cheng J, Novati G, Pan J, Bycroft C, Žemgulytė A, Applebaum T, et al. Accurate proteome-wide missense variant effect prediction with AlphaMissense. Science. 2023;381(6664):eadg7492. doi:10.1126/science.adg7492
[6] Ma W, Fong G, Lai J, Wu H, Hue SPY, Ying D, et al. AI-CURA, an automated LLM workflow for high-accuracy genetic variant classification. Science Translational Medicine. 2026;18(855):eadz4172. doi:10.1126/scitranslmed.adz4172
[7] Lin K, Kao T, Wang L, Kuo C, Chen PC, Chu Y, et al. Benchmarking large language models GPT-4o, llama 3.1, and qwen 2.5 for cancer genetic variant classification. npj Precision Oncology. 2025;9(1):141. doi:10.1038/s41698-025-00935-4
[8] Basharat H, Plotkin S, Le C, Zhu K, Pink M, Alfaro I. VariantBench: a framework for evaluating LLMs on justifications for genetic variant interpretation. In: Proceedings of the 9th International Joint Conference on Natural Language Processing and the 21st Conference of the Asia-Pacific Chapter of the Association for Computational Linguistics (SRW). Mumbai: ACL; 2025. https://aclanthology.org/2025.ijcnlp-srw.26/
[9] Saadat A, Fellay J. Large Language Models for Variant-Centric Functional Evidence Mining. arXiv:2604.00075 [preprint]. 2026.
[10] Sainz O, Campos JA, García-Ferrero I, Etxaniz J, Lacalle OLd, Agirre E. NLP Evaluation in trouble: On the Need to Measure LLM Data Contamination for each Benchmark. arXiv:2310.18018 [preprint]. 2023.
[11] Bordt S, Srinivas S, Boreiko V, von Luxburg U. How much can we forget about data contamination? In: Proceedings of the 42nd International Conference on Machine Learning (ICML 2025). 2025. https://openreview.net/forum?id=Pf0PaYS9KG
[12] Golchin S, Surdeanu M. Time Travel in LLMs: Tracing Data Contamination in Large Language Models. arXiv:2308.08493 [preprint]. 2023.
[13] Esposito D, Weile J, Shendure J, Starita LM, Papenfuss AT, Roth FP, et al. MaveDB: an open-source platform to distribute and interpret data from multiplexed assays of variant effect. Genome Biology. 2019;20(1):223. doi:10.1186/s13059-019-1845-6
[14] Wu C, MacLeod I, Su AI. BioGPS and MyGene.info: organizing online, gene-centric information. Nucleic Acids Research. 2013;41(D1):D561-D565. doi:10.1093/nar/gks1114
[15] DeepSeek-AI. DeepSeek-V3 technical report. arXiv:2412.19437 [preprint]. 2024.
[16] Kimi Team. Kimi K2: open agentic intelligence. arXiv:2507.20534 [preprint]. 2025.
[17] Yang A, Li A, Yang B, Zhang B, Hui B, Gao B, et al. Qwen3 technical report. arXiv:2505.09388 [preprint]. 2025.
[18] Xiaomi. MiMo API documentation [Internet]. Beijing: Xiaomi; 2026. Available from: https://mimo.mi.com

## Figure legends

**Fig. 1. Multi-model performance on the temporally blinded test set.**
A: Dual-metric accuracy for all nine models on the complete test set (n = 4,999 evaluable variants per model); all-inclusive accuracy (VUS counted as errors; Wilson 95% CI error bars) and conditional accuracy (committed calls only). International models shown with white fill and outline.
B: Benign-to-Pathogenic false-positive rates (log scale) with 95% CI.

**Fig. 2. Evidence availability governs reliability.**
A: Allele-frequency ablation on a Benign-rich subset (400 variants × 9 models; the 356 gold-standard Benign variants shown):
Benign sensitivity without vs. with population AF. B: The ablation on a
Pathogenic-enriched subset (n = 150 × 2). C: Abstention across evidence contexts:
with vs. without AF, main set vs. conflicting-interpretation variants, and the
no-evidence MaveDB task.

**Fig. 3. Output determinism and the collapse of the "Likely" tier.**
A: Re-run agreement at temperature 0 (n = 200 variants per model; international
models included). B: Output distribution for gold-standard Likely pathogenic and Likely
benign variants (Kimi, expert set): strength information polarizes to Pathogenic or
Benign; cross-ecosystem counts in text.

**Fig. 4. Fate of gold-standard Benign variants across the nine models.**
For each model, the share of the 2,500 gold-standard Benign variants that is
correctly called Benign (blue), abstained as VUS (grey), or misclassified as
Pathogenic (magenta) — the clinically dangerous direction. Conservative and
aggressive camps separate sharply on the magenta segment.

**Fig. 5. Behavioral dashboard of the nine models.**
Six audited dimensions per model (all-inclusive, conditional, expert-panel, abstention, Benign-to-Pathogenic FP, spoken rate), color-coded 0-100; the dashboard summarizes the audit and supports model selection.

### Supplementary material

- **Table S1.** Re-run consistency (n = 50 variants per model; temperature 0).
- **Table S2.** Nine-model comparison on the complete test set (n = 5,000 per model).
- **Table S3.** Expert-panel validation (n = 797 exclusive variants; 5 models).
- **Table S4.** Dedicated fully blinded set, LastEvaluated ≥ 2026-04 (n = 2,000; three international models, single session).
