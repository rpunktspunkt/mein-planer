import streamlit as st
import sqlite3
from datetime import date, datetime, timedelta
import calendar
import pandas as pd

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Mein Planer",
    page_icon="🗓️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
# CUSTOM CSS – Modern & Bunt
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Inter:wght@300;400;500&display=swap');

:root {
    --bg: #0f0f1a;
    --surface: #1a1a2e;
    --surface2: #16213e;
    --accent1: #e040fb;
    --accent2: #00e5ff;
    --accent3: #69ff47;
    --accent4: #ff6d00;
    --text: #f0f0ff;
    --text-muted: #8888aa;
    --radius: 16px;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

.stApp {
    background: linear-gradient(135deg, #0f0f1a 0%, #1a0a2e 50%, #0a1a2e 100%) !important;
}

/* Header */
.app-header {
    text-align: center;
    padding: 2rem 0 1rem;
    margin-bottom: 1.5rem;
}
.app-header h1 {
    font-family: 'Syne', sans-serif;
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(90deg, var(--accent1), var(--accent2), var(--accent3));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
}
.app-header p {
    color: var(--text-muted);
    font-size: 1rem;
    margin-top: 0.25rem;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: var(--surface) !important;
    border-radius: 50px !important;
    padding: 4px !important;
    gap: 4px !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 50px !important;
    color: var(--text-muted) !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    padding: 0.5rem 1.5rem !important;
    transition: all 0.2s !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, var(--accent1), var(--accent2)) !important;
    color: white !important;
}
.stTabs [data-baseweb="tab-panel"] {
    padding-top: 1.5rem !important;
}

/* Cards */
.card {
    background: var(--surface);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: var(--radius);
    padding: 1.25rem 1.5rem;
    margin-bottom: 0.75rem;
    transition: all 0.2s;
}
.card:hover {
    border-color: rgba(224, 64, 251, 0.3);
    transform: translateY(-1px);
}
.card-title {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1rem;
    margin: 0 0 0.25rem;
}
.card-meta {
    color: var(--text-muted);
    font-size: 0.8rem;
}
.badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 50px;
    font-size: 0.7rem;
    font-weight: 600;
    font-family: 'Syne', sans-serif;
}
.badge-pink { background: rgba(224,64,251,0.15); color: var(--accent1); border: 1px solid rgba(224,64,251,0.3); }
.badge-cyan { background: rgba(0,229,255,0.15); color: var(--accent2); border: 1px solid rgba(0,229,255,0.3); }
.badge-green { background: rgba(105,255,71,0.15); color: var(--accent3); border: 1px solid rgba(105,255,71,0.3); }
.badge-orange { background: rgba(255,109,0,0.15); color: var(--accent4); border: 1px solid rgba(255,109,0,0.3); }

/* Inputs */
.stTextInput input, .stTextArea textarea, .stSelectbox select {
    background: var(--surface2) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: var(--accent1) !important;
    box-shadow: 0 0 0 2px rgba(224,64,251,0.15) !important;
}

/* Buttons */
.stButton button {
    background: linear-gradient(135deg, var(--accent1), #7b2ff7) !important;
    color: white !important;
    border: none !important;
    border-radius: 50px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    padding: 0.5rem 2rem !important;
    transition: all 0.2s !important;
    letter-spacing: 0.5px !important;
}
.stButton button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(224,64,251,0.35) !important;
}

/* Kalender */
.cal-grid {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 6px;
    margin-top: 0.75rem;
}
.cal-day-header {
    text-align: center;
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    color: var(--text-muted);
    padding: 4px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
}
.cal-day {
    aspect-ratio: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    border-radius: 10px;
    font-size: 0.85rem;
    cursor: default;
    position: relative;
    background: var(--surface);
    border: 1px solid rgba(255,255,255,0.04);
    min-height: 44px;
}
.cal-day.today {
    background: linear-gradient(135deg, rgba(224,64,251,0.25), rgba(0,229,255,0.15));
    border-color: var(--accent1);
    font-weight: 700;
    color: white;
}
.cal-day.has-event::after {
    content: '';
    position: absolute;
    bottom: 5px;
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background: var(--accent2);
}
.cal-day.empty {
    background: transparent;
    border-color: transparent;
}
.cal-month-header {
    font-family: 'Syne', sans-serif;
    font-size: 1.4rem;
    font-weight: 800;
    color: white;
}

/* Section titles */
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: white;
    margin: 1.5rem 0 0.75rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* Stats */
