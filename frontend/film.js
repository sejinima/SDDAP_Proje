const params = new URLSearchParams(window.location.search);
const filmId = params.get("id");
const token = localStorage.getItem("token");
const API_BASE = "http://127.0.0.1:8000";

const username = JSON.parse(atob(token.split(".")[1])).sub;

async function loadFilm() {
  const res = await fetch(`${API_BASE}/films/${filmId}`);
  const film = await res.json();

  document.getElementById("film-poster").src = film.poster_url;
  document.getElementById("film-title").textContent = `${film.title} (${film.year})`;
  document.getElementById("film-year").textContent = film.year;
  document.getElementById("film-rating").textContent = film.rating;
}

async function loadComments() {
  const res = await fetch(`${API_BASE}/films/${filmId}/comments`);
  const comments = await res.json();
  const container = document.getElementById("comments");
  container.innerHTML = "";
  comments.forEach(c => {
    const div = document.createElement("div");
    div.className = "comment-box";
    div.innerHTML = `<strong>${c.username}</strong> <small>${c.timestamp}</small><br>${c.text}`;
    container.appendChild(div);
  });
}

async function submitComment() {
  const text = document.getElementById("comment-text").value;
  if (!text.trim()) return;

  await fetch(`${API_BASE}/films/${filmId}/comment`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({ text })
  });

  document.getElementById("comment-text").value = "";
  loadComments();
}

// Beğeni gönder

const likeBtn = document.getElementById("like-btn");
if (likeBtn) {
  likeBtn.addEventListener("click", () => {
    fetch(`${API_BASE}/films/${filmId}/like`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    .then(res => res.json())
    .then(data => {
      alert(data.message);
      loadLikeCount();
    })
    .catch(err => console.error("Beğeni hatası:", err));
  });
}

// Puan gönder
const ratingForm = document.getElementById("rating-form");
if (ratingForm) {
  ratingForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const score = parseInt(document.getElementById("rating").value);
    fetch(`${API_BASE}/films/${filmId}/rate`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({ score: score })
    })
    .then(res => res.json())
    .then(data => {
      alert(data.message);
      loadAverageRating();
    })
    .catch(err => console.error("Rating hatası:", err));
  });
}

// Beğeni sayısını getir
function loadLikeCount() {
  fetch(`${API_BASE}/films/${filmId}/likes`)
    .then(res => res.json())
    .then(data => {
      document.getElementById("like-count").textContent = `Beğeni: ${data.count}`;
    });
}

// Ortalama puanı getir
function loadAverageRating() {
  fetch(`${API_BASE}/films/${filmId}/average_rating`)
    .then(res => res.json())
    .then(data => {
      document.getElementById("average-rating").textContent = `Ortalama Puan: ${data.average.toFixed(1)}`;
    });
}

// Sayfa yüklendiğinde çağır
loadFilm();
loadComments();
loadLikeCount();
loadAverageRating();
