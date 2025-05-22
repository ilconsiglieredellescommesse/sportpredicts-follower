
import streamlit as st
import requests
from datetime import date

st.set_page_config(page_title="SportPredicts - Follower", layout="centered")

st.title("📊 Pronostici Sportivi - Versione Follower")

sport = st.selectbox("Seleziona sport", ["Calcio", "Basket"])
selected_date = st.date_input("Seleziona data", value=date.today())

st.write(f"## Pronostici del {selected_date.strftime('%d/%m/%Y')}")

API_KEY = "03A75364E9FA01F0BF505A560EB08496"
HEADERS = {"x-apisports-key": API_KEY}

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

if matches:
    for match in matches[:10]:  # Limita a 10 per esempio
        if sport == "Calcio":
            home = match["teams"]["home"]["name"]
            away = match["teams"]["away"]["name"]
            time = match["fixture"]["date"][11:16]
            st.markdown(f"- **{home} vs {away}** alle ore {time}")
        else:
            home = match["teams"]["home"]["name"]
            away = match["teams"]["away"]["name"]
            time = match["date"][11:16] if "date" in match else "-"
            st.markdown(f"- **{home} vs {away}** alle ore {time}")
else:
    st.info("Nessuna partita trovata per questa data.")
