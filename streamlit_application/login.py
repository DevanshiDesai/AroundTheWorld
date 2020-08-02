import streamlit as st
import pyodbc
import datetime

cnxn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=LAPTOP-4BH8IBHF\MSSQLSERVER01;Database=AroundTheWorld;Trusted_Connection=yes;')
cursor = cnxn.cursor()

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
        if st.button("Login"):
            loginResult = loginCustomer(username,password)
            if loginResult:
                st.success("Logged in as {}".format(username))

   elif choice == "SignUp":
        st.subheader("Create a New Account")
        CustFirstName = st.text_input("First Name")
        CustLastName = st.text_input("Last Name")
        CustBirthDate = st.text_input("Birth Date")
        CustPhoneNo = st.number_input("Customer Phone No",0)
        CustStreetName = st.text_input("Street Name")
        CustZipCode = st.text_input("ZipCode")
        CustEmail = st.text_input("Customer Email")
        CustPassword = st.text_input("Customer Password", type='password')
        CustAge = st.number_input("Age",5)
        CustGender = st.text_input("Gender")
        if st.button("SignUp"):
            addCustomerData(CustFirstName,CustLastName,CustBirthDate,CustPhoneNo,CustStreetName,CustZipCode,CustEmail,CustPassword,CustAge,CustGender)
            st.success("Congratulations!!! You have successfully created an account")
            st.info("Go to Login Page")
 
 
    cnxn.commit()
    cnxn.close()

main()
