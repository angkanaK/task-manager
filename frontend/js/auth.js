async function login() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const errorMsg = document.getElementById("error-msg");
    const btn = document.getElementById("login-btn");

    btn.disabled = true;
    btn.innerHTML = '<span class="spinner"></span>กำลังเข้าสู่ระบบ...';
    errorMsg.textContent = "";

    try {
        const response = await fetch("http://127.0.0.1:8000/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (response.ok) {
            localStorage.setItem("access_token", data.access_token);
            localStorage.setItem("username", data.username);
            window.location.href = "dashboard.html";
        } else {
            errorMsg.textContent = data.detail;
            btn.disabled = false;
            btn.textContent = "เข้าสู่ระบบ";
        }
    } catch (error) {
        errorMsg.textContent = "เชื่อมต่อ Server ไม่ได้";
        btn.disabled = false;
        btn.textContent = "เข้าสู่ระบบ";
    }
}

async function register() {
    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const errorMsg = document.getElementById("error-msg");
    const successMsg = document.getElementById("success-msg");

    const response = await fetch("https://task-manager-api-odbq.onrender.com/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, email, password })
    });

    const data = await response.json();

    if (response.ok) {
        successMsg.textContent = "สมัครสมาชิกสำเร็จ! กำลังไปหน้า Login...";
        setTimeout(() => {
            window.location.href = "index.html";
        }, 2000);
    } else {
        errorMsg.textContent = data.detail;
    }
}