const params = new URLSearchParams(window.location.search);
const filmId = params.get("id");
const token = localStorage.getItem("token");
const API_BASE = "http://127.0.0.1:8000";

if (!token) {
  alert("Giriş yapmalısınız.");
  window.location.href = "index.html";
  throw new Error("Token bulunamadı");
}

if (!filmId) {
  alert("Film ID bulunamadı.");
  window.location.href = "homepage.html";
  throw new Error("Film ID eksik");
}

let liked = false;
let userScore = null;

async function getUserStatus() {
  const res = await fetch(`${API_BASE}/films/${filmId}/user_status`, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  });
  const data = await res.json();
  liked = data.liked;
  userScore = data.user_score;

  updateLikeButton();
  updateScoreInput();
}

function updateLikeButton() {
  const likeBtn = document.getElementById("like-btn");
  if (liked) {
    likeBtn.textContent = "💔 Beğenmekten Vazgeç";
    likeBtn.style.backgroundColor = "#b91c1c"; // kırmızımsı
  } else {
    likeBtn.textContent = "❤️ Beğen";
    likeBtn.style.backgroundColor = "#1c64b9"; // mavimsi
  }
}

function updateScoreInput() {
  const input = document.getElementById("rating");
  if (userScore !== null) {
    input.value = userScore;
  }
}

async function loadFilm() {
  const res = await fetch(`${API_BASE}/films/${filmId}`);
  const film = await res.json();

  document.getElementById("film-poster").src = film.poster_url || "placeholder.jpg";
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

// Beğeni gönder / kaldır
const likeBtn = document.getElementById("like-btn");
if (likeBtn) {
  likeBtn.addEventListener("click", async () => {
    const endpoint = liked ? "unlike" : "like";
    const res = await fetch(`${API_BASE}/films/${filmId}/${endpoint}`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    const data = await res.json();
    alert(data.message);
    liked = !liked;
    updateLikeButton();
    loadLikeCount();
  });
}

// Puan gönder
const ratingForm = document.getElementById("rating-form");
if (ratingForm) {
  ratingForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const score = parseInt(document.getElementById("rating").value);
    if (score < 1 || score > 10) {
      alert("Puan 1 ile 10 arasında olmalı.");
      return;
    }

    fetch(`${API_BASE}/films/${filmId}/rate`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({ score })
    })
      .then(res => res.json())
      .then(data => {
        alert(data.message);
        loadAverageRating();
      })
      .catch(err => console.error("Puan hatası:", err));
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

// Başlangıçta her şeyi yükle
loadFilm();
loadComments();
loadLikeCount();
loadAverageRating();
getUserStatus();
