
// ===== Scroll to top =====
const upButton = document.getElementById("up-btn");
upButton.style.display = "none";

window.addEventListener('scroll', function () {
    upButton.style.display =
        (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20)
            ? "block" : "none";
});

function topFunction() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}

// ===== Hero Image Slider =====
const sliderImages = [
    '/static/images/background.jpg',
    '/static/images/goodwood-47.jpg',
    '/static/images/cofani-aperti-3.jpg',
];
const SLIDE_DURATION = 9000;

let currentSlide = 0;
let autoplayTimer = null;

const backgroundEl = document.querySelector('.background');
const dotEls = document.querySelectorAll('.slider-dot');
const progressEl = document.getElementById('slider-progress');
const prevBtn = document.getElementById('slider-prev');
const nextBtn = document.getElementById('slider-next');

function goToSlide(index) {
    currentSlide = (index + sliderImages.length) % sliderImages.length;

    backgroundEl.style.opacity = '0';
    setTimeout(function () {
        backgroundEl.style.backgroundImage =
            'linear-gradient(rgba(0,0,0,0.65),rgba(0,0,0,0.65)), url(' + sliderImages[currentSlide] + ')';
        backgroundEl.style.opacity = '1';
    }, 500);

    dotEls.forEach(function (dot, i) {
        dot.classList.toggle('active', i === currentSlide);
    });

    animateProgress();
}

function animateProgress() {
    if (!progressEl) return;
    progressEl.style.transition = 'none';
    progressEl.style.width = '0%';
    progressEl.offsetWidth; // force reflow
    progressEl.style.transition = 'width ' + SLIDE_DURATION + 'ms linear';
    progressEl.style.width = '100%';
}

function startAutoplay() {
    clearTimeout(autoplayTimer);
    autoplayTimer = setTimeout(function () {
        goToSlide(currentSlide + 1);
        startAutoplay();
    }, SLIDE_DURATION);
}

if (prevBtn) {
    prevBtn.addEventListener('click', function () {
        goToSlide(currentSlide - 1);
        startAutoplay();
    });
}

if (nextBtn) {
    nextBtn.addEventListener('click', function () {
        goToSlide(currentSlide + 1);
        startAutoplay();
    });
}

dotEls.forEach(function (dot, i) {
    dot.addEventListener('click', function () {
        goToSlide(i);
        startAutoplay();
    });
});

window.addEventListener('load', function () {
    goToSlide(0);
    startAutoplay();
});

// ===== Scroll Reveal =====
document.querySelectorAll('.events-container, .news-container, .merch-container').forEach(function (container) {
    container.querySelectorAll('.reveal-card').forEach(function (card, i) {
        card.style.setProperty('--delay', (i * 120) + 'ms');
    });
});

const revealObserver = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            revealObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

document.querySelectorAll('.reveal-card, .reveal-heading').forEach(function (el) {
    revealObserver.observe(el);
});
