import streamlit as st
import pandas as pd
import random
import json
import os

st.set_page_config(page_title="Biliardino League - Champions & Europa", page_icon="⚽", layout="centered")

# --- STILE GRAFICO CON PATTERN SAGOME OMINI DEL BILIARDINO ---
st.markdown("""
    <style>
    /* Sfondo blu notte con texture SVG ripetuta raffigurante la sagoma stilizzata di un omino del biliardino */
    .stApp {
        background-color: #02091d !important;
        background-image: 
            radial-gradient(circle at 50% 20%, rgba(29, 78, 216, 0.35) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(30, 58, 138, 0.4) 0%, transparent 60%),
            url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='%23ffffff' fill-opacity='0.04'%3E%3Cpath d='M50 12c-5.5 0-10 4.5-10 10 0 3.8 2.2 7.1 5.5 8.7L41 55h-8c-2.8 0-5 2.2-5 5v12c0 2.8 2.2 5 5 5h4l2 18c.2 1.8 1.7 3 3.5 3h11c1.8 0 3.3-1.2 3.5-3l2-18h4c2.8 0 5-2.2 5-5V60c0-2.8-2.2-5-5-5h-8l-4.5-24.3C57.8 19.1 60 15.8 60 12c0-5.5-4.5-10-10-10z'/%3E%3C/g%3E%3C/svg%3E") !important;
        background-attachment: fixed !important;
        color: #ffffff !important;
    }
    
    .main { 
        background: transparent !important; 
    }
    
    .champions-banner {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.9), rgba(30, 58, 138, 0.95));
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
        box-shadow: 0 0 30px rgba(59, 130, 246, 0.6), inset 0 0 15px rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }

    .europa-banner {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.9), rgba(124, 45, 18, 0.95));
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
        box-shadow: 0 0 30px rgba(249, 115, 22, 0.6), inset 0 0 15px rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }

    .section-header-cl {
        background: linear-gradient(90deg, #1d4ed8 0%, rgba(15, 23, 42, 0.8) 100%);
        border-left: 6px solid #60a5fa;
        padding: 12px 16px;
        border-radius: 10px;
        font-weight: 800;
        font-size: 1.15em;
        color: #ffffff;
        margin-top: 25px;
        margin-bottom: 12px;
        letter-spacing: 1.5px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4);
    }

    .section-header-el {
        background: linear-gradient(90deg, #c2410c 0%, rgba(15, 23, 42, 0.8) 100%);
        border-left: 6px solid #fb923c;
        padding: 12px 16px;
        border-radius: 10px;
        font-weight: 800;
        font-size: 1.15em;
        color: #ffffff;
        margin-top: 25px;
        margin-bottom: 12px;
        letter-spacing: 1.5px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4);
    }

    .match-card {
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.6);
        backdrop-filter: blur(10px);
    }

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
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.7);
    }
    </style>
""", unsafe_allow_html=True)

STATE_FILE = "biliardino_champions_state.json"

def salva_stato():
    data = {
        "teams": st.session_state.teams,
        "phase": st.session_state.phase,
        "history": st.session_state.history
    }
    with open(STATE_FILE, "w") as f:
        json.dump(data, f)

def carica_stato():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r") as f:
                data = json.load(f)
                st.session_state.teams = data.get("teams", [])
                st.session_state.phase = data.get("phase", "setup")
                st.session_state.history = data.get("history", [])
                return True
        except:
            return False
    return False

if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.history = []
    if not carica_stato():
        st.session_state.teams = []
        st.session_state.phase = "setup"

st.title("⚽ BILIARDINO LEAGUE ⚽")
st.markdown("<p style='text-align: center; color: #93c5fd; font-weight: 600;'>Format Unico Champions & Europa League</p>", unsafe_allow_html=True)

st.sidebar.title("⚙️ Gestione Torneo")
admin_pass = st.sidebar.text_input("Codice Admin", type="password")
is_admin = (admin_pass == "0000")

if is_admin:
    st.sidebar.success("Modo Admin Attivo 🔓")
else:
    st.sidebar.info("Inserisci il PIN 0000 per sbloccare la gestione.")

if st.session_state.phase == "setup":
    st.markdown("### 📥 Inserimento Coppie / Squadre")
    st.markdown("Incolla l'elenco delle coppie, una per riga:")
    
    input_testo = st.text_area("Elenco Coppie:", height=150, placeholder="Coppia 1: Mario & Luigi\nCoppia 2: Gigi & Sara\n...")
    
    if is_admin and st.button("🚀 Inizia la League Phase (Girone Unico)", type="primary"):
        righe = input_testo.split("\n")
        teams_list = []
        for r in righe:
            nome_pulito = r.strip()
            if nome_pulito:
                teams_list.append({
                    "name": nome_pulito,
                    "points": 0,
                    "played": 0,
                    "goal_diff": 0
                })
        
        if len(teams_list) >= 8:
            st.session_state.teams = teams_list
            st.session_state.phase = "league"
            salva_stato()
            st.success("Torneo avviato con successo!")
            st.rerun()
        else:
            st.error("Inserisci almeno 8 coppie per avviare il torneo.")

