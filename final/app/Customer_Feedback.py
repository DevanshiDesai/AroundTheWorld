import streamlit as st
import pyodbc
import datetime
import pandas as pd
from PIL import Image 

cnxn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=LAPTOP-4BH8IBHF\MSSQLSERVER01;Database=AroundTheWorld;Trusted_Connection=yes;')
cursor = cnxn.cursor()

def addFeedbackData(BookingID,CustomerRating,FeedbackDescription):
    cursor.execute('INSERT INTO CustomerFeedback(BookingID,CustomerRating,FeedbackDescription) VALUES (?,?,?)', (BookingID,CustomerRating,FeedbackDescription))  

st.markdown('<style>body{background-color: #C9C9FF;}</style>',unsafe_allow_html=True)

st.subheader("Please Rate Your Experience Below:")
BookingID = st.number_input("Enter your Booking ID:",1)
CustomerRating = st.number_input("Rate your experience on a scale of 1 to 10:",1)
FeedbackDescription=st.text_input("Additional feedback:")
if st.button("Save Feedback"):
    addFeedbackData(BookingID,CustomerRating,FeedbackDescription)
    st.success("Successfully added Feedback")
    st.info("Thank you for the feedback.")

cnxn.commit()
cnxn.close()