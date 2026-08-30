import streamlit as st
import pandas as pd
import random
import json
import os

st.set_page_config(page_title="Biliardino League - Champions & Europa", page_icon="🏆", layout="centered")

# --- STILE GRAFICO CHAMPIONS LEAGUE & EUROPA LEAGUE (DARK & GLOW) ---
st.markdown("""
    <style>
    .main { background: linear-gradient(135deg, #020b2d 0%, #081b4e 50%, #020515 100%); color: #ffffff; }
    
    .champions-banner {
        background: linear-gradient(135deg, #1e3a8a, #3b82f6);
        border: 2px solid #60a5fa;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        color: #ffffff;
        font-size: 1.3em;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 20px;
        box-shadow: 0 0 20px rgba(59, 130, 246, 0.4);
    }

    .europa-banner {
        background: linear-gradient(135deg, #7c2d12, #c2410c);
        border: 2px solid #fb923c;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        color: #ffedd5;
        font-size: 1.3em;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 20px;
        box-shadow: 0 0 20px rgba(234, 88, 12, 0.4);
    }

    .section-header-cl {
        background: linear-gradient(90deg, #1e3a8a, rgba(30,58,138,0.2));
        border-left: 5px solid #3b82f6;
        padding: 10px 15px;
        border-radius: 8px;
        font-weight: 800;
        font-size: 1.1em;
        color: #ffffff;
        margin-top: 20px;
        margin-bottom: 10px;
        letter-spacing: 1px;
    }

    .section-header-el {
        background: linear-gradient(90deg, #9a3412, rgba(154,52,18,0.2));
        border-left: 5px solid #f97316;
        padding: 10px 15px;
        border-radius: 8px;
        font-weight: 800;
        font-size: 1.1em;
        color: #ffffff;
        margin-top: 20px;
        margin-bottom: 10px;
        letter-spacing: 1px;
    }

    .match-card {
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.5);
    }

    .stButton > button {
        width: 100% !important;
        background: linear-gradient(135deg, #3b82f6, #1d4ed8) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border: 1px solid #60a5fa !important;
        border-radius: 8px !important;
        padding: 8px 0px !important;
        box-shadow: 0 4px 6px rgba(59, 130, 246, 0.3);
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #1d4ed8, #1e40af) !important;
    }
    </style>
""", unsafe_allow_html=True)

STATE_FILE = "biliardino_champions_state.json"

def salva_stato():
    data = {
        "teams": st.session_state.teams,
        "phase": st.session_state.phase,
        "matches": st.session_state.matches,
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
                st.session_state.matches = data.get("matches", {})
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
        st.session_state.phase = "setup"  # "setup", "league", "playoffs"
        st.session_state.matches = {}

st.title("⭐ BILIARDINO LEAGUE ⭐")
st.markdown("<p style='text-align: center; color: #93c5fd; font-weight: 600;'>Format Unico Champions & Europa League</p>", unsafe_allow_html=True)

# --- SIDEBAR: GESTIONE & CONFIGURAZIONE ---
st.sidebar.title("⚙️ Gestione Torneo")
admin_pass = st.sidebar.text_input("Codice Admin", type="password")
is_admin = (admin_pass == "0000")

if is_admin:
    st.sidebar.success("Modo Admin Attivo 🔓")
else:
    st.sidebar.info("Inserisci il PIN 0000 per sbloccare la gestione.")

if st.session_state.phase == "setup":
    st.markdown("### 📥 Inserimento Coppie / Squadre")
    st.markdown("Incolla l'elenco delle coppie (es. *I Fenomeni*, *I Badili*, ecc.), una per riga:")
    
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
                    "goal_diff": 0 # Scarti totali
                })
        
        if len(teams_list) >= 8:
            st.session_state.teams = teams_list
            st.session_state.phase = "league"
            salva_stato()
            st.success("Torneo avviato con successo!")
            st.rerun()
        else:
            st.error("Inserisci almeno 8 coppie per avviare il torneo stile Champions.")

elif st.session_state.phase == "league":
    st.markdown("""
        <div class="champions-banner">
            🏆 FASE 1: GIRONE UNICO (LEAGUE PHASE)
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("Regole punteggio: **Vittoria +2 gol (3 pt)** | **Vittoria +1 gol (2 pt)** | **Sconfitta +1 gol (1 pt)** | **Sconfitta netta (0 pt)**")
    
    # Mostra Classifica Attuale in tempo reale
    df_classifica = pd.DataFrame(st.session_state.teams)
    if not df_classifica.empty:
        df_classifica = df_classifica.sort_values(by=["points", "goal_diff"], ascending=[False, False]).reset_index(drop=True)
        df_classifica.index = df_classifica.index + 1
        
        st.markdown("### 📊 Classifica Generale Unica")
        
        # Evidenziamo le fasce Champions (1-24) ed Europa League (25+)
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
                    
                    # Assegnazione punti secondo le regole stabilite
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
    
    # Ordiniamo la classifica finale del girone
    teams_sorted = sorted(st.session_state.teams, key=lambda x: (x["points"], x["goal_diff"]), reverse=True)
    
    # Divisione automatica
    champions_teams = teams_sorted[:24] # Prime 24
    europa_teams = teams_sorted[24:]    # Dalla 25esima in poi
    
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
