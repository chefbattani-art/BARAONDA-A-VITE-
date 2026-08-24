import streamlit as st
import random
import re
import json
import os
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

st.set_page_config(page_title="Torneo A Vite - Baraonda", page_icon="⚽️", layout="centered")

# --- STILE GRAFICO PROFESSIONALE (DASHBOARD SPORTIVA) ---
st.markdown("""
    <style>
    .main { background-color: #0b0f19; }
    
    .turn-banner {
        background: linear-gradient(135deg, #1e3a8a, #3b82f6);
        border: 1px solid #60a5fa;
        border-radius: 12px;
        padding: 12px 20px;
        text-align: center;
        color: #ffffff;
        font-size: 1.2em;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }

    .info-red-box {
        background: linear-gradient(135deg, #7c2d12, #991b1b);
        border: 2px solid #ef4444;
        border-radius: 12px;
        padding: 14px 18px;
        color: #fee2e2;
        font-weight: 600;
        font-size: 0.95em;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.3);
    }

    .last-match-warning {
        background: linear-gradient(135deg, #7c2d12, #c2410c);
        border: 2px dashed #fb923c;
        border-radius: 10px;
        padding: 10px;
        text-align: center;
        color: #ffedd5;
        font-weight: 800;
        font-size: 0.95em;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 15px;
        box-shadow: 0 0 15px rgba(234, 88, 12, 0.4);
    }

    .biliardino-header {
        background: linear-gradient(90deg, #f59e0b, #d97706);
        color: #0f172a;
        text-align: center;
        font-weight: 800;
        font-size: 0.85em;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        padding: 6px;
        border-radius: 8px;
        margin-bottom: 12px;
    }

    .team-box {
        background: linear-gradient(145deg, #064e3b, #022c22);
        border: 1px solid #059669;
        border-radius: 10px;
        padding: 10px;
        text-align: center;
        color: #ecfdf5;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }

    .player-names {
        font-size: 1.05em;
        font-weight: 800;
        line-height: 1.4;
        text-transform: uppercase;
        color: #facc15 !important;
        letter-spacing: 0.5px;
    }

    .vs-text {
        text-align: center;
        font-weight: 900;
        color: #f59e0b;
        font-size: 1.1em;
        margin: 8px 0;
        letter-spacing: 2px;
    }

    .stButton > button {
        width: 100% !important;
        background: linear-gradient(135deg, #0284c7, #0369a1) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border: 1px solid #38bdf8 !important;
        border-radius: 8px !important;
        padding: 6px 0px !important;
        font-size: 0.8em !important;
        box-shadow: 0 4px 6px rgba(2, 132, 199, 0.2);
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #0369a1, #075985) !important;
        border-color: #7dd3fc !important;
    }

    .rank-header {
        font-size: 1.15em;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 14px;
        padding-bottom: 8px;
        border-bottom: 3px solid #334155;
        color: #38bdf8;
        text-align: center;
    }

    .player-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #1e293b;
        padding: 8px 12px;
        border-radius: 8px;
        margin-bottom: 8px;
        font-size: 0.95em;
        border: 1px solid #334155;
    }
    
    .player-row-eliminated {
        background: #111827;
        opacity: 0.8;
        border: 1px solid #374151;
    }
    
    .rank-name {
        font-weight: 800;
        text-transform: uppercase;
        color: #facc15;
    }

    .rank-name-eliminated {
        font-weight: 800;
        text-transform: uppercase;
        color: #ef4444;
        text-decoration: line-through;
    }

    .podium-title {
        text-align: center;
        font-size: 1.4em;
        font-weight: 900;
        color: #f8fafc;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 20px;
        border-bottom: 2px solid #312e81;
        padding-bottom: 10px;
    }
    .podium-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: rgba(30, 41, 59, 0.7);
        padding: 10px 14px;
        border-radius: 10px;
        margin-bottom: 10px;
        border: 1px solid #334155;
    }
    .podium-pos-1 { border-left: 6px solid #fbbf24; }
    .podium-pos-2 { border-left: 6px solid #94a3b8; }
    .podium-pos-3 { border-left: 6px solid #b45309; }
    .podium-pos-4 { border-left: 6px solid #38bdf8; }
    
    div.block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

STATE_FILE = "torneo_baraonda_state.json"

def salva_stato():
    data = {
        "players": st.session_state.players,
        "tournament_started": st.session_state.tournament_started,
        "initial_lives": st.session_state.initial_lives,
        "num_biliardini": st.session_state.num_biliardini,
        "current_round_matches": st.session_state.current_round_matches,
        "round_number": st.session_state.round_number,
        "history": st.session_state.history,
        "match_history": st.session_state.match_history
    }
    with open(STATE_FILE, "w") as f:
        json.dump(data, f)

def carica_stato():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r") as f:
                data = json.load(f)
                st.session_state.players = data.get("players", [])
                st.session_state.tournament_started = data.get("tournament_started", False)
                st.session_state.initial_lives = data.get("initial_lives", 5)
                st.session_state.num_biliardini = data.get("num_biliardini", 4)
                st.session_state.current_round_matches = data.get("current_round_matches", [])
                st.session_state.round_number = data.get("round_number", 0)
                st.session_state.history = data.get("history", [])
                st.session_state.match_history = data.get("match_history", [])
                return True
        except:
            return False
    return False

if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.history = []
    st.session_state.match_history = []
    if not carica_stato():
        st.session_state.players = []
        st.session_state.tournament_started = False
        st.session_state.initial_lives = 5
        st.session_state.num_biliardini = 4
        st.session_state.current_round_matches = []
        st.session_state.round_number = 0

if "giocatore_selezionato" not in st.session_state:
    st.session_state.giocatore_selezionato = None

if "vista_personale_attiva" not in st.session_state:
    st.session_state.vista_personale_attiva = False

def salva_snapshot():
    snapshot = {
        "players": json.loads(json.dumps(st.session_state.players)),
        "current_round_matches": json.loads(json.dumps(st.session_state.current_round_matches)),
        "round_number": st.session_state.round_number,
        "match_history": json.loads(json.dumps(st.session_state.match_history))
    }
    st.session_state.history.append(snapshot)

def genera_abbinamenti():
    attivi = [p for p in st.session_state.players if not p["eliminated"]]
    random.shuffle(attivi)
    
    partite = []
    i = 0
    while i + 3 < len(attivi):
        partite.append({
            "teamA": (attivi[i], attivi[i+1]),
            "teamB": (attivi[i+2], attivi[i+3])
        })
        i += 4
        
    avanzi = attivi[i:]
    return {"partite": partite, "pass": avanzi}

def genera_pdf_report():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=20, textColor=colors.HexColor("#1e3a8a"), alignment=1, spaceAfter=15)
    subtitle_style = ParagraphStyle('SubTitleStyle', parent=styles['Heading2'], fontSize=14, textColor=colors.HexColor("#334155"), spaceBefore=15, spaceAfter=8)
    normal_style = styles['Normal']
    
    elements.append(Paragraph("⚽️ REPORT UFFICIALE - BARAONDA A VITE", title_style))
    elements.append(Paragraph("Storico Partite e Risultati", ParagraphStyle('Sub', parent=normal_style, alignment=1, textColor=colors.HexColor("#64748b"))))
    elements.append(Spacer(1, 15))
    
    if st.session_state.match_history:
        for item in st.session_state.match_history:
            turno_num = item["turno"]
            elements.append(Paragraph(f"Turno N° {turno_num}", subtitle_style))
            
            table_data = [["Biliardino", "Squadra A", "Squadra B", "Esito"]]
            for idx, m in enumerate(item["partite"]):
                tA = f"{m['tA_1']} & {m['tA_2']}"
                tB = f"{m['tB_1']} & {m['tB_2']}"
                vincitore = m.get('vincitore', 'Completata')
                table_data.append([str(idx+1), tA, tB, vincitore])
                
            t = Table(table_data, colWidths=[65, 200, 200, 85])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#3b82f6")),
                ('TEXTCOLOR', (0,0), (-1,0), colors.white),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0,0), (-1,0), 6),
                ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#f8fafc")),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
                ('FONTSIZE', (0,0), (-1,-1), 9),
            ]))
            elements.append(t)
            elements.append(Spacer(1, 10))
    else:
        elements.append(Paragraph("Nessuna partita registrata nello storico.", normal_style))
        
    elements.append(Spacer(1, 15))
    elements.append(Paragraph("Classifica / Podio Baraonda", subtitle_style))
    players_sorted = sorted(st.session_state.players, key=lambda x: (x["lives"], not x["eliminated"]), reverse=True)
    
    podio_data = [["Posizione", "Giocatore", "Vite Rimaste"]]
    for i, p in enumerate(players_sorted[:10]):
        pos = f"{i+1}°"
        p_name = p["name"].upper()
        p_lives = f"{p['lives']} ❤️"
        podio_data.append([pos, p_name, p_lives])
        
    t_podio = Table(podio_data, colWidths=[100, 250, 150])
    t_podio.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1e293b")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('FONTSIZE', (0,0), (-1,-1), 9),
    ]))
    elements.append(t_podio)
    
    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()

st.sidebar.title("🔐 Accesso & Gestione")
admin_code = st.sidebar.text_input("Codice Amministratore", type="password", placeholder="Inserisci 0000")
is_admin = (admin_code == "0000")

if is_admin:
    st.sidebar.success("Modo Amministratore Attivo 🔓")
else:
    st.sidebar.info("Modalità Spettatore / Giocatore")

# --- GESTIONE ACCESSO (L'ADMIN ENTRA SUBITO, I GIOCATORI SCELGONO IL NOME) ---
nomi_giocatori = sorted(list(set([p["name"] for p in st.session_state.players]))) if st.session_state.players else []

if not is_admin and st.session_state.giocatore_selezionato is None:
    st.title("⚽️ Torneo Baraonda a Vite")
    st.markdown("""
        <div class="info-red-box" style="text-align: center; font-size: 1.1em;">
            👋 <b>FASE DI ACCESSO:</b> Se sei un giocatore, seleziona il tuo nome dall'elenco sottostante e clicca su <b>Accedi</b> per visualizzare la tua partita.
        </div>
    """, unsafe_allow_html=True)

    if nomi_giocatori:
        with st.container(border=True):
            st.markdown("### 👤 Seleziona il tuo profilo:")
            nome_scelto_temp = st.selectbox("Iscritti:", nomi_giocatori, label_visibility="collapsed")
            
            col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
            with col_b2:
                if st.button("🚀 Accedi al Torneo", type="primary", use_container_width=True):
                    st.session_state.giocatore_selezionato = nome_scelto_temp
                    st.rerun()
    else:
        st.warning("⚠️ Nessun giocatore registrato nel sistema. Inserisci il codice amministratore nella barra laterale per impostare i partecipanti.")
        
    st.stop()

# --- TITOLO PRINCIPALE TORNEO ---
st.title("⚽️ Torneo Baraonda a Vite")

if is_admin:
    st.info("🔓 Sei entrato come **AMMINISTRATORE**: hai pieno controllo su tutto il torneo e puoi gestire i campi senza filtri utente.")
else:
    col_u1, col_u2 = st.columns([3, 1])
    with col_u1:
        giocatore_selezionato = st.session_state.giocatore_selezionato
        st.info(f"👤 Stai visualizzando il torneo come: **{giocatore_selezionato.upper()}**")
    with col_u2:
        if st.button("🔄 Cambia Utente", use_container_width=True):
            st.session_state.giocatore_selezionato = None
            st.session_state.vista_personale_attiva = False
            st.rerun()

    etichetta_occhio = "👁️ Nascondi Vista Personale" if st.session_state.vista_personale_attiva else "👁️ Attiva Vista Personale (Solo la mia partita)"
    if st.button(etichetta_occhio, use_container_width=True):
        st.session_state.vista_personale_attiva = not st.session_state.vista_personale_attiva
        st.rerun()

# --- PANNELLO ADMIN ---
if is_admin:
    with st.expander("⚙️ Pannello Configurazione & Gestione (Admin)", expanded=not st.session_state.tournament_started):
        col_conf1, col_conf2 = st.columns(2)
        with col_conf1:
            st.session_state.initial_lives = st.number_input("Vite iniziali", min_value=1, max_value=10, value=st.session_state.initial_lives)
        with col_conf2:
            st.session_state.num_biliardini = st.number_input("Numero Biliardini", min_value=1, max_value=10, value=st.session_state.num_biliardini)
        
        st.markdown("---")
        st.markdown("Incolla la lista dei giocatori (con o senza numeri, es. `1) MERY` oppure solo `MERY`):")
        lista_input_testo = st.text_area("Partecipanti:", height=150, placeholder="1) MERY\n2) FRENCI\n3) MIRCO\n...")
        
        if st.button("📥 Importa e Registra Giocatori", type="primary"):
            righe = lista_input_testo.split("\n")
            count_aggiunti = 0
            for riga in righe:
                riga_pulita = riga.strip()
                if not riga_pulita: continue
                # Rimuove numeri iniziali, punti, trattini o parentesi (es: "1) ", "2 - ", "3.")
                nome = re.sub(r'^\d+[\.\-\)\s]*', '', riga_pulita).strip()
                if nome and not any(p["name"].lower() == nome.lower() for p in st.session_state.players):
                    st.session_state.players.append({
                        "id": len(st.session_state.players) + 1,
                        "name": nome,
                        "lives": st.session_state.initial_lives,
                        "max_lives": st.session_state.initial_lives,
                        "eliminated": False
                    })
                    count_aggiunti += 1
            salva_stato()
            st.success(f"Importati con successo {count_aggiunti} giocatori!")
            st.rerun()

        st.info(f"📊 Giocatori iscritti totali: {len(st.session_state.players)}")

        if len(st.session_state.players) >= 4:
            col_act1, col_act2 = st.columns(2)
            with col_act1:
                if not st.session_state.tournament_started:
                    if st.button("🚀 Avvia Torneo", type="primary"):
                        st.session_state.tournament_started = True
                        st.session_state.round_number = 1
                        st.session_state.history = []
                        st.session_state.match_history = []
                        st.session_state.current_round_matches = genera_abbinamenti()
                        salva_stato()
                        st.rerun()
            with col_act2:
                if st.button("🛑 Reset Totale Torneo"):
                    st.session_state.tournament_started = False
                    st.session_state.current_round_matches = []
                    st.session_state.round_number = 0
                    st.session_state.players = []
                    st.session_state.history = []
                    st.session_state.match_history = []
                    if os.path.exists(STATE_FILE):
                        os.remove(STATE_FILE)
                    st.rerun()

if st.session_state.tournament_started:
    pdf_data = genera_pdf_report()
    st.sidebar.markdown("---")
    st.sidebar.download_button(
        label="📥 Scarica Report PDF Partite",
        data=pdf_data,
        file_name="report_torneo_baraonda.pdf",
        mime="application/pdf",
        use_container_width=True
    )

st.markdown("---")

attivi_giocatori = [p for p in st.session_state.players if not p["eliminated"]]
torneo_finito = st.session_state.tournament_started and len(attivi_giocatori) < 4

if st.session_state.tournament_started:
    if torneo_finito:
        st.markdown("""
            <div style="text-align: center; font-size: 2em; font-weight: 900; color: #f59e0b; text-transform: uppercase; margin-bottom: 20px; letter-spacing: 2px;">
                🏆 Podio Ufficiale Finale (Baraonda) 🏆
            </div>
        """, unsafe_allow_html=True)
        
        players_sorted = sorted(st.session_state.players, key=lambda x: (x["lives"], not x["eliminated"]), reverse=True)
        
        with st.container(border=True):
            st.markdown("<div class='podium-title'>Classifica Generale</div>", unsafe_allow_html=True)
            for rank, p in enumerate(players_sorted[:10]):
                cuori = "❤️ " * p["lives"]
                bare = "⚰️ " * (p["max_lives"] - p["lives"])
                pos_class = f"podium-pos-{rank+1}" if rank < 4 else "podium-pos-4"
                st.markdown(f"""
                    <div class="podium-row {pos_class}">
                        <span style="font-weight: 900; color: #f8fafc;">{rank+1}° Posto</span>
                        <span style="font-weight: 800; color: #facc15; text-transform: uppercase;">{p['name']}</span>
                        <span style="font-size: 0.85em;">{cuori}{bare}</span>
                    </div>
                """, unsafe_allow_html=True)
            
        st.download_button(
            label="📄 Scarica il Report Completo in PDF (Risultati & Podio)",
            data=pdf_data,
            file_name="report_finale_baraonda.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    else:
        data_turno = st.session_state.current_round_matches
        
        if data_turno and not data_turno.get("partite"):
            st.session_state.round_number += 1
            st.session_state.current_round_matches = genera_abbinamenti()
            salva_stato()
            st.rerun()

        if is_admin and len(st.session_state.history) > 0:
            if st.button("↩️ Torna al Turno Precedente (Annulla Ultima Modifica)", type="secondary", use_container_width=True):
                last_state = st.session_state.history.pop()
                st.session_state.players = last_state.get("players", st.session_state.players)
                st.session_state.current_round_matches = last_state.get("current_round_matches", {})
                st.session_state.round_number = last_state.get("round_number", 1)
                st.session_state.match_history = last_state.get("match_history", [])
                salva_stato()
                st.rerun()

        st.markdown("""
            <div style="background: linear-gradient(135deg, #b45309, #d97706); border: 2px solid #f59e0b; border-radius: 12px; padding: 12px 18px; color: #fffbeb; font-weight: 700; font-size: 0.95em; text-align: center; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);">
                🏆 <b>IMPORTANTE:</b> Chi ha vinto? Una delle due coppie deve assegnarsi la vittoria!
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div class="turn-banner">
                ⚔️ Turno N° {st.session_state.round_number} (Baraonda)
            </div>
        """, unsafe_allow_html=True)
        
        if data_turno and data_turno.get("pass"):
            pass_names = ", ".join([f"{p['name'].upper()}" for p in data_turno["pass"]])
            st.info(f"💚 **Riposano (Pass):** {pass_names}")

        partite = data_turno.get("partite", []) if data_turno else []
        
        if partite:
            num_biliardini = st.session_state.num_biliardini
            partite_in_corso = partite[:num_biliardini]
            partite_in_coda = partite[num_biliardini:]
            
            is_vista_personale = (not is_admin) and st.session_state.vista_personale_attiva

            if is_vista_personale:
                partite_filtrate = []
                for idx, match in enumerate(partite_in_corso):
                    p1, p2 = match["teamA"]
                    p3, p4 = match["teamB"]
                    nomi_partita = [p1['name'], p2['name'], p3['name'], p4['name']]
                    if any(n.lower() == st.session_state.giocatore_selezionato.lower() for n in nomi_partita):
                        partite_filtrate.append((idx, match))
                
                if not partite_filtrate:
                    st.info(f"☕️ Al momento {st.session_state.giocatore_selezionato.upper()} non ha una partita attiva in questo turno (o è in pausa/riposo). Disattiva la vista personale per visualizzare l'intero torneo.")
                else:
                    st.markdown(f"#### 🎯 Partita di: {st.session_state.giocatore_selezionato.upper()} (Vista Personale 👁️)")
                
                iter_partite = partite_filtrate
            else:
                is_last_match_of_round = (len(partite_in_corso) == 1 and len(partite_in_coda) == 0)
                if is_last_match_of_round:
                    st.markdown("""
                        <div class="last-match-warning">
                            ⚠️ ULTIMA PARTITA DI QUESTO TURNO! Assegnando la vittoria, il torneo passerà subito al turno successivo.
                        </div>
                    """, unsafe_allow_html=True)
                st.markdown("#### 🏟️ Partite in Corso (Panoramica Torneo)")
                iter_partite = [(idx, match) for idx, match in enumerate(partite_in_corso)]

            for idx, match in iter_partite:
                biliardino_num = idx + 1
                p1, p2 = match["teamA"]
                p3, p4 = match["teamB"]
                
                giocatore_nella_squadra_a = False if is_admin else any(n.lower() == st.session_state.giocatore_selezionato.lower() for n in [p1['name'], p2['name']])
                giocatore_nella_squadra_b = False if is_admin else any(n.lower() == st.session_state.giocatore_selezionato.lower() for n in [p3['name'], p4['name']])

                with st.container(border=True):
                    st.markdown(f"""
                        <div class="biliardino-header">📍 Biliardino N. {biliardino_num}</div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                        <div class="team-box">
                            <div class="player-names">{p1['name'].upper()} &nbsp;|&nbsp; {p2['name'].upper()}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    mostra_tasto_A = is_admin or (not is_vista_personale) or giocatore_nella_squadra_a
                    
                    if mostra_tasto_A:
                        if st.button("🏆 Assegna la Vittoria a questa Coppia", key=f"win_A_{st.session_state.round_number}_{idx}", use_container_width=True):
                            salva_snapshot()
                            
                            match_record = {
                                "turno": st.session_state.round_number,
                                "partite": [{
                                    "tA_1": p1['name'].upper(), "tA_2": p2['name'].upper(),
                                    "tB_1": p3['name'].upper(), "tB_2": p4['name'].upper(),
                                    "vincitore": f"Vittoria Squadra A ({p1['name'].upper()} & {p2['name'].upper()})"
                                }]
                            }
                            found_h = next((h for h in st.session_state.match_history if h["turno"] == st.session_state.round_number), None)
                            if found_h:
                                found_h["partite"].append(match_record["partite"][0])
                            else:
                                st.session_state.match_history.append(match_record)

                            for per in [p3, p4]:
                                per["lives"] = max(0, per["lives"] - 1)
                                if per["lives"] == 0: per["eliminated"] = True
                            
                            st.session_state.current_round_matches["partite"].pop(idx)
                            
                            if not st.session_state.current_round_matches["partite"]:
                                st.session_state.round_number += 1
                                st.session_state.current_round_matches = genera_abbinamenti()
                                
                            salva_stato()
                            st.rerun()
                    
                    st.markdown("<div class='vs-text'>VS</div>", unsafe_allow_html=True)
                    
                    st.markdown(f"""
                        <div class="team-box">
                            <div class="player-names">{p3['name'].upper()} &nbsp;|&nbsp; {p4['name'].upper()}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    mostra_tasto_B = is_admin or (not is_vista_personale) or giocatore_nella_squadra_b

                    if mostra_tasto_B:
                        if st.button("🏆 Assegna la Vittoria a questa Coppia", key=f"win_B_{st.session_state.round_number}_{idx}", use_container_width=True):
                            salva_snapshot()
                            
                            match_record = {
                                "turno": st.session_state.round_number,
                                "partite": [{
                                    "tA_1": p1['name'].upper(), "tA_2": p2['name'].upper(),
                                    "tB_1": p3['name'].upper(), "tB_2": p4['name'].upper(),
                                    "vincitore": f"Vittoria Squadra B ({p3['name'].upper()} & {p4['name'].upper()})"
                                }]
                            }
                            found_h = next((h for h in st.session_state.match_history if h["turno"] == st.session_state.round_number), None)
                            if found_h:
                                found_h["partite"].append(match_record["partite"][0])
                            else:
                                st.session_state.match_history.append(match_record)

                            for per in [p1, p2]:
                                per["lives"] = max(0, per["lives"] - 1)
                                if per["lives"] == 0: per["eliminated"] = True
                            
                            st.session_state.current_round_matches["partite"].pop(idx)
                            
                            if not st.session_state.current_round_matches["partite"]:
                                st.session_state.round_number += 1
                                st.session_state.current_round_matches = genera_abbinamenti()
                                
                            salva_stato()
                            st.rerun()
                
            if partite_in_coda and not is_vista_personale:
                st.markdown("#### ⏳ In Coda")
                for q_idx, q_match in enumerate(partite_in_coda):
                    qa1, qa2 = q_match["teamA"]
                    qb1, qb2 = q_match["teamB"]
                    st.warning(f"Coda #{q_idx+1}: [{qa1['name'].upper()} & {qa2['name'].upper()}] vs [{qb1['name'].upper()} & {qb2['name'].upper()}]")

st.markdown("---")

# --- CLASSIFICA & VITE AGGIORNATA ---
if st.session_state.players:
    st.markdown("### 📊 Andamento Torneo & Vite Giocatori")
    
    players_sorted = sorted(st.session_state.players, key=lambda x: (x["eliminated"], -x["lives"]))
    
    with st.container(border=True):
        st.markdown("<div class='rank-header'>STATO VITE PARTECIPANTI</div>", unsafe_allow_html=True)
        for p in players_sorted:
            cuori = "❤️ " * p["lives"]
            bare = "⚰️ " * (p["max_lives"] - p["lives"])
            vite_display = cuori + bare
            
            css_class = "player-row player-row-eliminated" if p["eliminated"] else "player-row"
            name_class = "rank-name-eliminated" if p["eliminated"] else "rank-name"
            
            st.markdown(f"""
                <div class="{css_class}">
                    <span class="{name_class}">{p['name']}</span>
                    <span>{vite_display}</span>
                </div>
            """, unsafe_allow_html=True)
