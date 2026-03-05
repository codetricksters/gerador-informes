from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import os
import json

# Define the directory where templates are stored
templates_dir = 'templates'
environment = Environment(loader=FileSystemLoader(templates_dir))
template = environment.get_template("report.html")

# Load data from JSON file
with open("data.json", "r", encoding="utf-8") as f:
    dados = json.load(f)

# Render the HTML string from the template and data
html_string = template.render(dados)

# Create an HTML object from the string
# Setting base_url is important for loading relative assets like images/CSS
html = HTML(string=html_string, base_url=os.path.abspath(templates_dir))

# Write the PDF to a file
html.write_pdf('report.pdf')
print('PDF report.pdf generated successfully.')
