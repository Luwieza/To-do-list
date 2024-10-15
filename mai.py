import streamlit as st
import json

# Function to save tasks to a file
def save_tasks(task_list):
    with open("tasks.json", "w") as file:
        json.dump(task_list, file)

# Function to load tasks from a file
def load_tasks():
    try:
        with open("tasks.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Title of the app
st.title("Enhanced To-Do List")

# Initialize session state for task list and task priorities if not already created
if "task_list" not in st.session_state:
    st.session_state["task_list"] = load_tasks()

if "task_priorities" not in st.session_state:
    st.session_state["task_priorities"] = {}

# Input box to enter a new task
task = st.text_input("Enter your task", "")

# Priority input for tasks
priority = st.selectbox("Select priority", ["Low", "Medium", "High"])

# Add task to the list
if st.button("Add Task"):
    if task:
        st.session_state["task_list"].append(task)
        # Ensure every task has a priority
        st.session_state["task_priorities"][task] = priority
        save_tasks(st.session_state["task_list"])  # Save tasks after adding
        st.experimental_rerun()  # Refresh to reflect the added task

# Update Task Logic
for i, t in enumerate(st.session_state["task_list"]):
    col1, col2, col3 = st.columns(3)

    # Display the task and its priority
    with col1:
        task_priority = st.session_state["task_priorities"].get(t, "Low")
        st.write(f"{i + 1}. {t} - {task_priority} Priority")

    # Edit Task Button
    with col2:
        if st.button(f"Edit {t}", key=f"edit_{i}"):
            new_task = st.text_input(f"Edit Task {i}", value=t)  # Text input for editing
            new_priority = st.selectbox(f"Edit Priority {i}", ["Low", "Medium", "High"], index=["Low", "Medium", "High"].index(task_priority))  # Priority input
            if st.button(f"Update Task {i}", key=f"update_{i}"):  # Update button
                st.session_state["task_list"][i] = new_task  # Update the task name
                st.session_state["task_priorities"][new_task] = new_priority  # Update priority
                save_tasks(st.session_state["task_list"])  # Save changes
                st.experimental_rerun()  # Refresh to show updates

    # Delete Task Button
    with col3:
        if st.button(f"Delete {t}", key=f"delete_{i}"):
            st.session_state["task_list"].pop(i)  # Remove task
            st.session_state["task_priorities"].pop(t, None)  # Remove priority
            save_tasks(st.session_state["task_list"])  # Save changes
            st.experimental_rerun()  # Refresh to show updates

# Show remaining tasks
if st.session_state["task_list"]:
    st.write("Remaining Tasks:")
    for task in st.session_state["task_list"]:
        task_priority = st.session_state["task_priorities"].get(task, "Low")  # Default to "Low"
        st.write(f"- {task} ({task_priority} Priority)")
else:
    st.write("No remaining tasks.")

# Reset button to clear all tasks
if st.button("Reset"):
    st.session_state['task_list'] = []  # Clear the task list
    st.session_state['task_priorities'] = {}  # Clear the task priorities
    save_tasks(st.session_state["task_list"])  # Save the empty state to the file
    st.experimental_rerun()  # Refresh the app to reflect changes

# Divider between the To-Do list and the Calculator
st.write("---")

# Title of the Calculator
st.title("Calculator")

# Input fields for calculator
num1 = st.number_input("Enter the first number", value=0.0, step=1.0)
num2 = st.number_input("Enter the second number", value=0.0, step=1.0)

# Select the operation
operation = st.selectbox("Choose an operation", ["Add", "Subtract", "Multiply", "Divide"])

# Perform the calculation based on the selected operation
result = None
if operation == "Add":
    result = num1 + num2
elif operation == "Subtract":
    result = num1 - num2
elif operation == "Multiply":
    result = num1 * num2
elif operation == "Divide":
    if num2 != 0:
        result = num1 / num2
    else:
        st.error("Cannot divide by zero!")

# Display the result
if result is not None:
    st.write(f"Result: {result}")

