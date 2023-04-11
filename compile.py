import yaml
import argparse
from fpdf import FPDF
from qr_code import create_qr_code

# Load YAML data
with open('resume.yaml', 'r') as file:
    data = yaml.safe_load(file)

# Command-line arguments
parser = argparse.ArgumentParser(description='Generate resume PDF with custom size')
parser.add_argument('--size', type=float, default=1.0, help='Multiplier for font sizes and line spacing')
args = parser.parse_args()

# Set font sizes and line spacing based on the size argument
HEADING_FONT_SIZE = int(24 * args.size)
SUBHEADING_FONT_SIZE = int(12 * args.size)
BODY_FONT_SIZE = int(10 * args.size)
LINE_SPACING = 1.5 * args.size
CELL_HEIGHT = 5 * args.size
qr_dim = data['qr']['dim'] * 0.3 *  args.size

def makeHeader(fpdf, name):
    fpdf.set_text_color(31, 73, 125)
    fpdf.set_font('Arial', 'B', SUBHEADING_FONT_SIZE)
    fpdf.cell(0, CELL_HEIGHT, name, ln=1)
    fpdf.set_font('Arial', '', BODY_FONT_SIZE)
    fpdf.line(10, pdf.y, pdf.w - 10, pdf.y)
    fpdf.line(10, pdf.y, pdf.w - 10, pdf.y)
    fpdf.ln(LINE_SPACING)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Arial', '', BODY_FONT_SIZE)

# Create PDF document
pdf = FPDF()
pdf.add_page()

pdf.set_draw_color(31, 73, 125)

# Set font and size for headings and body text
pdf.set_font('Arial', 'B', HEADING_FONT_SIZE)
pdf.set_text_color(31, 73, 125)
# Center name
name_width = pdf.get_string_width(data['name'])
pdf.cell(0, 10, data['name'], align='C', ln=1)
pdf.set_font('Arial', '', BODY_FONT_SIZE)

# Add contact info
pdf.set_text_color(0, 0, 0)
contact_info = f"{data['phone']} | {data['email']} | {data['linkedin']} | {data['github']}"
contact_width = pdf.get_string_width(contact_info)
pdf.multi_cell(0, CELL_HEIGHT, contact_info, align='C')
pdf.ln(LINE_SPACING * 2)

# Add education section
makeHeader(pdf, 'EDUCATION')
pdf.cell(pdf.get_string_width(f"{data['education'][0]['institution']} | {data['education'][0]['location']}"), CELL_HEIGHT, f"{data['education'][0]['institution']} | {data['education'][0]['location']}", ln=0)

# Include the appropriate GPA based on gpa_type
gpa_type = data['education'][0]['gpa_type']
if gpa_type == 'general_gpa':
    gpa_label = 'GPA'
    gpa_value = data['education'][0]['general_gpa']
elif gpa_type == 'technical_gpa':
    gpa_label = 'Technical GPA'
    gpa_value = data['education'][0]['technical_gpa']
pdf.cell(0, CELL_HEIGHT, f"; {gpa_label}: {gpa_value}", ln=0)

pdf.cell(0, CELL_HEIGHT, f"Grad: {data['education'][0]['graduation']}", align='R', ln=1)
for degree in data['education'][0]['degree']:
    pdf.cell(5)
    pdf.cell(0, CELL_HEIGHT, f"- {degree}", ln=1)
pdf.ln(LINE_SPACING)

# Add relevant coursework section
makeHeader(pdf, 'RELEVANT COURSEWORK')
coursework_list = ', '.join(data['education'][0]['coursework'][:-1]) + ', and ' + data['education'][0]['coursework'][-1] + '.'
pdf.multi_cell(0, 5, coursework_list, align='J')
pdf.ln(LINE_SPACING)


# Add experiences section
makeHeader(pdf, 'EXPERIENCES')
for exp in data['experience']:
    pdf.set_font('Arial', 'B', BODY_FONT_SIZE)  # Set bold font for company names
    pdf.cell(pdf.get_string_width(exp['company']), CELL_HEIGHT, exp['company'])
    pdf.set_font('Arial', '', BODY_FONT_SIZE)  # Set regular font for position
    pdf.cell(0, CELL_HEIGHT, f" | {exp['position']}")
    pdf.cell(0, CELL_HEIGHT, f"{exp['start']} - {exp['end']}", align='R', ln=1)
    for resp in exp['responsibilities']:
        pdf.cell(5, CELL_HEIGHT, '-', ln=0)
        pdf.multi_cell(0, CELL_HEIGHT, resp, align='J')
    pdf.ln(LINE_SPACING)

# Add projects section
makeHeader(pdf, 'PROJECTS')
for project in data['projects']:
    pdf.set_font('Arial', 'B', BODY_FONT_SIZE)  # Set bold font for project names
    pdf.cell(pdf.get_string_width(project['name']), CELL_HEIGHT, project['name'])
    pdf.set_font('Arial', '', BODY_FONT_SIZE)  # Set regular font for project language
    pdf.cell(0, CELL_HEIGHT, f" | {project['language']}")
    pdf.cell(0, CELL_HEIGHT, f"{project['start']} - {project['end']}", align='R', ln=1)
    for desc in project['description']:
        pdf.cell(5, 5, '-', ln=0)
        pdf.multi_cell(0, CELL_HEIGHT, desc, align='J')
    pdf.ln(LINE_SPACING)

# Add skills section
makeHeader(pdf, 'SKILLS')
for skill in data['skills']:
    for category in skill:
        pdf.set_font('Arial', 'B', BODY_FONT_SIZE) # Set bold font for category
        pdf.cell(pdf.get_string_width(f"{category}: "), CELL_HEIGHT, f"{category}: ")
        pdf.set_font('Arial', '', BODY_FONT_SIZE) # Set regular font for skills
        pdf.multi_cell(0, CELL_HEIGHT, f"{skill[category]}")
pdf.ln(LINE_SPACING)

# Add qr code
if data['qr']['include']:
    qr_file_path = 'qr.png'
    qr_link = data['qr']['link']
    create_qr_code()
    pdf.image(qr_file_path, x=pdf.w-qr_dim-10, y=pdf.h-qr_dim-10, w=qr_dim, h=qr_dim)


# Generate PDF content
pdf_content = pdf.output(dest='S').encode('latin-1')

# Write PDF to file
with open('resume.pdf', 'wb') as file:
    file.write(pdf_content)