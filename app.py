import requests
import streamlit as st
from fpdf import FPDF
from datetime import date

def fetch_human_design_report(birthdate, birthtime, location):
    api_url = "https://metal-celerity-441810-f5.ey.r.appspot.com/v1/sample/trial"
    payload = {
        "birthdate": birthdate,
        "birthtime": birthtime,
        "location": location
    }

    try:
        response = requests.post(api_url, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error: Unable to fetch data ({response.status_code})")
            return None
    except Exception as e:
        st.error(f"Exception occurred: {e}")
        return None

def format_birthdate(date):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    day, month, year = date.split('-')
    month_abbr = months[int(month) - 1]
    return f"{int(day):02d}-{month_abbr}-{year}"

def reduce_to_single_digit(number):
    while number > 9 and number not in [11, 22, 33]:  # Keep master numbers
        number = sum(int(digit) for digit in str(number))
    return number

def calculate_life_path_number(birthdate):
    digits = [int(char) for char in birthdate if char.isdigit()]
    return reduce_to_single_digit(sum(digits))

def calculate_birthday_number(birthdate):
    birth_day = int(birthdate.split('-')[2])
    return reduce_to_single_digit(birth_day)

def calculate_destiny_number(full_name):
    letter_to_number = {char: (ord(char) - 96) % 9 or 9 for char in 'abcdefghijklmnopqrstuvwxyz'}
    total = sum(letter_to_number[char] for char in full_name.lower() if char.isalpha())
    return reduce_to_single_digit(total)

def calculate_soul_urge_number(full_name):
    vowels = 'aeiou'
    letter_to_number = {char: (ord(char) - 96) % 9 or 9 for char in 'abcdefghijklmnopqrstuvwxyz'}
    total = sum(letter_to_number[char] for char in full_name.lower() if char in vowels)
    return reduce_to_single_digit(total)

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
        pdf.cell(0, 10, f'{key}: {value}', ln=True)
    pdf.ln(10)

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

# Streamlit interface
st.title("Tetralogy Report")

# Input fields for Numerology and Human Design
name = st.text_input("Enter your full name:")
birthdate_text_input = st.text_input("Enter your birthdate (YYYY-MM-DD):")
birthtime_input = st.time_input("Enter your birth time:", value=None)
location_input = st.selectbox(
    "Select your location:",
    ["New York, United States", "Los Angeles, United States", "Chicago, United States"]
)

if st.button("Generate Report"):
    if birthdate_text_input:
        formatted_birthdate = birthdate_text_input
        formatted_birthdate_human_design = format_birthdate(birthdate_text_input)

        # Numerology Calculations
        numerology_data = {}
        if formatted_birthdate and name:
            numerology_data['Life Path Number'] = calculate_life_path_number(formatted_birthdate)
            numerology_data['Birthday Number'] = calculate_birthday_number(formatted_birthdate)
            numerology_data['Destiny Number'] = calculate_destiny_number(name)
            numerology_data['Soul Urge Number'] = calculate_soul_urge_number(name)

            st.subheader("Numerology Report")
            for key, value in numerology_data.items():
                st.write(f"**{key}:** {value}")
        else:
            st.error("Please fill in your full name and birthdate for Numerology.")

        # Human Design Calculations
        human_design_data = {}
        if formatted_birthdate_human_design and birthtime_input and location_input:
            formatted_birthtime = birthtime_input.strftime("%H:%M")

            st.write("Fetching your Human Design Report...")
            report_data = fetch_human_design_report(formatted_birthdate_human_design, formatted_birthtime, location_input)

            if report_data:
                human_design_data['Type'] = report_data.get('type', 'N/A')
                human_design_data['Profile'] = report_data.get('profile', 'N/A')
                human_design_data['Strategy'] = report_data.get('strategy', 'N/A')
                human_design_data['Authority'] = report_data.get('authority', 'N/A')
                human_design_data['Incarnation Cross'] = report_data.get('incarnation_cross', 'N/A')
                human_design_data['Channels'] = ', '.join(report_data.get('channels_long', []))
                human_design_data['Centers'] = ', '.join(report_data.get('centers', []))

                st.subheader("Human Design Report")
                for key, value in human_design_data.items():
                    st.write(f"**{key}:** {value}")

                # Generate PDF
                pdf_file = generate_pdf_report(name, numerology_data, human_design_data, formatted_birthdate)

                # Provide Download Link
                with open(pdf_file, 'rb') as f:
                    st.download_button(
                        label="Download Your Tetralogy Report",
                        data=f,
                        file_name=pdf_file,
                        mime="application/pdf"
                    )
            else:
                st.error("Failed to retrieve the report.")
        else:
            st.error("Please fill in all the fields for Human Design.")
    else:
        st.error("Please provide your birthdate in the specified format (YYYY-MM-DD).")
