import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

st.title("⚽ HKJC Home Odds > 1.9")

@st.cache_data(ttl=600)
def get_data():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options)

    driver.get("https://bet.hkjc.com/ch/football/home")
    time.sleep(10)

    rows = driver.find_elements("xpath", "//tr")

    data = []

    for row in rows:
        try:
            tds = row.find_elements("tag name", "td")
            home = tds[1].text
            away = tds[3].text
            odds = float(tds[5].text)

            if odds > 1.9:
                data.append([home, away, odds])
        except:
            continue

    driver.quit()
    return pd.DataFrame(data, columns=["Home", "Away", "Home Odds"])

df = get_data()

st.dataframe(df)