elif st.session_state.phase == "league":
    st.markdown("""
        <div class="champions-banner">
            🏆 FASE 1: GIRONE UNICO (LEAGUE PHASE)
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("Regole punteggio: **Vittoria +2 gol (3 pt)** | **Vittoria +1 gol (2 pt)** | **Sconfitta +1 gol (1 pt)** | **Sconfitta netta (0 pt)**")
    
    df_classifica = pd.DataFrame(st.session_state.teams)
    if not df_classifica.empty:
        df_classifica = df_classifica.sort_values(by=["points", "goal_diff"], ascending=[False, False]).reset_index(drop=True)
        df_classifica.index = df_classifica.index + 1
        
        st.markdown("### 📊 Classifica Generale Unica")
        
        def color_zones(row):
            idx = row.name
            if idx <= 24:
                return ['background-color: rgba(30, 58, 138, 0.4)'] * len(row)
            else:
                return ['background-color: rgba(120, 53, 15, 0.4)'] * len(row)

        st.dataframe(df_classifica.style.apply(color_zones, axis=1), use_container_width=True)
        st.markdown("<small>🔵 *Prime 24: Accesso Biliardino League (Champions)* &nbsp;&nbsp;|&nbsp;&nbsp; 🟠 *Dal 25° in poi: Accesso Biliardino League 2 (Europa)*</small>", unsafe_allow_html=True)

    if is_admin:
        st.markdown("---")
        st.markdown("### ✍️ Registra Risultato Partita del Girone")
        with st.form("form_partita"):
            nomi_squadre = [t["name"] for t in st.session_state.teams]
            col_s1, col_s2 = st.columns(2)
            with col_s1:
                sq_a = st.selectbox("Squadra A", nomi_squadre, key="sq_a")
            with col_s2:
                sq_b = st.selectbox("Squadra B", nomi_squadre, key="sq_b")
                
            scarto = st.slider("Scarto reti con cui ha vinto la squadra vincente:", min_value=1, max_value=5, value=1)
            vincente = st.radio("Chi ha vinto?", [sq_a, sq_b], horizontal=True)
            
            submit_match = st.form_submit_button("Registra Risultato e Aggiorna Punti")
            
            if submit_match:
                if sq_a == sq_b:
                    st.error("Le due squadre devono essere differenti!")
                else:
                    perente = sq_b if vincente == sq_a else sq_a
                    punti_vincitore = 3 if scarto >= 2 else 2
                    punti_perdente = 1 if scarto == 1 else 0
                    
                    for t in st.session_state.teams:
                        if t["name"] == vincente:
                            t["points"] += punti_vincitore
                            t["played"] += 1
                            t["goal_diff"] += scarto
                        elif t["name"] == perente:
                            t["points"] += punti_perdente
                            t["played"] += 1
                            t["goal_diff"] -= scarto
                            
                    salva_stato()
                    st.success(f"Risultato registrato! Vittoria a {vincente} (+{punti_vincitore} pt).")
                    st.rerun()

        st.markdown("---")
        if st.button("⚡ Passa alla Fase a Eliminazione Diretta (Playoffs & Tabelloni)", type="primary"):
            if len(st.session_state.teams) < 24:
                st.warning("Servono almeno 24 squadre per separare Champions (24) ed Europa League (resto).")
            else:
                st.session_state.phase = "playoffs"
                salva_stato()
                st.rerun()

elif st.session_state.phase == "playoffs":
    st.markdown("""
        <div class="champions-banner">
            ⭐ FASE 2: TABELLONI FINALI (CHAMPIONS & EUROPA LEAGUE)
        </div>
    """, unsafe_allow_html=True)
    
    teams_sorted = sorted(st.session_state.teams, key=lambda x: (x["points"], x["goal_diff"]), reverse=True)
    
    champions_teams = teams_sorted[:24]
    europa_teams = teams_sorted[24:]
    
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.markdown("""
            <div class="section-header-cl">
                🏆 BILIARDINO LEAGUE (Champions - Top 24)
            </div>
        """, unsafe_allow_html=True)
        for i, t in enumerate(champions_teams):
            st.markdown(f"<div class='match-card'><b>{i+1}°</b> {t['name']} <span style='float:right; color:#60a5fa;'>{t['points']} pt</span></div>", unsafe_allow_html=True)
            
    with col_c2:
        st.markdown("""
            <div class="section-header-el">
                🥈 BILIARDINO LEAGUE 2 (Europa League)
            </div>
        """, unsafe_allow_html=True)
        if europa_teams:
            for i, t in enumerate(europa_teams):
                st.markdown(f"<div class='match-card'><b>{i+25}°</b> {t['name']} <span style='float:right; color:#fb923c;'>{t['points']} pt</span></div>", unsafe_allow_html=True)
        else:
            st.info("Nessuna squadra qualificata in Europa League (meno di 25 partecipanti totali).")

    st.markdown("---")
    if is_admin and st.button("🔄 Reset / Torna al Setup Iniziale"):
        if os.path.exists(STATE_FILE):
            os.remove(STATE_FILE)
        st.session_state.clear()
        st.rerun()
