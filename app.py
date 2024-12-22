import requests
import streamlit as st
from fpdf import FPDF
import random
from datetime import time

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

def get_numerology_description(calculation, number):
    descriptions = {
        "Life Path Number": (
            "The Life Path Number represents your life's purpose and the lessons you are here to learn.",
            {
                1: "You are a natural leader, independent, and ambitious.",
                2: "You are cooperative, diplomatic, and seek harmony.",
                3: "You are creative, expressive, and bring joy to others.",
                4: "You are disciplined, practical, and value stability.",
                5: "You are adventurous, dynamic, and love freedom.",
                6: "You are nurturing, responsible, and family-oriented.",
                7: "You are introspective, analytical, and spiritual.",
                8: "You are ambitious, goal-oriented, and business-minded.",
                9: "You are compassionate, humanitarian, and idealistic."
            }
        ),
        "Birthday Number": (
            "The Birthday Number reveals a special talent or skill you bring into this life.",
            {
                1: "You are self-reliant and thrive in pioneering efforts.",
                2: "You excel in teamwork and fostering relationships.",
                3: "Your charm and wit inspire others.",
                4: "You have a gift for building and organizing.",
                5: "Your versatility and adaptability bring unique insights.",
                6: "You bring care and responsibility to those around you.",
                7: "Your curiosity drives deep exploration and understanding.",
                8: "You possess natural authority and business acumen.",
                9: "Your compassion and vision inspire change."
            }
        ),
        "Destiny Number": (
            "The Destiny Number reveals your ultimate goals and the direction you are destined to follow.",
            {
                1: "You are destined to be a trailblazer and innovator.",
                2: "You are meant to create balance and partnerships.",
                3: "Your destiny involves creativity and communication.",
                4: "You are here to establish order and systems.",
                5: "Your path involves exploration and transformation.",
                6: "You are destined to nurture and heal others.",
                7: "You seek truth, knowledge, and spiritual growth.",
                8: "You are destined for leadership and material success.",
                9: "Your path is about giving and making a global impact."
            }
        ),
        "Soul Urge Number": (
            "The Soul Urge Number reveals your inner desires and what truly motivates you.",
            {
                1: "You desire independence and personal achievement.",
                2: "You are driven by harmony and emotional connections.",
                3: "You long for creative expression and joy.",
                4: "You value security and hard work.",
                5: "You crave freedom and new experiences.",
                6: "You are motivated by love, care, and family.",
                7: "You seek inner peace and spiritual enlightenment.",
                8: "You are driven by power and financial stability.",
                9: "You desire to help others and make a difference."
            }
        )
    }

    if calculation in descriptions:
        short_description, number_meanings = descriptions[calculation]
        specific_meaning = number_meanings.get(number, "You have a unique path that combines diverse qualities.")
        return f"{short_description}\n{specific_meaning}"
    else:
        return "Description not available for this calculation."

# Streamlit interface
st.title("Tetralogy Report")


# Generate random values
random_name = random.choice(["Emily Carter", "Michael Anderson", "Sophia Martinez", "Ethan Turner", "Olivia White", "Benjamin Harris", "Isabella King", "Lucas Scott", "Mia Taylor", "Alexander Wilson" ])
random_birthdate = f"{random.randint(1970, 2005)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
random_birthtime = time(random.randint(0, 23), random.randint(0, 59))

# Input fields for Numerology and Human Design with random defaults
name = st.text_input("Enter your full name:", value=random_name)
birthdate_text_input = st.text_input("Enter your birthdate (YYYY-MM-DD):", value=random_birthdate)
birthtime_input = st.time_input("Enter your birth time:", value=random_birthtime)
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
                description = get_numerology_description(key, value)
                # Split explanation and meaning, ensuring clarity with a blank line
                explanation, meaning = description.split('\n', 1)
                st.write(f"**{key}:** {value}")
                st.write(explanation)
                st.write("")  # Add a blank line
                st.write(meaning)
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
