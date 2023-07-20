import csv
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import os
import seaborn as sns

def load_quiz_data(file_path):
    quiz_data = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            quiz_data.append(row)
    return quiz_data

def quiz_game(quiz_data, file_path2):
    session_state = st.session_state
    name = st.text_input("Enter your Name")
    if 'score' not in session_state:
        session_state.score = 0

    total_questions = len(quiz_data)

    for i, question in enumerate(quiz_data):
        st.write(f"Question {i+1}/{total_questions}: {question['Question']}")
        options = ['1', '2', '3', '4']
        for option in options:
            st.write(f"{option}. {question[option]}")

        user_choice_key = f"answer_{i}"
        user_choice = st.text_input(f"Enter the Answer for Question {i+1}: ", key=user_choice_key)

        correct_answer = question['Answer']
        correct_answer_normalized = correct_answer.strip().upper()

        enter_button_key = f"enter_{i}"
        if st.button(f"Enter", key=enter_button_key):
            if user_choice.strip().upper() == correct_answer_normalized:
                st.success("Correct!")
                session_state.score += 1
            else:
                st.warning("Incorrect!")
                st.write(f"The correct answer is: {correct_answer}")

    if st.button(f"Show Results", key="results"):
        st.write("Final Score: {}/{}".format(session_state.score, total_questions))
        display_results(session_state.score, total_questions)
        data = [name, session_state.score]
        add_performances(file_path2, data)
    if st.button("Leaderboard", key="othersperformance"):
        other_perfo(session_state.score, name)

def display_results(score, total_questions):
    labels = ['Correct Answers', 'Incorrect Answers']
    sizes = [score, total_questions - score]
    colors = ['lightgreen', 'lightcoral']
    explode = (0.1, 0)  # Explode the "Correct Answers" slice

    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle

    ax.set_title('Quiz Results')

    st.pyplot(fig)

def add_performances(file_path2, data):
    header = ['Name', 'Score']
    file_exists = os.path.isfile(file_path2)
    with open(file_path2, 'a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists or os.stat(file_path2).st_size == 0:
            writer.writerow(header)
        writer.writerow(data)

def other_perfo(score, name):
    df = pd.read_csv('performance.csv')
    df.sort_values('Score',ascending=False,inplace=True)
    fig,ax=plt.subplots()
    sns.barplot(x='Score',y='Name',data=df,palette="Blues_r",ax=ax)
    ax.set_title('Leaderboard',weight='bold',fontsize=20)
    ax.set_xlabel('Score',weight='bold',fontsize=15)
    ax.set_ylabel('Name',weight='bold',fontsize=15)
    ax.set_xticks([])

    for i,score in enumerate(df['Score']):
        ax.text(score,i,str(score),ha='left',va='center')
    plt.tight_layout()
    st.pyplot(fig)


file_path2 = 'performance.csv'

file_path = 'questions.csv'
quiz_data = load_quiz_data(file_path)
quiz_game(quiz_data, file_path2)
