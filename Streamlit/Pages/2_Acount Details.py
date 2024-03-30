import streamlit as st
import mysql.connector
import pandas as pd
from datetime import datetime
mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="Payment_Tracker"
)
mycursor=mydb.cursor()

def t():
    st.session_state.name=""
    st.session_state.signout=False
def show_name(variable_value):
    query="select name from user where mobile_number=%s"
    mycursor.execute(query, (variable_value,))
    data = mycursor.fetchall()
    return data
def update_student_details(phone,name,year,cl):
    name_update="update STUDENT_DETAILS set STUDENT_NAME=%s where PHONE_NUMBER=%s"
    year_update="update STUDENT_DETAILS set Academic_Year=%s where PHONE_NUMBER=%s"
    Class_update="update STUDENT_DETAILS set Class=%s where PHONE_NUMBER=%s"
    Ph_update="update STUDENT_DETAILS set PHONE_NUMBER=%s where PHONE_NUMBER=%s"
    name_val=(name,phone)
    year_val=(year,phone)
    cl_val=(cl,phone)
    new_ph_val=(st.session_state["name"],phone)
    mycursor.execute(name_update,name_val)
    mydb.commit()

    mycursor.execute(year_update,year_val)
    mydb.commit()

    mycursor.execute(Class_update,cl_val)
    mydb.commit()

    mycursor.execute(Ph_update,new_ph_val)
    mydb.commit()
    st.balloons()
def show_data(PHONE_NUMBER):
    query="select * from STUDENT_DETAILS where PHONE_NUMBER=%s"
    mycursor.execute(query, (PHONE_NUMBER,))
    data = mycursor.fetchall()
    return data
    #values=(stat,var)
    #mycursor.execute(query,values)
    #mydb.commit()
############################################################################################
if st.session_state["name"]=="":
    st.write("Please login")
elif(st.session_state["name"]!='8334039125'):
    Mobile_Number=st.text_input('Mobile Number',st.session_state["name"])
    s_data=show_data(Mobile_Number)

    N=s_data[0]#show_name(st.session_state["name"])
    #st.write(dat(N[3]))

    initial_date_str=N[3]
    initial_date=datetime.strptime(initial_date_str, '%Y-%m-%d')
    F_Name=st.text_input('First Name',(N[1].split())[0])
    L_Name=st.text_input('Last Name',(N[1].split())[1])
    ACADEMIC_YEAR=st.date_input('Academic Year Start Date',value=initial_date)
    CLASS=st.text_input('Class',N[4])
    if st.button("Submit"):
        update_student_details(Mobile_Number,(F_Name+' '+L_Name),ACADEMIC_YEAR,CLASS)
    #choice=st.selectbox('View Account Details/Update Account Details',['Select Option','View','Update'])
    #if choice=='View':
