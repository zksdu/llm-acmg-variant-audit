# -*- coding: utf-8 -*-
"""
build_docx.py — manuscript_GPB.md → 投稿用 Word（submission_GPB.docx）

处理：标题页、##/### 标题、段落（**粗体**/*斜体*）、Markdown 表格、
引用块跳过、内嵌图片行跳过（图单独上传）。

使用：python build_docx.py
"""
import re
from pathlib import Path

from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH

DOCS = Path(__file__).parent.parent / "docs"

RUNNING = "Multi-vendor LLM Variant Classification"
AUTHOR = "Bing Song\u00b9, Kai Zhang\u00b2,*"
AFFIL_1 = "\u00b9The Third Affiliated Hospital of Guangzhou Medical University, Guangzhou, Guangdong, China"
AFFIL_2 = "\u00b2Guangdong Communication Polytechnic, Guangzhou, Guangdong, China"
EMAIL = "zhangkai@gdcp.edu.cn"

# --- 以下内容从 manuscript_GPB.md 运行时提取（单一事实来源，杜绝三副本漂移） ---
MD_SRC = DOCS / "manuscript_GPB.md"
MD_TEXT = MD_SRC.read_text(encoding="utf-8")

def _extract(pattern, text, flags=0):
    m = re.search(pattern, text, flags)
    assert m, f"extraction failed: {pattern}"
    return m.group(1).strip()

TITLE = _extract(r"\*\*Title: (.+?)\*\*$", MD_TEXT, re.M)
KEYWORDS = _extract(r"\*\*Keywords:\*\* (.+)$", MD_TEXT, re.M)
ABSTRACT = _extract(r"## Abstract\n\n(.+?)\n\n## Introduction", MD_TEXT, re.S)

INLINE = re.compile(r"(\*\*.+?\*\*|\*[^*\n]+?\*)")


def add_runs(par, text):
    for tok in INLINE.split(text):
        if not tok:
            continue
        if tok.startswith("**") and tok.endswith("**"):
            r = par.add_run(tok[2:-2])
            r.bold = True
        elif tok.startswith("*") and tok.endswith("*") and len(tok) > 2:
            r = par.add_run(tok[1:-1])
            r.italic = True
        else:
            par.add_run(tok)


def add_table(doc, rows):
    cells = [ [c.strip() for c in r.strip().strip("|").split("|")] for r in rows ]
    cells = [r for r in cells if not all(set(c) <= set("-: ") for c in r)]
    if not cells:
        return
    ncol = max(len(r) for r in cells)
    t = doc.add_table(rows=len(cells), cols=ncol)
    t.style = "Table Grid"
    for i, row in enumerate(cells):
        for j in range(ncol):
            txt = row[j] if j < len(row) else ""
            cell = t.cell(i, j)
            cell.text = ""
            p = cell.paragraphs[0]
            add_runs(p, txt)
            for r in p.runs:
                r.font.size = Pt(9)
                if i == 0:
                    r.bold = True


def main():
    doc = Document()
    style = doc.styles["Normal"]
    style.font.name = "Times New Roman"
    style.font.size = Pt(11)
    for lvl, sz in (("Heading 1", 13), ("Heading 2", 12)):
        st = doc.styles[lvl]
        st.font.name = "Times New Roman"
        st.font.size = Pt(sz)
        st.font.bold = True
        st.font.color.rgb = None

    # ===== 标题页 =====
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(TITLE)
    r.bold = True
    r.font.size = Pt(14)

    for line, bold in [(RUNNING + "  (running title)", False),
                       ("", False), (AUTHOR, True), (AFFIL_1, False),
                       (AFFIL_2, False),
                       ("*Corresponding author. E-mail: " + EMAIL, False),
                       ("", False)]:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if line.startswith("*") and line.endswith("*") and len(line) > 2:
            r = p.add_run(line[1:-1]); r.italic = True
        else:
            add_runs(p, line)

    doc.add_heading("Abstract", level=1)
    for para in ABSTRACT.split("\n\n"):
        p = doc.add_paragraph()
        add_runs(p, para)

    p = doc.add_paragraph()
    r = p.add_run("Keywords: "); r.bold = True
    p.add_run(KEYWORDS)

    doc.add_page_break()

    # ===== 正文 =====
    src = MD_TEXT
    lines = src.splitlines()
    i = 0
    # 跳过文件头（# 标题行、> 引用块、--- 分隔、Abstract 占位与 Keywords 段）
    while i < len(lines):
        l = lines[i]
        if l.startswith("## Introduction"):
            break
        i += 1

    buf = []
    while i < len(lines):
        l = lines[i]
        if l.startswith("|"):
            buf.append(l)
            i += 1
            continue
        if buf:
            add_table(doc, buf)
            buf = []
        if not l.strip() or l.strip() == "---" \
                or l.startswith("![") or l.startswith("# "):
            i += 1
            continue
        if l.startswith(">"):
            note = l.lstrip("> ").strip()
            if note:
                p = doc.add_paragraph()
                add_runs(p, note)
                for r in p.runs:
                    r.italic = True
            i += 1
            continue
        if l.startswith("## "):
            doc.add_heading(l[3:].strip(), level=1)
        elif l.startswith("### "):
            doc.add_heading(l[4:].strip(), level=2)
        else:
            p = doc.add_paragraph()
            add_runs(p, l)
        i += 1
    if buf:
        add_table(doc, buf)

    out = DOCS / "submission_GPB.docx"
    doc.save(out)
    print(f"\u2713 {out}")
    d2 = Document(str(out))
    print(f"  \u6bb5\u843d {len(d2.paragraphs)} | \u8868\u683c {len(d2.tables)}")


if __name__ == "__main__":
    main()
