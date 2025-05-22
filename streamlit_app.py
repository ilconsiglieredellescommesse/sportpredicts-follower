
import streamlit as st
import requests
from datetime import datetime
import pytz

# Titolo e layout
st.set_page_config(layout="wide")
st.title("📊 SportPredicts - Partite in Tempo Reale")

# Selezione dello sport
sport = st.selectbox("Scegli lo sport", ["Calcio", "Basket"])

# HEADERS API (da personalizzare)
HEADERS = {
    "x-rapidapi-key": "03A75364E9FA01F0BF505A560EB08496",  # Inserisci la tua API key
    "x-rapidapi-host": "v3.football.api-sports.io" if sport == "Calcio" else "v3.basketball.api-sports.io"
}

# Funzione per recuperare le leghe
@st.cache_data(ttl=3600)
def get_leagues(sport):
    url = "https://v3.football.api-sports.io/leagues" if sport == "Calcio" else "https://v3.basketball.api-sports.io/leagues"
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    return [
        {"id": l["league"]["id"], "name": f'{l["league"]["name"]} - {l["country"]["name"]}'}
        for l in data.get("response", [])
    ]

# Selezione delle leghe
leagues = get_leagues(sport)
selected_leagues = st.multiselect("🔎 Seleziona le leghe da visualizzare", [l["name"] for l in leagues])
selected_ids = [l["id"] for l in leagues if l["name"] in selected_leagues]

# Funzione per caricare le partite
def get_matches(sport):
    if sport == "Calcio":
        url = "https://v3.football.api-sports.io/fixtures"
        params = {"date": datetime.now().strftime("%Y-%m-%d")}
    else:
        url = "https://v3.basketball.api-sports.io/games"
        params = {"date": datetime.now().strftime("%Y-%m-%d")}
    
    response = requests.get(url, headers=HEADERS, params=params)
    return response.json().get("response", [])

# Visualizzazione partite
matches = get_matches(sport)

if not matches:
    st.info("⚠️ Nessuna partita trovata per oggi.")
else:
    for match in matches:
        league_id = match["league"]["id"] if sport == "Calcio" else match["league"]["id"]
        if selected_ids and league_id not in selected_ids:
            continue

        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"### {match['teams']['home']['name']} 🆚 {match['teams']['away']['name']}")
            st.caption(f"🏆 {match['league']['name']} | 📍 {match['league']['country']}")
        
        with col2:
            # Orario corretto con fuso italiano
            utc_time = datetime.fromisoformat(match['fixture']['date'].replace("Z", "+00:00"))
            local_time = utc_time.astimezone(pytz.timezone("Europe/Rome"))
            st.write("🕒", local_time.strftime("%H:%M"))

        st.divider()

