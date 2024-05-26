import streamlit as st
import sqlite3

# Function to create a connection to SQLite database
def create_connection():
    conn = sqlite3.connect('todo.db')
    return conn

# Function to create the tasks table if it doesn't exist
def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            title TEXT
        )
    ''')
    conn.commit()

# Function to check if a task with the same title already exists
def task_exists(conn, title):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE title = ?', (title,))
    return cursor.fetchone() is not None

# Function to add a task to the database
def add_task(conn, title):
    if not task_exists(conn, title):
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tasks (title) VALUES (?)', (title,))
        conn.commit()
        return True
    else:
        return False

# Function to retrieve all tasks from the database
def get_tasks(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    return cursor.fetchall()

# Function to delete a task from the database
def delete_task(conn, id):
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (id,))
    conn.commit()

# Main function to run the Streamlit app
def main():
    # Create database connection and table
    conn = create_connection()
    create_table(conn)

    st.title('To Do App')

    # Add task input field
    new_task = st.text_input('Add new task:')
    add_task_button = st.button('Add Task')

    if add_task_button:
        if new_task.strip() != '':
            if add_task(conn, new_task):
                st.success('Task added successfully!')
                new_task = ''  # Clear the input field

    # Display tasks
    tasks = get_tasks(conn)
    if tasks:
        st.write('## Task List')
        for task in tasks:
            st.write(f'- {task[1]}')
            if st.button(f'Delete {task[1]}'):
                delete_task(conn, task[0])
                st.success(f'Task "{task[1]}" deleted successfully!')
                tasks = get_tasks(conn)

if __name__ == '__main__':
    main()
