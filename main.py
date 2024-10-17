import streamlit as st
import json

# Function to save tasks to a file


def save_tasks(task_list, task_priorities):
    with open("tasks.json", "w") as file:
        data = {
            "tasks": task_list,
            "priorities": task_priorities
        }
        json.dump(data, file)

# Function to load tasks from a file


def load_tasks():
    try:
        with open("tasks.json", "r") as file:
            data = json.load(file)
            return data.get("tasks", []), data.get("priorities", {})
    except FileNotFoundError:
        return [], {}


# Title of the app
st.title("Enhanced To-Do List")

# Initialize session state for task list and task priorities if not
# already created
if "task_list" not in st.session_state:
    st.session_state["task_list"], st.session_state["task_priorities"] = load_tasks()

# Initialize session state for task input
if "task_input" not in st.session_state:
    st.session_state["task_input"] = ""

# Initialize a session state for showing edit input
if "show_edit" not in st.session_state:
    st.session_state["show_edit"] = {}

# Input box to enter a new task
task = st.text_input("Enter your task", value=st.session_state["task_input"])

# Priority input for tasks
priority = st.selectbox("Select priority", ["Low", "Medium", "High"])

# Add task to the list
if st.button("Add Task"):
    if task:
        st.session_state["task_list"].append(task)
        # Ensure every task has a priority
        st.session_state["task_priorities"][task] = priority
        save_tasks(
            st.session_state["task_list"],
            st.session_state["task_priorities"])  # Save tasks after adding

        # Clear task input after adding
        st.session_state["task_input"] = ""

# Update the session state to reflect the current input
st.session_state["task_input"] = task

# Edit or delete task
for i, t in enumerate(st.session_state["task_list"]):
    col1, col2, col3 = st.columns(3)

    # Ensure task has a priority before displaying
    task_priority = st.session_state["task_priorities"].get(
        t, "Low")  # Default to "Low" if priority is missing

    with col1:
        st.write(f"{i + 1}. {t} - {task_priority} Priority")

    with col2:
        # Toggle visibility for editing
        if st.button(f"Edit {t}", key=f"edit_button_{i}"):
            # Toggle edit visibility
            st.session_state["show_edit"][i] = not st.session_state["show_edit"].get(
                i, False)

        # Only show edit fields if the button was clicked
        if st.session_state["show_edit"].get(i, False):
            new_task = st.text_input(
                f"Edit Task {t}", value=t, key=f"edit_task_{i}")
            new_priority = st.selectbox(
                "Select new priority", [
                    "Low", "Medium", "High"], index=[
                    "Low", "Medium", "High"].index(task_priority), key=f"edit_priority_{i}")

            if st.button(f"Update Task {i}", key=f"update_{i}"):
                if new_task:  # Ensure the new task is not empty
                    # Update task list and priorities
                    st.session_state["task_list"][i] = new_task
                    # Update the priority for the new task name
                    st.session_state["task_priorities"][new_task] = new_priority
                    if new_task != t:  # If the task name has changed, remove the old name from priorities
                        st.session_state["task_priorities"].pop(t, None)

                    save_tasks(
                        st.session_state["task_list"],
                        st.session_state["task_priorities"])  # Save updated tasks

    with col3:
        if st.button(f"Delete {t}", key=f"delete_{i}"):
            st.session_state["task_list"].pop(i)
            st.session_state["task_priorities"].pop(
                t, None)  # Remove from priorities if exists
            save_tasks(
                st.session_state["task_list"],
                st.session_state["task_priorities"])  # Save after deletion

# Show remaining tasks
if st.session_state["task_list"]:
    st.write("Remaining Tasks:")
    for task in st.session_state["task_list"]:
        task_priority = st.session_state["task_priorities"].get(
            task, "Low")  # Default to "Low"
        st.write(f"- {task} ({task_priority} Priority)")
else:
    st.write("No remaining tasks.")

# Reset button to clear all tasks
if st.button("Reset App"):
    st.session_state['task_list'] = []  # Clear the task list
    st.session_state['task_priorities'] = {}  # Clear the task priorities
    st.session_state["task_input"] = ""  # Clear task input
    save_tasks(
        st.session_state["task_list"],
        st.session_state["task_priorities"])  # Save the cleared state

# Divider between the To-Do list and the Calculator
st.write("---")

# Title of the Calculator
st.title("Calculator")

# Input fields for calculator
num1 = st.number_input("Enter the first number", value=0.0, step=1.0)
num2 = st.number_input("Enter the second number", value=0.0, step=1.0)

# Select the operation
operation = st.selectbox(
    "Choose an operation", [
        "Add", "Subtract", "Multiply", "Divide"])

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
