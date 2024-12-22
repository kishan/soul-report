import streamlit as st
import random
from datetime import time

from numerology import calculate_life_path_number, calculate_birthday_number, calculate_destiny_number, calculate_soul_urge_number, get_numerology_description
from human_design import fetch_human_design_report
from pdf_generator import generate_pdf_report

def format_birthdate(date):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    day, month, year = date.split('-')
    month_abbr = months[int(month) - 1]
    return f"{int(day):02d}-{month_abbr}-{year}"

# Streamlit interface
st.title("Tetralogy Report")

# Generate random default values
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
