import pyodbc

cnxn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=LAPTOP-O5O0H0NU;Database=AroundTheWorld;Trusted_Connection=yes;')
cursor = cnxn.cursor()

cnxn.commit()
cnxn.close()