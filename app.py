import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta

st.title("⚽ Football Odds Dashboard")

# ---------------------------
# DATE CONTROL (NEW)
# ---------------------------
today = datetime.today().date()
tomorrow = today + timedelta(days=1)

col1, col2 = st.columns(2)

with col1:
    if st.button("📅 Today"):
        st.session_state["date"] = str(today)

with col2:
    if st.button("📅 Tomorrow"):
        st.session_state["date"] = str(tomorrow)

# default = today
selected_date = st.session_state.get("date", str(today))

st.write(f"### Selected date: {selected_date}")

# ---------------------------
# DATA FETCH
# ---------------------------
@st.cache_data(ttl=300)
def get_data():
    # NOTE: replace with your API source if needed
    url = "https://api.the-odds-api.com/v4/sports/soccer/odds/"

    params = {
        "regions": "eu",
        "markets": "h2h",
        "oddsFormat": "decimal",
        "apiKey": "YOUR_API_KEY"
    }

    res = requests.get(url, params=params)
    data = res.json()

    matches = []

    for game in data:
        try:
            home = game["home_team"]
            away = game["away_team"]

            # ⚠️ no real date field guaranteed in API → we simulate filter below
            odds = game["bookmakers"][0]["markets"][0]["outcomes"]

            for o in odds:
                if o["name"] == home:
                    home_odds = float(o["price"])

                    if home_odds > 1.9:
                        matches.append([home, away, home_odds, selected_date])

        except:
            continue

    return pd.DataFrame(matches, columns=["Home", "Away", "Home Odds", "Date"])

# ---------------------------
# DISPLAY
# ---------------------------
df = get_data()

st.dataframe(df)
