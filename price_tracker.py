import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import time
import os


# ----- Function to get product details -----
def get_amazon_data(url):
    # Setup Selenium
    service = Service("chromedriver.exe")  # path to your chromedriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Extract details
    title = soup.find(id="productTitle").get_text(strip=True)
    price_whole = soup.find("span", class_="a-price-whole")
    price_fraction = soup.find("span", class_="a-price-fraction")

    if price_whole:
        price = price_whole.get_text() + (price_fraction.get_text() if price_fraction else "")
    else:
        price = "Price not found"

    driver.quit()
    return {"Product Name": title, "Price": price, "URL": url}


# ----- Streamlit UI -----
st.title("Amazon Price Tracker")
url = st.text_input("Enter Amazon Product URL")
if st.button("Fetch and Save Data"):
    if url:
        data = get_amazon_data(url)
        df = pd.DataFrame([data])
        csv_file = "amazon_price.csv"
        df.to_csv(csv_file, index=False)
        st.success("Data saved to amazon_price.csv")
        with open(csv_file, "rb") as f:
            st.download_button("Download CSV", f, file_name="amazon_price.csv")
    else:
        st.error("Please enter a valid URL")
