# Product Requirements Document (PRD) — Offline AI Presentation Factory

## 1. Problems
- **API Dependency & Costs:** Commercial presentation AI tools require expensive cloud APIs and expose confidential data.
- **Rigid Templates:** Standard presentation tools lack industry-specific design variations and scalable theme architecture.
- **Manual Formatting:** Converting raw Markdown insights into polished PowerPoint slides is tedious and error-prone.

## 2. Goals
- Provide a **100% offline desktop application** built with PyQt6 and Python.
- Implement a **Theme Factory design pattern** supporting multiple industries (Architectural, Construction, Engineering, Literature) and 30+ color palette groups.
- Integrate **50 zero-cost offline AI and NLP tools** organized into modular agents (Markdown manipulator, text deduplication, outline refinement).
- Enable instantaneous export to `.pptx` (via `python-pptx`) and `.pdf` (via ReportLab).

## 3. Solutions
- **PyQt6 Desktop Frontend:** Intuitive GUI with collapsible industry toolboxes, theme pickers, and live Markdown editing.
- **Agentic Pipeline Architecture:** Extensible `AgentFactory` pattern allowing incremental additions of AI agents across future Git commits.
- **Structured Markdown Parser:** Standardized Markdown format compatible with DeepSeek and local LLM outputs.