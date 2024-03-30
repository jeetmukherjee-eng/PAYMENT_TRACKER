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
def view_paid_fees(variable_value):
    query="SELECT SD.STUDENT_NAME,SF.PAID_STATUS,SF.YEAR,SF.MONTH FROM STUDENT_DETAILS SD INNER JOIN STUDENT_FEES SF ON  SD.PHONE_NUMBER=SF.PHONE_NUMBER where SD.PHONE_NUMBER=%s and SF.PAID_STATUS='Y'"
    mycursor.execute(query, (variable_value,))
    data = mycursor.fetchall()
    return data
def fees_update(PHONE_NUMBER,FEES,PAID_STATUS,YEAR,MONTH,curr_date,trnsc_id):
    
    query1="insert into STUDENT_FEES(PHONE_NUMBER,FEES,PAID_STATUS,YEAR,MONTH,PRIM_KEY_COL) values(%s,%s,%s,%s,%s,%s)"
    PRIM_KEY_COL=PHONE_NUMBER+'-'+YEAR+'-'+MONTH
    val=(PHONE_NUMBER,FEES,PAID_STATUS,YEAR,MONTH,PRIM_KEY_COL)
    mycursor.execute(query1,val)
    mydb.commit()
    query="insert into inter_trnsc_sts(phone_number,curr_date,trnsc_id) values(%s,%s,%s)"
    val1=(PHONE_NUMBER,curr_date,trnsc_id)
    mycursor.execute(query,val1)
    mydb.commit()
    st.balloons()
def view_rejected(variable_value):
    query="SELECT SD.STUDENT_NAME,SF.PAID_STATUS,SF.YEAR,SF.MONTH FROM STUDENT_DETAILS SD INNER JOIN STUDENT_FEES SF ON  SD.PHONE_NUMBER=SF.PHONE_NUMBER where SF.PAID_STATUS='N' and SD.PHONE_NUMBER=%s"
    mycursor.execute(query, (variable_value,))
    data = mycursor.fetchall()
    return data
year=[]
month=[]
status=[]
rej_status=[]
rej_year=[]
rej_month=[]
data = []
data1=[]
x=show_name(st.session_state["name"])

if "input_year" not in st.session_state:
    st.session_state["input_year"]=""
if "input_month" not in st.session_state:
    st.session_state["input_month"]=""

if st.session_state["name"]=="":
    st.write("Please login")
elif(st.session_state["name"]!='8334039125'):
    for i in x:
        st.write("Welcome",i[0])#st.session_state["name"])
    #st.button('View Paid Fees',on_click=view_paid_fees)\
    #button=st.button("View Paid Fees")
    choice=st.selectbox('View Paid Fees/Update Payment Status',['Select Option','View Paid Fees','Update Payment Status','View Rejected Payment'])
    if choice=='View Paid Fees':
        #st.write(st.session_state["name"])
        st.write("Showing Paid Fees for",i[0])

        demo=view_paid_fees(st.session_state["name"])
        
        #st.write(xx)
        #st.write(demo)
        for j in demo:
            #st.write(j)
            year.insert(len(year),j[2])
            month.insert(len(month),j[3])
            if j[1]=="N":
                status.insert(len(status),"Not Paid")
            elif j[1]=="Y":
                status.insert(len(status),"Paid")
        data={'year':year,
              'month':month,
              'status':status}
        df = pd.DataFrame(data)
        st.write(df)
    elif(choice=='Update Payment Status'):
        input_year=st.text_input("Enter The Year")
        
        hh=st.text_input("Enter The Month")
        input_month=hh[:3].upper()
        curr_time=datetime.now()
        transct=st.session_state["name"]+input_year+input_month
        update=st.button('Update')
        if update:
            fees_update(st.session_state["name"],'300','N',input_year,input_month,curr_time,transct)
            st.session_state["input_year"]=input_year
            st.session_state["input_month"]=input_month
            st.text("Fees details has been sent to admin for approval. Once approved please check the 'View Paid Fees' option in 'Home' Tab.")
    elif(choice=='View Rejected Payment'):
        #st.write(view_rejected())
        st.write("Showing Paid Fees for",i[0])

        demo=view_rejected(st.session_state["name"])
        
        #st.write(xx)
        #st.write(demo)
        for j in demo:
            #st.write(j)
            rej_year.insert(len(rej_year),j[2])
            rej_month.insert(len(rej_month),j[3])
            if j[1]=="N":
                rej_status.insert(len(rej_status),"Not Paid")
            elif j[1]=="Y":
                rej_status.insert(len(rej_status),"Paid")
        data1={'year':rej_year,
              'month':rej_month,
              'status':rej_status}
        df1 = pd.DataFrame(data1)
        st.write(df1)
        #st.write(year,month,status)   
        #st.write(df)




# Create the pandas DataFrame
#df = pd.DataFrame(data, columns=['Name', 'Age'])
        
        
        #query="select * from hff"
        #data = sql_executor(query)
        #for i in data:
        #    st.write(i)'''
        

if st.session_state["signout"]==True:
    st.button('Sign Out',on_click=t)