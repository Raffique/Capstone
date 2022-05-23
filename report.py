#pip install pdfkit
#sudo apt-get install wkhtmltopdf

"""
person = { 'name': 'Person', 'age': 34 }

tm = Template("My name is {{ per.name }} and I am {{ per.age }}")
# tm = Template("My name is {{ per['name'] }} and I am {{ per['age'] }}")
msg = tm.render(per=person)

print(msg)
"""
import pdfkit
from jinja2 import Template
import pandas as pd


def generate_report(**kwargs):

    output = None

    data ={
    'name': kwargs['name'], 
    'pe_total': kwargs['total'],
    'pe_amount': kwargs['pe'],
    'pe_l_amount': kwargs['left'],
    'pe_c_amount': kwargs['center'],
    'pe_r_amount': kwargs['right'],
    'dataset': kwargs['dataset']
    }

    with open('report.html') as file:
        template = Template(file.read())
        output = template.render(data=data)
        #print(output)

    pdfkit.from_string(output, kwargs['outputdir']+'/report.pdf')
    #pdfkit.from_url('https://www.google.co.in/','shaurya.pdf')
    #pdfkit.from_file(['file1.html', 'file2.html'], 'out.pdf')
    #pdfkit.from_url(['google.com', 'geeksforgeeks.org', 'facebook.com'], 'shaurya.pdf')


