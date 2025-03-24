import streamlit as st
from datetime import datetime
import os
import mysql.connector
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

#The connector
connector = mysql.connector.connect(
    host="localhost",
    user="test",
    password="password",
    database="persona"
    )
cursor = connector.cursor()

# Configure page
st.set_page_config(
    page_title='Persona',
    layout='centered',
    page_icon='🌿',
)



#The session variables
#Get userID and name
if "uID" not in st.session_state:
    st.session_state.uID = 1
    query = "SELECT name from users where uID = %s"
    values = [st.session_state.uID]
    cursor.execute(query,values)
    name = cursor.fetchone()[0]
    st.session_state.name = name
    st.session_state.trend = "Normal"


# Content header
st.title('🌿 Persona Counsellor Dashboard')





# Sidebar with information
with st.sidebar:
    st.title('🌿 Persona')
    st.markdown('''
    ## About
    A friendly, interactive AI powered platform curated to assist students' mental well-being
    
    This dashboard can be used to monitor the mental health of students

    _Made by Team Draco 🐉_
    ''')
    #Select the list of students
    query = "SELECT uID,name from users"
    cursor.execute(query)

    rows = cursor.fetchall()

    options = []
    for row in rows:
        options.append(str(row[0])+" : "+row[1])

    st.markdown(
        '''## Choose a profile'''
    )

    #A drop down menu to select the student
    option = st.selectbox(
    "Name",options
    )
    new_id = options.index(option)+1


    #If we have changed the user
    if(new_id!= st.session_state.uID):
        st.session_state.uID = new_id
        query = "SELECT name from users where uID = %s"
        values = [st.session_state.uID]
        cursor.execute(query,values)
        name = cursor.fetchone()[0]
        st.session_state.name = name

        #Rerun to update
        st.rerun()


#Get overviewdata
query = "SELECT sentiment,count(sentiment) from users,usercon,conmess,messages where users.uID = usercon.uID and usercon.cID = conmess.cID and conmess.mID = messages.mID and users.uID = %s group by sentiment"
values = [st.session_state.uID]
cursor.execute(query,values)
rows = cursor.fetchall()

x =[]
y =[]
#For each row
for row in rows:
    if(row[0]!=None):
        x.append(row[0])
        y.append(row[1])

#The actual information
st.header(str(st.session_state.name).title())
st.divider()

#Summary
st.subheader("Summary")
st.divider()
#Put summary down here

st.subheader("Mental State Map")
st.divider()
#Display
fig, ax = plt.subplots()
ax.pie(y,labels=None,autopct='%1.0f%%',pctdistance=1.2)
ax.legend(x, loc="upper left", bbox_to_anchor=(1, 1))  # Move legend outside

st.pyplot(fig)

#Trends
st.subheader("Psychological Trends")
st.divider()


#Get unique sentiments
query = "SELECT DISTINCT(SENTIMENT) FROM users,usercon,conmess,messages where users.uID = usercon.uID and usercon.cID = conmess.cID and conmess.mID = messages.mID and users.uID = %s"
values = [st.session_state.uID]
cursor.execute(query,values)

rows = cursor.fetchall()

selection = []
for row in rows:
    if(row[0] is None):
        continue
    selection.append(row[0])

trend = st.selectbox("Trend to Follow",selection)
#Update trend
if(trend!=st.session_state.trend):
    st.session_state.trend = trend
    st.rerun()

#Get graph
query = "SELECT count(*) from users,usercon,conversations,conmess,messages where users.uID = usercon.uID and usercon.cID =conversations.cID and conversations.CID = conmess.cID and conmess.mID = messages.mID and users.uID = %s and sentiment=%s group by conversations.cID order by conversations.lastInteraction;"
values = [st.session_state.uID,st.session_state.trend]
cursor.execute(query,values)
x = []
y = []
i=0
for row in cursor.fetchall():
    y.append(row[0])
    x.append(i)
    i+=1

#Smoothen the curve
x_smooth =x
y_smooth =y
if(len(x)>=3):
    spl = make_interp_spline(x,y,k=2)
    x_smooth = np.linspace(min(x),max(x),100)
    y_smooth = spl(x_smooth)

#Draw the plot
fig,ax = plt.subplots()
ax.plot(x_smooth,y_smooth,color="red")
ax.fill_between(x_smooth, y_smooth, alpha=0.3, color='red')

ax.set_xlabel("Conversation ID")
ax.set_ylabel("Frequency")
st.pyplot(fig)