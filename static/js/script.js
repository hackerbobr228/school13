function navigateToPage(pageName) {
  const origin = window.location.origin.replace(/\/$/, "")        // убираем слэш в конце
  const cleanPage = pageName.replace(/^\/|\/$/g, "")              // убираем / в начале и конце
  window.location.href = `${origin}/${cleanPage}/`
}




// Language translations
const translations = {
  ru: {
    "school-name": "Школа №13",
    home: "Главная",
    classes: "Классы",
    nominations: "Номинации",
    welcome: "Добро пожаловать в Школу №13",
    "hero-description":
      "Место, где формируется будущее наших детей через качественное образование и всестороннее развитие",
    "learn-more": "Узнать больше",
    "our-achievements": "Наши достижения",
    "total-students": "Всего Учеников",
    "active-students": "Активных учеников",
    "classes-count": "Классы",
    "nominations-count": "Номинации",
    "why-choose-us": "Почему выбирают нас",
    "quality-education": "Качественное образование",
    "quality-education-desc": "Современные методы обучения и опытные педагоги",
    "student-achievements": "Достижения учеников",
    "student-achievements-desc": "Признание талантов и поощрение успехов",
    "individual-approach": "Индивидуальный подход",
    "individual-approach-desc": "Учитываем особенности каждого ученика",
    "footer-description": "Образование для будущего",
    "quick-links": "Быстрые ссылки",
    contact: "Контакты",
    "all-rights-reserved": "Все права защищены.",
    "our-classes": "Наши классы",
    "classes-description": "Выберите класс для просмотра информации об учениках",
    grade: "класс",
    elementary: "Начальная школа",
    "middle-school": "Средняя школа",
    "high-school": "Старшая школа",
    students: "учеников",
    "student-nominations": "Номинации учеников",
    "nominations-description": "Признание достижений и талантов наших учеников",
    "view-recipients": "Просмотр Получателей",
    
    back: "Назад",
  },
  uz: {
    "school-name": "13-maktab",
    home: "Bosh sahifa",
    classes: "Sinflar",
    nominations: "Nominatsiyalar",
    welcome: "13-maktabga xush kelibsiz",
    "hero-description":
      "Bolalarimizning kelajagi sifatli ta'lim va har tomonlama rivojlanish orqali shakllanadigan joy",
    "learn-more": "Batafsil",
    "our-achievements": "Bizning yutuqlarimiz",
    "total-students": "Jami O'quvchilar",
    "active-students": "Faol o'quvchilar",
    "classes-count": "Sinflar",
    "nominations-count": "Nominatsiyalar",
    "why-choose-us": "Nima uchun bizni tanlashadi",
    "quality-education": "Sifatli ta'lim",
    "quality-education-desc": "Zamonaviy o'qitish usullari va tajribali o'qituvchilar",
    "student-achievements": "O'quvchilar yutuqlari",
    "student-achievements-desc": "Iste'dodlarni tan olish va muvaffaqiyatlarni rag'batlantirish",
    "individual-approach": "Individual yondashuv",
    "individual-approach-desc": "Har bir o'quvchining xususiyatlarini hisobga olamiz",
    "footer-description": "Kelajak uchun ta'lim",
    "quick-links": "Tezkor havolalar",
    contact: "Aloqa",
    "all-rights-reserved": "Barcha huquqlar himoyalangan.",
    "our-classes": "Bizning sinflarimiz",
    "classes-description": "O'quvchilar haqida ma'lumot olish uchun sinfni tanlang",
    grade: "sinf",
    elementary: "Boshlang'ich maktab",
    "middle-school": "O'rta maktab",
    "high-school": "Yuqori maktab",
    students: "o'quvchilar",
    "student-nominations": "O'quvchilar nominatsiyalari",
    "nominations-description": "O'quvchilarimizning yutuqlari va iste'dodlarini tan olish",
    "view-recipients": "Oluvchilarni Ko'rish",
    back: "Orqaga",
  },
}

// Current language and theme
let currentLang = localStorage.getItem("language") || "ru"
let currentTheme = localStorage.getItem("theme") || "light"


// Initialize the application
document.addEventListener("DOMContentLoaded", () => {
  initializeTheme()
  initializeLanguage()
  setupEventListeners()
  addAnimations()
  setupAccessibility()
  enhanceInteractivity()
  fixMobileViewport()
})

