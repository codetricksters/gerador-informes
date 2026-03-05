# Fix Guide — gerador-informes

## Priority: High

---

### 1. Remove unused `matplotlib` dependency

`matplotlib` is listed in `pyproject.toml` but is never imported or used.

**File:** `pyproject.toml`

Remove this line from `dependencies`:
```toml
"matplotlib>=3.10.8",
```

Then sync the environment:
```bash
uv remove matplotlib
```

---

### 2. Replace hardcoded data with JSON file loading

`main.py` currently uses a hardcoded `dados_teste` dictionary. It should load data from a JSON file using `pandas`.

**File:** `main.py`

Replace the hardcoded `dados_teste` block with a JSON load. The full file loading flow will be implemented later, but the structure should be:

```python
import pandas as pd
import json

# Load data from JSON file
with open("data.json", "r", encoding="utf-8") as f:
    dados = json.load(f)

# Or using pandas for structured tabular data inside the JSON:
# df = pd.read_json("data.json")
```

The `dados` dict should then be passed to `template.render()` instead of `dados_teste`:

```python
html_string = template.render(dados)
```

**Expected JSON structure** (based on current template variables):

```json
{
  "ano_calendario": "2025",
  "nome_fonte_pagadora": "...",
  "cnpj_fonte_pagadora": "...",
  "nome_fornecedora": "...",
  "cnpj_fornecedora": "...",
  "informacoes_complementares": "...",
  "nome_responsavel": "...",
  "data_emissao": "DD/MM/AAAA",
  "tabela_retencoes": [
    { "mes": "Jan", "codigo": "5952", "valor_pago": "0,00", "valor_retido": "0,00" }
  ],
  "tabela_rendimentos": [
    { "mes": "Jan", "codigo": "1708", "descricao": "...", "valor_rendimento": "0,00", "valor_imposto": "0,00" }
  ]
}
```

---

### 3. Fix malformed HTML in page 2 header table

The first `<tr>` in the page 2 header table is never closed before the second `<tr>` opens. This is invalid HTML and may cause rendering issues in WeasyPrint.

**File:** `templates/report.html`, around line 300

Current (broken):
```html
<tr>
    <td rowspan="2" ...>...</td>
    <td ...>...</td>
    <td ...>...</td>

<tr>
    <td ...>...</td>
    <td ...>...</td>
</tr>
```

Fixed:
```html
<tr>
    <td rowspan="2" ...>...</td>
    <td ...>...</td>
    <td ...>...</td>
</tr>
<tr>
    <td ...>...</td>
    <td ...>...</td>
</tr>
```

---

## Priority: Medium

---

### 4. WeasyPrint CSS compatibility — `display: flex` and `display: grid`

**File:** `templates/report.html` (CSS section)

`.row { display: flex; }` is used for the form field sections (fonte pagadora, fornecedora, responsável). `.container { display: grid; }` is defined but **never used** in the HTML.

WeasyPrint has limited support for flexbox and no support for CSS Grid in older versions. If the form sections render incorrectly (fields stacking vertically instead of side-by-side), replace the flex layout with a table-based approach:

```css
/* Replace this: */
.row {
    display: flex;
    border: 1px solid #000;
}
.col {
    padding: 4px 6px;
    border-right: 1px solid #000;
    flex: 1;
}

/* With this: */
.row {
    display: table;
    width: 100%;
    border: 1px solid #000;
    border-collapse: collapse;
}
.col {
    display: table-cell;
    padding: 4px 6px;
    border-right: 1px solid #000;
}
```

Also remove the unused `.container` CSS rule entirely:
```css
/* Remove this block: */
.container {
    display: grid;
    grid-template-columns: 10% 40% 50%;
}
```

---

## Priority: Low

---

### 5. Fix footer page number on page 2

Both pages currently show `"Pág. 1"` in the footer.

**File:** `templates/report.html`, around line 397

Current:
```html
<span>Pág. 1</span>
```

Fixed:
```html
<span>Pág. 2</span>
```

---

### 6. Fill in README.md

`README.md` is currently empty. At minimum it should document:
- What the project does
- How to install dependencies (`uv sync`)
- How to run (`python main.py`)
- Expected input format (JSON structure — see Fix #2 above)
