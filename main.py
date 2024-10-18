"""
This module provides an enhanced to-do list application using Streamlit.
"""

import json
import streamlit as st


# Function to save tasks to a file
def save_tasks(task_list, task_priorities):
    """Save tasks and their priorities to a JSON file."""
    with open("tasks.json", "w", encoding='utf-8') as file:
        data = {
            "tasks": task_list,
            "priorities": task_priorities
        }
        json.dump(data, file)


# Function to load tasks from a file
def load_tasks():
    """Load tasks and their priorities from a JSON file."""
    try:
        with open("tasks.json", "r", encoding='utf-8') as file:
            data = json.load(file)
            return data.get("tasks", []), data.get("priorities", {})
    except FileNotFoundError:
        return [], {}


# Title of the app
st.title("Enhanced To-Do List")

# Initialize session state for task list and task priorities if not
# already created
if "task_list" not in st.session_state:
    task_list, task_priorities = load_tasks()
    st.session_state["task_list"] = task_list
    st.session_state["task_priorities"] = task_priorities

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

# Add task to the list with validation
if st.button("Add Task"):
    if not task:
        st.error("Task cannot be empty!")
    elif task in st.session_state["task_list"]:
        st.error("Task already exists!")
    else:
        st.session_state["task_list"].append(task)
        st.session_state["task_priorities"][task] = priority
        save_tasks(
            st.session_state["task_list"],
            st.session_state["task_priorities"]
        )
        st.session_state["task_input"] = ""
        st.success(f"Task '{task}' added successfully!")

# Update the session state to reflect the current input
st.session_state["task_input"] = task

# Edit or delete task
for i, t in enumerate(st.session_state["task_list"]):
    col1, col2, col3 = st.columns(3)

    task_priority = st.session_state["task_priorities"].get(t, "Low")

    with col1:
        st.write(f"{i + 1}. {t} - {task_priority} Priority")

    with col2:
        button_label = f"Edit {t}"
        button_key = f"edit_button_{i}"

        if st.button(button_label, key=button_key):

            if st.session_state["show_edit"].get(i, False):
                new_task = st.text_input(
                    f"Edit Task {t}", value=t, key=f"edit_task_{i}")
                new_priority = st.selectbox(
                    "Select new priority",
                    ["Low", "Medium", "High"],
                    index=["Low", "Medium", "High"].index(task_priority),
                    key=f"edit_priority_{i}"
                )

                if st.button(f"Update Task {i}", key=f"update_{i}"):
                    if not new_task:
                        st.error("Task cannot be empty!")
                elif (
                    new_task in st.session_state["task_list"]
                    and new_task != t
                ):
                    st.error("Task already exists!")
                else:
                    st.session_state["task_list"][i] = new_task
                    st.session_state["task_priorities"][
                        new_task
                    ] = new_priority
                    if new_task != t:

                        st.session_state["task_priorities"].pop(t, None)
                    save_tasks(
                        st.session_state["task_list"],
                        st.session_state["task_priorities"]
                    )
                    st.success(f"Task '{t}' updated successfully!")

    with col3:
        if st.button(f"Delete {t}", key=f"delete_{i}"):
            st.session_state["task_list"].pop(i)
            st.session_state["task_priorities"].pop(t, None)
            save_tasks(
                st.session_state["task_list"],
                st.session_state["task_priorities"]
            )
            st.success(f"Task '{t}' deleted successfully!")

# Show remaining tasks
if st.session_state["task_list"]:
    st.write("Remaining Tasks:")
    for task in st.session_state["task_list"]:
        task_priority = st.session_state["task_priorities"].get(task, "Low")
        st.write(f"- {task} ({task_priority} Priority)")
else:
    st.write("No remaining tasks.")

# Reset button to clear all tasks
if st.button("Reset App"):
    st.session_state['task_list'] = []
    st.session_state['task_priorities'] = {}
    st.session_state["task_input"] = ""
    save_tasks(
        st.session_state["task_list"],
        st.session_state["task_priorities"]
    )
    st.success("All tasks have been reset.")

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
        "Add", "Subtract", "Multiply", "Divide"
    ]
)

# Initialize CALCULATION_RESULT
calculation_result = None

# Perform the calculation based on the selected operation
if operation == "Add":
    calculation_result = num1 + num2
elif operation == "Subtract":
    calculation_result = num1 - num2
elif operation == "Multiply":
    calculation_result = num1 * num2
elif operation == "Divide":
    if num2 != 0:
        calculation_result = num1 / num2
    else:
        st.error("Cannot divide by zero!")

# Display results
if calculation_result is not None:
    st.write(f"Result: {calculation_result}")