// Theme management functions
// Fix mobile viewport issues
function fixMobileViewport() {
  // Fix iOS Safari viewport height issues
  const setViewportHeight = () => {
    const vh = window.innerHeight * 0.01
    document.documentElement.style.setProperty("--vh", `${vh}px`)
  }

  setViewportHeight()
  window.addEventListener("resize", debounce(setViewportHeight, 100))
  window.addEventListener("orientationchange", debounce(setViewportHeight, 100))
}
function initializeTheme() {
  document.documentElement.setAttribute("data-theme", currentTheme)
  updateThemeIcon()

  // Add theme transition class
  document.body.classList.add("theme-transition")
  setTimeout(() => {
    document.body.classList.remove("theme-transition")
  }, 300)
}

function toggleTheme() {
  currentTheme = currentTheme === "light" ? "dark" : "light"
  document.documentElement.setAttribute("data-theme", currentTheme)
  localStorage.setItem("theme", currentTheme)
  updateThemeIcon()

  // Add smooth transition
  document.body.classList.add("theme-transition")
  setTimeout(() => {
    document.body.classList.remove("theme-transition")
  }, 300)

  // Announce theme change for screen readers
  announceToScreenReader(`Тема изменена на ${currentTheme === "light" ? "светлую" : "тёмную"}`)
}

function updateThemeIcon() {
  const themeToggle = document.getElementById("themeToggle")
  if (themeToggle) {
    const icon = themeToggle.querySelector("i")
    icon.className = currentTheme === "light" ? "fas fa-moon" : "fas fa-sun"
    themeToggle.setAttribute(
      "aria-label",
      currentTheme === "light" ? "Переключить на тёмную тему" : "Переключить на светлую тему",
    )
  }
}

// Language management functions
function initializeLanguage() {
  updateLanguage()
  updateLanguageToggle()
}

function toggleLanguage() {
  currentLang = currentLang === "ru" ? "uz" : "ru"
  localStorage.setItem("language", currentLang)
  updateLanguage()
  updateLanguageToggle()

  // Announce language change for screen readers
  announceToScreenReader(`Язык изменён на ${currentLang === "ru" ? "русский" : "узбекский"}`)
}

function updateLanguage() {
  const elements = document.querySelectorAll("[data-key]")
  elements.forEach((element) => {
    const key = element.getAttribute("data-key")
    if (translations[currentLang] && translations[currentLang][key]) {
      element.textContent = translations[currentLang][key]
    }
  })

  // Update document language
  document.documentElement.lang = currentLang
}

function updateLanguageToggle() {
  const langToggle = document.getElementById("langToggle")
  if (langToggle) {
    const langText = langToggle.querySelector(".lang-text")
    langText.textContent = currentLang === "ru" ? "УЗ" : "РУ"
    langToggle.setAttribute(
      "aria-label",
      currentLang === "ru" ? "Переключить на узбекский язык" : "Переключить на русский язык",
    )
  }
}

// Enhanced mobile menu management
function setupMobileMenu() {
  const hamburger = document.getElementById("hamburger")
  const navMenu = document.querySelector(".nav-menu")

  if (!hamburger || !navMenu) return

  // Toggle mobile menu
  hamburger.addEventListener("click", (e) => {
    e.preventDefault()
    e.stopPropagation()
    toggleMobileMenu()
  })

  // Close menu when clicking on nav links
  const navLinks = navMenu.querySelectorAll(".nav-link")
  navLinks.forEach((link) => {
    link.addEventListener("click", () => {
      closeMobileMenu()
    })
  })

  // Close menu when clicking outside
  document.addEventListener("click", (e) => {
    if (!hamburger.contains(e.target) && !navMenu.contains(e.target)) {
      closeMobileMenu()
    }
  })

  // Handle escape key
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && navMenu.classList.contains("active")) {
      closeMobileMenu()
      hamburger.focus()
    }
  })

  // Handle window resize
  window.addEventListener(
    "resize",
    debounce(() => {
      if (window.innerWidth > 768 && navMenu.classList.contains("active")) {
        closeMobileMenu()
      }
    }, 100),
  )
}

