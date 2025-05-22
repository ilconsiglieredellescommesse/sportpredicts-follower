import streamlit as st
import requests
from datetime import datetime, date
import pytz

st.set_page_config(page_title="SportPredicts - Follower", layout="centered")

st.markdown("<h2 style='text-align: center;'>📊 Pronostici Sportivi</h2>", unsafe_allow_html=True)

API_KEY = "03A75364E9FA01F0BF505A560EB08496"
HEADERS = {"x-apisports-key": API_KEY}
TIMEZONE = "Europe/Rome"

if "preferiti" not in st.session_state:
    st.session_state.preferiti = []

sport = st.selectbox("Seleziona sport", ["Calcio", "Basket"])
selected_date = st.date_input("Data", value=date.today())

st.write("Filtri avanzati (facoltativi):")
min_quota = st.slider("Quota minima", 1.0, 5.0, 1.5, 0.1)
max_quota = st.slider("Quota massima", 1.0, 10.0, 3.0, 0.1)

def get_matches(sport, selected_date):
    formatted_date = selected_date.strftime("%Y-%m-%d")
    if sport == "Calcio":
        url = f"https://v3.football.api-sports.io/fixtures?date={formatted_date}"
    else:
        url = f"https://v3.basketball.api-sports.io/games?date={formatted_date}"

    try:
        response = requests.get(url, headers=HEADERS)
        data = response.json()
        return data.get("response", [])
    except Exception as e:
        st.error("Errore nel recupero dei dati API")
        return []

matches = get_matches(sport, selected_date)

def convert_utc_to_local(utc_string):
    utc_time = datetime.fromisoformat(utc_string.replace("Z", "+00:00"))
    utc_time = utc_time.astimezone(pytz.timezone(TIMEZONE))
    return utc_time.strftime("%H:%M")

st.subheader(f"Pronostici del {selected_date.strftime('%d/%m/%Y')}")

if matches:
    for match in matches[:15]:  # max 15
        if sport == "Calcio":
            home = match["teams"]["home"]["name"]
            away = match["teams"]["away"]["name"]
            time = convert_utc_to_local(match["fixture"]["date"])
            match_id = match["fixture"]["id"]
            quote = 1.80  # Placeholder
        else:
            home = match["teams"]["home"]["name"]
            away = match["teams"]["away"]["name"]
            time = convert_utc_to_local(match["date"])
            match_id = match["id"]
            quote = 1.90  # Placeholder

        if min_quota <= quote <= max_quota:
            col1, col2 = st.columns([0.85, 0.15])
            with col1:
                st.markdown(f"**{home} vs {away}** — 🕒 {time} — Quota: {quote}")
            with col2:
                if st.button("❤️", key=str(match_id)):
                    st.session_state.preferiti.append(f"{home} vs {away} — {time}")

    if st.session_state.preferiti:
        st.subheader("⭐ Pronostici salvati")
        for p in st.session_state.preferiti:
            st.markdown(f"- {p}")
else:
    st.info("Nessuna partita trovata per questa data.")

