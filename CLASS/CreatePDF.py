from jinja2 import Environment, FileSystemLoader
import json
import pdfkit
from CRUD.crud import prepararExportDataJson

rutaJson = 'static/json/pdf.json'
class CreatePDF():
    def __init__(self, ruta_template):
        env = Environment(loader=FileSystemLoader(ruta_template))
        template = env.get_template('PDF.html')
        prepararExportDataJson()
        with open(rutaJson, 'r') as file:
            info = json.load(file)
        html = template.render(data=info)
        pdfkit.from_string(html, 'static/pdf/Reportes.pdf')
