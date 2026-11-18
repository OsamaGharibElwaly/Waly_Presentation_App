# Offline AI Presentation Factory — Complete Master Technical Specification & Architecture Guide

This comprehensive reference document details the entire architecture, data pipeline, design systems, UI components, and generation engines built into your **100% Offline AI Presentation Factory** desktop application.

---

## 1. Executive Summary & Core System Objectives

The Offline AI Presentation Factory is a professional-grade PyQt6 desktop application designed to ingest structured Markdown documents and transform them instantly into highly stylized, geometric widescreen (`16:9`) presentations (`.pptx` via `python-pptx`) and clean vector documents (`.pdf` via ReportLab).

### Core Pillars:

* **Air-Gapped & Zero API Cost:** Operates entirely offline with zero cloud dependency, safeguarding sensitive corporate intellectual property and eliminating recurring subscription token overhead.
* **Dynamic Geometry Over Flat Text:** Replaces plain static PowerPoint text boxes with advanced shape rendering, header banner cards, container shapes, accent bars, and offset shadows.
* **Real-Time Studio Synchronization:** Features an interactive multi-tab PyQt6 studio with collapsing industry categories, real-time color swatch inspection, and dynamic light/dark contrast text calculation.
* **30 Design Archetypes:** Encapsulates 30 distinct visual design systems ranging from Glassmorphism and Bento Grids to Neo-Brutalism, Swiss Editorial, and Executive KPI Strips.

---

## 2. Complete Project File Tree Architecture

```text
OfflineAIPresentationFactory/
├── .venv/                              # Python virtual environment (Python 3.12)
├── backend/
│   ├── agents/
│   │   ├── base/
│   │   │   └── agent.py                # BaseAgent, AgentContext, and SlideSpec dataclasses
│   │   ├── factory/
│   │   │   └── agent_factory.py        # Auto-registering AgentFactory with fallback resilience
│   │   └── markdown_manipulator.py     # Parses headers, bullets, and speaker notes
│   ├── pptx_engine/
│   │   └── builder.py                  # Advanced geometric python-pptx shape & archetype renderer
│   ├── pdf_engine/
│   │   └── builder.py                  # ReportLab landscape vector PDF compiler
│   └── pipeline/
│       └── orchestrator.py             # Coordinates agents, themes, palettes, and target builders
├── frontend/
│   ├── main.py                         # Application entry point (`python -m frontend.main`)
│   ├── theme_factory/
│   │   ├── catalog.py                  # Static/dynamic industry catalog loader (`utf-8-sig`)
│   │   └── registry.py                 # Palette registry and catalog parser
│   └── ui/
│       └── main_window.py              # Advanced QMainWindow studio interface & interactive swatches
├── knowledge/
│   └── catalog/
│       ├── industries.json             # Industry domains, descriptions, and theme mappings
│       └── palettes.json               # 30+ tuned color palette groups
├── out/                                # Local output directory for exported .pptx and .pdf files
├── requirements.txt                    # Core uncompiled dependencies (PyQt6, python-pptx, reportlab, etc.)
└── code_enhance_4.ps1                  # Master PowerShell installation and update script

```

---

## 3. Backend Agentic Pipeline & Core Engines

### A. Agent Base & Context (`backend/agents/base/agent.py`)

Defines the immutable data structures shared across all pipeline components:

* `AgentContext`: Holds the active theme dictionary, color palette dictionary, and presentation metadata (`deck_title`).
* `SlideSpec`: Represents an individual slide containing `title` (string), `bullets` (list of strings), and `notes` (speaker notes string).
* `BaseAgent`: Abstract interface enforcing a `run(content)` method across all agent implementations.

### B. Agent Factory (`backend/agents/factory/agent_factory.py`)

Implements a decorator-based auto-registration pattern (`@AgentFactory.register("name")`). If an agent key is missing, it triggers an automatic fallback search and provides a safe default `SafeFallbackAgent` so the application never crashes with a `KeyError`.

### C. Markdown Manipulator Agent (`backend/agents/markdown_manipulator.py`)

Parses raw Markdown input using clean line-by-line heuristic parsing:

* Skips top-level presentation titles (`# `).
* Splits slide boundaries upon encountering secondary headers (`## `).
* Collects bullet points (`- ` or `* `).
* Isolates speaker notes into dedicated metadata fields (`> ` or `> Speaker note:`).

### D. Presentation Builders (`PptxBuilder` & `PdfBuilder`)

* **`PptxBuilder` (`backend/pptx_engine/builder.py`)**: Configures 16:9 widescreen slides (`13.333` × `7.5` inches). Dynamically reads the active design archetype from the theme selection and constructs sophisticated shapes (`MSO_SHAPE.ROUNDED_RECTANGLE`, `RECTANGLE`), colored background fills, header banner cards, container boxes, and bullet lists using RGB color conversion.
* **`PdfBuilder` (`backend/pdf_engine/builder.py`)**: Compiles landscape letter vector documents via ReportLab, drawing slide titles and bullet points with precise coordinate positioning.

---

## 4. Frontend Studio UI & Real-Time Theme Synchronization

### A. Main Window Interface (`frontend/ui/main_window.py`)

Built with a sleek, dark-slate professional QSS stylesheet (`#090D16` canvas, `#111827` cards, `#2563EB` primary buttons, `#38BDF8` cyan accents):

