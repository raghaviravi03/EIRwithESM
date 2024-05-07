# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import numpy as np
import smtplib
from email.message import EmailMessage
import streamlit as st

if 'logged_in' not in st.session_state:
    st.session_state['logged_in']=False

if 'school_id' not in st.session_state:
    st.session_state['school_id']=None
    
if 'teacher_id' not in st.session_state:
    st.session_state['teacher_id']=None
    
student_id=None
if 'emotions_loaded' not in st.session_state:
    st.session_state['emotions_loaded']=pd.read_excel('8ESM.xlsx')

emotions = st.session_state['emotions_loaded']
emotions.teacher = emotions['teacher'].astype(str)
emotions.student = emotions['student'].astype(str)
emotions = emotions[emotions.sciclass==2]
emotions = emotions[['student', 'teacher', 'school', 'company', 'active', 'anxious', 'bored',
       'challenge', 'competitive', 'concentrate', 'confident', 'confused',
       'connect', 'control', 'cooperative', 'determined', 'enjoy', 'excited',
       'exploring', 'giveup', 'happy', 'imagination', 'importantfuture',
       'importantyou', 'interest', 'lonely', 'otherexpect', 'proud',
       'selfexpect', 'skill', 'solutions', 'stress', 'success', 'time',
       'want_had', 'work_play', 'activity','respyear','respmonth','respday','resphour']]
vals_4 = ['active', 'anxious', 'bored', 'challenge', 'competitive', 'concentrate', 'confident', 'confused', 'connect', 'control', 'cooperative', 'determined', 'enjoy', 'excited', 'exploring', 'giveup', 'happy', 'imagination', 'importantfuture', 'importantyou', 'interest', 'lonely', 'otherexpect', 'proud', 'selfexpect', 'skill', 'solutions', 'stress', 'success', 'time']
vals_4_map = {1.0:'Not at all',2.0:'Not much',3.0:'Somewhat',4.0:'Very much'}
vals_all_maps={}
vals_all_maps['company']={1.0:'Teacher',2.0:'Classmates',3.0:'Teacher and classmates',4.0:'Friends',5.0:'Other students',6.0:'Relatives',7.0:'Alone',8.0:'Other'}
vals_all_maps['want_had'] = {1.0:'You wanted to',2.0:'You had to',3.0:'You had nothing else to do'}
vals_all_maps['work_play'] = {1.0:'More like school work',2.0:'More like play',3.0:'Both',4.0:'Neither'}
vals_all_maps['activity'] = {1.0:'Listening',2.0:'Discussing',3.0:'Writing',4.0:'Calculating',5.0:'Taking a quiz/test',6.0:'Working on a computer',7.0:'Working in a group',8.0:'Laboratory work',9.0:'Presenting',10.0:'Other'}

chemistry_assessment = pd.ExcelFile("ChemistryUnitAssessments.xls")
chemistry_assessment = chemistry_assessment.parse(0)

chemistry_unit1 = chemistry_assessment.iloc[:, : 13]
chemistry_unit1 = pd.concat([chemistry_unit1, chemistry_assessment.iloc[:, list(range(31, 55))]], axis=1)  # get studentID to question info
chemistry_unit1 = pd.concat([chemistry_unit1, chemistry_assessment.iloc[:, [66, 67]]], axis=1)  # School and Region ID

chemistry_unit2 = chemistry_assessment.iloc[:, 13: 24]
chemistry_unit2 = pd.concat([chemistry_unit2, chemistry_assessment.iloc[:, list(range(31, 49))]], axis=1)  # get studentID to question info
chemistry_unit2 = pd.concat([chemistry_unit2, chemistry_assessment.iloc[:, list(range(55, 62))]], axis=1)  # get studentID to question info
chemistry_unit2 = pd.concat([chemistry_unit2, chemistry_assessment.iloc[:, [66, 67]]], axis=1) # School and Region ID

chemistry_unit3 = chemistry_assessment.iloc[:, 24: 27]
chemistry_unit3 = pd.concat([chemistry_unit3, chemistry_assessment.iloc[:, list(range(31, 49))]], axis=1)  # get studentID to question info
chemistry_unit3 = pd.concat([chemistry_unit3, chemistry_assessment.iloc[:, list(range(62, 68))]], axis=1)  

chemistry_unit1_og = chemistry_unit1.dropna(subset=['teacherID', 'stuID', 'schoolID'])
chemistry_unit2_og = chemistry_unit2.dropna(subset=['teacherID', 'stuID', 'schoolID'])
chemistry_unit3_og = chemistry_unit3.dropna(subset=['teacherID', 'stuID', 'schoolID'])

