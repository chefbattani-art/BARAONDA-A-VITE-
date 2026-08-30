import streamlit as st
import pandas as pd
import random
import json
import os
import re

st.set_page_config(
    page_title="Biliardino League - Champions Edition",
    page_icon="⭐",
    layout="wide", # Layout largo per valorizzare al massimo la classifica completa
    initial_sidebar_state="expanded",
)

# --- STILE GRAFICO CHAMPIONS LEAGUE PREMIUM & IMMERSIVO ---
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at 50% 10%, #03071e 0%, #02091d 40%, #000208 100%) !important;
        color: #f1f5f9 !important;
        font-family: 'Montserrat', 'Segoe UI', Roboto, sans-serif;
    }
    
    .main { background: transparent !important; }

    /* Header ufficiale stile Champions */
    .champions-header {
        background: linear-gradient(135deg, #020617 0%, #1e3a8a 50%, #020617 100%);
        border: 2px solid #3b82f6;
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        color: #ffffff;
        font-size: 1.8em;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 3px;
        margin-bottom: 25px;
        box-shadow: 0 0 40px rgba(59, 130, 246, 0.5), inset 0 0 20px rgba(255, 255, 255, 0.1);
    }

    /* Box riepilogo coppia dinamico */
    .coppia-box {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(30, 58, 138, 0.9));
        border: 2px solid #60a5fa;
        border-radius: 16px;
        padding: 22px;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(37, 99, 235, 0.4);
    }

    /* Card contenuti moderni */
    .cyber-card {
        background: rgba(15, 23, 42, 0.9);
        border: 1px solid rgba(96, 165, 250, 0.3);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.7);
        backdrop-filter: blur(12px);
    }

    /* Bottoni stile Champions */
    div.stButton > button {
        border-radius: 12px;
        font-weight: 800;
        border: 1px solid #93c5fd;
        background: linear-gradient(135deg, #2563eb, #1d4ed8, #1e3a8a);
        color: #ffffff;
        box-shadow: 0 4px 20px rgba(37, 99, 235, 0.5);
        width: 100% !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        padding: 10px;
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, #1d4ed8, #1e40af, #1e3a8a);
        border-color: #ffffff;
        box-shadow: 0 6px 25px rgba(59, 130, 246, 0.8);
    }
    
    /* Personalizzazione tabelle Streamlit */
    dataframe, table {
        width: 100% !important;
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

# --- SIDEBAR & ADMIN ---
st.sidebar.title("⚙️ Gestione Torneo")
admin_pin_input = st.sidebar.text_input("PIN Amministratore", type="password")
is_admin = (admin_pin_input == db["admin_pin"])

if is_admin:
    st.sidebar.success("Modo Admin Attivo 🔓")
else:
    st.sidebar.info("Inserisci il PIN 0000 per sbloccare la gestione.")

st.markdown("""
    <div class="champions-header">
        ⭐ BILIARDINO LEAGUE - THE CHAMPIONS ⭐
    </div>
""", unsafe_allow_html=True)

# --- RIEPILOGO COPPIA SEMPRE IN ALTO (SLIDE DEDICATO) ---
if db["stato"] in ["league", "playoffs"] and db["coppie"]:
    st.markdown("### 🔍 CRUSCOTTO PERSONALE COPPIA")
    coppia_selezionata = st.selectbox("Seleziona la tua coppia per visualizzare lo stato:", db["coppie"], label_visibility="collapsed")
    
    if coppia_selezionata:
        classifica_sort = sorted(
            db["classifica"].items(),
            key=lambda x: (x[1]["punti"], x[1]["dr"], x[1]["gf"]),
            reverse=True
        )
        squadre_ordinate = [item[0] for item in classifica_sort]
        pos_attuale = squadre_ordinate.index(coppia_selezionata) + 1
        dati_coppia = db["classifica"][coppia_selezionata]
        
        if pos_attuale <= 24:
            zona_testo = "⭐ Zona Champions League (Top 24)"
            badge_color = "#3b82f6"
        else:
            zona_testo = "🟠 Zona Europa League (Dalla 25ª in giù)"
            badge_color = "#f97316"

        st.markdown(f"""
            <div class="coppia-box">
                <h3 style="margin:0; color:#93c5fd; font-weight:900; letter-spacing:1px;">⭐ {coppia_selezionata}</h3>
                <hr style="border-color: rgba(255,255,255,0.2); margin: 12px 0;">
                <p style="font-size: 1.1em; margin-bottom: 8px;"><b>Posizione Attuale:</b> <span style="color: {badge_color}; font-weight: bold;">{pos_attuale}° posto</span> ({zona_testo})</p>
                <p style="margin:0;"><b>Punti:</b> {dati_coppia['punti']} | <b>Partite Giocate:</b> {dati_coppia['partite_giocate']} | <b>Differenza Reti:</b> {dati_coppia['dr']:+d} (GF: {dati_coppia['gf']} | GS: {dati_coppia['gs']})</p>
            </div>
        """, unsafe_allow_html=True)

        # Mini classifica di riferimento attorno alla coppia
        idx_coppia = squadre_ordinate.index(coppia_selezionata)
        inizio = max(0, idx_coppia - 2)
        fine = min(len(squadre_ordinate), idx_coppia + 3)
        mini_list = squadre_ordinate[inizio:fine]
        
        st.markdown("#### 📊 Riferimento di Classifica Diretto")
        mini_data = []
        for cp in mini_list:
            p = squadre_ordinate.index(cp) + 1
            st_val = db["classifica"][cp]
            evidenzia = " 👉 [LA TUA COPPIA]" if cp == coppia_selezionata else ""
            mini_data.append({
                "Pos": f"{p}°",
                "Coppia": cp + evidenzia,
                "Pt": st_val["punti"],
                "DR": f"{st_val['dr']:+d}"
            })
        st.dataframe(pd.DataFrame(mini_data), use_container_width=True, hide_index=True)

        # Partite della coppia (In coda / Disputate)
        partite_coppia = [m for m in db["calendario"] if m["c1"] == coppia_selezionata or m["c2"] == coppia_selezionata]
        partite_in_attesa = [m for m in partite_coppia if not m["giocata"]]
        partite_disputate = [m for m in partite_coppia if m["giocata"]]

        col_p1, col_p2 = st.columns(2)
        with col_p1:
            st.markdown(f"#### ⏳ Partite in Coda / Da Fare ({len(partite_in_attesa)})")
            if not partite_in_attesa:
                st.info("Nessuna partita in coda!")
            else:
                for m in partite_in_attesa:
                    avversario = m["c2"] if m["c1"] == coppia_selezionata else m["c1"]
                    st.markdown(f"- Contro: **{avversario}**")

        with col_p2:
            st.markdown(f"#### ✅ Partite Disputate ({len(partite_disputate)})")
            if not partite_disputate:
                st.info("Nessuna partita giocata.")
            else:
                for m in partite_disputate:
                    avversario = m["c2"] if m["c1"] == coppia_selezionata else m["c1"]
                    if m["c1"] == coppia_selezionata:
                        miei_gol, suoi_gol = m["gol1"], m["gol2"]
                    else:
                        miei_gol, suoi_gol = m["gol2"], m["gol1"]
                    
                    esito = "🟢" if miei_gol > suoi_gol else ("🔴" if miei_gol < suoi_gol else "🟡")
                    st.markdown(f"- {esito} vs **{avversario}**: **{miei_gol} - {suoi_gol}**")

        st.markdown("---")

# --- FASE 1: SETUP E ISCRIZIONI ---
if db["stato"] == "setup":
    st.markdown("### 📥 Registrazione Coppie")
    st.markdown("Inserisci le coppie manualmente o incolla la lista da WhatsApp.")

    with st.form("form_registrazione"):
        c1 = st.text_input("Giocatore 1")
        c2 = st.text_input("Giocatore 2")
        whatsapp_list = st.text_area("📋 Oppure incolla lista WhatsApp:")
        partite_scelta = st.slider("Partite casuali per ogni coppia nella League Phase:", min_value=3, max_value=10, value=6)
        
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

            aggiunte = 0
            for n in nuove:
                if n not in db["coppie"]:
                    db["coppie"].append(n)
                    aggiunte += 1
            
            db["partite_a_testa"] = partite_scelta
            salva_dati(db)
            st.success(f"Aggiunte {aggiunte} coppie con successo!")
            st.rerun()

    st.markdown("---")
    st.markdown(f"### 📋 Elenco Coppie Iscritte ({len(db['coppie'])})")
    if not db["coppie"]:
        st.info("Nessuna coppia iscritta.")
    else:
        for idx, cp in enumerate(db["coppie"], 1):
            col_i1, col_i2 = st.columns([0.85, 0.15])
            with col_i1:
                st.markdown(f"<div style='padding:8px; background:rgba(255,255,255,0.05); border-radius:8px; margin-bottom:5px;'><b>{idx}.</b> ⚽ {cp}</div>", unsafe_allow_html=True)
            with col_i2:
                if is_admin and st.button("🗑️", key=f"del_{idx}"):
                    db["coppie"].remove(cp)
                    salva_dati(db)
                    st.rerun()

    if is_admin and len(db["coppie"]) >= 4:
        st.markdown("---")
        if st.button("⚡ Avvia League Phase (Girone Unico)", type="primary"):
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
            st.success("Calendario e Girone Unico generati con successo!")
            st.rerun()

# --- FASE 2: LEAGUE PHASE (GIRONE UNICO COMPLETO ED ESPANSO) ---
elif db["stato"] == "league":
    st.markdown("""
        <div class="champions-header">
            🏆 LEAGUE PHASE - GIRONE UNICO UFFICIALE
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="cyber-card">
            <b>Regolamento Punteggio Scarti:</b><br>
            • <b>Vittoria con 2+ gol di scarto:</b> 3 punti alla vincente, 0 alla perdente.<br>
            • <b>Vittoria di misura (1 gol di scarto):</b> 2 punti alla vincente, 1 punto alla perdente.<br>
            • <span style="color:#60a5fa;"><b>Prime 24 in classifica:</b></span> Accesso diretto a Champions League (evidenziate in blu stellato).<br>
            • <span style="color:#f97316;"><b>Dalla 25ª in giù:</b></span> Accesso a Europa League (evidenziate in arancione).
        </div>
    """, unsafe_allow_html=True)

    classifica_sort = sorted(
        db["classifica"].items(),
        key=lambda x: (x[1]["punti"], x[1]["dr"], x[1]["gf"]),
        reverse=True
    )

    st.markdown("### 📊 CLASSIFICA GENERALE COMPLETA")
    
    def colora_posizioni(row):
        idx = row.name
        if idx < 24:
            return ['background-color: rgba(29, 78, 216, 0.35); color: #ffffff; font-weight: 500;'] * len(row)
        else:
            return ['background-color: rgba(154, 52, 18, 0.35); color: #ffedd5; font-weight: 500;'] * len(row)

    data_tabella = []
    for idx, (cp, st_vals) in enumerate(classifica_sort, 1):
        fascia = "⭐ Champions (Top 24)" if idx <= 24 else "🟠 Europa League"
        data_tabella.append({
            "Pos": f"{idx}°",
            "Squadra": cp,
            "Pt": st_vals["punti"],
            "G": st_vals["partite_giocate"],
            "GF": st_vals["gf"],
            "GS": st_vals["gs"],
            "DR": f"{st_vals['dr']:+d}",
            "Fascia": fascia
        })
    
    df_c = pd.DataFrame(data_tabella)
    
    # Altezza dinamica per mostrare l'intera classifica comodamente senza dover fare continui scroll microscopici
    altezza_tabella = min(800, max(250, len(df_c) * 38 + 40))
    st.dataframe(df_c.style.apply(colora_posizioni, axis=1), use_container_width=True, height=altezza_tabella, hide_index=True)

    st.markdown("---")
    st.markdown("### ⚽ Incontri della League Phase")

    da_giocare = [m for m in db["calendario"] if not m["giocata"]]
    giocate = [m for m in db["calendario"] if m["giocata"]]

    tab_da_giocare, tab_giocate = st.tabs([f"In Attesa ({len(da_giocare)})", f"Completate ({len(giocate)})"])

    with tab_da_giocare:
        if not da_giocare:
            st.info("Tutte le partite del girone unico sono state completate!")
        else:
            for m in da_giocare:
                with st.container(border=True):
                    st.markdown(f"**🤝 {m['c1']}** vs **🤝 {m['c2']}**")
                    if is_admin:
                        col_g1, col_g2 = st.columns(2)
                        with col_g1:
                            gol_a = st.number_input(f"Gol {m['c1']}", min_value=0, max_value=20, value=0, key=f"ga_{m['id']}")
                        with col_g2:
                            gol_b = st.number_input(f"Gol {m['c2']}", min_value=0, max_value=20, value=0, key=f"gb_{m['id']}")
                        
                        if st.button(f"Registra Risultato {m['id']}", key=f"btn_{m['id']}"):
                            m["gol1"] = int(gol_a)
                            m["gol2"] = int(gol_b)
                            m["giocata"] = True
                            
                            diff = abs(gol_a - gol_b)
                            if gol_a > gol_b:
                                vincitrice, perdente = m["c1"], m["c2"]
                                g_vin, g_per = gol_a, gol_b
                            elif gol_b > gol_a:
                                vincitrice, perdente = m["c2"], m["c1"]
                                g_vin, g_per = gol_b, gol_a
                            else:
                                vincitrice, perdente = m["c1"], m["c2"]
                                diff = 1
                                g_vin, g_per = gol_a, gol_b

                            pt_vin = 3 if diff >= 2 else 2
                            pt_per = 0 if diff >= 2 else 1

                            db["classifica"][vincitrice]["punti"] += pt_vin
                            db["classifica"][vincitrice]["gf"] += g_vin
                            db["classifica"][vincitrice]["gs"] += g_per
                            db["classifica"][vincitrice]["dr"] += (g_vin - g_per)
                            db["classifica"][vincitrice]["partite_giocate"] += 1

                            db["classifica"][perdente]["punti"] += pt_per
                            db["classifica"][perdente]["gf"] += g_per
                            db["classifica"][perdente]["gs"] += g_vin
                            db["classifica"][perdente]["dr"] += (g_per - g_vin)
                            db["classifica"][perdente]["partite_giocate"] += 1

                            salva_dati(db)
                            st.success("Risultato salvato e classifica aggiornata!")
                            st.rerun()

    with tab_giocate:
        if not giocate:
            st.text("Nessuna partita ancora conclusa.")
        else:
            for m in giocate:
                st.markdown(f"✅ **{m['c1']}** {m['gol1']} - {m['gol2']} **{m['c2']}**")

    if is_admin:
        st.markdown("---")
        if st.button("🌟 Genera Tabelloni Finali (Champions & Europa League)", type="primary"):
            db["stato"] = "playoffs"
            salva_dati(db)
            st.success("Passaggio alla fase a eliminazione diretta completato!")
            st.rerun()

# --- FASE 3: TABELLONI FINALI ---
elif db["stato"] == "playoffs":
    st.markdown("""
        <div class="champions-header">
            ⭐ FASE A ELIMINAZIONE DIRETTA ⭐
        </div>
    """, unsafe_allow_html=True)

    classifica_sort = sorted(
        db["classifica"].items(),
        key=lambda x: (x[1]["punti"], x[1]["dr"], x[1]["gf"]),
        reverse=True
    )
    
    squadre_ordinate = [item[0] for item in classifica_sort]
    champions_teams = squadre_ordinate[:24] 
    europa_teams = squadre_ordinate[24:]   

    tab_cl, tab_el = st.tabs(["🏆 Biliardino League (Champions)", "🥈 Biliardino League 2 (Europa League)"])

    with tab_cl:
        st.markdown("### 🏆 Tabellone Biliardino League")
        st.markdown("- **Top 8:** Qualificate direttamente agli Ottavi di Finale.")
        st.markdown("- **Dal 9° al 24° posto:** Spareggi preliminari a eliminazione diretta.")
        
        st.markdown("#### 🔹 Qualificate direttamente agli Ottavi (1° - 8°):")
        for i in range(min(8, len(champions_teams))):
            st.markdown(f"**{i+1}° posto:** {champions_teams[i]}")

        st.markdown("#### 🔹 Spareggi Play-off (9° - 24°):")
        spareggi = champions_teams[8:24]
        for i in range(0, len(spareggi), 2):
            s1 = spareggi[i]
            s2 = spareggi[i+1] if i+1 < len(spareggi) else "BYE"
            st.markdown(f"⚡ Spareggio: **{s1}** vs **{s2}**")

    with tab_el:
        st.markdown("### 🥈 Tabellone Biliardino League 2 (Europa League)")
        if not europa_teams:
            st.info("Nessuna squadra qualificata in Europa League (meno di 25 partecipanti totali).")
        else:
            for i in range(0, len(europa_teams), 2):
                s1 = europa_teams[i]
                s2 = europa_teams[i+1] if i+1 < len(europa_teams) else "RIPOSO"
                st.markdown(f"⚔️ Scontro EL: **{s1}** vs **{s2}**")

    if is_admin:
        st.markdown("---")
        if st.button("🔄 Reset Totale Torneo"):
            if os.path.exists(DB_FILE):
                os.remove(DB_FILE)
            st.session_state.clear()
            st.rerun()
