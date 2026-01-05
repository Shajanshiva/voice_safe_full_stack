document.querySelector(".report-form").addEventListener("submit", submitIssue);

function submitIssue(event) {
    event.preventDefault();


    const token = localStorage.getItem("access_token");

    if (!token) {
        alert("Please log in to submit an issue.");
        window.location.href = "./login.html";
        return;
    }

    const title = document.getElementById("title").value.trim();
    const category = document.getElementById("category").value;
    const description = document.getElementById("description").value.trim();

    if (!title || !category || !description) {
        alert("Please fill all required fields");
        return;
    }

  
    const issue_data = {
        title: title,
        category_name: category,
        description: description
    };

    fetch("http://127.0.0.1:8000/issues/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        },
        body: JSON.stringify(issue_data)
    })
    .then(async (response) => {
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Failed to submit issue");
        }

        return data;
    })
    .then((data) => {
        alert(data.message);
        document.querySelector(".report-form").reset();
    })
    .catch((error) => {
        alert(error.message);
    });
}


document.querySelector(".cancel-btn").addEventListener("click", () => {
    const confirmCancel = confirm("Are you sure you want to cancel?");
    if (confirmCancel) {
        window.location.href = "../pages/community.html";
    }
});


document.getElementById("loginBtn").addEventListener("click", () => {
    window.location.href = "../pages/login.html";
});
