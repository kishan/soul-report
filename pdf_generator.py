from fpdf import FPDF
from io import BytesIO
import unicodedata

class StyledPDF(FPDF):
    def header(self):
        # Add a decorative header
        self.set_fill_color(200, 230, 250)  # Light blue fill
        self.rect(0, 0, 210, 15, 'F')  # Rectangle at the top
        self.set_font('Arial', 'B', 14)
        self.set_text_color(30, 30, 100)
        self.cell(0, 10, 'Soul Report', align='C', ln=True)

    def footer(self):
        # Add footer with page number and branding
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Page {self.page_no()} | Generated by Soul Insights', align='C')

    def add_cover_page(self, name):
        self.add_page()
        # Add a solid background instead of gradient
        self.set_fill_color(220, 245, 255)  # Light blue fill
        self.rect(0, 0, 210, 297, 'F')

        # Title
        self.set_font('Arial', 'B', 28)
        self.set_text_color(0, 102, 204)
        self.cell(0, 20, 'Your Personalized Soul Report', ln=True, align='C')
        self.ln(20)

        # Subtitle
        self.set_font('Arial', '', 16)
        self.cell(0, 10, f'Prepared for: {name}', ln=True, align='C')
        self.ln(10)
        self.cell(0, 10, f'Date: {self.get_date()}', ln=True, align='C')
        self.ln(30)

        # Inspirational quote
        self.set_font('Arial', 'I', 14)
        self.set_text_color(128)
        self.multi_cell(0, 10, '"The cosmos is within us. We are made of star-stuff."', align='C')
        self.ln(10)


    def add_section_title(self, title):
        # Add a section title with a colored banner
        self.set_fill_color(0, 102, 204)  # Blue fill
        self.set_text_color(255, 255, 255)  # White text
        self.set_font('Arial', 'B', 18)
        self.cell(0, 12, title, ln=True, align='L', fill=True)
        self.ln(5)

    def add_key_value(self, key, value):
        # Add key-value pairs with consistent margins
        self.set_font('Arial', '', 12)
        self.set_text_color(0)
        self.cell(50, 10, f'{key}:', border=0, align='L')
        self.set_text_color(0, 102, 204)
        self.cell(0, 10, f'{value}', border=0, ln=True, align='L')

    def add_highlight_box(self, title, content):
        # Add a highlighted box for important insights
        self.set_fill_color(240, 240, 190)  # Light yellow
        self.set_text_color(0)
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, title, ln=True, align='L', fill=True)
        self.set_font('Arial', '', 12)
        self.ln(5)
        self.multi_cell(0, 10, content)
        self.ln(10)

    def get_date(self):
        from datetime import date
        return date.today().strftime('%B %d, %Y')

def sanitize_text(text):
    """Remove or replace unsupported characters in text."""
    return ''.join(
        c if unicodedata.category(c)[0] != 'C' else ' '
        for c in text
    ).replace('"', '"').replace('"', '"').replace('’', "'").replace('‘', "'")

def generate_pdf_report(name, numerology_data, human_design_data, birthdate):
    pdf = StyledPDF()

    # Cover Page
    pdf.add_cover_page(name)

    # Personal Details Section
    pdf.add_section_title('Personal Details')
    pdf.add_key_value('Name', name)
    pdf.add_key_value('Birthdate', birthdate)
    pdf.ln(10)

    # Numerology Section
    pdf.add_section_title('Numerology Report')
    for key, value in numerology_data.items():
        pdf.add_key_value(key, sanitize_text(str(value)))
    pdf.ln(10)

    # Human Design Section
    pdf.add_section_title('Human Design Report')
    for key, value in human_design_data.items():
        pdf.add_key_value(key, sanitize_text(str(value)))
    pdf.ln(10)

    # Summary Section
    pdf.add_highlight_box('Key Insight', 'Your Life Path Number suggests a strong tendency towards creativity and leadership.')

    # Save to BytesIO with latin-1 encoding
    pdf_output = BytesIO()
    pdf_output.write(pdf.output(dest='S').encode('latin-1'))  # Write binary data with latin-1 encoding
    pdf_output.seek(0)
    return pdf_output
