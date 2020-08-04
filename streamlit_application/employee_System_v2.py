import streamlit as st
import pyodbc
import datetime
import pandas as pd
from PIL import Image 

cnxn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=LAPTOP-FDBNNUQO;Database=AroundTheWorld;Trusted_Connection=yes;')
cursor = cnxn.cursor()


def addCustomerData(CustFirstName,CustLastName,CustBirthDate,CustPhoneNo,CustStreetName,CustZipCode,CustEmail,CustPassword,CustAge,CustGender):
    cursor.execute('INSERT INTO Customer(CustFirstName,CustLastName,CustBirthDate,CustPhoneNo,CustStreetName,CustZipCode,CustEmail,CustPassword,CustAge,CustGender) VALUES (?,?,?,?,?,?,?,?,?,?)', (CustFirstName,CustLastName,CustBirthDate,CustPhoneNo,CustStreetName,CustZipCode,CustEmail,CustPassword,CustAge,CustGender))

def addPreferenceData(CustID,CustBudget,PrefPackageType):
    cursor.execute('INSERT INTO CustomerPreference(CustID,CustBudget,PrefPackageType) VALUES (?,?,?)', (CustID,CustBudget,PrefPackageType))

def addPreferenceCityData(CustPrefID1,CityID1,CustPrefID2,CityID2):
    cursor.execute('INSERT INTO CustPreferredCity(CustPrefID,CityID) VALUES (?,?),(?,?)', (CustPrefID1,CityID1,CustPrefID2,CityID2))   

def addBookingData(CustID,EmployeeID,PackageID,IsLatest,BookingStatus,TripStartDate,TripEndDate,BookingAmount):
    cursor.execute('INSERT INTO Booking(CustID,EmployeeID,PackageID,IsLatest,BookingStatus,TripStartDate,TripEndDate,FinalBookingAmount) VALUES (?,?,?,?,?,?,?,?)', (CustID,EmployeeID,PackageID,IsLatest,BookingStatus,TripStartDate,TripEndDate,BookingAmount))   

def addFeedbackData(BookingID,CustomerRating,FeedbackDescription):
    cursor.execute('INSERT INTO CustomerFeedback(BookingID,CustomerRating,FeedbackDescription) VALUES (?,?,?)', (BookingID,CustomerRating,FeedbackDescription))  


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

def viewAllCustomerBookings():
    synth_state = st.text('Fetching Data...')
    df = data = pd.read_sql('SELECT * FROM Booking', cnxn)
    synth_state.text('Completed!')
    st.dataframe(df)


gender = {"Male":1, "Female":2, "Other":3}
islatest = {"Yes":1, "No":2}

def main():
    """ Around The World - Travel Management System """
    st.sidebar.title("Select Required Action")
    choice = st.sidebar.radio(label="View and Update Details", options=["Home", "Customer Registration", "Customer Preference", "Customer Preferred Destinations", "Visa Status", "Customer Booking", "Payment", "Customer Feedback"])
    
    if choice == "Home":
        st.markdown("<h1 style='text-align: center; color: black;'>Around The World - Employee Portal</h1>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center; color: black;'>The portal FETCHES, INSERTS and UPDATES data in <i>real-time<i>.</h4>", unsafe_allow_html=True)
        with open("style.css") as f:
            st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)
            st.markdown('<style>body{background-color: #CAFFCA;}</style>',unsafe_allow_html=True)

        image = Image.open("C:\\Users\\lenovo\\Desktop\\Streamlit\\AroundTheWorld-master\\streamlit_application\\Logo.png")
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

    elif choice == "Customer Booking":
        st.markdown('<style>body{background-color: #C9C9FF;}</style>',unsafe_allow_html=True)
        st.subheader("Check existing bookings for the customers")
        if st.button("View All Customer Bookings"):
            viewAllCustomerBookings()
        
        st.subheader("Enter the booking details for the customer")
        CustID = st.number_input("Customer ID")
        EmployeeID = st.number_input("Employee ID")
        PackageID = st.number_input("Package ID")
        IsLatest =st.radio("Is Latest",tuple(islatest.keys())) 
        TripStartDate = st.date_input("Trip Start Date")
        TripEndDate = st.date_input("Trip End Date")
        BookingAmount = st.number_input("Total Booking Amount")
        BookingStatus =st.text_input("Booking Status")
        if st.button("Save Booking"):
            addBookingData(CustID,EmployeeID,PackageID,IsLatest,BookingStatus,TripStartDate,TripEndDate,BookingAmount)
            st.success("Successfully added Booking Details!")

    elif choice == "Customer Feedback":
        st.markdown('<style>body{background-color: #C9C9FF;}</style>',unsafe_allow_html=True)
        st.subheader("Check existing bookings for the customers")
        if st.button("View All Customer Bookings"):
            viewAllCustomerBookings()
        
        st.subheader("Enter the customer feedback")
    
        BookingID = st.number_input("Booking ID")
        CustomerRating = st.number_input("Customer Rating")
        FeedbackDescription=st.text_input("Enter customer Feedback")
        if st.button("Save Feedback"):
            addFeedbackData(BookingID,CustomerRating,FeedbackDescription)
            st.success("Successfully added Feedback")
            


    cnxn.commit()
    cnxn.close()

main()