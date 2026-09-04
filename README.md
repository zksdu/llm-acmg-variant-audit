# LLM Variant Classification Reliability Audit

**Multi-vendor evaluation of large language models for ACMG/AMP variant classification with controlled data contamination**

> Companion repository for the manuscript submitted to *Journal of Genetics and Genomics* (JGG).

---

## Overview

This study audits the reliability of 9 large language models (6 Chinese + 3 international) for ACMG/AMP germline variant classification, using **temporal blinding** to control for training-data leakage from ClinVar.

### Key Findings

| Finding | Detail |
|---|---|
| **Scale** | 5,000 variants x 9 models = 45,000 evaluations |
| **All-inclusive accuracy** | 61.8% (DeepSeek V4-pro) to 76.5% (Gemini 3 Flash) |
| **Conditional accuracy** | 81.2% (V4-pro) to 98.7% (DeepSeek coder) |
| **False Pathogenic rate** | 1.3% (chat/coder) to 28.4% (V4-pro) |
| **AF evidence effect** | Benign sensitivity up to +60.1 pp when provided |
| **Consensus voting** | 98.3% conditional accuracy (n=2,915) |

---

## Repository Structure

```
github_submission/
├── README.md                          # This file
├── LICENSE                            # CC-BY-NC 4.0
├── .gitignore
│
├── manuscript/                        # Paper text
│   └── manuscript_JGG.md              # Submission manuscript (English, canonical)
│
├── figures/                           # Publication figures (5 main)
│   ├── fig1.pdf/png/tiff              # Nine-model dual-metric performance + FP
│   ├── fig2.pdf/png/tiff              # Evidence availability (AF ablation)
│   ├── fig3.pdf/png/tiff              # Determinism + "Likely" tier collapse
│   ├── fig4.pdf/png/tiff              # Fate of gold-standard Benign variants
│   └── fig5.pdf/png/tiff              # Behavioral dashboard (6 dimensions)
│
├── data/                              # Key datasets & analysis results
│   ├── clinvar_testset_temporal.csv   # 5,000-variant temporal test set (main)
│   ├── variant_classification_results_all.csv  # ALL 45,000 raw model outputs
│   ├── variant_classification_results_foreign.csv  # Intl-model batch (15,000)
│   ├── expert_panel_candidates.csv    # 900 expert-panel gold-standard variants
│   ├── expert_panel_exclusive_800.csv # 800 exclusive validation variants
│   ├── expert_panel_results.csv       # Expert-panel outputs, domestic (5-class)
│   ├── expert_panel_intl_exclusive.csv # Expert-panel outputs, international
│   ├── clinvar_testset_af[_only].csv  # AF-ablation test sets (400-variant)
│   ├── af_p_only.csv + af_p_results_on.csv  # AF P-subset (150 × 2)
│   ├── af_*_results.csv               # AF-ablation raw outputs (4 batches)
│   ├── experiment_results_all6.csv + variant_classification_results_*.csv
│   │                                  # Per-model intermediate results
│   ├── conflicting_sample_300.csv + conflicting_results.csv
│   ├── mavedb_testset.csv + mavedb_results.csv
│   ├── blinded2000_set.csv + blinded2000_results.csv  # Dedicated fully
│   │                                  # blinded set (2,000) + 6,000 outputs
│   ├── blinded2000_analysis.md        # Dedicated-set analysis (Table S4)
│   ├── prompt_sym_qwen_5000.csv       # Prompt-symmetry robustness check
│   ├── determ_200*.csv                # Determinism test sets + re-run outputs
│   ├── consistency_50.csv + consistency_results.csv
│   ├── ep_determ_intl_results.csv     # International determinism re-runs
│   ├── alphamissense_matched.csv      # AlphaMissense comparison subset
│   ├── bootstrap_gene_analysis.md    # Gene-level cluster-bootstrap CIs
│   ├── surface_cue_analysis.md       # LoF surface-cue stratification
│   └── *_analysis.md                  # Sub-experiment analysis reports

Verified: `python scripts/generate_figures_v2.py` runs end-to-end inside this
repository and reproduces all five publication figures byte-identically.
│
├── scripts/                           # Reproducible analysis code
│   ├── preprocess_clinvar.py          # ClinVar data extraction & filtering
│   ├── sample_clinvar_testset.py      # Temporal test set construction
│   ├── rebuild_temporal.py            # Test set temporal rebuild
│   ├── run_variant_classification.py  # Main experiment runner (9 models)
│   ├── call_llm.py                    # Unified LLM API caller
│   ├── merge_results.py               # Multi-model result merging
│   ├── restore_alleleids.py           # AlleleID recovery from ClinVar
│   ├── annotate_af.py                 # gnomAD AF annotation
│   ├── match_alphamissense.py         # AlphaMissense pathogenicity matching
│   ├── mavedb_sample.py               # MaveDB variant sampling
│   ├── extract_conflicting.py         # Conflicting-interpretation extraction
│   ├── extract_expert_panel.py        # Expert-panel variant extraction
│   ├── analyze_consensus.py           # Consensus voting analysis
│   ├── statistics_analysis.py         # Core statistics computation
│   ├── cost_profiling.py              # API cost & latency profiling
│   ├── generate_figures_v2.py         # Publication figure generation (data-driven, byte-reproducible)
│   ├── build_docx.py                  # DOCX manuscript builder
│   ├── build_docx_cn.py               # Chinese DOCX builder
│   └── download_segments.py           # UCSC genome browser segment download
│
└── supplementary/                     # Supplementary materials
    └── submission_package.md          # Submission checklist & metadata
```

