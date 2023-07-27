import streamlit as st
import pyshorteners
import mysql.connector
import pandas as pd

st.title("URL Shortener")

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Gautam@10",
    database="db1"
)

cur = mydb.cursor()

def add_data(longurl, shorturl):
    cur.execute("INSERT INTO linkinfo2(longurl, shorturl) VALUES (%s, %s)", (longurl, shorturl))
    mydb.commit()

def view_data():
    cur.execute("SELECT * FROM linkinfo2")
    data = cur.fetchall()
    return data

menu = ["URL_Shortener", "History"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "URL_Shortener":
    url = st.text_input("Enter long URL:")
    
    if url:
        try:
            s = pyshorteners.Shortener()
            short_url = s.tinyurl.short(url)
            st.write("Shortened URL:", short_url)
            add_data(url, short_url)
        except pyshorteners.exceptions.BadURLException:
            st.write("Invalid URL. Please enter a valid URL.")

if choice == "History":
    result = view_data()
    st.write(result)
    df=pd.DataFrame(result,columns=["LongURL","ShortURL"])
    st.dataframe(df)