chemistry_unit1_og['teacherID']=chemistry_unit1_og['teacherID'].astype(int).astype(str)
chemistry_unit1_og['schoolID']=chemistry_unit1_og['schoolID'].astype(int).astype(str)
chemistry_unit1_og['stuID']=chemistry_unit1_og['stuID'].astype(np.int64).astype(str)

chemistry_unit2_og['teacherID']=chemistry_unit2_og['teacherID'].astype(int).astype(str)
chemistry_unit2_og['schoolID']=chemistry_unit2_og['schoolID'].astype(int).astype(str)
chemistry_unit2_og['stuID']=chemistry_unit2_og['stuID'].astype(np.int64).astype(str)

chemistry_unit3_og['teacherID']=chemistry_unit3_og['teacherID'].astype(int).astype(str)
chemistry_unit3_og['schoolID']=chemistry_unit3_og['schoolID'].astype(int).astype(str)
chemistry_unit3_og['stuID']=chemistry_unit3_og['stuID'].astype(np.int64).astype(str)


def login_page():
    st.title('Student Performance Dashboard!')
    st.write("#### Please login with your school ID and teacher ID below")
    school_id = st.text_input('Enter School ID below:')
    teacher_id = st.text_input('Enter Teacher ID below:')
    login_button = st.button('Login')
    return school_id, teacher_id, login_button

