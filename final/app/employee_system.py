import streamlit as st
import pyodbc
import datetime
import pandas as pd
from PIL import Image 

cnxn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=LAPTOP-4BH8IBHF\MSSQLSERVER01;Database=AroundTheWorld;Trusted_Connection=yes;')
cursor = cnxn.cursor()


def addCustomerData(CustFirstName,CustLastName,CustBirthDate,CustPhoneNo,CustStreetName,CustZipCode,CustEmail,CustPassword,CustGender):
    cursor.execute('INSERT INTO Customer(CustFirstName,CustLastName,CustBirthDate,CustPhoneNo,CustStreetName,CustZipCode,CustEmail,CustPassword,CustGender) VALUES (?,?,?,?,?,?,?,?,?)', (CustFirstName,CustLastName,CustBirthDate,CustPhoneNo,CustStreetName,CustZipCode,CustEmail,CustPassword,CustGender))

def addPreferenceData(CustID,CustBudget,PrefPackageType):
    cursor.execute('INSERT INTO CustomerPreference(CustID,CustBudget,PrefPackageType) VALUES (?,?,?)', (CustID,CustBudget,PrefPackageType))

def addPreferenceCityData(CustPrefID1,CityName1,CustPrefID2,CityName2):
    cursor.execute('INSERT INTO CustPreferredCity(CustPrefID,CityID) VALUES (?,(SELECT CityID from City WHERE CityName =?)),(?,(SELECT CityID from City WHERE CityName =?))', (CustPrefID1,CityName1,CustPrefID2,CityName2))   

def addVisaStatusData(CustID,VisaID,VisaOutcome,RejectedReason,VisaDate):
    cursor.execute('INSERT INTO VisaStatus(CustID,VisaID,VisaOutcome,RejectedReason,VisaDate) VALUES(?,?,?,?,?)',(CustID,VisaID,VisaOutcome,RejectedReason,VisaDate))

def addBookingData(CustID,EmployeeID,PackageID,IsLatest,BookingStatus,TripStartDate,TripEndDate):
    cursor.execute('INSERT INTO Booking(CustID,EmployeeID,PackageID,IsLatest,BookingStatus,TripStartDate,TripEndDate) VALUES (?,?,?,?,?,?,?)', (CustID,EmployeeID,PackageID,IsLatest,BookingStatus,TripStartDate,TripEndDate))   

def Payment(BookingID):
    cursor.execute('UPDATE Payment SET PaymentStatus=1 where BookingID=(BookingID) and PaymentDate = (SELECT MAX(PaymentDate) from Payment)')

def Fluctuate():
    cursor.execute('EXEC FlightWrappingSP')

def viewCustomerInfo():
    synth_state = st.text('Fetching Data...')
    df = data = pd.read_sql('SELECT CustID, CustFirstName, CustLastName, CustEmail FROM Customer', cnxn)
    synth_state.text('Completed!')
    st.dataframe(df)

def viewAllCustomerPreference():
    synth_state = st.text('Fetching Data...')
    df = data = pd.read_sql('SELECT CustPrefID, CustFirstName, CustLastName FROM CustomerPreference p JOIN Customer c ON c.CustID = p.CustID', cnxn)
    synth_state.text('Completed!')
    st.dataframe(df)

def ViewVisaInformation():
    synth_state = st.text('Fetching Data...')
    df = data = pd.read_sql('SELECT VisaID, CountryName, IsVisaRequired FROM Visa v JOIN Country c ON v.CountryID = c.CountryID', cnxn)
    synth_state.text('Completed!')
    st.dataframe(df)

def viewPackages():
    synth_state = st.text('Fetching Data...')
    df = data = pd.read_sql('SELECT * FROM vwPackages', cnxn)
    synth_state.text('Completed!')
    st.dataframe(df)

def viewBookingAmount():
    synth_state = st.text('Fetching Data...')
    df = data = pd.read_sql('select BookingID, Discount, FinalAmount, PaymentStatus from Payment order by PaymentID desc', cnxn)
    synth_state.text('Completed!')
    st.dataframe(df)

def viewFlightPrices():
    synth_state = st.text('Fetching Data...')
    df = data = pd.read_sql('select * from LatestFlightPrices', cnxn)
    synth_state.text('Completed!')
    st.dataframe(df)

gender = {"Male":1, "Female":2, "Other":3}

package = {"Wildlife":1, "Family":2, "Adventure":3, "Romantic":4}

outcome = {"Accepted":1, "Rejected":2}

