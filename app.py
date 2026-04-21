import streamlit as st
import pandas as pd
import requests

st.title("⚽ Football Matches (Home Odds > 1.9)")

@st.cache_data(ttl=300)
def get_data():
    url = "https://api.the-odds-api.com/v4/sports/soccer/odds/"
    
    params = {
        "regions": "eu",
        "markets": "h2h",
        "oddsFormat": "decimal",
        "apiKey": "cf9ec9f6bd2c8e2fdead11116576821d"
    }

    res = requests.get(url, params=params)
    data = res.json()

    matches = []

    for game in data:
        try:
            home = game["home_team"]
            away = game["away_team"]

            # take first bookmaker
            odds = game["bookmakers"][0]["markets"][0]["outcomes"]

            for o in odds:
                if o["name"] == home:
                    home_odds = float(o["price"])

                    if home_odds > 1.9:
                        matches.append([home, away, home_odds])
        except:
            continue

    return pd.DataFrame(matches, columns=["Home", "Away", "Home Odds"])

df = get_data()

st.dataframe(df)
