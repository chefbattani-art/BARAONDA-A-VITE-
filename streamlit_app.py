import streamlit as st
import pandas as pd
import random
import json
import os
import re

st.set_page_config(
    page_title="Biliardino Champions League",
    page_icon="⭐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- STILE GRAFICO PREMIUM UEFA CHAMPIONS LEAGUE ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;800;900&display=swap');

    .stApp {
        background: radial-gradient(circle at 50% 10%, #030a1c 0%, #01040f 50%, #000000 100%) !important;
        color: #f8fafc !important;
        font-family: 'Montserrat', sans-serif;
    }
    
    .main { background: transparent !important; }

    /* Header stile TV / Dashboard */
    .champions-top-bar {
        background: linear-gradient(135deg, #06112a 0%, #1d4ed8 50%, #050b18 100%);
        border-bottom: 2px solid #3b82f6;
        padding: 15px 25px;
        border-radius: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 25px;
        box-shadow: 0 0 25px rgba(37, 99, 235, 0.4);
    }

    /* Card Box Standard stile Champions */
    .cl-card {
        background: linear-gradient(135deg, rgba(11, 19, 43, 0.9), rgba(15, 23, 42, 0.95));
        border: 1px solid rgba(59, 130, 246, 0.4);
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5), inset 0 0 10px rgba(59, 130, 246, 0.1);
    }

    /* Box Partita in Corso (Evidenziato) */
    .match-live-box {
        background: linear-gradient(135deg, #0b1d3a 0%, #172554 100%);
        border: 2px solid #60a5fa;
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 0 30px rgba(59, 130, 246, 0.6);
        margin-bottom: 20px;
    }

    /* Bottoni stile Champions */
    div.stButton > button {
        border-radius: 10px;
        font-weight: 800;
        border: 1px solid #93c5fd;
        background: linear-gradient(135deg, #2563eb, #1d4ed8);
        color: #ffffff;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4);
        width: 100% !important;
        text-transform: uppercase;
        padding: 10px;
        letter-spacing: 1px;
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, #1d4ed8, #1e40af);
        border-color: #ffffff;
        box-shadow: 0 0 20px rgba(96, 165, 250, 0.8);
    }
    </style>
""", unsafe_allow_html=True)

DB_FILE = "biliardino_champions_pro.json"

def carica_dati():
    dati_default = {
        "stato": "setup", 
        "coppie": [],
        "partite_a_testa": 6,
        "classifica": {},
        "calendario": [],
        "admin_pin": "0000"
    }
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    return dati_default

def salva_dati(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

if "db" not in st.session_state:
    st.session_state.db = carica_dati()

db = st.session_state.db

# --- SIDEBAR DI NAVIGAZIONE ---
st.sidebar.markdown("### ⚙️ Pannello di Controllo")
admin_pin_input = st.sidebar.text_input("PIN Amministratore", type="password")
is_admin = (admin_pin_input == db["admin_pin"])

if is_admin:
    st.sidebar.success("Modo Admin Sbloccato 🔓")
else:
    st.sidebar.info("Inserisci il PIN 0000 per sbloccare la gestione.")

# Top Bar stile Champions
st.markdown("""
    <div class="champions-top-bar">
        <div><span style="color: #ef4444; font-weight: 900;">● LIVE</span> &nbsp; <b>BILIARDINO CHAMPIONS LEAGUE</b></div>
        <div style="font-size: 0.9em; color: #93c5fd;">Stagione Ufficiale</div>
    </div>
""", unsafe_allow_html=True)

# --- GESTIONE SCHERMATA PRINCIPALE ---
if db["stato"] == "setup":
    st.markdown("### 📥 Registrazione Coppie (Fase Iniziale)")
    with st.form("form_registrazione"):
        c1 = st.text_input("Giocatore 1")
        c2 = st.text_input("Giocatore 2")
        whatsapp_list = st.text_area("📋 Oppure incolla lista da WhatsApp:")
        partite_scelta = st.slider("Partite per coppia nella League Phase:", min_value=3, max_value=10, value=6)
        
        submit_reg = st.form_submit_button("Aggiungi Coppie 🚀")
        
        if submit_reg:
            nuove = []
            if c1.strip() and c2.strip():
                nuove.append(f"{c1.strip().upper()} / {c2.strip().upper()}")
            if whatsapp_list.strip():
                for riga in whatsapp_list.split("\n"):
                    riga_p = riga.strip()
                    if riga_p:
                        riga_p = re.sub(r'^\s*(\d+[\.\)]\s*|-\s*)', '', riga_p).strip()
                        if "/" in riga_p:
                            parti = riga_p.split("/")
                            if len(parti) >= 2:
                                nuove.append(f"{parti[0].strip().upper()} / {parti[1].strip().upper()}")
                        else:
                            parole = riga_p.split()
                            if len(parole) >= 2:
                                meta = len(parole) // 2
                                nuove.append(f"{' '.join(parole[:meta]).upper()} / {' '.join(parole[meta:]).upper()}")

            for n in nuove:
                if n not in db["coppie"]:
                    db["coppie"].append(n)
            
            db["partite_a_testa"] = partite_scelta
            salva_dati(db)
            st.success("Coppie aggiunte correttamente!")
            st.rerun()

    if is_admin and len(db["coppie"]) >= 4:
        st.markdown("---")
        if st.button("⚡ Avvia League Phase", type="primary"):
            db["classifica"] = {cp: {"punti": 0, "gf": 0, "gs": 0, "dr": 0, "partite_giocate": 0} for cp in db["coppie"]}
            coppie_azz = db["coppie"].copy()
            calendario = []
            target_partite = db["partite_a_testa"]
            match_id_counter = 1
            
            accoppiamenti_creati = set()
            for c1 in coppie_azz:
                avversari_possibili = [c2 for c2 in coppie_azz if c2 != c1]
                random.shuffle(avversari_possibili)
                scelti = avversari_possibili[:target_partite]
                for c2 in scelti:
                    pair_key = tuple(sorted([c1, c2]))
                    if pair_key not in accoppiamenti_creati:
                        accoppiamenti_creati.add(pair_key)
                        calendario.append({
                            "id": f"m_{match_id_counter}",
                            "c1": pair_key[0],
                            "c2": pair_key[1],
                            "giocata": False,
                            "gol1": 0,
                            "gol2": 0
                        })
                        match_id_counter += 1

            db["calendario"] = calendario
            db["stato"] = "league"
            salva_dati(db)
            st.success("Girone avviato!")
            st.rerun()

elif db["stato"] == "league":
    # Layout a due colonne stile dashboard televisiva
    col_ sinistra, col_destra = st.columns([1.3, 0.9])

    with col_sinistra:
        st.markdown("### 📊 CLASSIFICA CHAMPIONS LEAGUE")
        classifica_sort = sorted(
            db["classifica"].items(),
            key=lambda x: (x[1]["punti"], x[1]["dr"], x[1]["gf"]),
            reverse=True
        )

        data_tabella = []
        for idx, (cp, st_vals) in enumerate(classifica_sort, 1):
            fascia = "⭐ Top 24" if idx <= 24 else "🟠 EL"
            data_tabella.append({
                "Pos": f"{idx}°",
                "Squadra": cp,
                "Pt": st_vals["punti"],
                "G": st_vals["partite_giocate"],
                "DR": f"{st_vals['dr']:+d}"
            })
        
        st.dataframe(pd.DataFrame(data_tabella), use_container_width=True, height=520, hide_index=True)

    with col_destra:
        st.markdown("### 🔍 CRUSCOTTO COPPIA")
        coppia_selezionata = st.selectbox("Seleziona la tua squadra:", db["coppie"])
        
        if coppia_selezionata:
            squadre_ordinate = [item[0] for item in classifica_sort]
            pos_attuale = squadre_ordinate.index(coppia_selezionata) + 1
            dati_coppia = db["classifica"][coppia_selezionata]
            
            st.markdown(f"""
                <div class="cl-card">
                    <h4 style="margin:0; color:#60a5fa;">⭐ {coppia_selezionata}</h4>
                    <hr style="border-color: rgba(255,255,255,0.1);">
                    <p><b>Posizione:</b> <span style="color:#38bdf8;">{pos_attuale}° posto</span></p>
                    <p><b>Punti:</b> {dati_coppia['punti']} | <b>Giocate:</b> {dati_coppia['partite_giocate']}</p>
                    <p><b>Differenza Reti:</b> {dati_coppia['dr']:+d} (GF: {dati_coppia['gf']} | GS: {dati_coppia['gs']})</p>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("### ⚽ PARTITE DA GIOCARE")
        da_giocare = [m for m in db["calendario"] if not m["giocata"]]
        
        if not da_giocare:
            st.info("Nessuna partita in coda.")
        else:
            m_corrente = da_giocare[0]
            st.markdown(f"""
                <div class="match-live-box">
                    <div style="font-size: 0.9em; color: #93c5fd; margin-bottom: 5px;">PROSSIMA PARTITA IN CODA</div>
                    <div style="font-size: 1.2em; font-weight: 800; color: #ffffff;">
                        {m_corrente['c1']} <span style="color: #f59e0b;">VS</span> {m_corrente['c2']}
                    </div>
                </div>
            """, unsafe_allow_html=True)

            if is_admin:
                with st.form(f"form_match_{m_corrente['id']}"):
                    col_g1, col_g2 = st.columns(2)
                    with col_g1:
                        g1 = st.number_input(f"Gol {m_corrente['c1']}", 0, 20, 0, key=f"g1_{m_corrente['id']}")
                    with col_g2:
                        g2 = st.number_input(f"Gol {m_corrente['c2']}", 0, 20, 0, key=f"g2_{m_corrente['id']}")
                    
                    if st.form_submit_button("Registra Risultato ⚡"):
                        m_corrente["gol1"] = int(g1)
                        m_corrente["gol2"] = int(g2)
                        m_corrente["giocata"] = True
                        
                        diff = abs(g1 - g2)
                        if g1 > g2:
                            vin, per = m_corrente["c1"], m_corrente["c2"]
                            gv, gp = g1, g2
                        elif g2 > g1:
                            vin, per = m_corrente["c2"], m_corrente["c1"]
                            gv, gp = g2, g1
                        else:
                            vin, per = m_corrente["c1"], m_corrente["c2"]
                            diff, gv, gp = 1, g1, g2

                        pt_v = 3 if diff >= 2 else 2
                        pt_p = 0 if diff >= 2 else 1

                        db["classifica"][vin]["punti"] += pt_v
                        db["classifica"][vin]["gf"] += gv
                        db["classifica"][vin]["gs"] += gp
                        db["classifica"][vin]["dr"] += (gv - gp)
                        db["classifica"][vin]["partite_giocate"] += 1

                        db["classifica"][per]["punti"] += pt_p
                        db["classifica"][per]["gf"] += gp
                        db["classifica"][per]["gs"] += gv
                        db["classifica"][per]["dr"] += (gp - gv)
                        db["classifica"][per]["partite_giocate"] += 1

                        salva_dati(db)
                        st.success("Risultato registrato con successo!")
                        st.rerun()

    if is_admin:
        st.markdown("---")
        if st.button("🌟 Passa alla Fase a Eliminazione Diretta (Play-off)", type="primary"):
            db["stato"] = "playoffs"
            salva_dati(db)
            st.rerun()

elif db["stato"] == "playoffs":
    st.markdown("""
        <div style="background: linear-gradient(135deg, #0b132b, #1d4ed8); padding: 20px; border-radius: 14px; text-align: center; border: 2px solid #60a5fa; margin-bottom: 25px;">
            <h2 style="margin:0; color:#ffffff;">⭐ TABELLONE FASE FINALE ⭐</h2>
        </div>
    """, unsafe_allow_html=True)
    
    classifica_sort = sorted(
        db["classifica"].items(),
        key=lambda x: (x[1]["punti"], x[1]["dr"], x[1]["gf"]),
        reverse=True
    )
    squadre = [item[0] for item in classifica_sort]
    
    st.markdown("#### 🏆 Scontro diretto e griglia finale pronta per i match decisivi.")
    for i in range(0, min(len(squadre), 16), 2):
        s1 = squadre[i] if i < len(squadre) else "TBD"
        s2 = squadre[i+1] if i+1 < len(squadre) else "TBD"
        st.markdown(f"""
            <div class="cl-card" style="padding: 12px; display: flex; justify-content: space-between; align-items: center;">
                <b>Match {i//1+1}</b>
                <span style="color: #60a5fa; font-weight: 800;">{s1} vs {s2}</span>
                <span style="font-size: 0.8em; color: #94a3b8;">Fase a Eliminazione</span>
            </div>
        """, unsafe_allow_html=True)

    if is_admin:
        if st.button("🔄 Reset Torneo"):
            if os.path.exists(DB_FILE):
                os.remove(DB_FILE)
            st.session_state.clear()
            st.rerun()
