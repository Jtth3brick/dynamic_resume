import yaml
import argparse
from fpdf import FPDF
import os

class ResumePDF:
    def __init__(self, data, size):
        self.data = data
        self.size = size
        self.heading_font_size = int(24 * self.size)
        self.subheading_font_size = int(12 * self.size)
        self.body_font_size = int(10 * self.size)
        self.cell_height = 5 * self.size
        self.big_line = 1.5 * self.size
        self.small_line = 0.5 * self.size

        self.initialize_pdf()
        
        self.add_name(self.data['name'])
        self.add_contact(self.data['contact'])
        for section in self.data['sections']:
            self.add_section(section)
        
        if self.data.get('qr', {}).get('include', False):
            self.add_qr_code(self.data['qr'])  # Make sure to define this method in the class

        self.generate()

    def initialize_pdf(self):
        self.pdf = FPDF()
        self.pdf.add_page()
        self.pdf.set_draw_color(31, 73, 125)

    def add_name(self, name):
        self.pdf.set_font('Arial', 'B', self.heading_font_size)
        self.pdf.set_text_color(31, 73, 125)
        name_width = self.pdf.get_string_width(name)
        self.pdf.cell(0, 10, name, align='C', ln=1)
    
    def add_header(self, header_title):
        self.pdf.set_text_color(31, 73, 125)
        self.pdf.set_font('Arial', 'B', self.subheading_font_size)
        self.pdf.cell(0, self.body_font_size, header_title, ln=1)
        self.pdf.set_font('Arial', '', self.body_font_size)
        self.pdf.line(10, self.pdf.y, self.pdf.w - 10, self.pdf.y)

        self.pdf.set_text_color(0, 0, 0)
        self.pdf.set_font('Arial', '', self.body_font_size)

    def add_contact(self, contact_data):
        self.pdf.set_font('Arial', '', self.body_font_size)
        self.pdf.set_text_color(0, 0, 0)

        if len(contact_data['contents']) < 1:
            raise ValueError("Contact data is empty")
        contact_info = contact_data['contents'][0]
        for i in range(1, len(contact_data['contents'])):
            contact_info = contact_info + f" {contact_data['rowSeparator']} {contact_data['contents'][i]}"
        
        align = 'C' if 'align' in contact_data and contact_data['align'] == 'center' else 'L'
        self.pdf.multi_cell(0, self.body_font_size, contact_info, align=align)

    def add_section(self, section):
        if section['addHeader']:
            self.add_header(section['name'])

        for item in section['items']:
            self.add_subsection(item)

    def add_subsection(self, subsection):
        if 'title' in subsection:
            title = subsection['title']
            if 'description' in subsection:
                description = subsection['description']
            else:
                description = None
            if 'rightAlign' in subsection:
                rightAlign = subsection['rightAlign']
            else:
                rightAlign = None

            self.add_subsection_title(title, description, rightAlign)
        
        if 'contentType' in subsection and subsection['contentType'] == 'list':
            self.add_subsection_list(subsection['contents'])
        elif 'contentType' in subsection and subsection['contentType'] == 'paragraph':
            self.add_subsection_paragraph(subsection['contents'])
        elif 'contentType' in subsection:
            raise ValueError(f"{subsection['contentType']} is unrecognized as content type.")
        
    def add_subsection_title(self, title, description, rightAlign):
        self.pdf.set_font('Arial', 'B', self.body_font_size)  # Set bold font for project names
        self.pdf.cell(self.pdf.get_string_width(title), self.cell_height, title)
        self.pdf.set_font('Arial', '', self.body_font_size)  # Set regular font for project language
        if description and rightAlign:
            self.pdf.cell(0, self.cell_height, f" | {description}")
            self.pdf.cell(0, self.cell_height, rightAlign, align='R', ln=1)
        elif description:
            self.pdf.cell(0, self.cell_height, f" | {description}", ln=1)
        elif rightAlign:
            self.pdf.cell(0, self.cell_height, rightAlign, align='R', ln=1)
        
    
    def add_subsection_list(self, contents):
        for content in contents:
            self.pdf.cell(5, self.cell_height, '-', ln=0)
            self.pdf.multi_cell(0, self.cell_height, content, align='J')
        self.pdf.ln(self.small_line)
    
    def add_subsection_paragraph(self, contents):
        coursework_list = ', '.join(contents[:-1]) + ', and ' + contents[-1] + '.'
        self.pdf.multi_cell(0, self.cell_height, coursework_list, align='J')

    def generate(self):
        self.pdf.output('resume.pdf')

def parse_arguments():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Generate resume PDF with custom size')
    parser.add_argument('--size', type=float, default=1.0, help='Multiplier for font sizes and line spacing')
    parser.add_argument('--data', action='store_true', help='Set current working directory to data folder')
    args = parser.parse_args()
    return args

def load_yaml_data(file_path):
    # Load YAML data from a file
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data

def main():
    args = parse_arguments()
    if args.data:
        os.chdir('./data')
    else:
        os.chdir('./example_data')
    
    yaml_name = 'resume.yaml'
    data = load_yaml_data(yaml_name)

    ResumePDF(data, args.size)

if __name__ == "__main__":
    main()
