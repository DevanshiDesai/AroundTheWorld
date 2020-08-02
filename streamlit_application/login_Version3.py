import streamlit as st
import pyodbc
import datetime
from PIL import Image
cnxn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=LAPTOP-FDBNNUQO;Database=AroundTheWorld;Trusted_Connection=yes;')
cursor = cnxn.cursor()
def addCustomerData(CustFirstName,CustLastName,CustBirthDate,CustPhoneNo,CustStreetName,CustZipCode,CustEmail,CustPassword,CustAge,CustGender):
    cursor.execute('INSERT INTO Customer(CustFirstName,CustLastName,CustBirthDate,CustPhoneNo,CustStreetName,CustZipCode,CustEmail,CustPassword,CustAge,CustGender) VALUES (?,?,?,?,?,?,?,?,?,?)', (CustFirstName,CustLastName,CustBirthDate,CustPhoneNo,CustStreetName,CustZipCode,CustEmail,CustPassword,CustAge,CustGender))
def addPreferenceData(CustBudget,PrefPackageType,CustID):
    cursor.execute('INSERT INTO CustomerPreference(CustBudget,PrefPackageType,CustID) VALUES (?,?,?)', (CustBudget,PrefPackageType,CustID))
def addPreferenceCity(CityID,CustPrefID):
    cursor.execute('INSERT INTO CustomerPreferredCity(CityID,CustPrefID) VALUES (?,?)', (CityID,CustPrefID))   
def loginCustomer(CustEmail,CustPassword):
    cursor.execute('SELECT * FROM Customer WHERE CustEmail=? AND CustPassword=?', (CustEmail,CustPassword))
    data = cursor.fetchall()
    return data
def viewAllCustomers():
    cursor.execute('SELECT * FROM Customer')
    data = cursor.fetchall()
    return data
def fetchCustIDbyEmail(CustEmail):
    cursor.execute('SELECT CustID FROM Customer WHERE CustEmail=?', (CustEmail))
    data = cursor.fetchall()
    return data
def fetchCustPrefIDbyCustID(CustID):
    cursor.execute('SELECT CustPrefID FROM CustomerPreference WHERE CustID=?', (CustID))
    data = cursor.fetchall()
    return data
def login():
    st.subheader("Login")
    username = st.text_input("Email")
    password = st.text_input("Password", type='password')
    if st.button("Login"):
        loginResult = loginCustomer(username,password)
        if loginResult:
            st.success("Logged in as {}".format(username))
            CustID=fetchCustIDbyEmail(username)
            preference(CustID)
            #st.info(CustID)
        else:
            st.warning("Invalid Username/Password")
def signup():
    st.subheader("Create a New Account")
    CustFirstName = st.text_input("First Name")
    CustLastName = st.text_input("Last Name")
    CustBirthDate = st.date_input("Birth Date")
    CustPhoneNo = st.text_input("Customer Phone No")
    CustStreetName = st.text_input("Street Name")
    CustZipCode = st.text_input("ZipCode")
    CustEmail = st.text_input("Customer Email")
    CustPassword = st.text_input("Customer Password", type='password')
    CustAge = st.number_input("Age",5)
    CustGender = st.text_input("Gender")
    if st.button("SignUp"):
        addCustomerData(CustFirstName,CustLastName,CustBirthDate,CustPhoneNo,CustStreetName,CustZipCode,CustEmail,CustPassword,CustAge,CustGender)
        st.success("Congratulations!!! You have successfully created an account")
        login()
def preference(CustID):
    st.subheader("Enter your preferences")
    CustBudget = st.text_input("Budget")
    PrefPackageType = st.text_input("Package Type")
    if st.button("Submit"):
        addPreferenceData(CustBudget,PrefPackageType,CustID)
        CustPrefID=fetchCustPrefIDbyCustID(CustID)
        preferenceCity(CustPrefID)
def preferenceCity(CustPrefID):
    st.subheader("Enter your preferred cities")
    CustDestination = st.text_input("Preferred Destination")
    if st.button("Proceed"):
        st.info(CustPrefID)
        addPreferenceCity(CustDestination,CustPrefID) 
def main():
    
  
    menu = ["Home", "SignUp","Login","Preference","Package"]
    choice = st.sidebar.selectbox("Menu", menu)
    if choice == "Home":
        with open("style.css") as f:
            st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)
            st.markdown("<h2 style='text-align: center; color: black;'>Around The World - A Travel Management System </h2>", unsafe_allow_html=True)
            st.markdown('<style>body{background-color: #CAFFCA;}</style>',unsafe_allow_html=True)

        image = Image.open("C:\\Users\\lenovo\\Desktop\\Streamlit\\AroundTheWorld-master\\streamlit_application\\Logo.png")
        st.image(image, caption ='', width=None )
    
    elif choice == "Login":
        login()
    elif choice == "SignUp":
        signup()
    elif choice == "Preference":
        preference(9)
    elif choice == "City Preference":
        preferenceCity(5)
    cnxn.commit()
    cnxn.close()
main()