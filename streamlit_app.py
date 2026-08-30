import streamlit as st
import pandas as pd
import random
import json
import os

st.set_page_config(page_title="Biliardino League - Champions & Europa", page_icon="⭐", layout="centered")

# --- STILE GRAFICO CHAMPIONS LEAGUE (BLU NOTTE STELLATO & GLOW) ---
st.markdown("""
    <style>
    /* Sfondo generale con gradiente blu notte Champions e stelle simulate in CSS */
    .stApp {
        background: radial-gradient(circle at 50% 20%, #1e3a8a 0%, #0b132b 40%, #030712 100%) !important;
        background-attachment: fixed !important;
        color: #ffffff !important;
    }
    
    .main { 
        background: transparent !important; 
    }
    
    .champions-banner {
        background: linear-gradient(135deg, rgba(30, 58, 138, 0.9), rgba(15, 23, 42, 0.95));
        border: 2px solid #3b82f6;
        border-radius: 16px;
        padding: 18px;
        text-align: center;
        color: #ffffff;
        font-size: 1.4em;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 20px;
        box-shadow: 0 0 25px rgba(59, 130, 246, 0.5), inset 0 0 15px rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }

    .europa-banner {
        background: linear-gradient(135deg, rgba(124, 45, 18, 0.9), rgba(15, 23, 42, 0.95));
        border: 2px solid #f97316;
        border-radius: 16px;
        padding: 18px;
        text-align: center;
        color: #ffedd5;
        font-size: 1.4em;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 20px;
        box-shadow: 0 0 25px rgba(249, 115, 22, 0.5), inset 0 0 15px rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }

    .section-header-cl {
        background: linear-gradient(90deg, #1d4ed8 0%, rgba(30, 58, 138, 0.2) 100%);
        border-left: 6px solid #60a5fa;
        padding: 12px 16px;
        border-radius: 10px;
        font-weight: 800;
        font-size: 1.15em;
        color: #ffffff;
        margin-top: 25px;
        margin-bottom: 12px;
        letter-spacing: 1.5px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }

    .section-header-el {
        background: linear-gradient(90deg, #c2410c 0%, rgba(124, 45, 18, 0.2) 100%);
        border-left: 6px solid #fb923c;
        padding: 12px 16px;
        border-radius: 10px;
        font-weight: 800;
        font-size: 1.15em;
        color: #ffffff;
        margin-top: 25px;
        margin-bottom: 12px;
        letter-spacing: 1.5px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }

    .match-card {
        background: rgba(15, 23, 42, 0.75);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 15px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.4);
        backdrop-filter: blur(8px);
    }

    /* Stile pulsanti stile Champions */
    .stButton > button {
        width: 100% !important;
        background: linear-gradient(135deg, #2563eb, #1e40af) !important;
        color: #ffffff !important;
        font-weight: 800 !important;
        border: 1px solid #60a5fa !important;
        border-radius: 10px !important;
        padding: 10px 0px !important;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4);
        letter-spacing: 1px;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #1d4ed8, #1e3a8a) !important;
        border-color: #93c5fd !important;
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.6);
    }

    /* Personalizzazione tabelle per integrarsi con lo sfondo scuro */
    dataframe, table {
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)
