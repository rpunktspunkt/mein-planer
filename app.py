import streamlit as st
import sqlite3
from datetime import date, datetime, timedelta
import calendar

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Mein Planer",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
# CUSTOM CSS – Grün & Natur
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Lato:wght@300;400;500&display=swap');

:root {
    --bg:        #f4f1eb;
    --surface:   #ffffff;
    --surface2:  #eef4ee;
    --border:    #d4e4d4;
    --green1:    #2d6a4f;
    --green2:    #52b788;
    --green3:    #95d5b2;
    --green4:    #b7e4c7;
    --accent:    #774936;
    --text:      #2c2c2c;
    --text-muted:#7a8c7a;
    --radius:    14px;
}

html, body, [class*="css"] {
    font-family: 'Lato', sans-serif !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

.stApp {
    background-color: var(--bg) !important;
}

/* Header */
.app-header {
    text-align: center;
    padding: 2rem 0 1.5rem;
    border-bottom: 2px solid var(--border);
    margin-bottom: 1.5rem;
}
.app-header h1 {
    font-family: 'Playfair Display', serif;
    font-size: 2.8rem;
    font-weight: 700;
    color: var(--green1);
    margin: 0;
    letter-spacing: -0.5px;
}
.app-header p {
    color: var(--text-muted);
    font-size: 0.95rem;
    margin-top: 0.3rem;
    font-weight: 300;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: var(--surface) !important;
    border-radius: 50px !important;
    padding: 5px !important;
    gap: 4px !important;
    border: 1.5px solid var(--border) !important;
    box-shadow: 0 2px 8px rgba(45,106,79,0.07) !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 50px !important;
    color: var(--text-muted) !important;
    font-family: 'Lato', sans-serif !important;
    font-weight: 500 !important;
    padding: 0.45rem 1.4rem !important;
    font-size: 0.9rem !important;
}
.stTabs [aria-selected="true"] {
    background: var(--green1) !important;
    color: white !important;
}
.stTabs [data-baseweb="tab-panel"] {
    padding-top: 1.5rem !important;
}

/* Cards */
.card {
    background: var(--surface);
    border: 1.5px solid var(--border);
    border-radius: var(--radius);
    padding: 1rem 1.25rem;
    margin-bottom: 0.65rem;
    transition: box-shadow 0.2s, border-color 0.2s;
}
.card:hover {
    box-shadow: 0 4px 16px rgba(45,106,79,0.1);
    border-color: var(--green3);
}
.card-title {
    font-family: 'Playfair Display', serif;
    font-weight: 600;
    font-size: 1rem;
    color: var(--green1);
    margin: 0 0 0.2rem;
}
.card-meta {
    color: var(--text-muted);
    font-size: 0.8rem;
}

/* Badges */
.badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 50px;
    font-size: 0.72rem;
    font-weight: 600;
}
.badge-green  { background: #d8f3dc; color: var(--green1); border: 1px solid var(--green3); }
.badge-brown  { background: #f2e8e5; color: var(--accent); border: 1px solid #c9a99a; }
.badge-sage   { background: #eef4ee; color: #4a7c59;       border: 1px solid #b0ccb0; }
.badge-olive  { background: #f0f4e8; color: #5a6e2a;       border: 1px solid #c2d18a; }
.badge-red    { background: #fde8e8; color: #c0392b;       border: 1px solid #f5b7b1; }

/* Stats */
.stat-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 1.5rem;
}
.stat-card {
    background: var(--surface);
    border-radius: var(--radius);
    padding: 1rem;
    text-align: center;
    border: 1.5px solid var(--border);
    box-shadow: 0 2px 8px rgba(45,106,79,0.05);
}
.stat-number {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    font-weight: 700;
    color: var(--green1);
}
.stat-label {
    font-size: 0.72rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* Section titles */
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--green1);
    margin: 1.25rem 0 0.75rem;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid var(--border);
}

/* Inputs */
.stTextInput input, .stTextArea textarea {
    background: var(--surface) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'Lato', sans-serif !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: var(--green2) !important;
    box-shadow: 0 0 0 3px rgba(82,183,136,0.15) !important;
}

/* Buttons */
.stButton button {
    background: var(--green1) !important;
    color: white !important;
    border: none !important;
    border-radius: 50px !important;
    font-family: 'Lato', sans-serif !important;
    font-weight: 600 !important;
    padding: 0.45rem 1.8rem !important;
    letter-spacing: 0.3px !important;
    transition: all 0.2s !important;
}
.stButton button:hover {
    background: #1b4332 !important;
    box-shadow: 0 4px 14px rgba(45,106,79,0.25) !important;
    transform: translateY(-1px) !important;
}

/* Kalender */
.cal-grid {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 5px;
    margin-top: 0.75rem;
}
.cal-day-header {
    text-align: center;
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
    background: var(--surface);
    border: 1.5px solid var(--border);
    min-height: 42px;
    color: var(--text);
    position: relative;
}
.cal-day.today {
    background: var(--green1);
    border-color: var(--green1);
    color: white;
    font-weight: 700;
}
.cal-day.has-event::after {
    content: '';
    position: absolute;
    bottom: 5px;
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background: var(--green2);
}
.cal-day.today.has-event::after {
    background: var(--green4);
}
.cal-day.empty {
    background: transparent;
    border-color: transparent;
}
.cal-month-header {
    font-family: 'Playfair Display', serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--green1);
    text-align: center;
}

/* Tagesplan */
.hour-block {
    display: flex;
    gap: 12px;
    margin-bottom: 4px;
    align-items: stretch;
    min-height: 38px;
}
.hour-label {
    font-size: 0.75rem;
    color: var(--text-muted);
    width: 42px;
    text-align: right;
    padding-top: 8px;
    flex-shrink: 0;
    font-weight: 500;
}
.hour-content {
    flex: 1;
    background: var(--surface);
    border: 1.5px solid var(--border);
    border-radius: 8px;
    padding: 6px 12px;
    font-size: 0.85rem;
    color: var(--text);
    min-height: 38px;
}
.hour-content.has-entry {
    background: var(--surface2);
    border-color: var(--green3);
    color: var(--green1);
    font-weight: 500;
}
.hour-content.current-hour {
    border-color: var(--green1);
    border-width: 2px;
}

/* Einkaufsliste */
.shop-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 12px;
    background: var(--surface);
    border: 1.5px solid var(--border);
    border-radius: 10px;
    margin-bottom: 5px;
}
.shop-item.gekauft {
    opacity: 0.45;
    text-decoration: line-through;
}

/* Checkbox */
.stCheckbox label { color: var(--text) !important; }

/* Success */
.stSuccess { background: #d8f3dc !important; color: var(--green1) !important; border-color: var(--green2) !important; }
.stError { background: #fde8e8 !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--green3); border-radius: 3px; }

/* Selectbox */
div[data-baseweb="select"] > div {
    background: var(--surface) !important;
    border-color: var(--border) !important;
    border-radius: 10px !important;
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
            farbe TEXT DEFAULT 'green',
            wiederkehrend TEXT DEFAULT 'einmalig',
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
            farbe TEXT DEFAULT 'green',
            erstellt TEXT DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS einkauf (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            artikel TEXT NOT NULL,
            menge TEXT,
            kategorie TEXT DEFAULT 'Sonstiges',
            gekauft INTEGER DEFAULT 0,
            erstellt TEXT DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS tagesplan (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            datum TEXT NOT NULL,
            stunde INTEGER NOT NULL,
            eintrag TEXT NOT NULL
        );
    """)
    conn.commit()
    conn.close()

init_db()

today = date.today()


# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
wochentage_de = ["Montag","Dienstag","Mittwoch","Donnerstag","Freitag","Samstag","Sonntag"]
monate_de = ["","Januar","Februar","März","April","Mai","Juni","Juli","August","September","Oktober","November","Dezember"]
wochentag = wochentage_de[today.weekday()]

st.markdown(f"""
<div class="app-header">
    <h1>🌿 Mein Planer</h1>
    <p>{wochentag}, {today.day}. {monate_de[today.month]} {today.year}</p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# STATS
# ─────────────────────────────────────────────
conn = get_db()
n_termine   = conn.execute("SELECT COUNT(*) FROM termine WHERE datum >= ?", (str(today),)).fetchone()[0]
n_offen     = conn.execute("SELECT COUNT(*) FROM aufgaben WHERE erledigt=0").fetchone()[0]
n_notizen   = conn.execute("SELECT COUNT(*) FROM notizen").fetchone()[0]
n_einkauf   = conn.execute("SELECT COUNT(*) FROM einkauf WHERE gekauft=0").fetchone()[0]
conn.close()

st.markdown(f"""
<div class="stat-grid">
    <div class="stat-card">
        <div class="stat-number">{n_termine}</div>
        <div class="stat-label">Kommende Termine</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">{n_offen}</div>
        <div class="stat-label">Offene Aufgaben</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">{n_notizen}</div>
        <div class="stat-label">Notizen</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">{n_einkauf}</div>
        <div class="stat-label">Einkauf offen</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📆 Kalender", "🗓️ Termine", "⏰ Tagesplan", "✅ Aufgaben", "🛒 Einkauf", "📝 Notizen"
])


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
        if st.button("◀ Zurück", key="cal_back"):
            if st.session_state.cal_month == 1:
                st.session_state.cal_month = 12
                st.session_state.cal_year -= 1
            else:
                st.session_state.cal_month -= 1

    with col_nav3:
        if st.button("Vor ▶", key="cal_fwd"):
            if st.session_state.cal_month == 12:
                st.session_state.cal_month = 1
                st.session_state.cal_year += 1
            else:
                st.session_state.cal_month += 1

    yr = st.session_state.cal_year
    mo = st.session_state.cal_month

    with col_nav2:
        st.markdown(f'<div class="cal-month-header">{monate_de[mo]} {yr}</div>', unsafe_allow_html=True)

    conn = get_db()
    month_str = f"{yr}-{mo:02d}"
    termine_im_monat = conn.execute(
        "SELECT datum FROM termine WHERE datum LIKE ?", (f"{month_str}%",)
    ).fetchall()
    conn.close()
    tage_mit_termin = set(t["datum"] for t in termine_im_monat)

    cal = calendar.monthcalendar(yr, mo)
    wochentage_kurz = ["Mo","Di","Mi","Do","Fr","Sa","So"]

    cal_html = '<div class="cal-grid">'
    for tag in wochentage_kurz:
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
    st.markdown('<div class="card-meta" style="margin-top:0.5rem">● Grüner Punkt = Termin vorhanden &nbsp;·&nbsp; Grün ausgefüllt = Heute</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Termine in diesem Monat</div>', unsafe_allow_html=True)
    conn = get_db()
    termine_liste = conn.execute(
        "SELECT * FROM termine WHERE datum LIKE ? ORDER BY datum, uhrzeit", (f"{month_str}%",)
    ).fetchall()
    conn.close()

    if not termine_liste:
        st.markdown('<div class="card-meta">Keine Termine in diesem Monat.</div>', unsafe_allow_html=True)
    else:
        for t in termine_liste:
            uhr = f"⏰ {t['uhrzeit'][:5]}" if t['uhrzeit'] else ""
            wdh = f" · 🔁 {t['wiederkehrend']}" if t['wiederkehrend'] != 'einmalig' else ""
            desc = f"<br><span class='card-meta'>{t['beschreibung']}</span>" if t['beschreibung'] else ""
            st.markdown(f"""
            <div class="card">
                <div class="card-title">{t['titel']}</div>
                <div class="card-meta">
                    <span class="badge badge-green">{t['datum']}</span>
                    &nbsp;{uhr}{wdh}{desc}
                </div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 2: TERMINE
# ══════════════════════════════════════════════
with tab2:
    col_form, col_list = st.columns([1, 1], gap="large")

    with col_form:
        st.markdown('<div class="section-title">Neuen Termin eintragen</div>', unsafe_allow_html=True)
        titel = st.text_input("Titel *", placeholder="z.B. Arzttermin, Geburtstag...")
        col_d, col_t = st.columns(2)
        with col_d:
            datum_t = st.date_input("Datum", today, key="t_datum")
        with col_t:
            uhrzeit_t = st.time_input("Uhrzeit", key="t_uhrzeit")
        beschreibung = st.text_area("Beschreibung (optional)", height=70, placeholder="Details...")

        wiederkehrend = st.selectbox("Wiederkehrend?", 
            ["einmalig", "täglich", "wöchentlich", "monatlich", "jährlich"],
            format_func=lambda x: {
                "einmalig": "⬜ Einmalig",
                "täglich": "🔁 Täglich",
                "wöchentlich": "🔁 Wöchentlich",
                "monatlich": "🔁 Monatlich",
                "jährlich": "🎂 Jährlich (z.B. Geburtstag)"
            }[x])

        if st.button("💾 Termin speichern"):
            if titel.strip():
                conn = get_db()
                conn.execute(
                    "INSERT INTO termine (titel, datum, uhrzeit, beschreibung, wiederkehrend) VALUES (?,?,?,?,?)",
                    (titel.strip(), str(datum_t), str(uhrzeit_t), beschreibung.strip(), wiederkehrend)
                )
                conn.commit()
                conn.close()
                st.success("✅ Termin gespeichert!")
                st.rerun()
            else:
                st.error("Bitte einen Titel eingeben.")

    with col_list:
        st.markdown('<div class="section-title">Alle Termine</div>', unsafe_allow_html=True)
        conn = get_db()
        alle_termine = conn.execute("SELECT * FROM termine ORDER BY datum, uhrzeit").fetchall()
        conn.close()

        if not alle_termine:
            st.markdown('<div class="card-meta">Noch keine Termine eingetragen.</div>', unsafe_allow_html=True)
        else:
            for t in alle_termine:
                ist_vergangen = t['datum'] < str(today)
                uhr = f" · {t['uhrzeit'][:5]}" if t['uhrzeit'] else ""
                wdh = f" · 🔁 {t['wiederkehrend']}" if t['wiederkehrend'] != 'einmalig' else ""
                opacity = "opacity:0.45;" if ist_vergangen else ""
                desc = f"<br><span class='card-meta'>{t['beschreibung']}</span>" if t['beschreibung'] else ""
                st.markdown(f"""
                <div class="card" style="{opacity}">
                    <div class="card-title">{t['titel']}</div>
                    <div class="card-meta">
                        <span class="badge badge-green">{t['datum']}{uhr}</span>
                        {wdh}{desc}
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
# TAB 3: TAGESPLAN
# ══════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-title">Tagesplan</div>', unsafe_allow_html=True)

    col_tp1, col_tp2 = st.columns([1, 2], gap="large")

    with col_tp1:
        plan_datum = st.date_input("Tag auswählen", today, key="tagesplan_datum")

        st.markdown('<div class="section-title" style="font-size:0.95rem">Eintrag hinzufügen</div>', unsafe_allow_html=True)
        stunde = st.selectbox("Uhrzeit", list(range(6, 23)),
                               format_func=lambda x: f"{x:02d}:00 Uhr")
        eintrag_text = st.text_input("Was ist geplant?", placeholder="z.B. Sport, Meeting...")

        if st.button("➕ Eintrag speichern", key="save_tp"):
            if eintrag_text.strip():
                conn = get_db()
                # Vorhandenen Eintrag für diese Stunde ersetzen
                conn.execute("DELETE FROM tagesplan WHERE datum=? AND stunde=?", (str(plan_datum), stunde))
                conn.execute("INSERT INTO tagesplan (datum, stunde, eintrag) VALUES (?,?,?)",
                             (str(plan_datum), stunde, eintrag_text.strip()))
                conn.commit()
                conn.close()
                st.success("✅ Gespeichert!")
                st.rerun()

    with col_tp2:
        datum_label = f"{plan_datum.day}. {monate_de[plan_datum.month]} {plan_datum.year}"
        st.markdown(f'<div class="section-title">{datum_label}</div>', unsafe_allow_html=True)

        conn = get_db()
        eintraege = conn.execute(
            "SELECT stunde, eintrag FROM tagesplan WHERE datum=?", (str(plan_datum),)
        ).fetchall()
        conn.close()
        stunden_map = {e['stunde']: e['eintrag'] for e in eintraege}

        # Auch Termine dieses Tages laden
        conn = get_db()
        termine_heute = conn.execute(
            "SELECT titel, uhrzeit FROM termine WHERE datum=?", (str(plan_datum),)
        ).fetchall()
        conn.close()
        termin_map = {}
        for t in termine_heute:
            if t['uhrzeit']:
                h = int(t['uhrzeit'][:2])
                termin_map[h] = f"📌 {t['titel']}"

        aktuell_stunde = datetime.now().hour

        html = ""
        for h in range(6, 23):
            eintrag = stunden_map.get(h, "")
            termin = termin_map.get(h, "")
            inhalt = ""
            if termin:
                inhalt += termin
            if eintrag:
                inhalt += f" · {eintrag}" if inhalt else eintrag

            is_current = (str(plan_datum) == str(today) and h == aktuell_stunde)
            content_class = "hour-content"
            if inhalt:
                content_class += " has-entry"
            if is_current:
                content_class += " current-hour"

            anzeige = inhalt if inhalt else ""
            html += f"""
            <div class="hour-block">
                <div class="hour-label">{h:02d}:00</div>
                <div class="{content_class}">{anzeige}</div>
            </div>
            """
        st.markdown(html, unsafe_allow_html=True)

        # Löschen-Option
        if stunden_map:
            st.markdown('<div class="section-title" style="font-size:0.9rem;margin-top:1rem">Eintrag löschen</div>', unsafe_allow_html=True)
            del_stunde = st.selectbox("Welche Stunde löschen?",
                sorted(stunden_map.keys()),
                format_func=lambda x: f"{x:02d}:00 – {stunden_map[x]}")
            if st.button("🗑️ Eintrag löschen", key="del_tp"):
                conn = get_db()
                conn.execute("DELETE FROM tagesplan WHERE datum=? AND stunde=?", (str(plan_datum), del_stunde))
                conn.commit()
                conn.close()
                st.rerun()


# ══════════════════════════════════════════════
# TAB 4: AUFGABEN
# ══════════════════════════════════════════════
with tab4:
    col_form2, col_list2 = st.columns([1, 1], gap="large")

    with col_form2:
        st.markdown('<div class="section-title">Neue Aufgabe</div>', unsafe_allow_html=True)
        aufgabe_text = st.text_input("Aufgabe *", placeholder="Was muss erledigt werden?")
        faellig = st.date_input("Fällig bis (optional)", value=None, key="aufgabe_faellig")
        prio = st.selectbox("Priorität", ["hoch", "mittel", "niedrig"],
                             format_func=lambda x: {"hoch": "🔴 Hoch", "mittel": "🟡 Mittel", "niedrig": "🟢 Niedrig"}[x])

        if st.button("💾 Aufgabe hinzufügen"):
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
        st.markdown('<div class="section-title">Meine Aufgaben</div>', unsafe_allow_html=True)
        conn = get_db()
        alle_aufgaben = conn.execute(
            "SELECT * FROM aufgaben ORDER BY erledigt ASC, CASE prioritaet WHEN 'hoch' THEN 0 WHEN 'mittel' THEN 1 ELSE 2 END, faellig"
        ).fetchall()
        conn.close()

        prio_badge = {"hoch": "badge-red", "mittel": "badge-brown", "niedrig": "badge-sage"}
        prio_icon  = {"hoch": "🔴", "mittel": "🟡", "niedrig": "🟢"}

        offen    = [a for a in alle_aufgaben if not a['erledigt']]
        erledigt = [a for a in alle_aufgaben if a['erledigt']]

        if not alle_aufgaben:
            st.markdown('<div class="card-meta">Noch keine Aufgaben eingetragen.</div>', unsafe_allow_html=True)

        for a in offen:
            badge_cls = prio_badge.get(a['prioritaet'], 'badge-sage')
            icon = prio_icon.get(a['prioritaet'], '')
            faellig_str = f" · fällig: {a['faellig']}" if a['faellig'] else ""
            ueberfaellig = a['faellig'] and a['faellig'] < str(today)
            ue_html = ' <span class="badge badge-red">⚠️ Überfällig</span>' if ueberfaellig else ""

            col_cb, col_info, col_d = st.columns([0.5, 3.5, 0.8])
            with col_cb:
                if st.checkbox("", key=f"cb_{a['id']}", value=False):
                    conn = get_db()
                    conn.execute("UPDATE aufgaben SET erledigt=1 WHERE id=?", (a['id'],))
                    conn.commit()
                    conn.close()
                    st.rerun()
            with col_info:
                st.markdown(f"""
                <div style="padding-top:0.3rem">
                    <span style="font-weight:500">{a['text']}</span>{ue_html}
                    <br><span class="badge {badge_cls}">{icon} {a['prioritaet'].capitalize()}</span>
                    <span class="card-meta">{faellig_str}</span>
                </div>""", unsafe_allow_html=True)
            with col_d:
                if st.button("🗑️", key=f"del_a_{a['id']}"):
                    conn = get_db()
                    conn.execute("DELETE FROM aufgaben WHERE id=?", (a['id'],))
                    conn.commit()
                    conn.close()
                    st.rerun()

        if erledigt:
            st.markdown('<div class="section-title" style="color:var(--text-muted);font-size:0.9rem;margin-top:1rem">✅ Erledigt</div>', unsafe_allow_html=True)
            for a in erledigt:
                col_cb2, col_info2, col_d2 = st.columns([0.5, 3.5, 0.8])
                with col_cb2:
                    if not st.checkbox("", key=f"cb_{a['id']}", value=True):
                        conn = get_db()
                        conn.execute("UPDATE aufgaben SET erledigt=0 WHERE id=?", (a['id'],))
                        conn.commit()
                        conn.close()
                        st.rerun()
                with col_info2:
                    st.markdown(f'<div style="padding-top:0.3rem;opacity:0.4;text-decoration:line-through">{a["text"]}</div>', unsafe_allow_html=True)
                with col_d2:
                    if st.button("🗑️", key=f"del_a_{a['id']}"):
                        conn = get_db()
                        conn.execute("DELETE FROM aufgaben WHERE id=?", (a['id'],))
                        conn.commit()
                        conn.close()
                        st.rerun()


# ══════════════════════════════════════════════
# TAB 5: EINKAUFSLISTE
# ══════════════════════════════════════════════
with tab5:
    col_shop1, col_shop2 = st.columns([1, 1], gap="large")

    with col_shop1:
        st.markdown('<div class="section-title">Artikel hinzufügen</div>', unsafe_allow_html=True)
        artikel = st.text_input("Artikel *", placeholder="z.B. Brot, Milch...")
        col_m, col_k = st.columns(2)
        with col_m:
            menge = st.text_input("Menge", placeholder="z.B. 2x, 500g...")
        with col_k:
            kategorie = st.selectbox("Kategorie", 
                ["Obst & Gemüse", "Milchprodukte", "Fleisch & Fisch", "Backwaren",
                 "Getränke", "Tiefkühl", "Haushalt", "Sonstiges"])

        if st.button("➕ Hinzufügen", key="save_shop"):
            if artikel.strip():
                conn = get_db()
                conn.execute("INSERT INTO einkauf (artikel, menge, kategorie) VALUES (?,?,?)",
                             (artikel.strip(), menge.strip(), kategorie))
                conn.commit()
                conn.close()
                st.success("✅ Hinzugefügt!")
                st.rerun()
            else:
                st.error("Bitte einen Artikel eingeben.")

        st.markdown('<div style="margin-top:1rem"></div>', unsafe_allow_html=True)
        if st.button("🧹 Alle erledigten löschen", key="clear_shop"):
            conn = get_db()
            conn.execute("DELETE FROM einkauf WHERE gekauft=1")
            conn.commit()
            conn.close()
            st.rerun()

    with col_shop2:
        st.markdown('<div class="section-title">Einkaufsliste</div>', unsafe_allow_html=True)
        conn = get_db()
        alle_artikel = conn.execute(
            "SELECT * FROM einkauf ORDER BY gekauft ASC, kategorie, artikel"
        ).fetchall()
        conn.close()

        if not alle_artikel:
            st.markdown('<div class="card-meta">Die Einkaufsliste ist leer.</div>', unsafe_allow_html=True)
        else:
            aktuelle_kat = None
            for a in alle_artikel:
                if not a['gekauft'] and a['kategorie'] != aktuelle_kat:
                    aktuelle_kat = a['kategorie']
                    st.markdown(f'<div class="card-meta" style="margin-top:0.75rem;font-weight:600;color:var(--green1)">{aktuelle_kat}</div>', unsafe_allow_html=True)

                menge_str = f" · {a['menge']}" if a['menge'] else ""
                durchgestrichen = "text-decoration:line-through;opacity:0.4;" if a['gekauft'] else ""

                col_cb3, col_info3, col_d3 = st.columns([0.5, 3.5, 0.8])
                with col_cb3:
                    checked = st.checkbox("", key=f"shop_{a['id']}", value=bool(a['gekauft']))
                    if checked != bool(a['gekauft']):
                        conn = get_db()
                        conn.execute("UPDATE einkauf SET gekauft=? WHERE id=?", (1 if checked else 0, a['id']))
                        conn.commit()
                        conn.close()
                        st.rerun()
                with col_info3:
                    st.markdown(f'<div style="padding-top:0.3rem;{durchgestrichen}">{a["artikel"]}<span class="card-meta">{menge_str}</span></div>', unsafe_allow_html=True)
                with col_d3:
                    if st.button("🗑️", key=f"del_shop_{a['id']}"):
                        conn = get_db()
                        conn.execute("DELETE FROM einkauf WHERE id=?", (a['id'],))
                        conn.commit()
                        conn.close()
                        st.rerun()


# ══════════════════════════════════════════════
# TAB 6: NOTIZEN
# ══════════════════════════════════════════════
with tab6:
    col_form3, col_list3 = st.columns([1, 1], gap="large")

    with col_form3:
        st.markdown('<div class="section-title">Neue Notiz</div>', unsafe_allow_html=True)
        notiz_titel = st.text_input("Titel (optional)", placeholder="z.B. Ideen, Rezept...")
        notiz_inhalt = st.text_area("Notiz *", height=150, placeholder="Schreib hier...")
        notiz_farbe = st.selectbox("Farbe", ["green", "brown", "sage", "olive"],
                                    format_func=lambda x: {"green": "🟢 Grün", "brown": "🟤 Braun", "sage": "🌿 Salbei", "olive": "🫒 Olive"}[x])

        if st.button("💾 Notiz speichern"):
            if notiz_inhalt.strip():
                conn = get_db()
                conn.execute("INSERT INTO notizen (titel, inhalt, farbe) VALUES (?,?,?)",
                             (notiz_titel.strip(), notiz_inhalt.strip(), notiz_farbe))
                conn.commit()
                conn.close()
                st.success("✅ Notiz gespeichert!")
                st.rerun()
            else:
                st.error("Bitte Inhalt eingeben.")

    with col_list3:
        st.markdown('<div class="section-title">Meine Notizen</div>', unsafe_allow_html=True)
        conn = get_db()
        alle_notizen = conn.execute("SELECT * FROM notizen ORDER BY erstellt DESC").fetchall()
        conn.close()

        farb_map = {
            "green": ("#2d6a4f", "#d8f3dc"),
            "brown": ("#774936", "#f2e8e5"),
            "sage":  ("#4a7c59", "#eef4ee"),
            "olive": ("#5a6e2a", "#f0f4e8"),
        }

        if not alle_notizen:
            st.markdown('<div class="card-meta">Noch keine Notizen vorhanden.</div>', unsafe_allow_html=True)
        else:
            for n in alle_notizen:
                text_color, bg_color = farb_map.get(n['farbe'], ("#2d6a4f", "#d8f3dc"))
                titel_html = f"<div class='card-title' style='color:{text_color}'>{n['titel']}</div>" if n['titel'] else ""
                datum_fmt = n['erstellt'][:10] if n['erstellt'] else ""
                st.markdown(f"""
                <div class="card" style="border-left:3px solid {text_color};background:{bg_color}">
                    {titel_html}
                    <div style="white-space:pre-wrap;font-size:0.9rem;line-height:1.6">{n['inhalt']}</div>
                    <div class="card-meta" style="margin-top:0.4rem">{datum_fmt}</div>
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
