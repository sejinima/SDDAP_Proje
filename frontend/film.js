document.addEventListener("DOMContentLoaded", () => {
  const params = new URLSearchParams(window.location.search);
  const filmId = params.get("id");

  if (!filmId) {
    document.getElementById("film-title").innerText = "Film ID bulunamadı.";
    return;
  }

  fetch(`http://localhost:8000/film/${filmId}`)
    .then((res) => {
      if (!res.ok) throw new Error("Film bulunamadı");
      return res.json();
    })
    .then((film) => {
      document.getElementById("film-title").innerText = film.title;
      document.getElementById("film-year").innerText = film.year;
      document.getElementById("film-rating").innerText = film.rating;
      document.getElementById("film-poster").src = film.poster_url;
    })
    .catch((err) => {
      document.getElementById("film-title").innerText = "Hata: " + err.message;
    });
});