function toggleMobileMenu() {
  const hamburger = document.getElementById("hamburger")
  const navMenu = document.querySelector(".nav-menu")

  if (!hamburger || !navMenu) return

  const isExpanded = hamburger.getAttribute("aria-expanded") === "true"

  hamburger.setAttribute("aria-expanded", !isExpanded)
  hamburger.classList.toggle("active")
  navMenu.classList.toggle("active")

  // Prevent body scroll when menu is open
  if (!isExpanded) {
    document.body.style.overflow = "hidden"
  } else {
    document.body.style.overflow = ""
  }

  // Focus management
  if (!isExpanded) {
    // Menu is opening - focus first link
    const firstLink = navMenu.querySelector(".nav-link")
    if (firstLink) {
      setTimeout(() => firstLink.focus(), 100)
    }
  }
}

function closeMobileMenu() {
  const hamburger = document.getElementById("hamburger")
  const navMenu = document.querySelector(".nav-menu")

  if (!hamburger || !navMenu) return

  hamburger.setAttribute("aria-expanded", "false")
  hamburger.classList.remove("active")
  navMenu.classList.remove("active")
  document.body.style.overflow = ""
}
// Event listeners setup
function setupEventListeners() {
  // Theme toggle
  const themeToggle = document.getElementById("themeToggle")
  if (themeToggle) {
    themeToggle.addEventListener("click", toggleTheme)
  }

  // Language toggle
  const langToggle = document.getElementById("langToggle")
  if (langToggle) {
    langToggle.addEventListener("click", toggleLanguage)
  }

  // Mobile menu toggle
   setupMobileMenu()

  // Smooth scrolling for anchor links
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault()
      const target = document.querySelector(this.getAttribute("href"))
      if (target) {
        target.scrollIntoView({
          behavior: "smooth",
          block: "start",
        })
      }
    })
  })
}

// Enhanced interactivity
function enhanceInteractivity() {
  // Add interactive element class to cards
  const interactiveElements = document.querySelectorAll(".stat-card, .feature-card, .class-card, .nomination-card")
  interactiveElements.forEach((element) => {
    element.classList.add("interactive-element")
  })

  // Enhanced button interactions
  const buttons = document.querySelectorAll("button, .cta-button, .view-recipients-btn")
  buttons.forEach((button) => {
    button.addEventListener("mouseenter", () => {
      button.style.transform = "translateY(-2px)"
    })

    button.addEventListener("mouseleave", () => {
      button.style.transform = "translateY(0)"
    })
  })

  // Add loading states for navigation
  const navLinks = document.querySelectorAll(".nav-link")
  navLinks.forEach((link) => {
    link.addEventListener("click", (e) => {
      if (link.href && !link.href.includes("#")) {
        link.classList.add("loading")
      }
    })
  })
}

// Animation functions
function addAnimations() {
  // Intersection Observer for animations
  const observerOptions = {
    threshold: 0.1,
    rootMargin: "0px 0px -50px 0px",
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("fade-in")
        observer.unobserve(entry.target) // Only animate once
      }
    })
  }, observerOptions)

  // Observe all animatable elements
  const animatableElements = document.querySelectorAll(
    ".stat-card, .feature-card, .class-card, .nomination-card, .student-card, .info-card",
  )
  animatableElements.forEach((element) => {
    observer.observe(element)
  })

  // Counter animation for stats
  const statsSection = document.querySelector(".stats")
  if (statsSection) {
    const statsObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            animateCounters()
            statsObserver.unobserve(entry.target)
          }
        })
      },
      { threshold: 0.5 },
    )
    statsObserver.observe(statsSection)
  }
}

// Counter animation
function animateCounters() {
  const counters = document.querySelectorAll(".stat-number")

  counters.forEach((counter) => {
    const text = counter.textContent
    const target = Number.parseInt(text.replace(/[^\d]/g, ""))
    const suffix = text.replace(/[\d]/g, "")

    if (target > 0) {
      const increment = target / 100
      let current = 0

      const timer = setInterval(() => {
        current += increment
        if (current >= target) {
          counter.textContent = target + suffix
          clearInterval(timer)
        } else {
          counter.textContent = Math.floor(current) + suffix
        }
      }, 20)
    }
  })
}

