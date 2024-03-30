
import streamlit as st
import mysql.connector
#streamlit run main.py to run the file
mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="Payment_Tracker"
)
mycursor=mydb.cursor()
def sql_executor(raw_code):
    mycursor.execute(raw_code)
    data=mycursor.fetchall()
    return data

st.title("Welcome to Jeet's Classroom")
choice=st.selectbox('Login/Sign Up',['Login','Sign Up'])

#Creating different buttons for sign up and log in


def fetch_data_with_variable(query,variable_value):
    #query = "SELECT password FROM user WHERE mobile_number = %s"
    mycursor.execute(query, (variable_value,))
    data = mycursor.fetchall()
    return data
def auth(name,password):
    fetchphone="select mobile_number from user"
    result=sql_executor(fetchphone)
    query = "SELECT password FROM user WHERE mobile_number = %s"
    data=fetch_data_with_variable(query,name)
    for i in data:
        if(user_password==i[0]):
            return True
        else:
             return False
def admin_sign_up(mobile_number,password,f_name):
    query="insert into user(mobile_number,password,name) values(%s,%s,%s)"
    val=(mobile_number,password,f_name)
    mycursor.execute(query,val)
    mydb.commit()
def sign_up(mobile_number,password,f_name,academic,cla):
    query="insert into user(mobile_number,password,name) values(%s,%s,%s)"
    val=(mobile_number,password,f_name)
    mycursor.execute(query,val)
    mydb.commit()
    query1="insert into STUDENT_DETAILS(STUDENT_NAME,PHONE_NUMBER,Academic_Year,Class) values(%s,%s,%s,%s)"
    val2=(f_name,mobile_number,academic,cla)
    mycursor.execute(query1,val2)
    mydb.commit()
    st.balloons()
def submit():
    st.session_state.my_text = st.session_state.widget
    st.session_state.widget = ""
if "name" not in st.session_state:
        st.session_state["name"]=""
if "signout" not in st.session_state:
     st.session_state["signout"]=""

if choice=='Login':
    name=st.text_input("Enter Your Phone Number")
    user_password=st.text_input("Enter Your Password")
    button=st.button("Log In")
    if button:
        #st.markdown("DB Connection Established")
        #sql="insert into user(mobile_number,password) values(%s,%s)"
        #val=(name,password)
        #mycursor.execute(sql,val)
        if(auth(name,user_password)):
            st.success("Login Successful")
            st.session_state["name"]=name
            st.session_state["signout"]=True
        else:
            st.write("User Not found/Incorrect Credentials.")
elif choice=='Sign Up':
    name=st.text_input("Enter Your Name")
    Phone_number=st.text_input("Enter Your Phone Number")
    user_password=st.text_input("Enter Your Password")
    button1=st.button("Sign Up")
    if button1:
        if Phone_number=='8334039125':
            admin_sign_up(Phone_number,user_password,name)
        else:
            sign_up(Phone_number,user_password,name,'','')
        