* **Top Header Bar:** Direct input field for customizing the output file name and presentation title (`deck_title`).
* **Tab 1 (Industry & Style Studio):** Features a collapsing `QToolBox` listing industry domains (*Architecture, Construction, Engineering, Literature*) and sub-themes. Clicking any theme instantly synchronizes the right-panel inspector, updating the active title, description, and color swatches.
* **Tab 2 (Markdown AI Input):** A fully editable code/text workspace pre-loaded with the structured *Enterprise AI Transformation* master presentation markdown.
* **Interactive Color Swatch Grid:** Displays the exact hex codes of the active palette group. Each swatch button is clickable, dynamically calculating RGB luminance (`_is_light`) to set contrasting foreground text (`#000000` or `#FFFFFF`) for instant visual interpretation.

---

## 5. The 30 Design Archetypes System

The presentation builder assigns layouts based on the active design archetype linked to each industry theme:

| Category | Archetype Name | Visual Layout & Geometry Characteristics |
| --- | --- | --- |
| **Modern Tech & SaaS (1–6)** | 1. Glassmorphism Card | Translucent rounded rectangle over deep gradient fill. |
|  | 2. Bento Grid Layout | Asymmetrical rounded squares on a light canvas. |
|  | 3. Dark Mode Neon Glow | Pitch-black canvas with thin dark containers and glowing cyan borders. |
|  | 4. SaaS Hero Split | Vertical split with left text column and floating browser mockup. |
|  | 5. Floating Pill Badges | Pill-shaped container above oversized 48pt sans-serif headlines. |
|  | 6. Isometric Layer Stack | Vertically stacked tilted diamond shapes with drop shadows. |
| **Minimalist & Editorial (7–12)** | 7. Swiss Grid Editorial | Razor-thin hairline dividers on off-white canvas with serif titles. |
|  | 8. Monochromatic Slate | Three shades of slate gray with sharp rectangular geometry. |
|  | 9. Asymmetric Magazine Cutout | Tall vertical frame on left overlapping crisp white text box. |
|  | 10. Oversized Number Watermark | Giant ultra-light background numbers (`01`, `02`, `03`) behind text. |
|  | 11. Minimalist Timeline Bar | Horizontal center line with solid circular nodes and alternating text. |
|  | 12. Negative Space Spotlight | Centered small rounded square card surrounded by whitespace. |
| **Bold & Creative (13–18)** | 13. Neo-Brutalist Pop | Pastel yellow cards with thick 3pt black outlines and hard offset shadows. |
|  | 14. Diagonal Geometric Slice | Full-height vibrant coral shape sliced diagonally across canvas. |
|  | 15. Duotone Duet | High-contrast portrait inside circle frame with navy/mint filter. |
|  | 16. Organic Blob Mask | Soft wavy vector shapes behind clean white content cards. |
|  | 17. Kinetic Stripe Accent | Parallel diagonal parallelogram bars in top-right corner. |
|  | 18. Gradient Border Frame | Dark card wrapped in linear gradient border (magenta to amber). |
| **Corporate & Executive (19–24)** | 19. Executive KPI Strip | Equal-width white rectangles topped with thick forest green accent bars. |
|  | 20. Chevron Process Flow | Interlocking horizontal arrows shifting from light to deep navy. |
|  | 21. Frosted Sidebar Navigation | Full-height vertical charcoal panel on left for section titles. |
|  | 22. Dual Comparison Matrix | Side-by-side containers ("Before" vs. "After"). |
|  | 23. Concentric Circle Target | Layered circles with decreasing opacity for market reach visualization. |
|  | 24. Gold-Trimmed Luxury | Deep emerald background with metallic gold corner brackets. |
| **Playful, Soft & Futuristic (25–30)** | 25. Claymorphism 3D Soft | Chunky pastel lilac rounded rectangles with puffy inner highlights. |
|  | 26. Retro Terminal Window | Container with top title bar featuring red, yellow, green dots. |
|  | 27. Cyberpunk HUD Frame | Octagonal chamfered rectangles with thin neon lime borders. |
|  | 28. Warm Sand & Clay | Warm beige canvas with muted sage pill-shaped containers. |
|  | 29. Stacked Folder Tabs | Staggered rounded rectangles mimicking physical file folders. |
|  | 30. Radial Sunburst Hub | Central circular hub connected by dashed lines to floating badges. |

---

## 6. Execution & Local Export Workflow

1. **Launch Application:**
```powershell
.venv\Scripts\Activate.ps1
python -m frontend.main

```


2. **Select Theme & Palette:** In Tab 1, browse the collapsing industry categories, pick an industry and design archetype (e.g., *Engineering* -> *Quantum & Neon*), and choose a color palette group (e.g., *Cyber Slate & Neon Blue*).
3. **Review Swatches:** Inspect the live color swatches in the right panel to verify aesthetic contrast.
4. **Input Markdown:** Switch to Tab 2 to review or paste your presentation structure.
5. **Export:** Click **Export Styled .pptx Presentation** or **Export Clean .pdf Presentation**. The file is generated instantly and saved locally into the `out/` directory in your project root (`H:\devH\offlinepresentationapp\OfflineAIPresentationFactory\out\`).