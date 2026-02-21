/**
 * oka-pi-lp Main JavaScript
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Initialise Particles.js for Hero Section
    initParticles();

    // 2. Element Fade-up Animation on Scroll
    initScrollAnimations();

    // 3. Header Scrolled State
    initHeaderScroll();

    // 4. Mobile Menu Toggle
    initMobileMenu();

    // 5. Smooth Scroll for Anchor Links
    initSmoothScroll();

    // 6. Initialize Swiper for Works Carousel
    initWorksSwiper();
});

/**
 * Initialize Swiper JS for the Works Section Carousel
 */
function initWorksSwiper() {
    if (document.querySelector('.works-slider')) {
        new Swiper('.works-slider', {
            // Optional parameters
            slidesPerView: 1,
            spaceBetween: 24,
            loop: true,
            grabCursor: true,

            // Auto play
            autoplay: {
                delay: 5000,
                disableOnInteraction: false,
            },

            // Responsive breakpoints
            breakpoints: {
                // when window width is >= 640px
                640: {
                    slidesPerView: 2,
                    spaceBetween: 24
                },
                // when window width is >= 968px
                968: {
                    slidesPerView: 3,
                    spaceBetween: 30
                }
            },

            // Pagination
            pagination: {
                el: '.swiper-pagination',
                clickable: true,
            },

            // Navigation arrows
            navigation: {
                nextEl: '.swiper-button-next',
                prevEl: '.swiper-button-prev',
            },
        });
    }
}

/**
 * Initializes particles.js to create a subtle network effect in the background
 */
function initParticles() {
    if (typeof particlesJS !== 'undefined' && document.getElementById('particles-js')) {
        particlesJS('particles-js', {
            "particles": {
                "number": {
                    "value": 40,
                    "density": {
                        "enable": true,
                        "value_area": 800
                    }
                },
                "color": {
                    "value": "#3b82f6" // Secondary/Primary light blue
                },
                "shape": {
                    "type": "circle",
                },
                "opacity": {
                    "value": 0.3,
                    "random": false,
                },
                "size": {
                    "value": 3,
                    "random": true,
                },
                "line_linked": {
                    "enable": true,
                    "distance": 150,
                    "color": "#3b82f6",
                    "opacity": 0.2,
                    "width": 1
                },
                "move": {
                    "enable": true,
                    "speed": 1.5,
                    "direction": "none",
                    "random": false,
                    "straight": false,
                    "out_mode": "out",
                    "bounce": false,
                }
            },
            "interactivity": {
                "detect_on": "canvas",
                "events": {
                    "onhover": {
                        "enable": true,
                        "mode": "grab"
                    },
                    "onclick": {
                        "enable": true,
                        "mode": "push"
                    },
                    "resize": true
                },
                "modes": {
                    "grab": {
                        "distance": 140,
                        "line_linked": {
                            "opacity": 0.5
                        }
                    },
                    "push": {
                        "particles_nb": 2
                    }
                }
            },
            "retina_detect": true
        });
    }
}

/**
 * Intersection Observer for fade-up animations
 */
function initScrollAnimations() {
    const fadeElements = document.querySelectorAll('.fade-up');

    // Check if IntersectionObserver is supported
    if ('IntersectionObserver' in window) {
        const observerOptions = {
            root: null,
            rootMargin: '0px',
            threshold: 0.15
        };

        const observer = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    // Stop observing once animated
                    observer.unobserve(entry.target);
                }
            });
        }, observerOptions);

        fadeElements.forEach(el => {
            observer.observe(el);
        });
    } else {
        // Fallback for older browsers
        fadeElements.forEach(el => {
            el.classList.add('visible');
        });
    }

    // Trigger animations for elements already in viewport on load
    setTimeout(() => {
        fadeElements.forEach(el => {
            const rect = el.getBoundingClientRect();
            if (rect.top < window.innerHeight) {
                el.classList.add('visible');
            }
        });
    }, 100);
}

/**
 * Adds a shadow/shrink effect to header on scroll
 */
function initHeaderScroll() {
    const header = document.querySelector('.header');
    if (!header) return;

    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });
}

/**
 * Mobile menu toggle functionality
 */
function initMobileMenu() {
    const menuBtn = document.querySelector('.mobile-menu-btn');
    const nav = document.querySelector('.nav');

    if (!menuBtn || !nav) return;

    menuBtn.addEventListener('click', () => {
        nav.classList.toggle('active');
        const spans = menuBtn.querySelectorAll('span');

        // Simple hamburger to X animation
        if (nav.classList.contains('active')) {
            if (spans[0]) spans[0].style.transform = 'translateY(7px) rotate(45deg)';
            if (spans[1]) spans[1].style.opacity = '0';
            if (spans[2]) spans[2].style.transform = 'translateY(-7px) rotate(-45deg)';
            document.body.style.overflow = 'hidden'; // Prevent scrolling
        } else {
            if (spans[0]) spans[0].style.transform = 'none';
            if (spans[1]) spans[1].style.opacity = '1';
            if (spans[2]) spans[2].style.transform = 'none';
            document.body.style.overflow = '';
        }
    });
}

/**
 * Smooth scrolling for all anchor links
 */
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href');

            // Skip if it's just '#'
            if (targetId === '#') {
                e.preventDefault();
                return;
            }

            const targetElement = document.querySelector(targetId);

            if (targetElement) {
                e.preventDefault();

                // Close mobile menu if open
                const nav = document.querySelector('.nav');
                const menuBtn = document.querySelector('.mobile-menu-btn');
                if (nav && nav.classList.contains('active')) {
                    menuBtn.click();
                }

                // Calculate scroll position taking fixed header into account
                const header = document.querySelector('.header');
                const headerHeight = header ? header.offsetHeight : 80;
                const elementPosition = targetElement.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerHeight;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}
