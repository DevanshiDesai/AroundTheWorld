import streamlit as st
import pyodbc
import datetime
import pandas as pd
from PIL import Image 

cnxn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=LAPTOP-4BH8IBHF\MSSQLSERVER01;Database=AroundTheWorld;Trusted_Connection=yes;')
cursor = cnxn.cursor()

st.title('Around The World Admin Portal')

def addEmployeeData(EmpFirstName, EmpLastName, EmpPhoneNumber, EmpEmailAddress, EmpUsername, EmpPassword, EmpDesignation, EmpSalary, EmpAvgRating):
    cursor.execute('INSERT INTO Employee(EmpFirstName, EmpLastName, EmpPhoneNumber, EmpEmailAddress, EmpUsername, EmpPassword, EmpDesignation, EmpSalary, EmpAvgRating) VALUES (?,?,?,?,?,?,?,?,?)', (EmpFirstName,EmpLastName, EmpPhoneNumber, EmpEmailAddress, EmpUsername, EmpPassword, EmpDesignation, EmpSalary, EmpAvgRating)) 


designation = {"Associate Executive":1, "Sales Executive":2, "Senior Sales Executive":3, "Travel Manager":4}

st.markdown('<style>body{background-color: #FFC9C9;}</style>',unsafe_allow_html=True)

st.subheader("New Employee Registration: Enter Employee's Details")
EmpFirstName = st.text_input("First Name")
EmpLastName = st.text_input("Last Name")
EmpPhoneNumber = st.text_input("Phone No")
EmpEmailAddress = st.text_input("Email")
EmpUsername = st.text_input("Username")
EmpPassword = st.text_input("Password", type='password')
EmpDesignation = st.radio("Designation",tuple(designation.keys()))
EmpSalary = st.number_input("Salary",40000.00)
EmpAvgRating = st.number_input("Rating",5.00)      
if st.button("Register"):
    addEmployeeData(EmpFirstName, EmpLastName, EmpPhoneNumber, EmpEmailAddress, EmpUsername, EmpPassword, EmpDesignation, EmpSalary, EmpAvgRating)
    st.success("Employee was successfully registered!")

cnxn.commit()
cnxn.close()

