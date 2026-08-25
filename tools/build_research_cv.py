"""Build Praveena Satti's focused two-page research CV."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "Praveena_Satti_Research_CV.pdf"

INK = colors.HexColor("#14231F")
FOREST = colors.HexColor("#164F46")
ACCENT = colors.HexColor("#A63F2A")
MUTED = colors.HexColor("#52615B")
LINE = colors.HexColor("#D7D0C2")
PAPER = colors.HexColor("#FFFDF8")
TINT = colors.HexColor("#F2EEE6")

PAGE_WIDTH, PAGE_HEIGHT = A4
LEFT = 14 * mm
RIGHT = 14 * mm
TOP = 12 * mm
BOTTOM = 13 * mm


def make_styles():
    base = getSampleStyleSheet()
    return {
        "name": ParagraphStyle(
            "Name",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=25,
            leading=27,
            textColor=INK,
            alignment=TA_CENTER,
            spaceAfter=2,
        ),
        "title": ParagraphStyle(
            "TitleLine",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=9.5,
            leading=12,
            textColor=FOREST,
            alignment=TA_CENTER,
            spaceAfter=4,
        ),
        "contact": ParagraphStyle(
            "Contact",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=7.7,
            leading=10,
            textColor=MUTED,
            alignment=TA_CENTER,
            spaceAfter=6,
        ),
        "section": ParagraphStyle(
            "Section",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=10.2,
            leading=12,
            textColor=ACCENT,
            spaceBefore=6,
            spaceAfter=3,
            borderWidth=0,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8.35,
            leading=10.6,
            textColor=INK,
            spaceAfter=2.5,
        ),
        "small": ParagraphStyle(
            "Small",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=7.6,
            leading=9.5,
            textColor=INK,
            spaceAfter=1.5,
        ),
        "entry_title": ParagraphStyle(
            "EntryTitle",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=8.6,
            leading=10.5,
            textColor=INK,
            spaceAfter=1,
        ),
        "entry_meta": ParagraphStyle(
            "EntryMeta",
            parent=base["BodyText"],
            fontName="Helvetica-Oblique",
            fontSize=7.5,
            leading=9.2,
            textColor=MUTED,
            spaceAfter=1.5,
        ),
        "bullet": ParagraphStyle(
            "Bullet",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=7.9,
            leading=10.1,
            leftIndent=10,
            firstLineIndent=-6,
            bulletIndent=2,
            textColor=INK,
            spaceAfter=1.3,
        ),
        "card_title": ParagraphStyle(
            "CardTitle",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=8.2,
            leading=10,
            textColor=FOREST,
            spaceAfter=2,
        ),
        "card_body": ParagraphStyle(
            "CardBody",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=7.25,
            leading=9.1,
            textColor=INK,
        ),
        "flagship": ParagraphStyle(
            "Flagship",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8.25,
            leading=10.6,
            textColor=INK,
            spaceAfter=2,
        ),
        "footer": ParagraphStyle(
            "Footer",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=7,
            leading=8,
            textColor=MUTED,
            alignment=TA_LEFT,
        ),
    }


STYLES = make_styles()


def paragraph(text, style="body"):
    return Paragraph(text, STYLES[style])


def bullet(text):
    return Paragraph(f"<bullet>&bull;</bullet>{text}", STYLES["bullet"])


def section(title):
    return KeepTogether(
        [
            Spacer(1, 2),
            Table(
                [[Paragraph(title.upper(), STYLES["section"])]],
                colWidths=[167 * mm],
                style=TableStyle(
                    [
                        ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
                        ("LINEBELOW", (0, 0), (-1, -1), 0.7, LINE),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                        ("TOPPADDING", (0, 0), (-1, -1), 0),
                    ]
                ),
            ),
            Spacer(1, 3),
        ]
    )


def entry(title, meta, bullets, link_url=None, link_label=None):
    title_text = title
    if link_url and link_label:
        title_text += (
            f' - <link href="{link_url}" color="#A63F2A">'
            f"<u>{link_label}</u></link>"
        )
    items = [Paragraph(title_text, STYLES["entry_title"])]
    if meta:
        items.append(Paragraph(meta, STYLES["entry_meta"]))
    items.extend(bullet(item) for item in bullets)
    items.append(Spacer(1, 2))
    return KeepTogether(items)


def card(title, body):
    return [
        Paragraph(title, STYLES["card_title"]),
        Paragraph(body, STYLES["card_body"]),
    ]


def on_page(canvas, doc):
    canvas.saveState()
    canvas.setTitle("Praveena Satti - Research CV")
    canvas.setAuthor("Praveena Satti")
    canvas.setSubject("Reliable retrieval-augmented language systems")
    canvas.setCreator("ReportLab")
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.5)
    canvas.line(LEFT, 10 * mm, PAGE_WIDTH - RIGHT, 10 * mm)
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7)
    canvas.drawString(LEFT, 6.5 * mm, "Praveena Satti | Research CV")
    canvas.drawRightString(
        PAGE_WIDTH - RIGHT, 6.5 * mm, f"Page {doc.page} of 2"
    )
    canvas.restoreState()


def build():
    frame = Frame(
        LEFT,
        BOTTOM,
        PAGE_WIDTH - LEFT - RIGHT,
        PAGE_HEIGHT - TOP - BOTTOM,
        leftPadding=0,
        rightPadding=0,
        topPadding=0,
        bottomPadding=0,
    )
    doc = BaseDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        leftMargin=LEFT,
        rightMargin=RIGHT,
        topMargin=TOP,
        bottomMargin=BOTTOM,
        title="Praveena Satti - Research CV",
        author="Praveena Satti",
        subject="Reliable retrieval-augmented language systems",
    )
    doc.addPageTemplates(PageTemplate(id="CV", frames=[frame], onPage=on_page))

    story = []

    story.extend(
        [
            paragraph("PRAVEENA SATTI", "name"),
            paragraph(
                "AI/ML RESEARCHER | RELIABLE RAG | INFORMATION RETRIEVAL | EVIDENCE VERIFICATION",
                "title",
            ),
            paragraph(
                'Hyderabad, India | '
                '<link href="mailto:sattipraveena3@gmail.com" color="#164F46"><u>Email</u></link> | '
                '<link href="https://www.linkedin.com/in/praveenasatti" color="#164F46"><u>LinkedIn</u></link> | '
                '<link href="https://github.com/sattipraveena3-sudo" color="#164F46"><u>GitHub</u></link> | '
                '<link href="https://sattipraveena3-sudo.github.io/" color="#164F46"><u>Portfolio</u></link> | '
                '<link href="https://orcid.org/0009-0000-6555-5072" color="#164F46"><u>ORCID</u></link>',
                "contact",
            ),
        ]
    )

    story.append(section("Research identity"))
    story.append(
        paragraph(
            "<b>Reliable retrieval-augmented language systems.</b> I study how changes "
            "in retrieved evidence cause answer reversals, and how evidence-aware "
            "verification and abstention can prevent harmful transitions. My central "
            "methods are information retrieval, transition-based evaluation, controlled "
            "failure analysis, and reproducible systems research."
        )
    )

    story.append(section("Flagship research program"))
    flagship = [
        paragraph(
            "<b>From Measurement to Mitigation of Evidence-Induced Answer Reversals in RAG</b>",
            "flagship",
        ),
        paragraph(
            "<b>Question:</b> When retrieved evidence is expanded along a fixed ranking, "
            "which answer changes are harmful, why do they persist or recover, and can "
            "a change-triggered evidence-stability gate reduce correct-to-incorrect "
            "transitions without suppressing incorrect-to-correct repairs?",
            "flagship",
        ),
        paragraph(
            "<b>Status:</b> Unit tests and the no-cost mock smoke workflow pass. EAR, "
            "BCR, RTB, persistence, recovery, and first-reversal metrics are implemented. "
            "The primary real-model experiment and mitigation study are pending; mock "
            "outputs are not reported as research findings.",
            "small",
        ),
        paragraph(
            '<link href="https://github.com/sattipraveena3-sudo/Evidence-Induced-Answer-Reversals" color="#A63F2A"><u>Repository</u></link> | '
            '<link href="https://github.com/sattipraveena3-sudo/Evidence-Induced-Answer-Reversals/blob/main/docs/LITERATURE_MAP.md" color="#A63F2A"><u>27-paper literature map</u></link> | '
            '<link href="https://github.com/sattipraveena3-sudo/Evidence-Induced-Answer-Reversals/blob/main/docs/RESEARCH_IDENTITY.md" color="#A63F2A"><u>Scope and zero-budget plan</u></link>',
            "small",
        ),
    ]
    flagship_table = Table(
        [[flagship]],
        colWidths=[PAGE_WIDTH - LEFT - RIGHT],
        style=TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), TINT),
                ("BOX", (0, 0), (-1, -1), 0.7, LINE),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        ),
    )
    story.append(flagship_table)

    story.append(section("Research and open-source evidence"))
    story.append(
        entry(
            "Evidence-Induced Answer Reversals",
            "Flagship research implementation | 2026",
            [
                "Built fixed-prefix trajectory generation, strict input validation, exact-match/token-F1 scoring, bootstrap analysis, and machine-readable result contracts.",
                "Mapped 27 primary papers and identified retrieval-size robustness, transition metrics under spurious features, sufficient-context selection, and adaptive stopping as required comparisons.",
            ],
            "https://github.com/sattipraveena3-sudo/Evidence-Induced-Answer-Reversals",
            "code",
        )
    )
    story.append(
        entry(
            "Castorini Foundations of Retrieval",
            "Anserini and Pyserini | 2026",
            [
                "Reproduced classical, sparse, and dense retrieval runs and contributed evidence logs to established open-source IR toolkits.",
                'Both contributions passed maintainer review and were merged upstream: <link href="https://github.com/castorini/anserini/pull/3391" color="#A63F2A"><u>Anserini PR #3391</u></link> and <link href="https://github.com/castorini/pyserini/pull/2650" color="#A63F2A"><u>Pyserini PR #2650</u></link>.',
            ],
        )
    )
    story.append(
        entry(
            "Emotion Classification Using BERT: A Comprehensive Study",
            "Journal of Propulsion Technology, 44(4) | 2023",
            [
                "Developed a Transformer-based multi-label emotion-classification workflow on GoEmotions, including preprocessing, BERT fine-tuning, evaluation, and label-level analysis.",
            ],
            "https://www.propulsiontechjournal.com/index.php/journal/article/view/8744",
            "record",
        )
    )

    story.append(section("Research-relevant experience"))
    story.append(
        entry(
            "AI/ML Engineer Intern - Infor, Hyderabad",
            "2025 - Present",
            [
                "Built enterprise retrieval-augmented generation pipelines using LangChain, vector indexing, SQL preprocessing, REST deployment layers, and evaluation-oriented data flows.",
                "Developed NLP automation and reusable AWS data/ML workflows using S3, Lambda, Docker, CI/CD, preprocessing, and monitoring.",
            ],
        )
    )
    story.append(
        entry(
            "Software Development Intern - Swecha",
            "Internship",
            [
                "Improved backend reliability for an open-access learning platform by auditing API/database retrieval paths, resolving data bottlenecks, and building reusable backend modules.",
            ],
        )
    )

    story.append(section("Primary study design"))
    story.append(
        paragraph(
            "Open QA datasets; one fixed BM25 ranking and one open dense ranking; "
            "at least two model families; deterministic prompts; exact-match and "
            "token-F1 scoring; bootstrap confidence intervals; and controlled "
            "relevance, conflict, order, and support analysis. The gate will report "
            "EAR, BCR, RTB, accuracy, abstention coverage, verifier calls, latency, "
            "and token overhead. The core path uses open data and open models on "
            "available local or free notebook compute; a paid API is not required.",
            "small",
        )
    )

    story.append(PageBreak())

    story.extend(
        [
            paragraph("PRAVEENA SATTI", "name"),
            paragraph(
                "CORE SYSTEMS, REPRODUCIBLE ENGINEERING, AND CREDENTIALS",
                "title",
            ),
        ]
    )
    story.append(section("Selected systems supporting the research program"))
    card_rows = [
        [
            card(
                "Hybrid Wiki Search Engine - 10 tests passed",
                "BM25, TF-IDF, reciprocal-rank fusion, and evaluation utilities in a compact retrieval system. "
                '<link href="https://github.com/sattipraveena3-sudo/hybrid-wiki-search-engine" color="#A63F2A"><u>Repository</u></link>',
            ),
            card(
                "PraxisMesh - 9 tests passed",
                "Typed task graphs, deterministic policy gates, human approval, independent postcondition checks, and tamper-evident audit trails. "
                '<link href="https://github.com/sattipraveena3-sudo/PraxisMesh" color="#A63F2A"><u>Repository</u></link>',
            ),
        ],
        [
            card(
                "Repo-Aware Coding Assistant - 6 tests passed",
                "AST chunking, call-graph expansion, lexical retrieval, and traceable file/line grounding for repository-aware suggestions. "
                '<link href="https://github.com/sattipraveena3-sudo/repo-aware-coding-assistant" color="#A63F2A"><u>Repository</u></link>',
            ),
            card(
                "Clinical Trial Matching - 8 tests and build passed",
                "Semantic retrieval plus structured eligibility filters. Tests avoid the optional model download; default embedding bootstrap is a separate integration step. "
                '<link href="https://github.com/sattipraveena3-sudo/clinical-trial-matching-engine" color="#A63F2A"><u>Repository</u></link>',
            ),
        ],
    ]
    cards_table = Table(
        card_rows,
        colWidths=[82 * mm, 82 * mm],
        hAlign="LEFT",
        style=TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BACKGROUND", (0, 0), (-1, -1), PAPER),
                ("BOX", (0, 0), (-1, -1), 0.55, LINE),
                ("INNERGRID", (0, 0), (-1, -1), 0.55, LINE),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        ),
    )
    story.append(cards_table)

    story.append(section("Portfolio audit and engineering foundation"))
    story.append(
        paragraph(
            "<b>13 executable repositories passed their available test or build checks "
            "on 25 August 2026.</b> Supporting systems cover infrastructure validation, "
            "ETL observability, distributed ML execution, graph anomaly detection, "
            "language analysis, physiological-signal fusion, synchronized-signal "
            "analysis, and authenticated application deployment. These demonstrate "
            "testing, observability, controlled execution, and documented boundaries; "
            "they are not presented as separate research agendas.",
            "body",
        )
    )

    story.append(section("Education"))
    story.append(
        entry(
            "Bachelor of Technology (Honours) - Computer Science and Engineering",
            "Artificial Intelligence and Machine Learning | KL University | 2022 - 2026",
            [
                "Coursework and independent work across machine learning, deep learning, NLP, information retrieval, databases, algorithms, cloud/data systems, and software engineering.",
            ],
        )
    )

    story.append(section("Research methods and technical skills"))
    skills_data = [
        [
            Paragraph("<b>Research</b>", STYLES["entry_title"]),
            paragraph(
                "Reliable RAG, information retrieval, answer-trajectory analysis, "
                "retrieval robustness, evidence attribution, faithfulness, abstention, "
                "failure analysis, and reproducible evaluation.",
                "small",
            ),
        ],
        [
            Paragraph("<b>Methods</b>", STYLES["entry_title"]),
            paragraph(
                "BM25, sparse/dense retrieval, SPLADE, Lucene, reciprocal-rank fusion, "
                "BERT/Transformers, PyTorch, Scikit-learn, semantic search, bootstrap "
                "confidence intervals, and controlled ablations.",
                "small",
            ),
        ],
        [
            Paragraph("<b>Engineering</b>", STYLES["entry_title"]),
            paragraph(
                "Python, SQL, Pandas, NumPy, PySpark, FastAPI, Flask, Docker, AWS, "
                "Terraform, Neo4j, NetworkX, CI/CD, testing, observability, and Linux.",
                "small",
            ),
        ],
    ]
    skills_table = Table(
        skills_data,
        colWidths=[25 * mm, 139 * mm],
        style=TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LINEBELOW", (0, 0), (-1, -2), 0.35, LINE),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        ),
    )
    story.append(skills_table)

    story.append(section("Earlier work and evidence boundaries"))
    story.append(
        bullet(
            "<b>EMCAD checkpoint screening:</b> earlier medical-segmentation "
            "reproducibility scripts and recorded evaluation evidence; the public branch "
            "does not include an automated test suite. "
            '<link href="https://github.com/sattipraveena3-sudo/praveenasatti/tree/emcad-screening" color="#A63F2A"><u>Branch</u></link>'
        )
    )
    story.append(
        bullet(
            "<b>BioTwin-PE:</b> earlier conceptual multimodal monitoring preprint; "
            "the public repository is documentation-focused and does not currently "
            "contain an executable implementation. "
            '<link href="https://github.com/sattipraveena3-sudo/BioTwin-PE-APEE" color="#A63F2A"><u>Repository</u></link>'
        )
    )

    story.append(section("Credentials, affiliations, and research practice"))
    story.append(
        paragraph(
            "<b>Certifications:</b> AWS Certified Cloud Practitioner | Google Associate "
            "Cloud Engineer | GitHub Foundations | Neo4j Certified Professional | "
            "Automation Anywhere Advanced RPA Professional<br/>"
            "<b>Affiliations:</b> IEEE Member | IEEE Women in Engineering | IEEE SIGHT",
            "small",
        )
    )
    story.append(
        paragraph(
            "<b>Practice:</b> freeze the question and protocol; record dataset/split, "
            "retrieval ranking, model and prompt, source revision, environment, raw "
            "outputs, and limitations; distinguish passing software checks from "
            "scientific findings; report harmful and beneficial transitions together.",
            "small",
        )
    )

    doc.build(story)


if __name__ == "__main__":
    build()
    print(OUTPUT)
