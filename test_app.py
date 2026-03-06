import io
import zipfile

import pandas as pd
import pytest

from app import app


BASE_ROW = {
    'ano_calendario': '2025',
    'nome_fonte_pagadora': 'EMPRESA EXEMPLO S.A.',
    'cnpj_fonte_pagadora': '00.000.000/0001-00',
    'nome_fornecedora': 'FORNECEDOR EXEMPLO LTDA',
    'cnpj_fornecedora': '00.000.000/0001-00',
    'informacoes_complementares': '',
    'nome_responsavel': 'JOAO DA SILVA',
    'data_emissao': '28/02/2025',
}


def make_excel(rows):
    buf = io.BytesIO()
    pd.DataFrame(rows).to_excel(buf, sheet_name='Informes', index=False)
    buf.seek(0)
    return buf


def post_excel(client, rows):
    excel_buf = make_excel(rows)
    return client.post(
        '/generate',
        data={'excel_file': (excel_buf, 'test.xlsx')},
        content_type='multipart/form-data',
    )


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c


def test_no_file_returns_400(client):
    response = client.post('/generate', data={}, content_type='multipart/form-data')
    assert response.status_code == 400


def test_single_supplier_returns_zip_with_one_pdf(client):
    rows = [
        {**BASE_ROW, 'mes': 'Jan', 'tipo': 'retencao', 'codigo': '5952',
         'descricao': '', 'valor': 1000.00, 'valor_retido': 10.00},
        {**BASE_ROW, 'mes': 'Jan', 'tipo': 'rendimento', 'codigo': '1708',
         'descricao': 'Remuneração de serviços profissionais', 'valor': 1000.00, 'valor_retido': 15.00},
    ]
    response = post_excel(client, rows)

    assert response.status_code == 200
    assert response.mimetype == 'application/zip'

    with zipfile.ZipFile(io.BytesIO(response.data)) as zf:
        names = zf.namelist()
        assert len(names) == 1
        assert names[0].endswith('.pdf')
        assert len(zf.read(names[0])) > 0


def test_multiple_suppliers_produce_separate_pdfs(client):
    supplier_a = {**BASE_ROW, 'nome_fornecedora': 'FORNECEDOR A LTDA', 'cnpj_fornecedora': '11.111.111/0001-11'}
    supplier_b = {**BASE_ROW, 'nome_fornecedora': 'FORNECEDOR B LTDA', 'cnpj_fornecedora': '22.222.222/0001-22'}

    rows = [
        {**supplier_a, 'mes': 'Jan', 'tipo': 'retencao', 'codigo': '5952',
         'descricao': '', 'valor': 500.00, 'valor_retido': 5.00},
        {**supplier_b, 'mes': 'Fev', 'tipo': 'rendimento', 'codigo': '1708',
         'descricao': 'Remuneração de serviços', 'valor': 800.00, 'valor_retido': 12.00},
    ]
    response = post_excel(client, rows)

    assert response.status_code == 200
    with zipfile.ZipFile(io.BytesIO(response.data)) as zf:
        assert len(zf.namelist()) == 2


def test_tipo_retencao_only(client):
    rows = [
        {**BASE_ROW, 'mes': 'Mar', 'tipo': 'retencao', 'codigo': '5952',
         'descricao': '', 'valor': 2000.00, 'valor_retido': 20.00},
    ]
    response = post_excel(client, rows)
    assert response.status_code == 200
    with zipfile.ZipFile(io.BytesIO(response.data)) as zf:
        assert len(zf.namelist()) == 1


def test_tipo_rendimento_only(client):
    rows = [
        {**BASE_ROW, 'mes': 'Abr', 'tipo': 'rendimento', 'codigo': '1708',
         'descricao': 'Serviços de TI', 'valor': 3000.00, 'valor_retido': 45.00},
    ]
    response = post_excel(client, rows)
    assert response.status_code == 200
    with zipfile.ZipFile(io.BytesIO(response.data)) as zf:
        assert len(zf.namelist()) == 1


def test_pdf_filename_uses_supplier_names(client):
    rows = [
        {**BASE_ROW, 'mes': 'Mai', 'tipo': 'retencao', 'codigo': '5952',
         'descricao': '', 'valor': 100.00, 'valor_retido': 1.00},
    ]
    response = post_excel(client, rows)

    with zipfile.ZipFile(io.BytesIO(response.data)) as zf:
        name = zf.namelist()[0]
        assert 'EMPRESA EXEMPLO' in name
        assert 'FORNECEDOR EXEMPLO' in name
