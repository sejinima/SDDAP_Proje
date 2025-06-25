async function verify() {
  const code = document.getElementById("code").value.trim();
  const email = localStorage.getItem("verify_email");
  const resultEl = document.getElementById("result");

  if (!email) {
    resultEl.style.color = "red";
    resultEl.innerText = "❌ E-posta bulunamadı. Lütfen önce kayıt olun.";
    return;
  }

  if (!code) {
    resultEl.style.color = "red";
    resultEl.innerText = "❗ Doğrulama kodunu girin.";
    return;
  }

  try {
    const response = await fetch("http://localhost:8000/auth/verify", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, code })
    });

    const data = await response.json();

    if (response.ok) {
      resultEl.style.color = "green";
      resultEl.innerText = "✅ Hesap doğrulandı. Giriş yapabilirsiniz.";
      localStorage.removeItem("verify_email");
      setTimeout(() => {
        window.location.href = "index.html";
      }, 2000);
    } else {
      resultEl.style.color = "red";
      resultEl.innerText = Array.isArray(data.detail)
        ? data.detail.map(err => err.msg).join(" | ")
        : data.detail || data.message || "❌ Kod yanlış veya süresi dolmuş.";
    }
  } catch (error) {
    resultEl.style.color = "red";
    resultEl.innerText = "❌ Sunucuya ulaşılamadı.";
  }
}
