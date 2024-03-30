import streamlit as st
import mysql.connector
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
def show_number(var):
    v=var.split()
    variable_name=v[0]
    query="select mobile_number from user where name=%s"
    mycursor.execute(query, (variable_name,))
    data = mycursor.fetchall()
    return data

def show_tranct(var):
    #v=show_number(var)
    #query="select trnsc_id from inter_trnsc_sts where phone_number=%s"
    query="select PHONE_NUMBER,trnsc_id from inter_trnsc_sts where PHONE_NUMBER in (SELECT PHONE_NUMBER FROM STUDENT_DETAILS WHERE STUDENT_NAME =%s)"
    mycursor.execute(query, (var,))
    data = mycursor.fetchall()
    return data
def approved_fees(stat,var):
    query="update student_fees set PAID_STATUS=%s where PRIM_KEY_COL=%s"
    values=(stat,var)
    mycursor.execute(query,values)
    mydb.commit()
def sign_up(mobile_number,password,f_name):
    query="insert into user(mobile_number,password,name) values(%s,%s,%s)"
    val=(mobile_number,password,f_name)
    mycursor.execute(query,val)
    mydb.commit()
    st.balloons()
def fees_update(status,ph_number,year,month):
    query="update student_fees set PAID_STATUS=%s where PHONE_NUMBER=%s and YEAR=%s and MONTH=%s"
    values=(status,ph_number,year,month)
    mycursor.execute(query,values)
    mydb.commit()
def approve_paymeny_status(var,st):
    query="update inter_trnsc_sts set APPROVED_STS=%s where trnsc_id=%s"
    values=(var,st)
    mycursor.execute(query,values)
    mydb.commit()
def view_pending():
    query="select SD.STUDENT_NAME,I.PHONE_NUMBER,I.trnsc_id from inter_trnsc_sts I LEFT JOIN STUDENT_DETAILS SD ON I.phone_number=SD.PHONE_NUMBER where I.APPROVED_STS is NULL or I.APPROVED_STS='Rejected' order by I.id;"
    mycursor.execute(query)
    data=mycursor.fetchall()
    return data
def create_checkboxes(key, values):
    st.write(f"## {key}")
    checkboxes = {}
    for value in values:
        # Concatenate key and value to generate a unique identifier
        checkbox_key = f"{key}-{value}"
        checkboxes[value] = st.checkbox(checkbox_key)
    return checkboxes
def display_quiz(quiz):
    total_questions = len(quiz)
    #correct_answers = 0

    for i, question_data in enumerate(quiz):
        st.write(f"### Question {i+1}/{total_questions}:")
        st.write(question_data['question'])
        # Append the question index to the radio button's key
        selected_option = st.radio(f"Choose an answer for question {i+1}:", ['True', 'False'], key=f"quiz_{i}")
x=show_name(st.session_state["name"])

checkboxes = {}
dic={}
choices=("Approve","Reject")
app_transct=[]
rej_transct=[]
total_pending=[]
agree=[]
approved=[]
rejected=[]
f_approved=[]
f_rejected=[]
jon=[]
if st.session_state["name"]=="":
    st.write("Please login")
elif(st.session_state["name"]=="8334039125"):
    for i in x:
        st.write("Welcome admin",i[0])
    st.markdown("""
            <style>
                div[data-testid="column"] {
                    width: fit-content !important;
                    flex: unset;
                }
                div[data-testid="column"] * {
                    width: fit-content !important;
                }
            </style>
            """, unsafe_allow_html=True)
    col1, col2 = st.columns([1,1])
    with col1:
        choice=st.selectbox('Add Student/Update Payment Status',['Add Student','Update Payment Status','View Pending Approval'])
    #with col2:
    #
    #     button2=st.button('Update Paid Status')
    if choice=='Add Student':
        name=st.text_input("Enter Studen's Name")
        Phone_number=st.text_input("Enter Student's Phone Number")
        user_password=st.text_input("Enter Student's Password")
        b=st.button('Add')
        if b:
            sign_up(Phone_number,user_password,name)
    elif (choice=='Update Payment Status'):
        Phone_number=st.text_input("Enter Student's Phone Number")
        Year=st.text_input("Enter the effective year")
        Month=st.text_input("Enter the effective month(First 3 letter or the month)")
        paid_choice=st.selectbox('Fees Paid/Fees Not Paid',['Paid','Not_Paid'])
        update=st.button('Update Status')
        if update:
            #st.write('k')
            if paid_choice=='Paid':
                fees_update('Y',Phone_number,Year,Month)
                st.write("Thanks For Payment")
            else:
                fees_update('N',Phone_number,Year,Month)
                st.write("Not paid")
    #button1=st.button('Add User')
    #button2=st.button('Update Paid Status')
    elif(choice=='View Pending Approval'):
        
        d=view_pending()
        #st.write(len(d))
        if len(d)>0:
            for i in d:
                #st.write(i)
                Y=i[2]
                NAME_A=i[0]
                YEAR_A=Y[10:14]
                MONTH_A=Y[14:]
                #st.write(NAME_A,YEAR_A,MONTH_A)
                CON=NAME_A+" Has asked you to approve the payment status for"+MONTH_A+" Of "+YEAR_A+" Transaction_ID "+Y
                total_pending.append(CON)
                for i in total_pending:
                    dic[i]=choices
            #st.write(dic)
            for i in dic.items():
                #st.write(i)
                selected_option = st.radio(i[0],('Approve','Reject'))
                if selected_option=='Approve':
                    jon=i[0].split()
                    approved.append(jon[-1])#name only
                elif selected_option=='Reject':
                    jon=i[0].split()
                    rejected.append(jon[-1])
            
            if st.button('Submit'):
                #st.text('Approved')
                for i in approved:
                    #st.write(i)
                    c=i[:10]+"-"+i[10:14]+"-"+i[14:]
                    approved_fees('Y',c)
                    #app_transct.append(show_tranct(i))
                    approve_paymeny_status('Approved',i)

                    #st.write()

                #st.text('Rejected')
                for i in rejected:
                    #st.write(i)
                    #rej_transct.append(show_tranct(i))
                    approve_paymeny_status('Rejected',i)
        else:
            st.write("No Pending Approval")
            
            
        
        
else:
    st.text("You are not authorised to access the admin page.\nPlease navigate to HOME Page or contact the Admin.")


if st.session_state["signout"]==True:
    st.button('Sign Out',on_click=t)