document.addEventListener("DOMContentLoaded", loadIssues);

function loadIssues() {
  fetch("http://127.0.0.1:8000/issues/")
    .then(response => response.json())
    .then(data => {
      const container = document.getElementById("storiesContainer");
      container.innerHTML = "";

      if (data.length === 0) {
        container.innerHTML = "<p>No issues reported yet.</p>";
        return;
      }

      data.forEach(issue => {
        const storyDiv = document.createElement("div");
        storyDiv.className = "story";

        storyDiv.innerHTML = `
        <div class="story-header">
            <span class="tag yellow">${issue.category_name}</span>
            <span class="tag light">🔥 Trending</span>
        </div>

        <h3>${issue.title}</h3>

        <p>${issue.description.substring(0, 2000)}...</p>

        <div class="tags">
            <span>#workplace</span>
            <span>#anonymous</span>
            <span>#support</span>
        </div>

        <div class="story-footer">
            <div class="actions">
            <span>👍 0</span>
            <span>💬 0</span>
            <span>🤝 Support</span>
            </div>
        </div>
        `;

        container.appendChild(storyDiv);
      });
    })
    .catch(error => {
      console.error("Error loading issues:", error);
    });
}

document.getElementById("loginBtn").addEventListener("click", () => {
    window.location.href = "../pages/login.html";
});

document.getElementById("postIssueBtn").addEventListener("click", () => {
    const userId = localStorage.getItem("user_id");

    if (!userId) {
        alert("Please login to post an issue.");
        window.location.href = "../pages/login.html";
    } else {
        window.location.href = "../pages/post_issue.html";
    }
});