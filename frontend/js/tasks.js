const user_id = localStorage.getItem("user_id");
const username = localStorage.getItem("username");

if (!user_id) {
    window.location.href = "index.html";
}

document.getElementById("welcome-msg").textContent = "สวัสดี " + username + "!";

// ดึง Tasks ทั้งหมด
async function getTasks() {
    const response = await fetch(`http://127.0.0.1:8000/tasks/?user_id=${user_id}`);
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
                    <button onclick="deleteTask(${task.id})">ลบ</button>
                </div>
            </div>
        `;
    });
}

// สร้าง Task ใหม่
async function createTask() {
    const title = document.getElementById("task-title").value;
    if (!title) return;

    await fetch(`http://127.0.0.1:8000/tasks/?user_id=${user_id}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title })
    });

    document.getElementById("task-title").value = "";
    getTasks();
}

// อัปเดต Status
async function updateTask(task_id, status) {
    await fetch(`http://127.0.0.1:8000/tasks/${task_id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status })
    });
    getTasks();
}

// ลบ Task
async function deleteTask(task_id) {
    await fetch(`http://127.0.0.1:8000/tasks/${task_id}`, {
        method: "DELETE"
    });
    getTasks();
}

function logout() {
    localStorage.removeItem("user_id");
    localStorage.removeItem("username");
    window.location.href = "index.html";
}

getTasks();
