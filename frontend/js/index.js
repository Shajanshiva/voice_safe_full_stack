document.getElementById("postStoryBtn").addEventListener("click", () => {
  window.location.href = "./pages/post_issue.html";
});

document.getElementById("readStoriesBtn").addEventListener("click", () => {
  window.location.href = "./pages/community.html";
});


document.getElementById("loginBtn").addEventListener("click", () => {
    window.location.href = "./pages/login.html";
});

document.getElementById("postIssueBtn").addEventListener("click", () => {
    const userId = localStorage.getItem("user_id");

    if (!userId) {
        alert("Please login to post an issue.");
        window.location.href = "./pages/login.html";
    } else {
        window.location.href = "./pages/post_issue.html";
    }
});
