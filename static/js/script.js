// =============================================
// MOBILE NAVIGATION MENU LOGIC
// =============================================

const hamburger = document.querySelector(".hamburger");
const navMenu = document.querySelector(".nav-menu");

// Toggles the 'active' class on the hamburger menu and the navigation menu
// when the hamburger icon is clicked.
hamburger.addEventListener("click", () => {
    hamburger.classList.toggle("active");
    navMenu.classList.toggle("active");
});

// Closes the mobile menu when a navigation link is clicked.
// This provides a better user experience on mobile devices.
document.querySelectorAll(".nav-link").forEach(link => {
    link.addEventListener("click", () => {
        if (hamburger.classList.contains("active")) {
            hamburger.classList.remove("active");
            navMenu.classList.remove("active");
        }
    });
});


// =============================================
// SCROLL-IN ANIMATION LOGIC
// =============================================

// This function is the callback that runs whenever an observed element's
// visibility changes.
const handleIntersection = (entries, observer) => {
    entries.forEach(entry => {
        // 'isIntersecting' is a boolean that's true if the element is in the viewport.
        if (entry.isIntersecting) {
            // Add the 'visible' class, which triggers our CSS fade-in animation.
            entry.target.classList.add('visible');
            
            // Once the animation is triggered, we don't need to watch this element anymore.
            // This improves performance.
            observer.unobserve(entry.target);
        }
    });
};

// The IntersectionObserver is a modern API for efficiently detecting when
// an element enters the viewport.
const observer = new IntersectionObserver(handleIntersection, {
    root: null, // `null` means the observer uses the browser viewport as the boundary.
    rootMargin: '0px', // No extra margin around the viewport.
    threshold: 0.15 // The animation will trigger when 15% of the element is visible.
});

// Select all elements that we want to animate on scroll.
const sectionsToAnimate = document.querySelectorAll('.fade-in-section');

// Loop through each element and tell the observer to start watching it.
sectionsToAnimate.forEach(section => {
    observer.observe(section);
});