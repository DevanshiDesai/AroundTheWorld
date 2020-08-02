import streamlit as st
import datetime
import hashlib

from SQLServerConnection import *

def generateHashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def verifyHashes(password,hashed_text):
    if generateHashes(password) == hashed_text:
        return hashed_text
    return False

def addCustomerData(CustFirstName,CustLastName,CustBirthDate,CustPhoneNo,CustStreetName,CustZipCode,CustEmail,CustPassword,CustAge,CustGender):
    cursor.execute('INSERT INTO Customer(CustFirstName,CustLastName,CustBirthDate,CustPhoneNo,CustStreetName,CustZipCode,CustEmail,CustPassword,CustAge,CustGender) VALUES (?,?,?,?,?,?,?,?,?,?)', (CustFirstName,CustLastName,CustBirthDate,CustPhoneNo,CustStreetName,CustZipCode,CustEmail,CustPassword,CustAge,CustGender))

def loginCustomer(CustEmail,CustPassword):
    cursor.execute('SELECT * FROM Customer WHERE CustEmail=? AND CustPassword=?', (CustEmail,CustPassword))
    data = cursor.fetchall()
    return data

def viewAllCustomers():
    cursor.execute('SELECT * FROM Customer')
    data = cursor.fetchall()
    return data

gender = {"Male":1, "Female":2, "None":3}

def get_value(val, my_dict):
    for key,value in my_dict.items():
        if val == key:
            return value

def get_key(val, my_dict):
    for key,value in my_dict.items():
        if val == key:
            return key

def main():

    """ Around The World - Travel Management System """

    menu = ["Home", "Login", "SignUp"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Welcome to Around The World - Travel Management System")

    elif choice == "Login":
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        hashed_password = generateHashes(password)
        if st.button("Login"):
            loginResult = loginCustomer(username,verifyHashes(password,hashed_password))
            if loginResult:
                st.success("Logged in as {}".format(username))
            else:
                st.warning("Invalid Username/Password")

    elif choice == "SignUp":
        st.subheader("Create a New Account")
        CustFirstName = st.text_input("First Name")
        CustLastName = st.text_input("Last Name")
        CustBirthDate = st.date_input("Birth Date")
        CustPhoneNo = st.text_input("Customer Phone Number")
        CustStreetName = st.text_input("Street Name")
        CustZipCode = st.text_input("ZipCode")
        CustEmail = st.text_input("Customer Email")
        CustPassword = st.text_input("Customer Password", type='password')
        new_Cust_hashed_password = generateHashes(CustPassword)
        CustAge = st.number_input("CustAge",7)
        CustGender = st.radio("Gender",tuple(gender.keys()))
        if st.button("SignUp"):
            addCustomerData(CustFirstName,CustLastName,CustBirthDate,CustPhoneNo,CustStreetName,CustZipCode,CustEmail,new_Cust_hashed_password,CustAge,CustGender)
            st.success("Congratulations!!! You have successfully created an account")
            st.info("Go to Login Page")

main()