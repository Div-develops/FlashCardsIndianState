import streamlit as st
import json
from random import randint

# Set page configuration
st.set_page_config(
    page_title="RKK",
    page_icon="icon.jpg",
    layout="centered",
    initial_sidebar_state="expanded",
)

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style',unsafe_allow_html=True)

st.header("राज्यों का खेल🦚")

# Load data from states.json
with open("states.json", "r") as f:
    data = json.load(f)

# Set up Streamlit session state
ss = st.session_state
if 'state_quiz' not in ss:
    ss['state_quiz'] = data[randint(0, len(data) - 1)]
    ss['user_answer'] = None
    ss['keep_play'] = True
    ss['submitted'] = False
    ss['key'] = 0
    ss['score'] = 0
    ss['questions_covered'] = set()

# Function to display state information
def display_state():
    state_info = ss['state_quiz']
    st.write(f"State: {state_info['state']}")
    st.write(f"Capital: {state_info['capital']}")
    st.write(f"Date of Formation: {state_info['date_of_formation']}")
    st.write(f"Official Language: {state_info['official_language']}")
    st.image(state_info['costume_img'], caption='Costume Image')

# Function to check user's answer
def check_answer():
    # Checks if the user has entered an empty string
    if not ss['user_answer']:
        st.warning("Please enter an answer before submitting.")
        return
    
    # Checks the user's answer against the correct capital for the current state.
    # Updates the session state with whether the answer was correct, increments the score if correct,
    # checks if all states have been covered, and displays the state information if the answer is correct.
    ss['submitted'] = True
    if ss['submitted']:
        if ss['user_answer'].lower() == ss['state_quiz']['capital'].lower():
            st.success("Correct!")
            if ss['state_quiz']['state'] not in ss['questions_covered']:
                ss['score'] += 1
            if len(data) == ss['score']:
                st.write("Congratulations! You have got all Indian state's capitals covered")
                quit_game()
            display_state()
        else:
            st.error("Incorrect!")
            st.image("incorrect.jpg")
            st.write(f"The correct answer is {ss['state_quiz']['capital']}")
            st.subheader(f"Trick to memorise:")
            st.write(ss['state_quiz']['cue'])
    ss['questions_covered'].add(ss['state_quiz']['state'])


# Function to generate a new question
def generate_new_question():
    ss['key'] += 1
    ss['state_quiz'] = data[randint(0, len(data) - 1)]
    ss['user_answer'] = None
    ss['submitted'] = False  # Reset form submitted state
    st.rerun()



# Function to quit the game
def quit_game():
    ss['keep_play'] = False
    st.rerun()

# Quit game
if not ss['keep_play']:
    st.subheader("Thanks for playing!")
    st.subheader(f"Your score was {ss['score']}/{len(ss['questions_covered'])}")
    st.image("bye.jpg")

# Main part of the app
if ss['keep_play']:
    # Displays the state quiz UI if "keep_play" is True.By clicking on quit "keep_play" will become false
    # Shows the question text, input for user's answer, and buttons to check answer,
    # get next question, and quit game. State is updated on button clicks.
    st.subheader(f"What is the capital of {ss['state_quiz']['state']}?")
    ss['user_answer'] = st.text_input("Enter your answer", key=f"input_{ss['key']}",placeholder="")  
    button_container = st.container()
    
    with button_container:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Check", key=f"check_button_{ss['key']}"):
                check_answer()

        with col2:
            if st.button("Next", key=f"next_button_{ss['key']}"):
                generate_new_question()

    if st.button("Quit", key=f"quit_button_{ss['key']}", type="primary"):
        quit_game()
