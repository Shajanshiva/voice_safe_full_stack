document.querySelector(".login-btn").addEventListener("click", createUser);
 
function createUser() {
        const username = document.getElementById("username").value;
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        if (!username || !email || !password) {
          alert("Please fill all required fields");
          return;
        }

        const user_data = {
          full_name: username,
          email: email,
          password: password,
        };

        fetch("http://127.0.0.1:8000/users/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(user_data),
        })
          .then((response) => response.json())
          .then((data) => {
            console.log("Success:", data);
            alert("User " + username + " created successfully!");
            window.location.href = "./login.html";
          })

          .catch((error) => {
            console.error("Error:", error);
            alert("Error creating user.");
          });
      }