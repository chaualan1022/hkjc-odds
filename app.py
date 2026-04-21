import streamlit as st
import pandas as pd
import requests

st.title("⚽ HKJC Home Odds > 1.9")

@st.cache_data(ttl=300)
def get_data():
    url = "https://bet.hkjc.com/football/getJSON.aspx?jsontype=odds_allodds"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    res = requests.get(url, headers=headers)
    data = res.json()

    matches = []

    try:
        for match in data["matches"]:
            home = match.get("homeTeamName")
            away = match.get("awayTeamName")

            had = match.get("had", {})
            home_odds = had.get("h")

            if home_odds:
                home_odds = float(home_odds)

                if home_odds > 1.9:
                    matches.append([home, away, home_odds])
    except:
        pass

    return pd.DataFrame(matches, columns=["Home", "Away", "Home Odds"])

df = get_data()

st.dataframe(df)
