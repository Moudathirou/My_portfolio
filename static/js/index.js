// Animations GSAP
gsap.registerPlugin(ScrollTrigger);

// Animation du header
gsap.from("header", {
  y: "-100%",
  opacity: 0,
  duration: 1,
  ease: "power3.out"
});

// Animation de la section hero
gsap.from(".hero-content", {
  y: 50,
  opacity: 0,
  duration: 1,
  delay: 0.5,
  ease: "power3.out"
});

// Animation des cartes de projet
gsap.from(".project-card", {
  scrollTrigger: {
    trigger: "#projets",
    start: "top center"
  },
  y: 50,
  opacity: 0,
  duration: 0.8,
  stagger: 0.2,
  ease: "power3.out"
});

// Animation des compétences
gsap.from(".skill-item", {
  scrollTrigger: {
    trigger: "#competences",
    start: "top center"
  },
  scale: 0,
  opacity: 0,
  duration: 0.5,
  stagger: 0.1,
  ease: "back.out(1.7)"
});

// Animation de la timeline
gsap.from(".timeline-item", {
  scrollTrigger: {
    trigger: "#experiences",
    start: "top center"
  },
  x: (index) => index % 2 === 0 ? -50 : 50,
  opacity: 0,
  duration: 0.8,
  stagger: 0.2,
  ease: "power3.out"
});


// Fonction pour obtenir le jeton CSRF
async function getCsrfToken() {
  try {
    const response = await fetch('/get-csrf-token');
    const data = await response.json();
    return data.csrf_token;
  } catch (error) {
    console.error('Erreur lors de la récupération du jeton CSRF:', error);
    return null;
  }
}

// Mise à jour du gestionnaire de formulaire de contact
document.getElementById("contact-form").addEventListener("submit", async function(e) {
  e.preventDefault();
  const name = this.name.value;
  const email = this.email.value;
  const message = this.message.value;

  try {
    // Obtenir le jeton CSRF
    const csrfToken = await getCsrfToken();
    
    const response = await fetch('/contact', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      },
      body: JSON.stringify({ name, email, message })
    });

    const result = await response.json();
    
    if (result.success) {
      alert("Merci pour votre message ! Je vous répondrai dans les plus brefs délais.");
      this.reset();
    } else {
      alert("Erreur : " + (result.error || "Impossible d'envoyer le message."));
    }
  } catch (error) {
    console.error('Erreur:', error);
    alert("Une erreur est survenue lors de l'envoi du message. Veuillez réessayer plus tard.");
  }
});

// Navigation fluide
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    document.querySelector(this.getAttribute('href')).scrollIntoView({
      behavior: 'smooth'
    });
  });
});

const adminBtn = document.getElementById('adminBtn');
    const loginModal = document.getElementById('loginModal');
    const closeBtn = document.getElementsByClassName('close')[0];
    const loginForm = document.getElementById('loginForm');

    adminBtn.onclick = function() {
      loginModal.style.display = "block";
    }

    closeBtn.onclick = function() {
      loginModal.style.display = "none";
    }

    window.onclick = function(event) {
      if (event.target == loginModal) {
        loginModal.style.display = "none";
      }
    }
    loginForm.onsubmit = async function(e) {
      e.preventDefault();
      const username = document.getElementById('username').value;
      const password = document.getElementById('password').value;
      const csrfToken = document.querySelector('input[name="csrf_token"]').value;
    
      const response = await fetch('/admin', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ username: username, password: password })
      });
    
      const result = await response.json();
      if (result.success) {
        window.location.href = "/admin";
      } else {
        alert("Identifiants incorrects. Veuillez réessayer.");
      }
    }
   
