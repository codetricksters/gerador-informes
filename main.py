from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import os

# Define the directory where templates are stored
templates_dir = 'templates'
environment = Environment(loader=FileSystemLoader(templates_dir))
template = environment.get_template("report.html")

# Define the dynamic data to pass to the template
dados_teste = {
    "ano_calendario": "2025",
    "nome_fonte_pagadora": "EMPRESA FICTÍCIA BRASIL S.A.",
    "cnpj_fonte_pagadora": "12.345.678/0001-99",
    "nome_fornecedora": "FORNECEDOR DE TESTES LTDA",
    "cnpj_fornecedora": "98.765.432/0001-11",
    "informacoes_complementares": "Documento gerado automaticamente para fins de teste de renderização de template Jinja2.",
    "nome_responsavel": "JOÃO DA SILVA TESTE",
    "data_emissao": "04/03/2026",
    
    # Tabela 1: Relação de Pagamentos e Retenções
    "tabela_retencoes": [
        {
            "mes": "Jan",
            "codigo": "5952",
            "valor_pago": "150.000,00",
            "valor_retido": "6.975,00"
        },
        {
            "mes": "Fev",
            "codigo": "5952",
            "valor_pago": "200.500,50",
            "valor_retido": "9.323,27"
        },
        {
            "mes": "Mar",
            "codigo": "5960",
            "valor_pago": "50.000,00",
            "valor_retido": "1.500,00"
        }
    ],
    
    # Tabela 2: Rendimento e Imposto Retido na Fonte
    "tabela_rendimentos": [
        {
            "mes": "Jan",
            "codigo": "1708",
            "descricao": "Remuneração de serviços profissionais prestados por Pessoa Jurídica",
            "valor_rendimento": "150.000,00",
            "valor_imposto": "2.250,00"
        },
        {
            "mes": "Fev",
            "codigo": "1708",
            "descricao": "Remuneração de serviços profissionais prestados por Pessoa Jurídica",
            "valor_rendimento": "200.500,50",
            "valor_imposto": "3.007,50"
        }
    ]
}

# Render the HTML string from the template and data
html_string = template.render(dados_teste)

# Create an HTML object from the string
# Setting base_url is important for loading relative assets like images/CSS
html = HTML(string=html_string, base_url=os.path.abspath(templates_dir))

# Write the PDF to a file
html.write_pdf('report.pdf')
print('PDF report.pdf generated successfully.')
