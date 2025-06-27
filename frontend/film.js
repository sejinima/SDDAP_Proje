console.log("film.js gerçekten yüklendi!");

window.addEventListener("DOMContentLoaded", () => {
  const filmId = new URLSearchParams(window.location.search).get("id");
  const token = localStorage.getItem("token");
  const API_BASE = "http://127.0.0.1:8000";

  if (!filmId || !token) {
    alert("Giriş yapmalısınız.");
    window.location.href = "index.html";
    return;
  }

  let liked = false;
  let userScore = null;

  // === Yorum Gönderme ===
  document.getElementById("comment-submit").addEventListener("click", submitComment);

  async function submitComment() {
    const text = document.getElementById("comment-text").value;
    if (!text.trim()) {
      alert("Yorum boş olamaz!");
      return;
    }
    try {
      const response = await fetch(`${API_BASE}/films/${filmId}/comment`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({ text })
      });
      if (!response.ok) {
        const err = await response.json();
        alert("Yorum eklenemedi: " + (err.detail || response.status));
        return;
      }
      document.getElementById("comment-text").value = "";
      await loadComments();
    } catch (err) {
      alert("Bir hata oluştu: " + err);
    }
  }

  // === Yorumları Getir ===
  async function loadComments() {
    try {
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
    } catch (err) {
      document.getElementById("comments").innerHTML = "<i>Yorumlar yüklenemedi.</i>";
    }
  }

  // === Beğeni Butonu ===
  document.getElementById("like-btn").addEventListener("click", toggleLike);

  async function toggleLike() {
    const endpoint = liked ? "unlike" : "like";
    const res = await fetch(`${API_BASE}/films/${filmId}/${endpoint}`, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` }
    });
    const data = await res.json();
    alert(data.message);
    liked = !liked;
    updateLikeButton();
    loadLikeCount();
  }

  function updateLikeButton() {
    const likeBtn = document.getElementById("like-btn");
    if (likeBtn) {
      likeBtn.textContent = liked ? "💔 Beğenmekten Vazgeç" : "❤️ Beğen";
      likeBtn.style.backgroundColor = liked ? "#b91c1c" : "#1c64b9";
    }
  }

  // === Kullanıcı Like/Puan Bilgisi ===
  async function getUserStatus() {
    const res = await fetch(`${API_BASE}/films/${filmId}/user_status`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    const data = await res.json();
    liked = data.liked;
    userScore = data.user_score;
    updateLikeButton();
    updateScoreInput();
  }

  // === Puanlama ===
  document.getElementById("rating-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const score = parseInt(document.getElementById("rating").value);
    if (score < 1 || score > 10) {
      alert("Puan 1 ile 10 arasında olmalı.");
      return;
    }
    const response = await fetch(`${API_BASE}/films/${filmId}/rate`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({ score })
    });
    const data = await response.json();
    alert(data.message);
    loadAverageRating();
  });

  function updateScoreInput() {
    const input = document.getElementById("rating");
    if (input && userScore !== null) input.value = userScore;
  }

  // === Film Detaylarını Getir ===
  async function loadFilm() {
    const res = await fetch(`${API_BASE}/films/${filmId}`);
    const film = await res.json();
    document.getElementById("film-poster").src = film.poster_url || "placeholder.jpg";
    document.getElementById("film-title").textContent = `${film.title} (${film.year})`;
    document.getElementById("film-year").textContent = film.year;
    document.getElementById("film-rating").textContent = film.rating;
  }

  // === Beğeni ve Ortalama Puan ===
  function loadLikeCount() {
    fetch(`${API_BASE}/films/${filmId}/likes`)
      .then(res => res.json())
      .then(data => {
        document.getElementById("like-count").textContent = `Beğeni: ${data.count}`;
      });
  }

  function loadAverageRating() {
    fetch(`${API_BASE}/films/${filmId}/average_rating`)
      .then(res => res.json())
      .then(data => {
        document.getElementById("average-rating").textContent = `Ortalama Puan: ${data.average.toFixed(1)}`;
      });
  }

  // === Başlangıçta Her Şeyi Yükle ===
  loadFilm();
  loadComments();
  loadLikeCount();
  loadAverageRating();
  getUserStatus();
});
