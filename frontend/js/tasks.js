const API_URL = "https://task-manager-api-odbq.onrender.com";
const token = localStorage.getItem("access_token");
const username = localStorage.getItem("username");

if (!token) {
    window.location.href = "index.html";
}

document.getElementById("welcome-msg").textContent = "สวัสดี " + username + "!";

async function getTasks() {
    const response = await fetch(`${API_URL}/tasks/`, {
        headers: { "Authorization": "Bearer " + token }
    });
    
    if (response.status === 401) {
        logout();
        return;
    }

    const tasks = await response.json();
    
    const taskList = document.getElementById("task-list");
    taskList.innerHTML = "";

    tasks.forEach(task => {
        taskList.innerHTML += `
            <div class="task-item">
                <span>${task.title}</span>
                <div>
                    <select onchange="updateTask(${task.id}, this.value)">
                        <option ${task.status === "todo" ? "selected" : ""}>todo</option>
                        <option ${task.status === "in_progress" ? "selected" : ""}>in_progress</option>
                        <option ${task.status === "done" ? "selected" : ""}>done</option>
                    </select>
                    <button onclick="openEdit(${task.id}, '${task.title}')">แก้ไข</button>
                    <button onclick="deleteTask(${task.id})">ลบ</button>
                </div>
            </div>
        `;
    });
}

async function createTask() {
    const title = document.getElementById("task-title").value;
    if (!title) return;

    await fetch(`${API_URL}/tasks/`, {
        method: "POST",
        headers: { 
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        },
        body: JSON.stringify({ title })
    });

    document.getElementById("task-title").value = "";
    getTasks();
}

async function updateTask(task_id, status) {
    await fetch(`${API_URL}/tasks/${task_id}`, {
        method: "PUT",
        headers: { 
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        },
        body: JSON.stringify({ status })
    });
    getTasks();
}

async function deleteTask(task_id) {
    await fetch(`${API_URL}/tasks/${task_id}`, {
        method: "DELETE",
        headers: { "Authorization": "Bearer " + token }
    });
    getTasks();
}

function logout() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("username");
    window.location.href = "index.html";
}

let editingTaskId = null;

function openEdit(task_id, title) {
    editingTaskId = task_id;
    document.getElementById("edit-title").value = title;
    document.getElementById("edit-modal").style.display = "flex";
}

function closeEdit() {
    document.getElementById("edit-modal").style.display = "none";
    editingTaskId = null;
}

async function saveEdit() {
    const title = document.getElementById("edit-title").value;
    if (!title) return;

    await fetch(`${API_URL}/tasks/${editingTaskId}`, {
        method: "PUT",
        headers: { 
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        },
        body: JSON.stringify({ title })
    });

    closeEdit();
    getTasks();
}

getTasks();