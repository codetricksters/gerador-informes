# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
uv sync

# Generate a single PDF from data.json (CLI mode)
uv run main.py

# Run the Flask web app
uv run app.py
# or
flask --app app run
```

```bash
# Run tests
uv run --with pytest pytest test_app.py -v
```

## Architecture

This project has two entry points that share the same Jinja2 template and WeasyPrint rendering pipeline:

**`main.py`** — CLI mode. Reads `data.json` from the project root, renders `templates/report.html` via Jinja2, and writes `report.pdf`.

**`app.py`** — Flask web app. Accepts an Excel file upload (`.xlsx`) via a browser form (`templates/index.html`), reads the `Informes` sheet with pandas, groups rows by `cnpj_fornecedora`, builds the same `dados` dict for each supplier, renders a PDF per supplier, and returns all PDFs bundled in a `informes.zip` download.

**`templates/report.html`** — Single Jinja2 template that renders a two-page A4 PDF:
- Page 1: Comprovante de Retenção de CSLL, COFINS e PIS/PASEP (tabela_retencoes)
- Page 2: Comprovante de Rendimentos e Retenção de IRRF (tabela_rendimentos)

The template uses `page-break-after: always` to separate pages and loads static assets (government logos) relative to `templates/` via `base_url`.

## Data structures

The template expects a `dados` dict with these keys:

| Key | Source in Excel sheet |
|---|---|
| `ano_calendario` | `ano_calendario` column |
| `nome_fonte_pagadora` | `nome_fonte_pagadora` column |
| `cnpj_fonte_pagadora` | `cnpj_fonte_pagadora` column |
| `nome_fornecedora` | `nome_fornecedora` column |
| `cnpj_fornecedora` | `cnpj_fornecedora` column |
| `informacoes_complementares` | `informacoes_complementares` column |
| `nome_responsavel` | `nome_responsavel` column |
| `data_emissao` | `data_emissao` column |
| `tabela_retencoes` | list of dicts: `mes`, `codigo`, `valor_pago`, `valor_retido` |
| `tabela_rendimentos` | list of dicts: `mes`, `codigo`, `descricao`, `valor_rendimento`, `valor_imposto` |

### Excel sheet columns (`Informes`)

Each row is one month entry. The `tipo` column (`retencao` or `rendimento`) determines which table a row feeds. Rows sharing the same `cnpj_fornecedora` are grouped into one PDF.

| Excel column | Maps to |
|---|---|
| `mes` | Row in `tabela_retencoes` or `tabela_rendimentos` |
| `tipo` | `retencao` → `tabela_retencoes`; `rendimento` → `tabela_rendimentos` |
| `codigo` | `dados['tabela_*'][n]['codigo']` |
| `descricao` | `dados['tabela_rendimentos'][n]['descricao']` (empty for retencao) |
| `valor` | `valor_pago` (retencao) / `valor_rendimento` (rendimento) |
| `valor_retido` | `valor_retido` (retencao) / `valor_imposto` (rendimento) |

## Known issues (FIXES.md)

- WeasyPrint has limited flexbox support and no CSS Grid support — use `display: table` / `display: table-cell` instead of flex if layout breaks.
- The `base_url` passed to `HTML(string=..., base_url=...)` must be the absolute path to `templates/` so images resolve correctly.