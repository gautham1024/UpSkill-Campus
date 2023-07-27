import streamlit as st
import mysql.connector
import random
import pandas as pd
import string
import re

st.title("Password Manager")
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Gautam@10",
    database="db1"
)
cur = mydb.cursor()

def add_data(name,password,key):
    cur.execute("INSERT INTO pass1(acc_name, password) VALUES (%s, AES_ENCRYPT(%s, %s))", (name, password, key))
    mydb.commit()

def view_data(input_key):
    cur.execute("SELECT CONVERT(AES_DECRYPT(password, %s) USING utf8) AS password FROM pass1",(input_key,))
    data = cur.fetchone()
    return data
 


menu = ["Password Store","Password Generator","Password Retrieve","Password Checker"]
choice = st.sidebar.selectbox("Menu", menu)
if choice == "Password Store":
    name = st.text_input("Enter name: ")
    password = st.text_input("Enter password: ")
    key = st.text_input("Enter key which is required to retrieve: ")
    if st.button("Add Password"):
        add_data(name, password, key)
        st.success("Password added successfully.")


if choice == "Password Checker":
    def password_check_strength(password):
        length_regex = re.compile(r'.{8,}')
        uppercase_regex = re.compile(r'[A-Z]')
        lowercase_regex = re.compile(r'[a-z]')
        digit_regex = re.compile(r'\d')
        special_char_regex = re.compile(r'[!@#$%^&*(),.?":{}|<>]')

        if not length_regex.search(password):
            return "Weak: Password should be atleast 8 characters long."
        if not uppercase_regex.search(password):
            return "Weak: Password should contain atleast one uppercase letter."
        if not lowercase_regex.search(password):
            return "Weak: Password should contain atleast one lowercase letter."
        if not digit_regex.search(password):
            return "Weak: Password should contain atleast one digit."
        if not special_char_regex.search(password):
            return "Weak: Password should contain atleast one special character."
        
        return "Strong: Password is strong."
    password = st.text_input("Enter the password: ")
    result = password_check_strength(password)
    st.write(result)

    

if choice == "Password Generator":
    passw_regex = re.compile(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[' + re.escape(string.punctuation) + r'])[\w' + re.escape(string.punctuation) + r']{8,}$')
    passlen = st.number_input("Enter Password Length: ", min_value=8)
    
    while True:
        password = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=int(passlen)))
        if passw_regex.match(password):
            break
    
    st.write("Generated Password:", password)

if choice == "Password Retrieve":
    input_key = st.text_input("Enter key: ")
    if input_key:
        result = view_data(input_key)
        if result:
            df = pd.DataFrame(result)
            st.dataframe(df)
        else:
            st.write("No passwords found for the given key.")