def main():
    """ Around The World - Travel Management System """
    st.sidebar.title("Select Required Action")
    choice = st.sidebar.radio(label="View and Update Details", options=["Home", "Customer Registration", "Customer Preference", "Customer Preferred Destinations", "Visa Status", "Customer Booking", "Payment", "Flight"])
    
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
        st.subheader("New Customer Registration: Enter Customer's Details")
        CustFirstName = st.text_input("First Name")
        CustLastName = st.text_input("Last Name")
        CustBirthDate = st.date_input("Birth Date")
        CustPhoneNo = st.text_input("Customer Phone No")
        CustStreetName = st.text_input("Street Name")
        CustZipCode = st.text_input("ZipCode")
        CustEmail = st.text_input("Customer Email")
        CustPassword = st.text_input("Customer Password", type='password')
        CustGender = st.radio("Gender",tuple(gender.keys()))       
        if st.button("Register"):
            addCustomerData(CustFirstName,CustLastName,CustBirthDate,CustPhoneNo,CustStreetName,CustZipCode,CustEmail,CustPassword,CustGender)
            st.success("Customer was successfully registered!")

    
    elif choice == "Customer Preference":
        st.markdown('<style>body{background-color: #C9C9FF;}</style>',unsafe_allow_html=True)
        st.subheader("Check existing customer information")
        if st.button("View Customer Information"):
            viewCustomerInfo()
        st.subheader("New Preference Registration: Enter Customer's Preference")
        CustID = st.number_input("Customer ID",1)
        CustBudget = st.number_input("Budget",100.00)
        PrefPackageType = st.radio("Package Type",tuple(package.keys()))  
        if st.button("Save Preference"):
            addPreferenceData(CustID,CustBudget,PrefPackageType)
            st.success("Preference successfully recorded!")
    
    elif choice == "Customer Preferred Destinations":
        st.markdown('<style>body{background-color: #CAFFCA;}</style>',unsafe_allow_html=True)
        st.subheader("Check existing customer preference information")
        if st.button("View destination preferences"):
            viewAllCustomerPreference()
        st.subheader("New Destination Registration: Provide Minimum 2 Preferred Destinations")
        CustPrefID1 = st.number_input("Customer Preference ID",1)
        CityName1 = st.text_input("First Preferred City")
        CustPrefID2 = st.number_input("Re-enter Customer Preference ID",1)
        CityName2 = st.text_input("Second Preferred City")
        if st.button("Save Destinations"):
            addPreferenceCityData(CustPrefID1,CityName1,CustPrefID2,CityName2)
            st.success("Destinations successfully recorded!")
            st.info("Re-enter IDs to provide more preferences.")

    elif choice == "Visa Status":
        st.markdown('<style>body{background-color: #FFC9C9;}</style>',unsafe_allow_html=True)
        st.subheader("Check Visa and customer information")
        if st.button("View Customer information"):
            viewCustomerInfo()
        if st.button("View Visa Information"):
            ViewVisaInformation()
        st.subheader("Provide Visa Status Information")
        CustID = st.text_input("Enter CustID")
        VisaID = st.text_input("Enter VisaID")
        VisaOutcome = st.radio("Visa Outcome",tuple(outcome.keys()))
        RejectedReason = st.text_input("Mention reason for rejection")
        VisaDate = st.date_input("Enter visa application date")
        if st.button("Save Visa Status"):
            addVisaStatusData(CustID,VisaID,VisaOutcome,RejectedReason,VisaDate)
            st.success("Visa status information saved successfully!")

    elif choice == "Customer Booking":
        st.markdown('<style>body{background-color: #C9C9FF;}</style>',unsafe_allow_html=True)
        st.subheader("Check customers' information and package details")
        if st.button("View Customer information"):
            viewCustomerInfo()
        if st.button("View All Packages"):
            viewPackages()
        st.subheader("Enter the booking details for the customer")
        CustID = st.number_input("Customer ID",1)
        EmployeeID = st.number_input("Employee ID",1)
        PackageID = st.number_input("Package ID",1)
        IsLatest = 1 
        TripStartDate = st.date_input("Trip Start Date")
        TripEndDate = st.date_input("Trip End Date")
        BookingStatus = "New"
        if st.button("Save Booking"):
            addBookingData(CustID,EmployeeID,PackageID,IsLatest,BookingStatus,TripStartDate,TripEndDate)
            st.success("Successfully added Booking Details!")
                
    elif choice == "Payment":
        st.markdown('<style>body{background-color: #C9C9FF;}</style>',unsafe_allow_html=True)
        st.subheader("Click the button below to check the payment information")
        if st.button("Check Payment Details"):
            viewBookingAmount()
        st.subheader("Confirm Payment")
        BookingID = st.number_input ("Booking ID:",1)
        if st.button("Confirm Payment"):
            Payment(BookingID)
            st.success("Payment was successful") 

    elif choice == "Flight":
        st.markdown('<style>body{background-color: #FFC9C9;}</style>',unsafe_allow_html=True)
        st.subheader ("Update Flight Prices")
        if st.button("Refresh Flight Prices"):
            Fluctuate()
        if st.button("Check updated Prices"):
            viewFlightPrices()


    cnxn.commit()
    cnxn.close()

main()
