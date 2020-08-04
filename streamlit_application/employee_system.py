import streamlit as st
import pyodbc
import datetime
import pandas as pd
from PIL import Image 

cnxn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=LAPTOP-4BH8IBHF\MSSQLSERVER01;Database=AroundTheWorld;Trusted_Connection=yes;')
cursor = cnxn.cursor()


def addCustomerData(CustFirstName,CustLastName,CustBirthDate,CustPhoneNo,CustStreetName,CustZipCode,CustEmail,CustPassword,CustAge,CustGender):
    cursor.execute('INSERT INTO Customer(CustFirstName,CustLastName,CustBirthDate,CustPhoneNo,CustStreetName,CustZipCode,CustEmail,CustPassword,CustAge,CustGender) VALUES (?,?,?,?,?,?,?,?,?,?)', (CustFirstName,CustLastName,CustBirthDate,CustPhoneNo,CustStreetName,CustZipCode,CustEmail,CustPassword,CustAge,CustGender))

def addPreferenceData(CustID,CustBudget,PrefPackageType):
    cursor.execute('INSERT INTO CustomerPreference(CustID,CustBudget,PrefPackageType) VALUES (?,?,?)', (CustID,CustBudget,PrefPackageType))

def addPreferenceCityData(CustPrefID1,CityID1,CustPrefID2,CityID2):
    cursor.execute('INSERT INTO CustPreferredCity(CustPrefID,CityID) VALUES (?,?),(?,?)', (CustPrefID1,CityID1,CustPrefID2,CityID2))   

def viewAllCustomers():
    synth_state = st.text('Fetching Data...')
    df = data = pd.read_sql('SELECT * FROM Customer', cnxn)
    synth_state.text('Completed!')
    st.dataframe(df)

def viewAllCustomerPreferences():
    synth_state = st.text('Fetching Data...')
    df = data = pd.read_sql('SELECT * FROM CustomerPreference', cnxn)
    synth_state.text('Completed!')
    st.dataframe(df)

def viewAllCustomerPrefCities():
    synth_state = st.text('Fetching Data...')
    df = data = pd.read_sql('SELECT * FROM CustPreferredCity', cnxn)
    synth_state.text('Completed!')
    st.dataframe(df)

gender = {"Male":1, "Female":2, "None":3}

def main():
    """ Around The World - Travel Management System """
    st.sidebar.title("Select Required Action")
    choice = st.sidebar.radio(label="View and Update Details", options=["Home", "Customer Registration", "Customer Preference", "Customer Preferred Destinations", "Visa Status", "Booking", "Payment", "Customer Feedback"])
    
    if choice == "Home":
        st.markdown("<h1 style='text-align: center; color: black;'>Around The World - Employee Portal</h1>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center; color: black;'>The portal FETCHES, INSERTS and UPDATES data in <i>real-time<i>.</h4>", unsafe_allow_html=True)
        with open("style.css") as f:
            st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)
            st.markdown('<style>body{background-color: #CAFFCA;}</style>',unsafe_allow_html=True)

        image = Image.open("C:\\Users\\Logo.png")
        st.image(image, caption ='', width=None )
    
    elif choice == "Customer Registration":
        st.markdown('<style>body{background-color: #FFC9C9;}</style>',unsafe_allow_html=True)
        st.subheader("Check existing customers")
        if st.button("View customers"):
            viewAllCustomers()
        st.subheader("New Customer Registration: Enter Customer's Details")
        CustFirstName = st.text_input("First Name")
        CustLastName = st.text_input("Last Name")
        CustBirthDate = st.date_input("Birth Date")
        CustPhoneNo = st.text_input("Customer Phone No")
        CustStreetName = st.text_input("Street Name")
        CustZipCode = st.text_input("ZipCode")
        CustEmail = st.text_input("Customer Email")
        CustPassword = st.text_input("Customer Password", type='password')
        CustAge = st.number_input("Age",5)
        CustGender = st.radio("Gender",tuple(gender.keys()))       
        if st.button("Register"):
            addCustomerData(CustFirstName,CustLastName,CustBirthDate,CustPhoneNo,CustStreetName,CustZipCode,CustEmail,CustPassword,CustAge,CustGender)
            st.success("Customer was successfully registered!")

    
    elif choice == "Customer Preference":
        st.markdown('<style>body{background-color: #C9C9FF;}</style>',unsafe_allow_html=True)
        st.subheader("Check existing customer preferences")
        if st.button("View preferences"):
            viewAllCustomerPreferences()
        st.subheader("New Preference Registration: Enter Customer's Preference")
        CustID = st.number_input("Customer ID",1)
        CustBudget = st.number_input("Budget",100.00)
        PrefPackageType = st.text_input("Package Type")  ##change to drop-down
        if st.button("Save Preference"):
            addPreferenceData(CustID,CustBudget,PrefPackageType)
            st.success("Preference successfully recorded!")
    
    elif choice == "Customer Preferred Destinations":
        st.markdown('<style>body{background-color: #CAFFCA;}</style>',unsafe_allow_html=True)
        st.subheader("Check existing customer preferred destinations")
        if st.button("View destination preferences"):
            viewAllCustomerPrefCities()
        st.subheader("New Destination Registration: Provide Minimum 2 Preferred Destinations")
        CustPrefID1 = st.number_input("Customer Preference ID",1)
        CityID1 = st.number_input("First Preferred City ID",1)
        CustPrefID2 = st.number_input("Re-enter Customer Preference ID",1)
        CityID2 = st.number_input("Second Preferred City ID",1)
        if st.button("Save Destinations"):
            addPreferenceCityData(CustPrefID1,CityID1,CustPrefID2,CityID2)
            st.success("Destinations successfully recorded!")
            st.info("Re-enter IDs to provide more preferences.")
        
    cnxn.commit()
    cnxn.close()

main()
