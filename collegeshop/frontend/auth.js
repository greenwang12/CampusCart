const API = "http://127.0.0.1:8000/api/";

// LOGIN
const loginForm = document.getElementById("login-form");
if (loginForm) {
  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const username = document.getElementById("login-username").value;
    const password = document.getElementById("login-password").value;
    const messageEl = document.getElementById("auth-message");
    if (!username || !password) {
      messageEl.innerText = "Please fill in both username and password";
      return;
    }
    messageEl.innerText = "Logging in...";
    try {
      const response = await fetch(API + "token/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });
      const data = await response.json();
      if (response.ok && data.access && data.refresh) {
        localStorage.setItem("access", data.access);
        localStorage.setItem("refresh", data.refresh);
        localStorage.setItem("username", username);
        messageEl.style.color = "green";
        messageEl.innerText = "Login successful! Redirecting...";
        setTimeout(() => {
          window.location.href = "index.html";
        }, 900);
      } else {
        messageEl.style.color = "red";
        messageEl.innerText = data.detail || "Login failed";
      }
    } catch (error) {
      messageEl.style.color = "red";
      messageEl.innerText = "Network error: " + error.message;
    }
  });
}

// REGISTER
const registerForm = document.getElementById("register-form");
if (registerForm) {
  registerForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const username = document.getElementById("register-username").value;
    const email = document.getElementById("register-email").value;
    const password = document.getElementById("register-password").value;
    const messageEl = document.getElementById("auth-message");
    messageEl.innerText = "Registering...";
    try {
      const response = await fetch(API + "register/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, email, password }),
      });
      const data = await response.json();
      if (response.ok) {
        messageEl.style.color = "green";
        messageEl.innerText = "Registration successful! Please login.";
        setTimeout(() => {
          document.getElementById("show-login").click();
        }, 1500);
      } else {
        messageEl.style.color = "red";
        if (data.username) messageEl.innerText = data.username[0];
        else if (data.email) messageEl.innerText = data.email[0];
        else if (data.password) messageEl.innerText = data.password[0];
        else messageEl.innerText = "Registration failed. Check your input.";
      }
    } catch (error) {
      messageEl.style.color = "red";
      messageEl.innerText = "Network error: " + error.message;
    }
  });
}
