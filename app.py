from flask import Flask, render_template, request, send_file
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import pandas as pd
import os
import io
import re
import zipfile

app = Flask(__name__)

TEMPLATES_DIR = 'templates'
report_env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
report_template = report_env.get_template("report.html")


def safe_str(value, default=''):
    if pd.isna(value):
        return default
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def format_currency(value):
    try:
        return f"{float(value):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    except (ValueError, TypeError):
        return str(value)


def format_date(value):
    if pd.isna(value):
        return ''
    if hasattr(value, 'strftime'):
        return value.strftime('%d/%m/%Y')
    return str(value)


def sanitize_filename(name):
    return re.sub(r'[^\w\s\-]', '_', name).strip()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    file = request.files.get('excel_file')
    if not file:
        return 'Nenhum arquivo enviado.', 400

    df = pd.read_excel(file, sheet_name='Informes')
    df['cnpj_fornecedora'] = df['cnpj_fornecedora'].astype(str)

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        for cnpj_key, group in df.groupby('cnpj_fornecedora', sort=False):
            first = group.iloc[0]

            dados = {
                'ano_calendario': safe_str(first['ano_calendario']),
                'nome_fonte_pagadora': safe_str(first['nome_fonte_pagadora']),
                'cnpj_fonte_pagadora': safe_str(first['cnpj_fonte_pagadora']),
                'nome_fornecedora': safe_str(first['nome_fornecedora']),
                'cnpj_fornecedora': safe_str(first['cnpj_fornecedora']),
                'informacoes_complementares': safe_str(first.get('informacoes_complementares', ''), ''),
                'nome_responsavel': safe_str(first['nome_responsavel']),
                'data_emissao': format_date(first['data_emissao']),
                'tabela_retencoes': [
                    {
                        'mes': safe_str(r['mes']),
                        'codigo': safe_str(r['codigo_retencao']),
                        'valor_pago': format_currency(r['valor_pago']),
                        'valor_retido': format_currency(r['valor_retido']),
                    }
                    for _, r in group.iterrows()
                ],
                'tabela_rendimentos': [
                    {
                        'mes': safe_str(r['mes']),
                        'codigo': safe_str(r['codigo_rendimento']),
                        'descricao': safe_str(r['descricao_rendimento']),
                        'valor_rendimento': format_currency(r['valor_rendimento']),
                        'valor_imposto': format_currency(r['valor_imposto']),
                    }
                    for _, r in group.iterrows()
                ],
            }

            html_string = report_template.render(dados)
            html = HTML(string=html_string, base_url=os.path.abspath(TEMPLATES_DIR))
            pdf_bytes = html.write_pdf()

            nome_fonte = sanitize_filename(dados['nome_fonte_pagadora'])
            nome_forn = sanitize_filename(dados['nome_fornecedora'])
            filename = f"{nome_fonte}-{nome_forn}.pdf"
            zf.writestr(filename, pdf_bytes)

    zip_buffer.seek(0)
    return send_file(
        zip_buffer,
        mimetype='application/zip',
        as_attachment=True,
        download_name='informes.zip'
    )


if __name__ == '__main__':
    app.run(debug=True)
