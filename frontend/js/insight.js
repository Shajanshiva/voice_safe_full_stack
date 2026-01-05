document.addEventListener("DOMContentLoaded", loadCategoryPieChart);

async function loadCategoryPieChart() {
  try {
    const token = localStorage.getItem("access_token");

    if (!token) {
      console.error("No token found. Please login.");
      return;
    }

    const response = await fetch(
      "http://127.0.0.1:8000/issues/category-count",
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    if (!response.ok) {
      throw new Error("API error");
    }

    const data = await response.json();

    const labels = Object.keys(data);
    const values = Object.values(data);

    const ctx = document
      .getElementById("categoryPieChart")
      .getContext("2d");

    new Chart(ctx, {
      type: "pie",
      data: {
        labels: labels,
        datasets: [
          {
            data: values,
            backgroundColor: [
              "#ef4444",
              "#f59e0b",
              "#22c55e",
              "#14b8a6",
              "#a855f7",
            ],
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: "bottom",
          },
        },
      },
    });
  } catch (error) {
    console.error("Pie chart error:", error);
  }
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