# Submission Package — Title Page, Declarations, Cover Letter（GPB 终版 2026-09-04）

> ⚠️ 本文件为 GPB Editorial Manager 投稿时逐字复制用的唯一权威版本。
> 权威正文：docs/manuscript_GPB.md / docs/submission_GPB.docx
> 投稿图（5 张）：docs/figures_v2/fig1-fig5（.tiff/.pdf/.png）
> 代码仓库：https://github.com/zksdu/llm-acmg-variant-audit（Zenodo DOI: 10.5281/zenodo.22637274）

---

## Title Page

**Title:** Multi-vendor evaluation of large language models for ACMG/AMP variant classification with controlled data contamination

**Running title (≤50 chars):** Multi-vendor LLM Variant Classification

**Authors:** Bing Song¹, Kai Zhang²,*

**Affiliations:**
¹ The Third Affiliated Hospital of Guangzhou Medical University, Guangzhou, Guangdong, China
² Guangdong Communication Polytechnic, Guangzhou, Guangdong, China

**Corresponding author:** Kai Zhang
E-mail: zhangkai@gdcp.edu.cn

**Keywords (6):** variant classification; ACMG/AMP; large language models; data leakage; ClinVar; temporal blinding

---

## Abstract

Large language models (LLMs) are increasingly proposed for ACMG/AMP variant classification, but their training corpora include public variant databases, so reported accuracy may reflect label memorization rather than reasoning. We audited nine LLMs (six Chinese, three international flagships; 45,000 evaluations) on 5,000 ClinVar variants whose gold-standard labels postdate every model's training cutoff (temporal blinding), with independent validation on 900 expert-panel-curated variants. Under blinding, current-generation models achieved 61.8–71.6% all-inclusive accuracy (86–93% on expert-panel variants); conservative models reached 97.8–98.7% conditional accuracy with 1.3–2.5% Benign-to-Pathogenic false-positive rates, whereas reasoning models mislabeled 22–28% of Benign variants as Pathogenic. Adding allele-frequency evidence raised Benign sensitivity by up to 60.1 percentage points. On a dedicated fully blinded set (n = 2,000), Gemini and Claude were statistically indistinguishable (81.4% vs. 80.2%), while GPT-5.6-terra fell to 64.7% with 25.0% false positives. LLM variant interpretation is trustworthy only under blinded model selection, complete evidence provision, and abstention-as-human-review policies. All data and analysis code are archived at Zenodo (DOI: 10.5281/zenodo.22637274).

---

## Declarations（与正文一致，逐字复制）

**Ethics statement.** This study used only publicly available database records (ClinVar, ClinGen-derived review statuses, and MaveDB). No human participants, patient material, or personal data were involved; institutional review board approval was not required.

