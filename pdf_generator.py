from fpdf import FPDF
from io import BytesIO

def generate_pdf_report(name, numerology_data, human_design_data, birthdate):
    pdf = FPDF()
    pdf.add_page()

    # Title
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Soul Report', ln=True, align='C')
    pdf.ln(10)

    # User Details
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f'Name: {name}', ln=True)
    pdf.cell(0, 10, f'Birthdate: {birthdate}', ln=True)
    pdf.ln(10)

    # Numerology Section
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Numerology Report:', ln=True)
    pdf.set_font('Arial', '', 12)
    for key, value in numerology_data.items():
        pdf.cell(0, 10, f'{key}: {value}', ln=True)
    pdf.ln(10)

    # Human Design Section
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Human Design Report:', ln=True)
    pdf.set_font('Arial', '', 12)
    for key, value in human_design_data.items():
        pdf.cell(0, 10, f'{key}: {value}', ln=True)

    # Save to BytesIO
    pdf_output = BytesIO()
    pdf.output(dest='S').encode('latin1')  # Ensure content is saved as a string
    pdf_output.write(pdf.output(dest='S').encode('latin1'))
    pdf_output.seek(0)
    return pdf_output
