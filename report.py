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

class Reporter:
    def __init__(self):
        self.out = ""
        self.sop_level = ""
        self.study_level = ""
        self.counter = 0
        self.config = {}

        self.sop_results = pd.DataFrame(columns=['root','image','pe_present_on_image','leftsided_pe','central_pe','rightsided_pe'])

        self.study_results = pd.DataFrame(columns=['Name','Detection'])

    
    def study_lvl_adder(self, data):
        self.study_results = pd.concat([self.study_results, pd.DataFrame([data])], ignore_index=True)

    def sop_lvl_adder(self, data):
        self.sop_results = pd.concat([self.sop_results, pd.DataFrame([data])], ignore_index=True)
        print(self.sop_results)

    def sop_concluder(self):
        
        """ self.sop_results.loc[self.sop_results['pe_present_on_image'] >= self.config['probability'] / 100, 'pe_present_on_image'] = 1
        self.sop_results.loc[self.sop_results['pe_present_on_image'] < self.config['probability'] / 100, 'pe_present_on_image'] = 0

        self.sop_results.loc[self.sop_results['leftsided_pe'] >= self.config['probability'] / 100, 'leftsided_pe'] = 1
        self.sop_results.loc[self.sop_results['leftsided_pe'] < self.config['probability'] / 100, 'leftsided_pe'] = 0

        self.sop_results.loc[self.sop_results['central_pe'] >= self.config['probability'] / 100, 'central_pe'] = 1
        self.sop_results.loc[self.sop_results['central_pe'] < self.config['probability'] / 100, 'central_pe'] = 0

        self.sop_results.loc[self.sop_results['rightsided_pe'] >= self.config['probability'] / 100, 'rightsided_pe'] = 1
        self.sop_results.loc[self.sop_results['rightsided_pe'] < self.config['probability'] / 100, 'rightsided_pe'] = 0 """

        #self.root = self.sop_results.iloc[0]['root']
        for idx, el in self.sop_results.iterrows():
            self.root = el['root']
            break
        self.amount = len(self.sop_results.index)
        self.pe = self.sop_results['pe_present_on_image'].sum()
        self.left = self.sop_results['leftsided_pe'].sum()
        self.central = self.sop_results['central_pe'].sum()
        self.right = self.sop_results['rightsided_pe'].sum()
        self.dataset = self.sop_results.values.tolist()

        detect = ''
        if self.pe == 0:
            detect = "NO PE"
        elif self.pe >= 1 and (self.left == 0 or self.central == 0 or self.right == 0):
            detect = "NO PE"
        elif self.pe in range(5):
            detect = "LOW PE"
        else:
            detect = "HIGH PE"
        
        data = {'Name': self.root, 'Detection': detect}
        self.study_lvl_adder(data)




    def reset_study(self):
        self.study_results = pd.DataFrame(columns=['Name','Detection'])
        self.sop_results = pd.DataFrame(columns=['root','image','pe_present_on_image','leftsided_pe','central_pe','rightsided_pe'])

    def reset_sop(self):
        self.sop_results = pd.DataFrame(columns=['root','image','pe_present_on_image','leftsided_pe','central_pe','rightsided_pe'])


    def generate_sop_report(self, **kwargs):

        output = None

        """ data ={
        'name': kwargs['name'], 
        'pe_total': kwargs['total'],
        'pe_amount': kwargs['pe'],
        'pe_l_amount': kwargs['left'],
        'pe_c_amount': kwargs['center'],
        'pe_r_amount': kwargs['right'],
        'dataset': kwargs['dataset']
        } """

        data ={
            'name': self.root, 
            'pe_total': self.amount,
            'pe_amount': self.pe,
            'pe_l_amount': self.left,
            'pe_c_amount': self.central,
            'pe_r_amount': self.right,
            'dataset': self.dataset
        }

        with open('report.html') as file:
            template = Template(file.read())
            output = template.render(data=data)
            #print(output)

        pdfkit.from_string(output, kwargs['outputdir']+'/'+self.root+'-report.pdf')
        #pdfkit.from_url('https://www.google.co.in/','shaurya.pdf')
        #pdfkit.from_file(['file1.html', 'file2.html'], 'out.pdf')
        #pdfkit.from_url(['google.com', 'geeksforgeeks.org', 'facebook.com'], 'shaurya.pdf')

        self.sop_results.to_csv(kwargs['outputdir']+"/"+self.root+"-report.csv")

    def generate_study_report(self, **kwargs):
        pass

        output = None

        data = self.study_results.values.tolist()
        self.study_results.to_csv(kwargs['outputdir']+"/report01.csv")
        print(data)

        """ with open('full-report.html') as file:
            template = Template(file.read())
            output = template.render(data=data)

        pdfkit.from_string(output, kwargs['outputdir']+'/full-report.pdf') """


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

    


