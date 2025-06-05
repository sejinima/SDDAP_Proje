      async function login() {
        
      const username = document.getElementById("username").value;
      const password = document.getElementById("password").value;
      const messageEl = document.getElementById("message");

      try {
        const response = await fetch("http://localhost:8000/auth/login", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ username, password }),
        });

        const data = await response.json();

        if (response.ok) {
          localStorage.setItem("username", username);
          localStorage.setItem("token", data.access_token);
          messageEl.style.color = "lightgreen";
          messageEl.innerText = "✅ Giriş başarılı. Yönlendiriliyorsunuz...";
          setTimeout(() => {
            window.location.href = "homepage.html";
          }, 1000);
        } else {
          messageEl.style.color = "tomato";
          messageEl.innerText = data.detail || "❌ Giriş başarısız.";
        }
      } catch (error) {
        messageEl.style.color = "tomato";
        messageEl.innerText = "❌ Sunucuya bağlanılamadı.";
      }
    }