import requests
import streamlit as st

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
