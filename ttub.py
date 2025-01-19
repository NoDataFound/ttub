import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="TikTok Unbanned", layout="wide", page_icon="🎥")

GA_MEASUREMENT_ID = "G-HFPL7QTT20"
ga_tracking_code = f"""
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_MEASUREMENT_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{GA_MEASUREMENT_ID}');
</script>
"""
st.components.v1.html(ga_tracking_code, height=0)

# Modern CSS with dark gray and purple theme
st.markdown("""
    <style>
        body {
            background-color: #121212;
            font-family: 'Poppins', sans-serif;
        }
        .main .block-container {
            max-width: 900px;
            padding: 2rem;
            background: #1e1e1e;
            border: 1px solid #8a2be2; /* Purple border */
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
        }
        h1, h2, h3 {
            color: #8a2be2; /* Purple for headings */
            text-align: center;
        }
        .counter, .ledger-container {
            text-align: center;
            margin-top: 1rem;
            color: #8a2be2; /* Purple for highlights */
        }
        .sidebar .sidebar-content {
            background: #1e1e1e;
            color: white;
        }
        .btn-custom {
            background-color: #8a2be2; /* Purple button */
            color: white;
            padding: 0.5rem 1rem;
            border: none;
            border-radius: 5px;
            font-size: 1rem;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        .btn-custom:hover {
            background-color: #7a1cd2; /* Darker purple on hover */
        }
    </style>
""", unsafe_allow_html=True)

LEDGER_FILE = "hacked_ledger.csv"

def load_ledger(file_path):
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        return pd.DataFrame(columns=["Username", "Timestamp"])

def save_ledger(dataframe, file_path):
    dataframe.to_csv(file_path, index=False)

ledger = load_ledger(LEDGER_FILE)

if "has_pushed_button" not in st.session_state:
    st.session_state["has_pushed_button"] = False

hacked_count = len(ledger)


st.info("Unban TikTok Form")
with st.form("unban_form"):
    username = st.text_input("Enter your TikTok username", placeholder="@yourusername")
    submitted = st.form_submit_button("Unban TikTok")
    if submitted:
        if username:
            hacked_count += 1
            new_entry = {"Username": username, "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            new_entry_df = pd.DataFrame([new_entry])
            ledger = pd.concat([ledger, new_entry_df], ignore_index=True)
            save_ledger(ledger, LEDGER_FILE)
            st.session_state["has_pushed_button"] = True
            st.success(f"Thank you, {username}! Your request has been submitted. 😉")
        else:
            st.warning("Please enter a TikTok username before submitting.")


if st.session_state["has_pushed_button"]:
    st.error(f"{hacked_count} people pushed this button and got hacked")
    st.code("Running Ledger of Hacked Users")
    st.dataframe(ledger)

