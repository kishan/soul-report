from fpdf import FPDF

def generate_pdf_report(name, numerology_data, human_design_data, birthdate):
    pdf = FPDF()
    pdf.add_page()

    # Title
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Tetralogy Report', ln=True, align='C')
    pdf.ln(10)

    # User Details
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f'Name: {name}', ln=True)
    pdf.cell(0, 10, f'Date of Birth: {birthdate}', ln=True)
    pdf.ln(5)

    # Numerology Section
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Numerology Report:', ln=True)
    pdf.set_font('Arial', '', 12)
    for key, value in numerology_data.items():
        description = get_numerology_description(key, value)
        pdf.cell(0, 10, f'{key}: {value}', ln=True)
        pdf.multi_cell(0, 10, description)
        pdf.ln(5)

    # Human Design Section
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Human Design Report:', ln=True)
    pdf.set_font('Arial', '', 12)
    for key, value in human_design_data.items():
        pdf.cell(0, 10, f'{key}: {value}', ln=True)
    pdf.ln(10)

    # Save PDF
    pdf_output = 'tetralogy_report.pdf'
    pdf.output(pdf_output)
    return pdf_output
