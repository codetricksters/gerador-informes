# gerador-informes

Generates a two-page PDF with the annual Brazilian tax retention certificates:

- Page 1: Comprovante de Retenção de CSLL, COFINS e PIS/PASEP (Lei nº 10.833/2003, art. 30)
- Page 2: Comprovante de Rendimentos e Retenção de IRRF — Pessoa Jurídica

## Requirements

- Python >= 3.12
- [uv](https://github.com/astral-sh/uv)

## Setup

```bash
uv sync
```

## Usage

### Web app (batch mode)

```bash
uv run app.py
```

Open `http://localhost:5000`, upload an Excel file, and download a ZIP containing one PDF per supplier.

### CLI (single report)

Create a `data.json` file in the project root (see structure below), then run:

```bash
uv run main.py
```

This generates `report.pdf` in the project root.

## Excel model (web app)

The Excel file must have a sheet named **`Informes`** with the following columns. Each row is one month entry. Rows for the same `cnpj_fornecedora` are grouped into a single PDF. The `tipo` column determines which table each row goes into.

| Column | Values / Notes |
|---|---|
| `ano_calendario` | e.g. `2025` |
| `nome_fonte_pagadora` | Company name of the payer |
| `cnpj_fonte_pagadora` | e.g. `00.000.000/0001-00` |
| `nome_fornecedora` | Company name of the supplier |
| `cnpj_fornecedora` | e.g. `00.000.000/0001-00` — used to group rows per PDF |
| `informacoes_complementares` | Optional free text |
| `nome_responsavel` | Name of the responsible person |
| `data_emissao` | Emission date, e.g. `28/02/2025` |
| `mes` | Month abbreviation, e.g. `Jan`, `Fev`, … |
| `tipo` | `retencao` or `rendimento` |
| `codigo` | Tax code (e.g. `5952` for retencao, `1708` for rendimento) |
| `descricao` | Description (used only for `rendimento` rows) |
| `valor` | Gross amount paid / earned |
| `valor_retido` | Amount withheld / tax amount |

## data.json structure (CLI)

```json
{
  "ano_calendario": "2025",
  "nome_fonte_pagadora": "EMPRESA EXEMPLO S.A.",
  "cnpj_fonte_pagadora": "00.000.000/0001-00",
  "nome_fornecedora": "FORNECEDOR EXEMPLO LTDA",
  "cnpj_fornecedora": "00.000.000/0001-00",
  "informacoes_complementares": "",
  "nome_responsavel": "NOME DO RESPONSAVEL",
  "data_emissao": "DD/MM/AAAA",
  "tabela_retencoes": [
    {
      "mes": "Jan",
      "codigo": "5952",
      "valor_pago": "0,00",
      "valor_retido": "0,00"
    }
  ],
  "tabela_rendimentos": [
    {
      "mes": "Jan",
      "codigo": "1708",
      "descricao": "Remuneração de serviços profissionais prestados por Pessoa Jurídica",
      "valor_rendimento": "0,00",
      "valor_imposto": "0,00"
    }
  ]
}
```