.stat-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin-bottom: 1.5rem;
}
.stat-card {
    background: var(--surface);
    border-radius: var(--radius);
    padding: 1rem;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.06);
}
.stat-number {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
}
.stat-label {
    font-size: 0.75rem;
    color: var(--text-muted);
}

/* Checkbox styling */
.stCheckbox { margin-bottom: 0.25rem; }
.stCheckbox label { color: var(--text) !important; }

/* Date picker */
.stDateInput input { color: var(--text) !important; }

/* Divider */
hr { border-color: rgba(255,255,255,0.06) !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: rgba(224,64,251,0.3); border-radius: 3px; }

/* Success/Info messages */
.stSuccess { background: rgba(105,255,71,0.1) !important; border-color: var(--accent3) !important; }
.stInfo { background: rgba(0,229,255,0.1) !important; border-color: var(--accent2) !important; }

/* Delete button small */
.stButton.delete button {
    background: rgba(255,50,50,0.15) !important;
    color: #ff6b6b !important;
    font-size: 0.75rem !important;
    padding: 0.2rem 0.75rem !important;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# DATENBANK
# ─────────────────────────────────────────────
def get_db():
    conn = sqlite3.connect("planer.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS termine (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titel TEXT NOT NULL,
            datum TEXT NOT NULL,
            uhrzeit TEXT,
            beschreibung TEXT,
            farbe TEXT DEFAULT 'pink',
            erstellt TEXT DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS aufgaben (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            faellig TEXT,
            erledigt INTEGER DEFAULT 0,
            prioritaet TEXT DEFAULT 'mittel',
            erstellt TEXT DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS notizen (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titel TEXT,
            inhalt TEXT NOT NULL,
            farbe TEXT DEFAULT 'cyan',
            erstellt TEXT DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    conn.close()

init_db()


# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
today = date.today()
st.markdown(f"""
<div class="app-header">
    <h1>🗓️ Mein Planer</h1>
    <p>{today.strftime('%A, %d. %B %Y')}</p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# STATS OVERVIEW
# ─────────────────────────────────────────────
conn = get_db()
n_termine = conn.execute("SELECT COUNT(*) FROM termine WHERE datum >= ?", (str(today),)).fetchone()[0]
n_offen = conn.execute("SELECT COUNT(*) FROM aufgaben WHERE erledigt=0").fetchone()[0]
n_notizen = conn.execute("SELECT COUNT(*) FROM notizen").fetchone()[0]
conn.close()

st.markdown(f"""
<div class="stat-grid">
    <div class="stat-card">
        <div class="stat-number" style="color:#e040fb">{n_termine}</div>
        <div class="stat-label">Kommende Termine</div>
    </div>
    <div class="stat-card">
        <div class="stat-number" style="color:#00e5ff">{n_offen}</div>
        <div class="stat-label">Offene Aufgaben</div>
    </div>
    <div class="stat-card">
        <div class="stat-number" style="color:#69ff47">{n_notizen}</div>
        <div class="stat-label">Notizen</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["📆 Kalender", "🗓️ Termine", "✅ Aufgaben", "📝 Notizen"])


# ══════════════════════════════════════════════
# TAB 1: KALENDER
# ══════════════════════════════════════════════
with tab1:
    col_nav1, col_nav2, col_nav3 = st.columns([1, 3, 1])

    if "cal_year" not in st.session_state:
        st.session_state.cal_year = today.year
    if "cal_month" not in st.session_state:
        st.session_state.cal_month = today.month

    with col_nav1:
        if st.button("◀ Zurück"):
            if st.session_state.cal_month == 1:
                st.session_state.cal_month = 12
                st.session_state.cal_year -= 1
            else:
                st.session_state.cal_month -= 1

    with col_nav3:
        if st.button("Vor ▶"):
            if st.session_state.cal_month == 12:
                st.session_state.cal_month = 1
                st.session_state.cal_year += 1
            else:
                st.session_state.cal_month += 1

    yr = st.session_state.cal_year
    mo = st.session_state.cal_month
    monate_de = ["", "Januar", "Februar", "März", "April", "Mai", "Juni",
                 "Juli", "August", "September", "Oktober", "November", "Dezember"]

    with col_nav2:
        st.markdown(f'<div class="cal-month-header" style="text-align:center">{monate_de[mo]} {yr}</div>', unsafe_allow_html=True)

    # Termine dieses Monats laden
    conn = get_db()
    month_str = f"{yr}-{mo:02d}"
    termine_im_monat = conn.execute(
        "SELECT datum FROM termine WHERE datum LIKE ?", (f"{month_str}%",)
    ).fetchall()
    conn.close()
    tage_mit_termin = set(t["datum"] for t in termine_im_monat)

    cal = calendar.monthcalendar(yr, mo)
    wochentage = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]

    cal_html = '<div class="cal-grid">'
    for tag in wochentage:
        cal_html += f'<div class="cal-day-header">{tag}</div>'

    for woche in cal:
        for tag in woche:
            if tag == 0:
                cal_html += '<div class="cal-day empty"></div>'
            else:
                datum_str = f"{yr}-{mo:02d}-{tag:02d}"
                classes = "cal-day"
                if date(yr, mo, tag) == today:
                    classes += " today"
                if datum_str in tage_mit_termin:
                    classes += " has-event"
                cal_html += f'<div class="{classes}"><span>{tag}</span></div>'
    cal_html += '</div>'

    st.markdown(cal_html, unsafe_allow_html=True)
    st.markdown('<div class="card-meta" style="margin-top:0.5rem">● Punkt unter dem Tag = Termin vorhanden &nbsp;&nbsp; Lila Hintergrund = Heute</div>', unsafe_allow_html=True)

    # Termine des Monats auflisten
    st.markdown('<div class="section-title">📌 Termine in diesem Monat</div>', unsafe_allow_html=True)
    conn = get_db()
    termine_liste = conn.execute(
        "SELECT * FROM termine WHERE datum LIKE ? ORDER BY datum, uhrzeit", (f"{month_str}%",)
    ).fetchall()
    conn.close()

    if not termine_liste:
        st.markdown('<div class="card-meta">Keine Termine in diesem Monat.</div>', unsafe_allow_html=True)
    else:
        farben = {"pink": "badge-pink", "cyan": "badge-cyan", "green": "badge-green", "orange": "badge-orange"}
        for t in termine_liste:
            uhr = f"⏰ {t['uhrzeit']}" if t['uhrzeit'] else ""
            badge = farben.get(t['farbe'], 'badge-pink')
            desc = f"<br><span class='card-meta'>{t['beschreibung']}</span>" if t['beschreibung'] else ""
            st.markdown(f"""
            <div class="card">
                <div class="card-title">{t['titel']} <span class="badge {badge}">{t['datum']}</span></div>
                <div class="card-meta">{uhr}{desc}</div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 2: TERMINE
# ══════════════════════════════════════════════
with tab2:
    col_form, col_list = st.columns([1, 1], gap="large")

    with col_form:
        st.markdown('<div class="section-title">➕ Neuer Termin</div>', unsafe_allow_html=True)
        with st.container():
            titel = st.text_input("Titel *", placeholder="z.B. Arzttermin, Meeting...")
            col_d, col_t = st.columns(2)
            with col_d:
                datum = st.date_input("Datum", today, key="termin_datum")
            with col_t:
                uhrzeit = st.time_input("Uhrzeit", key="termin_uhrzeit")
            beschreibung = st.text_area("Beschreibung (optional)", height=80, placeholder="Weitere Details...")
            farbe = st.selectbox("Farbe / Kategorie", ["pink", "cyan", "green", "orange"],
                                  format_func=lambda x: {"pink": "🟣 Lila", "cyan": "🔵 Blau", "green": "🟢 Grün", "orange": "🟠 Orange"}[x])

            if st.button("💾 Termin speichern", key="save_termin"):
                if titel.strip():
                    conn = get_db()
                    conn.execute("INSERT INTO termine (titel, datum, uhrzeit, beschreibung, farbe) VALUES (?,?,?,?,?)",
                                 (titel.strip(), str(datum), str(uhrzeit), beschreibung.strip(), farbe))
                    conn.commit()
                    conn.close()
                    st.success("✅ Termin gespeichert!")
                    st.rerun()
                else:
                    st.error("Bitte einen Titel eingeben.")

    with col_list:
        st.markdown('<div class="section-title">📋 Alle Termine</div>', unsafe_allow_html=True)
        conn = get_db()
        alle_termine = conn.execute("SELECT * FROM termine ORDER BY datum, uhrzeit").fetchall()
        conn.close()

        if not alle_termine:
            st.markdown('<div class="card-meta">Noch keine Termine eingetragen.</div>', unsafe_allow_html=True)
        else:
            farben = {"pink": "badge-pink", "cyan": "badge-cyan", "green": "badge-green", "orange": "badge-orange"}
            vergangen_gezeigt = False
            for t in alle_termine:
                ist_vergangen = t['datum'] < str(today)
                badge = farben.get(t['farbe'], 'badge-pink')
                uhr = f" · {t['uhrzeit'][:5]}" if t['uhrzeit'] else ""
                desc = f"<br><span class='card-meta'>{t['beschreibung']}</span>" if t['beschreibung'] else ""

                opacity = "opacity:0.45;" if ist_vergangen else ""
                st.markdown(f"""
                <div class="card" style="{opacity}">
                    <div style="display:flex;justify-content:space-between;align-items:start">
                        <div>
                            <div class="card-title">{t['titel']}</div>
                            <div class="card-meta"><span class="badge {badge}">{t['datum']}{uhr}</span>{desc}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                col_del, _ = st.columns([1, 4])
                with col_del:
                    if st.button("🗑️ Löschen", key=f"del_t_{t['id']}"):
                        conn = get_db()
                        conn.execute("DELETE FROM termine WHERE id=?", (t['id'],))
                        conn.commit()
                        conn.close()
                        st.rerun()


# ══════════════════════════════════════════════
# TAB 3: AUFGABEN
# ══════════════════════════════════════════════
with tab3:
    col_form2, col_list2 = st.columns([1, 1], gap="large")

    with col_form2:
        st.markdown('<div class="section-title">➕ Neue Aufgabe</div>', unsafe_allow_html=True)
        aufgabe_text = st.text_input("Aufgabe *", placeholder="Was muss erledigt werden?")
        faellig = st.date_input("Fällig bis (optional)", value=None, key="aufgabe_faellig")
        prio = st.selectbox("Priorität", ["hoch", "mittel", "niedrig"],
                             format_func=lambda x: {"hoch": "🔴 Hoch", "mittel": "🟡 Mittel", "niedrig": "🟢 Niedrig"}[x])

        if st.button("💾 Aufgabe hinzufügen", key="save_aufgabe"):
            if aufgabe_text.strip():
                conn = get_db()
                conn.execute("INSERT INTO aufgaben (text, faellig, prioritaet) VALUES (?,?,?)",
                             (aufgabe_text.strip(), str(faellig) if faellig else None, prio))
                conn.commit()
                conn.close()
                st.success("✅ Aufgabe hinzugefügt!")
                st.rerun()
            else:
                st.error("Bitte eine Aufgabe eingeben.")

    with col_list2:
        st.markdown('<div class="section-title">📋 Meine Aufgaben</div>', unsafe_allow_html=True)
        conn = get_db()
        alle_aufgaben = conn.execute(
            "SELECT * FROM aufgaben ORDER BY erledigt ASC, CASE prioritaet WHEN 'hoch' THEN 0 WHEN 'mittel' THEN 1 ELSE 2 END, faellig"
        ).fetchall()
        conn.close()

        prio_badge = {"hoch": ("badge-pink", "🔴"), "mittel": ("badge-orange", "🟡"), "niedrig": ("badge-green", "🟢")}

        if not alle_aufgaben:
            st.markdown('<div class="card-meta">Noch keine Aufgaben eingetragen.</div>', unsafe_allow_html=True)
        else:
            offen = [a for a in alle_aufgaben if not a['erledigt']]
            erledigt = [a for a in alle_aufgaben if a['erledigt']]

            if offen:
                for a in offen:
                    badge_cls, icon = prio_badge.get(a['prioritaet'], ("badge-cyan", ""))
                    faellig_str = f" · fällig: {a['faellig']}" if a['faellig'] else ""
                    ueberfaellig = a['faellig'] and a['faellig'] < str(today)
                    ueberfaellig_html = ' <span class="badge badge-pink">⚠️ Überfällig</span>' if ueberfaellig else ""

                    col_cb, col_info, col_d = st.columns([0.5, 3, 1])
                    with col_cb:
                        checked = st.checkbox("", key=f"cb_{a['id']}", value=False)
                        if checked:
                            conn = get_db()
                            conn.execute("UPDATE aufgaben SET erledigt=1 WHERE id=?", (a['id'],))
                            conn.commit()
                            conn.close()
                            st.rerun()
                    with col_info:
                        st.markdown(f"""
                        <div style="padding-top:0.4rem">
                            <span style="font-weight:600">{a['text']}</span>
                            {ueberfaellig_html}
                            <br>
                            <span class="badge {badge_cls}">{icon} {a['prioritaet'].capitalize()}</span>
                            <span class="card-meta">{faellig_str}</span>
                        </div>
                        """, unsafe_allow_html=True)
                    with col_d:
                        if st.button("🗑️", key=f"del_a_{a['id']}"):
                            conn = get_db()
                            conn.execute("DELETE FROM aufgaben WHERE id=?", (a['id'],))
                            conn.commit()
                            conn.close()
                            st.rerun()

            if erledigt:
                st.markdown('<div class="section-title" style="color:var(--text-muted);font-size:0.9rem">✅ Erledigt</div>', unsafe_allow_html=True)
                for a in erledigt:
                    col_cb2, col_info2, col_d2 = st.columns([0.5, 3, 1])
                    with col_cb2:
                        unchecked = st.checkbox("", key=f"cb_{a['id']}", value=True)
                        if not unchecked:
                            conn = get_db()
                            conn.execute("UPDATE aufgaben SET erledigt=0 WHERE id=?", (a['id'],))
                            conn.commit()
                            conn.close()
                            st.rerun()
                    with col_info2:
                        st.markdown(f'<div style="padding-top:0.4rem;opacity:0.4;text-decoration:line-through">{a["text"]}</div>', unsafe_allow_html=True)
                    with col_d2:
                        if st.button("🗑️", key=f"del_a_{a['id']}"):
                            conn = get_db()
                            conn.execute("DELETE FROM aufgaben WHERE id=?", (a['id'],))
                            conn.commit()
                            conn.close()
                            st.rerun()


# ══════════════════════════════════════════════
# TAB 4: NOTIZEN
# ══════════════════════════════════════════════
with tab4:
    col_form3, col_list3 = st.columns([1, 1], gap="large")

    with col_form3:
        st.markdown('<div class="section-title">➕ Neue Notiz</div>', unsafe_allow_html=True)
        notiz_titel = st.text_input("Titel (optional)", placeholder="z.B. Ideen, Einkauf...")
        notiz_inhalt = st.text_area("Notiz *", height=150, placeholder="Schreib hier deine Notiz...")
        notiz_farbe = st.selectbox("Farbe", ["cyan", "pink", "green", "orange"],
                                    format_func=lambda x: {"cyan": "🔵 Blau", "pink": "🟣 Lila", "green": "🟢 Grün", "orange": "🟠 Orange"}[x],
                                    key="notiz_farbe")

        if st.button("💾 Notiz speichern", key="save_notiz"):
            if notiz_inhalt.strip():
                conn = get_db()
                conn.execute("INSERT INTO notizen (titel, inhalt, farbe) VALUES (?,?,?)",
                             (notiz_titel.strip(), notiz_inhalt.strip(), notiz_farbe))
                conn.commit()
                conn.close()
                st.success("✅ Notiz gespeichert!")
                st.rerun()
            else:
                st.error("Bitte einen Notiz-Inhalt eingeben.")

    with col_list3:
        st.markdown('<div class="section-title">📋 Meine Notizen</div>', unsafe_allow_html=True)
        conn = get_db()
        alle_notizen = conn.execute("SELECT * FROM notizen ORDER BY erstellt DESC").fetchall()
        conn.close()

        farb_map = {
            "cyan": ("badge-cyan", "#00e5ff"),
            "pink": ("badge-pink", "#e040fb"),
            "green": ("badge-green", "#69ff47"),
            "orange": ("badge-orange", "#ff6d00")
        }

        if not alle_notizen:
            st.markdown('<div class="card-meta">Noch keine Notizen vorhanden.</div>', unsafe_allow_html=True)
        else:
            for n in alle_notizen:
                badge_cls, color = farb_map.get(n['farbe'], ("badge-cyan", "#00e5ff"))
                titel_html = f"<div class='card-title'>{n['titel']}</div>" if n['titel'] else ""
                datum_fmt = n['erstellt'][:10] if n['erstellt'] else ""

                st.markdown(f"""
                <div class="card" style="border-left: 3px solid {color}">
                    {titel_html}
                    <div style="white-space:pre-wrap;font-size:0.9rem;line-height:1.5">{n['inhalt']}</div>
                    <div class="card-meta" style="margin-top:0.5rem">{datum_fmt}</div>
                </div>
                """, unsafe_allow_html=True)

                col_del2, _ = st.columns([1, 4])
                with col_del2:
                    if st.button("🗑️ Löschen", key=f"del_n_{n['id']}"):
                        conn = get_db()
                        conn.execute("DELETE FROM notizen WHERE id=?", (n['id'],))
                        conn.commit()
                        conn.close()
                        st.rerun()
