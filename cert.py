from docxtpl import DocxTemplate
from os import path

def genCert(name, date):
    tpl = DocxTemplate(path.abspath("static\SecureMe Online Safety Certification.docx"))

    context = {
        'name': name,
        'date': date
    }

    tpl.render(context)

    return tpl