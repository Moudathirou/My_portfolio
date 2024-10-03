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

// Gestion du formulaire de contact
document.getElementById("contact-form").addEventListener("submit", function(e) {
  e.preventDefault();
  // Ici, vous pouvez ajouter le code pour envoyer le formulaire à votre backend
  alert("Merci pour votre message ! Je vous répondrai dans les plus brefs délais.");
  this.reset();
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
   