// Accessibility functions
function setupAccessibility() {
  // Skip to main content link
  const skipLink = document.createElement("a")
  skipLink.href = "#main"
  skipLink.textContent = "Перейти к основному содержанию"
  skipLink.className = "sr-only"
  skipLink.style.cssText = `
    position: absolute;
    top: -40px;
    left: 6px;
    background: var(--primary-color);
    color: white;
    padding: 8px 16px;
    text-decoration: none;
    border-radius: 4px;
    z-index: 1001;
    transition: top 0.3s;
    font-weight: 600;
    box-shadow: var(--shadow-md);
  `

  skipLink.addEventListener("focus", () => {
    skipLink.style.top = "6px"
    skipLink.classList.remove("sr-only")
  })

  skipLink.addEventListener("blur", () => {
    skipLink.style.top = "-40px"
    skipLink.classList.add("sr-only")
  })

  document.body.insertBefore(skipLink, document.body.firstChild)

  // Add main landmark if not present
  const main = document.querySelector("main")
  if (main && !main.id) {
    main.id = "main"
  }

  // Enhanced keyboard navigation
  document.addEventListener("keydown", (e) => {
    // Alt + T for theme toggle
    if (e.altKey && e.key === "t") {
      e.preventDefault()
      const themeToggle = document.getElementById("themeToggle")
      if (themeToggle) themeToggle.click()
    }

    // Alt + L for language toggle
    if (e.altKey && e.key === "l") {
      e.preventDefault()
      const langToggle = document.getElementById("langToggle")
      if (langToggle) langToggle.click()
    }
  // Alt + M for mobile menu toggle
    if (e.altKey && e.key === "m") {
      e.preventDefault()
      const hamburger = document.getElementById("hamburger")
      if (hamburger && window.innerWidth <= 768) hamburger.click()
    }
  })
}

// Screen reader announcements
function announceToScreenReader(message) {
  const announcement = document.createElement("div")
  announcement.setAttribute("aria-live", "polite")
  announcement.setAttribute("aria-atomic", "true")
  announcement.className = "sr-only"
  announcement.textContent = message

  document.body.appendChild(announcement)

  setTimeout(() => {
    document.body.removeChild(announcement)
  }, 1000)
}

// Utility functions
function debounce(func, wait) {
  let timeout
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout)
      func(...args)
    }
    clearTimeout(timeout)
    timeout = setTimeout(later, wait)
  }
}

// Performance optimization
function lazyLoadImages() {
  const images = document.querySelectorAll('img[loading="lazy"]')

  if ("IntersectionObserver" in window) {
    const imageObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const img = entry.target
          img.src = img.dataset.src || img.src
          img.classList.remove("lazy")
          imageObserver.unobserve(img)
        }
      })
    })

    images.forEach((img) => imageObserver.observe(img))
  }
}

// Initialize lazy loading


document.addEventListener("DOMContentLoaded", lazyLoadImages)

// Error handling
window.addEventListener("error", (e) => {
  console.error("JavaScript error:", e.error)
  // Could send error to logging service in production
})

let lastScrollTop = 0
const navbar = document.querySelector(".navbar")

window.addEventListener(
  "scroll",
  debounce(() => {
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop

     if (navbar) {
      // Only hide navbar on mobile when scrolling down
      if (window.innerWidth <= 768) {
        if (scrollTop > lastScrollTop && scrollTop > 100) {
          // Scrolling down - hide navbar
          navbar.style.transform = "translateY(-100%)"
        } else {
          // Scrolling up - show navbar
          navbar.style.transform = "translateY(0)"
        }
      } else {
        // Always show navbar on desktop
        navbar.style.transform = "translateY(0)"
      }
    }

    lastScrollTop = scrollTop <= 0 ? 0 : scrollTop
  }, 100),
)


// Add CSS for theme transitions
const themeTransitionCSS = `
.theme-transition * {
  transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease !important;
}
`

const style = document.createElement("style")
style.textContent = themeTransitionCSS
document.head.appendChild(style)



// Touch event handling for better mobile experience
let touchStartY = 0
let touchEndY = 0

document.addEventListener(
  "touchstart",
  (e) => {
    touchStartY = e.changedTouches[0].screenY
  },
  { passive: true },
)

document.addEventListener(
  "touchend",
  (e) => {
    touchEndY = e.changedTouches[0].screenY
    handleSwipe()
  },
  { passive: true },
)

function handleSwipe() {
  const swipeThreshold = 50
  const diff = touchStartY - touchEndY

  // Swipe up to hide mobile menu
  if (diff > swipeThreshold) {
    const navMenu = document.querySelector(".nav-menu")
    if (navMenu && navMenu.classList.contains("active")) {
      closeMobileMenu()
    }
  }
}
