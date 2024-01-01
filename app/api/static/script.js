document.addEventListener('DOMContentLoaded', () => {
    const taskForm = document.getElementById('taskForm');
    const taskTitle = document.getElementById('taskTitle');
    const taskList = document.getElementById('taskList');

    taskForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        await addTask(taskTitle.value);
        taskTitle.value = '';
    });

    async function addTask(title) {
        try {
            const response = await fetch('http://127.0.0.1:8000/todo/todos/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ title }),
            });
            const task = await response.json();

            if (!task) {
                throw new Error('Failed to add task');
            }

            loadTasks();
        } catch (error) {
            console.error('Error adding task:', error);
        }
    }

    async function loadTasks() {
        try {
            const response = await fetch('http://127.0.0.1:8000/todo/todos/');
            const tasks = await response.json();
            renderTasks(tasks);
        } catch (error) {
            console.error('Error loading tasks:', error);
        }
    }

    async function deleteTask(id) {
        try {
            const response = await fetch(`http://127.0.0.1:8000/todo/todos/${id}`,
            {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ id }),
            });

            const task = await response.json();

            if (!task) {
                throw new Error('Failed to delete task');
            }

            loadTasks();
        } catch (error) {
            console.error('Error deleting task:', error);
        }
    }

    function renderTasks(tasks) {
        taskList.innerHTML = '';
        tasks.forEach(task => {
            const li = document.createElement('li');
            li.innerHTML = `
                ${task.title}
                <button class="delete-button"
                data-task-id="${task.id}">Delete</button>
            `;
            taskList.appendChild(li);
        });

        const deleteButtons = document.querySelectorAll('.delete-button');
        deleteButtons.forEach((button) => {
            button.addEventListener('click', () => {
                const taskId = button.getAttribute('data-task-id');
                deleteTask(taskId);
            });
        });
    }

    loadTasks();
});