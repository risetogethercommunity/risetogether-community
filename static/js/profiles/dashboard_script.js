// Interactive like button functionality
function toggleLike(button) {
    const icon = button.querySelector('i');
    const countSpan = button.querySelector('.like-count');
    let count = parseInt(countSpan.textContent);

    if (button.classList.contains('liked')) {
        // Unlike
        button.classList.remove('liked');
        icon.classList.remove('fas', 'fa-heart');
        icon.classList.add('far', 'fa-heart');
        count--;
    } else {
        // Like
        button.classList.add('liked');
        icon.classList.remove('far', 'fa-heart');
        icon.classList.add('fas', 'fa-heart');
        count++;
        
        // Add animation
        button.style.transform = 'scale(1.1)';
        setTimeout(() => {
            button.style.transform = 'scale(1)';
        }, 200);
    }

    countSpan.textContent = count;
}

// Navigation active state management
document.querySelectorAll('.nav-link, .mobile-nav-link').forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        
        // Remove active class from all links in the same navigation
        const parent = this.closest('nav') || this.closest('aside');
        parent.querySelectorAll('.active').forEach(activeLink => {
            activeLink.classList.remove('active');
        });
        
        // Add active class to clicked link
        this.classList.add('active');
    });
});

// Post composer functionality
document.querySelector('.composer-input').addEventListener('input', function() {
    const postBtn = document.querySelector('.composer-actions .btn-primary');
    if (this.value.trim()) {
        postBtn.style.opacity = '1';
        postBtn.disabled = false;
    } else {
        postBtn.style.opacity = '0.5';
        postBtn.disabled = true;
    }
});

// Initialize post button state
document.querySelector('.composer-actions .btn-primary').style.opacity = '0.5';
document.querySelector('.composer-actions .btn-primary').disabled = true;

// Smooth scrolling for feed
const feedPosts = document.querySelector('.feed-posts');
let isScrolling = false;

feedPosts.addEventListener('scroll', function() {
    if (!isScrolling) {
        window.requestAnimationFrame(function() {
            // Add any scroll-based animations here
            isScrolling = false;
        });
        isScrolling = true;
    }
});

// Auto-resize textarea
const textarea = document.querySelector('.composer-input');
textarea.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 200) + 'px';
});

// Simulate real-time updates
function simulateActivity() {
    const activities = [
        'New comment on your post',
        'Someone liked your project',
        'New follower joined',
        'Trending topic update'
    ];
    
    // This would typically be handled by WebSocket connections
    // or polling for real applications
}

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    console.log('Rise Together Dashboard loaded successfully!');
});