def display_overall_avg_scores(selection):
    st.write('### Overall Average Scores for Each Question')
    
    if selection=='unit1':
        question_avg = chemistry_unit1.iloc[:, 0:12].mean()
    elif selection=='unit2':
        question_avg = chemistry_unit2.iloc[:, 0:10].mean()
    elif selection=='unit3':
        question_avg = chemistry_unit3.iloc[:, 0:3].mean()
    question_avg_sorted = question_avg.sort_values()
    
    fig = go.Figure(data=[go.Bar(
        x=question_avg_sorted.index,
        y=question_avg_sorted.values,
        marker_color='skyblue'  # Set color of bars
    )])
    
    fig.update_layout(
        xaxis=dict(title='Questions'),
        yaxis=dict(title='Average Score'),
        bargap=0.15,  # Gap between bars of adjacent location coordinates
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    st.write("The overall average scores serve as a benchmark for assessing the overall understanding and mastery of the unit's concepts by the student population.")
    st.plotly_chart(fig)
    st.write("By examining which questions have higher or lower average scores, you can identify topics that students excel in and areas that may require additional focus and instruction.")

def display_specific_avg_scores(school_id, teacher_id, selection):
    st.write('### Average Scores of your students for Each Question')
    if selection=='unit1':
        teacher_data = chemistry_unit1[(chemistry_unit1_og['teacherID'] == teacher_id) & (chemistry_unit1['schoolID'] == school_id)]
        if not teacher_data.empty:
            question_avg = teacher_data.iloc[:, 0:12].mean()
        else:
            st.warning('No data found for the given School ID and Teacher ID.')
    elif selection=='unit2':
        teacher_data = chemistry_unit2_og[(chemistry_unit2_og['teacherID'] == teacher_id) & (chemistry_unit2_og['schoolID'] == school_id)]
        if not teacher_data.empty:
            question_avg = teacher_data.iloc[:, 0:10].mean()
        else:
            st.warning('No data found for the given School ID and Teacher ID.')
    elif selection=='unit3':
        teacher_data = chemistry_unit3_og[(chemistry_unit3_og['teacherID'] == teacher_id) & (chemistry_unit3_og['schoolID'] == school_id)]
        if not teacher_data.empty:
            question_avg = teacher_data.iloc[:, 0:3].mean()
        else:
            st.warning('No data found for the given School ID and Teacher ID.')
        
    question_avg_sorted = question_avg.sort_values()

    # Create a Plotly bar plot
    fig = go.Figure(data=[go.Bar(
        x=question_avg_sorted.index,
        y=question_avg_sorted.values,
        marker_color='skyblue'  # Set color of bars
    )])

    fig.update_layout(
        #title=f'Average Scores for Each Question for {teacher_id} in {school_id}',
        xaxis=dict(title='Questions'),
        yaxis=dict(title='Average Score'),
        bargap=0.15,  # Gap between bars of adjacent location coordinates
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.write("Specific average scores allow you to assess the overall performance of your students compared to others in the same unit.")
    st.plotly_chart(fig)
    st.write("By analyzing how your students perform on average across various questions, you can gauge the effectiveness of your teaching methods and curriculum delivery.")
    
        
def color(x, student_id, temp):
    maximum = temp.Scores.max()
    minimum = temp.Scores.min()
    if x == maximum:
        return 'Max'
    elif x == minimum:
        return 'Min'
    else:
        return 'Moderate'
    
def highlight(s,temp):
    maximum = temp.Scores.max()
    minimum = temp.Scores.min()
    if s.Scores==maximum:
        return ['background-color: green'] * len(s)
    elif s.Scores==minimum:
        return ['background-color: red'] * len(s)
    else:
        return ['background-color: yellow'] * len(s)
        
def student_scores(school_id,teacher_id,student_id):
    temp = chemistry_unit1[(chemistry_unit1['teacherID'] == st.session_state['teacher_id']) & (chemistry_unit1['schoolID'] == st.session_state['school_id']) & (chemistry_unit1['stuID'] == student_id)]
    questions = [i for i in temp.columns if '_Q' in i]
    temp = temp[questions].T.reset_index()
    temp.columns=['Questions','Scores']
    temp = temp.sort_values(by='Scores',ascending=False)
    temp['Color']=temp.Scores.apply(color,args=[student_id, temp])
    color_mapping = {'Max': 'green', 'Moderate': '#ebde34', 'Min': 'red'}
    fig = px.bar(temp, x="Questions", y='Scores', color='Color', color_discrete_map=color_mapping)
    #st.plotly_chart(fig)
    temp = temp[['Questions','Scores']]
    df_colored = temp.set_index('Questions')
    df_colored = df_colored.style.apply(highlight,args=[temp], axis=1)
    #df_colored[['Scores']] = df_colored[['Scores']].style.apply(highlight,args=[temp], axis=1)
    st.dataframe(df_colored, width = 500)
    
def display_question_counts(school_id, teacher_id, unit):
    st.write("#### Question Counts for Selected Teacher and Unit")  
    
    teacher_data = chemistry_unit1[(chemistry_unit1['teacherID'] == teacher_id) & (chemistry_unit1['schoolID'] == school_id)]
    if not teacher_data.empty:
        # Calculate the average score for each question
        if unit=='unit1':
            data = teacher_data.iloc[:, 0:12]
        elif unit=='unit2':
            data = teacher_data.iloc[:, 0:10]
        elif unit=='unit3':
            data = teacher_data.iloc[:, 0:3]
    
    questions = [i for i in data.columns if '_Q' in i]
    temp = data[questions].T.reset_index()
    temp.columns=['Questions','Scores']
    
    # Calculate counts of students who got each question right
    question_counts = temp.apply(lambda x: x.value_counts().get(1, 0))  # Assuming 1 represents correct answer
    
    # Display counts in a table
    question_counts_df = pd.DataFrame({'Question': question_counts.index, 'Correct Count': question_counts.values})
    st.table(question_counts_df)

def plot_emotions(df):
    temp = df.T.reset_index()
    temp_names = ['Emotion']
    for i in range(len(temp.columns)-1):
        temp_names.append(f'Response{i+1}')
    temp.columns = temp_names
    others = temp[temp.Emotion.isin(['company','want_had','work_play','activity'])]
    others.columns = ['Details','Response']
    temp = temp[temp.Emotion.isin(vals_4)]
    
    if len(temp):
        # Create a horizontal layout for the table and the first bar chart
        col1, col2 = st.columns(2)
        
        # Display the DataFrame in the first column
        with col1:
            st.write("To provide deeper insights into student emotions, we've categorized their responses into several key areas. Below, you'll find a breakdown of these categories along with the corresponding responses from the students.")
            st.dataframe(others, width = 500)
            st.write("**company:** Who were you with?")
            st.write("**want_had:** Were you doing the main activity because you...")
            st.write("**work_play:** Was what you were doing...")
            st.write("**activity:** What were you doing when signaled?")
        
        # Display the first bar chart in the second column
        with col2:
            fig = px.bar(temp.iloc[:10,:], x="Emotion", y='Response1')
            fig.update_layout(
                yaxis=dict(
                    tickmode='array',
                    tickvals=[1, 2, 3, 4],
                    ticktext=['Not at all', 'Not much', 'Somewhat', 'Very much']
                )
            )
            st.plotly_chart(fig)
        
        # Create a horizontal layout for the remaining two bar charts
        col3, col4 = st.columns(2)
        
        # Display the second bar chart in the third column
        with col3:
            fig = px.bar(temp.iloc[10:20,:], x="Emotion", y='Response1')
            fig.update_layout(
                yaxis=dict(
                    tickmode='array',
                    tickvals=[1, 2, 3, 4],
                    ticktext=['Not at all', 'Not much', 'Somewhat', 'Very much']
                )
            )
            st.plotly_chart(fig)
        
        # Display the third bar chart in the fourth column
        with col4:
            fig = px.bar(temp.iloc[20:30,:], x="Emotion", y='Response1')
            fig.update_layout(
                yaxis=dict(
                    tickmode='array',
                    tickvals=[1, 2, 3, 4],
                    ticktext=['Not at all', 'Not much', 'Somewhat', 'Very much']
                )
            )
            st.plotly_chart(fig)
    else:
        st.write("No emotion data available.")


    
#school_id, teacher_id, login_button = login_page()

# Create a placeholder for the login form
#ogin_placeholder = st.empty()

if not st.session_state.get('logged_in', False):
    school_id, teacher_id, login_button = login_page()
    if login_button:
        st.session_state['logged_in'] = True
        st.session_state['school_id'] = school_id
        st.session_state['teacher_id'] = teacher_id
else:
    st.set_page_config(layout="wide")
    st.write("## Unit Selection")
    st.write("###### Choose the unit you would like to analyze from the dropdown menu below. You can select from Unit 1, Unit 2, or Unit 3 to view performance metrics and analyze student progress in each specific unit.")
    selection = st.selectbox('Select the unit',['unit1','unit2','unit3'])
    if selection == 'unit1':
        chemistry_unit1 = chemistry_unit1_og
    elif selection == 'unit2':
        chemistry_unit1 = chemistry_unit2_og
    elif selection == 'unit3':
        chemistry_unit1 = chemistry_unit3_og
        
    # Display charts after login
    
    overall, specific = st.columns(2)
    
    with overall:
        display_overall_avg_scores(selection)
    with specific:
        display_specific_avg_scores(st.session_state['school_id'], st.session_state['teacher_id'],selection)
    students = list(chemistry_unit1[(chemistry_unit1['teacherID'] == st.session_state['teacher_id']) & (chemistry_unit1['schoolID'] == st.session_state['school_id'])].stuID)
    st.write("## Check performance of a specific student")
    st.write("Use the dropdown menu below to select a student and view their individual performance scores. This section allows you to analyze the performance of individual students, view their scores across different questions, and identify areas for improvement or further support.")
    student_id = st.selectbox('Select a student to view more information',students,index=None)
    if student_id:
        student_scores(st.session_state['school_id'], st.session_state['teacher_id'], student_id)
        #display_question_counts(st.session_state['school_id'], st.session_state['teacher_id'], selection)
    
    st.markdown('# Student Emotions Explorer')
    st.write("Understanding students' emotional experiences in the learning environment is crucial for creating supportive and engaging educational experiences. This section provides insights into the emotions expressed by students over time, allowing you to gain a deeper understanding of students' well-being and engagement levels.")
   
    st.write("First step is to choose a specific teacher to analyze the emotional responses of their students and then select a particular student to explore their emotional journey.")
    st.write("Dive into emotions expressed by students over different time periods, such as days, months, or years, to identify trends and patterns.")
    left, right = st.columns(2)
    left2,mid2,right2,rightmost2 = st.columns(4)
    
    emotions_teachers = list(emotions.teacher.unique())
    
    teacher_id2 = left.selectbox('Select a teacher',emotions_teachers)
    df = emotions[emotions.teacher == teacher_id2]
    student_id2 = right.selectbox('Select a student',list(df.student.unique()))
    df = df[df.student==student_id2]
    
    respyear = left2.selectbox('Select response year', list(df.respyear.unique()))
    df = df[df.respyear==respyear]
    
    respmonth = mid2.selectbox('Select response month', list(df.respmonth.unique()))
    df = df[df.respmonth==respmonth]
    
    respday = right2.selectbox('Select response day', list(df.respday.unique()))
    df = df[df.respday==respday]
    
    resphour = rightmost2.selectbox('Select response hour',list(df.resphour.unique()))
    df = df[df.resphour==resphour]
    df.replace(vals_all_maps, inplace=True)
    
    plot_emotions(df)
    
    #############################################Email##########################################
    
    st.markdown("## Send a Message")
    
    PORT = 587  
    EMAIL_SERVER = "smtp-mail.outlook.com"

    from_mail = st.text_input('Please enter your email address')
    pwd = st.text_input('Please enter your password',type="password")


    sender_email = from_mail
    password_email = pwd

    to_email = st.text_input('Please enter the email of the receiver')
    sub = st.text_input('Please enter the subject')
    cont = st.text_area('Please enter the body of the email', height=200)



    def send_email(subject, receiver_email, content):
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = receiver_email

        msg.set_content(content)

        with smtplib.SMTP(EMAIL_SERVER, PORT) as server:
            server.starttls()
            server.login(sender_email, password_email)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            
    send = st.button('Send', type='primary')

    if from_mail and pwd and to_email and sub and cont:
        if send:
            print(cont)
            send_email(
                    subject=sub,
                    receiver_email=to_email,
                    content = cont
                )
    else:
        st.error('Please fill all fields!')
