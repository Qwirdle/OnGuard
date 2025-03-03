from docxtpl import DocxTemplate
from os import path

# Generates/fills out a certification for a user request, and gets it ready for flask to sned out
def genCert(name, date):
    tpl = DocxTemplate(path.abspath("static\OnGuard Online Safety Certification.docx"))

    context = {
        'name': name,
        'date': date
    }

    tpl.render(context)

    return tpl