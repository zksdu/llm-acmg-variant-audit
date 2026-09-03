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
| **AF evidence effect** | Benign sensitivity +57.8 pp when provided |
| **Consensus voting** | 98.4% conditional accuracy (n=2,911) |

---

## Repository Structure

```
github_submission/
├── README.md                          # This file
├── LICENSE                            # CC-BY-NC 4.0
├── .gitignore
│
├── manuscript/                        # Paper text
│   ├── manuscript_JGG.md              # JGG submission version (English)
│   └── manuscript_draft_EN.md         # Full English draft with all sections
│
├── figures/                           # Publication figures
│   ├── fig1.pdf/png/tiff              # Model performance comparison
│   ├── fig2.pdf/png/tiff              # Evidence gradient analysis
│   ├── fig3.pdf/png/tiff              # AF ablation study
│   ├── fig4.pdf/png/tiff              # Cost-latency profiling
│   ├── fig5.pdf/png/tiff              # Determinism analysis
│   └── jgg/                           # JGG-format figures (4 panels)
│       ├── fig1_JGG.pdf/png/tiff
│       ├── fig2_JGG.pdf/png/tiff
│       ├── fig3_JGG.pdf/png/tiff
│       └── fig4_JGG.pdf/png/tiff
│
├── data/                              # Key datasets & analysis results
│   ├── clinvar_testset_temporal.csv   # 5,000-variant temporal test set
│   ├── experiment_results_variant.csv # Main experiment results (9 models)
│   ├── determ_200.csv                 # Determinism test (200 variants x 3 runs)
│   ├── conflicting_sample_300.csv     # Conflicting-interpretation variants
│   ├── mavedb_testset.csv             # MaveDB functional-effect variants
│   ├── consistency_50.csv             # Within-session consistency
│   ├── statistics_analysis.md         # Statistical analysis report
│   ├── fiveclass_analysis.md          # 5-class boundary analysis
│   ├── cost_profiling.md              # API cost & latency profiling
│   ├── consensus_analysis.md          # Multi-model consensus analysis
│   ├── conflicting_analysis.md        # Conflicting variants analysis
│   └── mavedb_analysis.md             # MaveDB sub-experiment analysis
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
│   ├── generate_figures.py            # Original figure generation
│   ├── generate_figures_v2.py         # Revised figure generation (v2)
│   ├── generate_figures_jgg.py        # JGG-format figure generation
│   ├── build_jgg.py                   # JGG manuscript builder
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
