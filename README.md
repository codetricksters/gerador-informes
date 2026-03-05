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

Create a `data.json` file in the project root (see structure below), then run:

```bash
uv run main.py
```

This generates `report.pdf` in the project root.

## data.json structure

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
