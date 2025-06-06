async function signup() {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;
  const messageEl = document.getElementById("message");

  try {
    const response = await fetch("http://localhost:8000/auth/signup", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username,
        password,
        user_type: "user" 
      }),
    });

    const data = await response.json();

    if (response.ok) {
      messageEl.style.color = "lightgreen";
      messageEl.innerText = "✅ Kayıt başarılı. Giriş sayfasına yönlendiriliyorsunuz...";
      setTimeout(() => {
        window.location.href = "index.html";
      }, 1500);
    } else {
      messageEl.style.color = "tomato";
      messageEl.innerText = data.detail || "❌ Kayıt başarısız.";
    }
  } catch (error) {
    messageEl.style.color = "tomato";
    messageEl.innerText = "❌ Sunucuya bağlanılamadı.";
  }
}
