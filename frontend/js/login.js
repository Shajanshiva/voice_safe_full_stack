document.querySelector(".login-btn").addEventListener("click", verify_user);

function verify_user(event) {
    event.preventDefault();

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();

    if (!email || !password) {
        alert("Please fill all required fields");
        return;
    }

 
    const formData = new URLSearchParams();
    formData.append("username", email); 
    formData.append("password", password);

    fetch("http://127.0.0.1:8000/users/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: formData.toString()
    })
    .then(async response => {
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Invalid email or password");
        }

        return data;
    })
    .then(data => {
        alert("Login successful!");

        localStorage.setItem("access_token", data.access_token);

        window.location.href = "../index.html";
    })
    .catch(error => {
        alert(error.message);
    });
}