---

## Reproducing the Analysis

### Prerequisites

- Python 3.12+
- Packages: `pandas`, `numpy`, `scipy`, `matplotlib`, `seaborn`, `requests`, `openpyxl`
- API keys for the 9 LLMs (see `scripts/call_llm.py` for configuration)

### Quick Start

```bash
# 1. Build the temporally-blinded test set from ClinVar
python scripts/preprocess_clinvar.py
python scripts/sample_clinvar_testset.py

# 2. Run variant classification (requires API keys)
python scripts/run_variant_classification.py

# 3. Analyze results
python scripts/statistics_analysis.py
python scripts/analyze_consensus.py

# 4. Generate figures
python scripts/generate_figures_v2.py

# 5. Verification suite (no network needed)
python scripts/final_gate.py          # 101 submission assertions
python scripts/table_cell_audit.py    # docx tables vs. raw data
python scripts/fig_geom_check.py      # figure legend-overlap / text-spill check
```

---

## Models Evaluated

| Model | Vendor | Type | Test Set Size |
|---|---|---|---|
| Qwen3.7-max | Alibaba | Flagship | 5,000 |
| Kimi-K2.6 | Moonshot | Flagship | 5,000 |
| MiMo V2.5 Pro | Xiaomi | Reasoning | 5,000 |
| DeepSeek V4-pro | DeepSeek | Reasoning | 5,000 |
| DeepSeek chat | DeepSeek | Conservative | 5,000 |
| DeepSeek coder | DeepSeek | Conservative | 5,000 |
| Claude Sonnet 5 | Anthropic | Flagship | 5,000 |
| Gemini 3 Flash | Google | Flagship | 5,000 |
| GPT-5.6-terra | OpenAI | Flagship | 5,000 |

---

## Data Availability

- **ClinVar**: [https://www.ncbi.nlm.nih.gov/clinvar/](https://www.ncbi.nlm.nih.gov/clinvar/)
- **gnomAD**: [https://gnomad.broadinstitute.org/](https://gnomad.broadinstitute.org/)
- **AlphaMissense**: [https://github.com/google-deepmind/alphamissense](https://github.com/google-deepmind/alphamissense)
- **MaveDB**: [https://www.mavedb.org/](https://www.mavedb.org/)

The temporally-blinded test set (5,000 variants with LastEvaluated >= 2026-01) is provided in `data/clinvar_testset_temporal.csv`.

---

## Citation

If you use this code or data, please cite:

> Multi-vendor evaluation of large language models for ACMG/AMP variant classification with controlled data contamination. *Journal of Genetics and Genomics* (2026).

---

## License

This project is licensed under the **Creative Commons Attribution-NonCommercial 4.0 International License** (CC BY-NC 4.0). See [LICENSE](LICENSE) for details.

---

## Contact

For questions about the code or data, please open an issue on this repository.
