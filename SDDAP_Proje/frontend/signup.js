async function signup() {
  const username = document.getElementById("username").value.trim();
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value.trim();
  const messageEl = document.getElementById("message");

  if (!username || !email || !password) {
    messageEl.style.color = "red";
    messageEl.innerText = "❗ Lütfen tüm alanları doldurun.";
    return;
  }

  try {
    const response = await fetch("http://localhost:8000/auth/signup", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username,
        email,
        password,
        user_type: "user",
      }),
    });

    const data = await response.json();

    if (response.ok) {
  localStorage.setItem("verify_email", email);  // e-posta saklanır
  messageEl.style.color = "green";
  messageEl.innerText = "✅ Kod e-posta adresinize gönderildi.";
  setTimeout(() => {
    window.location.href = "verify.html";
  }, 1500);
}
else {
      messageEl.style.color = "red";
      messageEl.innerText = data.detail || "❌ Kayıt başarısız.";
    }
  } catch (error) {
    messageEl.style.color = "red";
    messageEl.innerText = "❌ Sunucuya ulaşılamadı.";
  }
}