**Data availability.** All source data are publicly available: ClinVar variant_summary and VCF (https://ftp.ncbi.nlm.nih.gov/pub/clinvar/), MaveDB Ensembl-mapped release (https://ftp.ensembl.org/pub/current_variation/MaveDB/), and mygene.info. The temporally blinded test sets, gold standards, all 45,000 raw model outputs (four rows failed on relay/network errors and, per the all-inclusive convention, are counted as errors rather than excluded), the dedicated fully blinded set and its 6,000 raw outputs, and analysis scripts are available at https://github.com/zksdu/llm-acmg-variant-audit (archived on Zenodo, DOI: 10.5281/zenodo.22637274).

**Code availability.** Custom analysis code is available at https://github.com/zksdu/llm-acmg-variant-audit (archived on Zenodo, DOI: 10.5281/zenodo.22637274). The pipeline uses the Python 3 standard library only; sampling is byte-reproducible at seed 42.

**CRediT authorship contribution statement.** Bing Song: Conceptualization, Investigation, Data curation, Validation, Writing – original draft. Kai Zhang: Methodology, Software, Formal analysis, Visualization, Supervision, Writing – review & editing. All authors read and approved the final manuscript.

**Conflict of interest.** The authors declare that they have no conflict of interest.

**AI use declaration.** During the preparation of this work the authors used an AI language model (GLM, Z.ai) to assist with drafting, language editing, and analysis-code development. After using this tool, the authors reviewed and edited the content as needed and take full responsibility for the content of the published article.

**Acknowledgments.** Not applicable.

---

## Cover Letter（EM 上传文件或粘贴）

Dear Editor-in-Chief,

We are pleased to submit our manuscript, "Multi-vendor evaluation of large language models for ACMG/AMP variant classification with controlled data contamination," for consideration as a Research Article in Genomics, Proteomics & Bioinformatics.

LLMs are increasingly proposed for clinical variant interpretation, with recent reports of near-expert agreement. However, training corpora include public variant databases, so these scores may partly reflect memorization of gold-standard labels. Our study combines three controls that no prior variant-classification evaluation has combined: temporal label blinding (5,000 ClinVar variants assessed strictly after every model's training cutoff), multi-vendor coverage (nine models across seven vendors, including Gemini, GPT, and Claude; 45,000 evaluations), and independent ClinGen expert-panel validation. A dedicated fully blinded set (n = 2,000) additionally reorders the international ranking and places it on a statistically verified footing.

Our central findings are actionable: model choice dominates ensemble strategies (majority voting can reduce accuracy below the best single model); error direction differs sharply by model style (reasoning models mislabel 22–28% of Benign variants as Pathogenic, the clinically dangerous direction); evidence completeness governs reliability (allele-frequency provision raises Benign sensitivity by up to 60.1 percentage points); and abstention behaves as a calibrated, trustworthy triage signal for human review. All results, scripts, and sampling are fully reproducible from public data (github.com/zksdu/llm-acmg-variant-audit, archived with DOI 10.5281/zenodo.22637274).

This manuscript is original, has not been published previously, and is not under consideration elsewhere. All authors have approved the submission and declare no competing interests.

Thank you for your consideration.

Sincerely,
Kai Zhang (corresponding author), on behalf of all authors
Guangdong Communication Polytechnic, Guangzhou, Guangdong, China
E-mail: zhangkai@gdcp.edu.cn

---

## GPB EM 投稿填写映射（www.editorialmanager.com/gpb）

| 字段 | 填写内容 |
|---|---|
| Article Type | Research Article |
| Title | 与 Title Page 一致 |
| Running title | Multi-vendor LLM Variant Classification |
| Abstract | 上方 Abstract 全文（≤200 词，含存档 DOI） |
| Keywords | 上方 6 个，逐词添加 |
| Personal Keywords（若栏目存在） | variant classification / ACMG/AMP / large language model / ClinVar / artificial intelligence |
| Authors | 系统默认通讯 Kai Zhang；**手动添加 Bing Song 置顶**（The Third Affiliated Hospital of Guangzhou Medical University） |
| Classifications | Bioinformatics（子类 computational biology） |
| Funding | No specific funding |
| Conflict of Interest | No |
| Ethics | 上方 Ethics statement 全文 |

**上传文件（按序）**：`docs/submission_GPB.docx`（Manuscript）→ `docs/figures_v2/fig1.tiff` ~ `fig5.tiff`（Figure，600 dpi TIFF，PDF 备选）→ `docs/cover_letter_GPB.txt`（Cover Letter）。表格与图注均在 Manuscript 内，无需单独上传。

**Suggested Reviewers（选填）**：VariantBench 作者（Basharat 等）；Saadat & Fellay（EPFL, VarLitBench）；AI-CURA 团队（香港基因组研究所）。

---

## 合规自查（GPB 版）

| 项目 | 状态 |
|---|---|
| Research Article 正文（Introduction→Methods）<6,000 词 | ✅ ~5,900 |
| 摘要非结构化 ≤200 词（含数据 DOI 尾注） | ✅ |
| 关键词 ≤6 | ✅ 6 个 |
| 参考文献 Vancouver 编号制、全部在文内被引（1–18 连续）| ✅ |
| CRediT 作者贡献声明 | ✅ |
| 图：Arial、色盲安全、600dpi TIFF | ✅ figures_v2/ |
| 图-表-正文数字三方一致 | ✅ 门禁 101+ 项断言 |
| AI 使用声明 / 数据可用性（含 DOI）| ✅ |
