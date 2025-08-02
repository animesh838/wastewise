/**
 * WasteWise Platform - Modern Interactive JavaScript
 * Sexy animations, dynamic features and utilities
 */

// Global WasteWise object with enhanced features
window.WasteWise = {
    // Initialization
    init: function() {
        this.setupEventListeners();
        this.initializeComponents();
        this.startRealTimeUpdates();
        this.initializeModernFeatures();
        this.setupParticleSystem();
        this.initializeScrollAnimations();
    },

    // Event listeners
    setupEventListeners: function() {
        // Smooth scrolling for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });

        // Auto-hide alerts
        setTimeout(() => {
            const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
            alerts.forEach(alert => {
                if (alert.classList.contains('show')) {
                    const bsAlert = new bootstrap.Alert(alert);
                    bsAlert.close();
                }
            });
        }, 5000);

        // Form validation enhancement
        const forms = document.querySelectorAll('form[data-validate="true"]');
        forms.forEach(form => {
            form.addEventListener('submit', this.validateForm);
        });
    },

    // Initialize components
    initializeComponents: function() {
        // Initialize tooltips
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });

        // Initialize progress bars animation
        this.animateProgressBars();

        // Initialize counters
        this.animateCounters();

        // Initialize map components
        this.initializeMaps();
    },

    // Real-time updates
    startRealTimeUpdates: function() {
        // Simulate real-time sensor updates
        if (document.getElementById('sensorDashboard')) {
            setInterval(this.updateSensorData, 30000); // Update every 30 seconds
        }

        // Update timestamps
        setInterval(this.updateTimestamps, 60000); // Update every minute
    },

    // Progress bar animations
    animateProgressBars: function() {
        const progressBars = document.querySelectorAll('.progress-bar[data-animate="true"]');
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const progressBar = entry.target;
                    const finalWidth = progressBar.style.width;
                    progressBar.style.width = '0%';
                    
                    setTimeout(() => {
                        progressBar.style.transition = 'width 2s ease-in-out';
                        progressBar.style.width = finalWidth;
                    }, 100);
                    
                    observer.unobserve(progressBar);
                }
            });
        });

        progressBars.forEach(bar => observer.observe(bar));
    },

    // Counter animations
    animateCounters: function() {
        const counters = document.querySelectorAll('[data-counter]');
        
        const animateCounter = (counter) => {
            const target = parseInt(counter.getAttribute('data-counter'));
            const duration = 2000; // 2 seconds
            const steps = 60;
            const increment = target / steps;
            let current = 0;
            
            const timer = setInterval(() => {
                current += increment;
                if (current >= target) {
                    current = target;
                    clearInterval(timer);
                }
                counter.textContent = Math.floor(current);
            }, duration / steps);
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    animateCounter(entry.target);
                    observer.unobserve(entry.target);
                }
            });
        });

        counters.forEach(counter => observer.observe(counter));
    },

    // Map initialization
    initializeMaps: function() {
        const mapContainers = document.querySelectorAll('.map-container[data-interactive="true"]');
        
        mapContainers.forEach(container => {
            // Simulate interactive map functionality
            container.addEventListener('click', () => {
                this.showNotification('Map feature coming soon!', 'info');
            });
        });
    },

    // Form validation
    validateForm: function(e) {
        const form = e.target;
        let isValid = true;
        
        // Clear previous validation
        form.querySelectorAll('.is-invalid').forEach(field => {
            field.classList.remove('is-invalid');
        });
        
        // Validate required fields
        form.querySelectorAll('[required]').forEach(field => {
            if (!field.value.trim()) {
                field.classList.add('is-invalid');
                isValid = false;
            }
        });
        
        // Validate email fields
        form.querySelectorAll('input[type="email"]').forEach(field => {
            if (field.value && !WasteWise.isValidEmail(field.value)) {
                field.classList.add('is-invalid');
                isValid = false;
            }
        });
        
        if (!isValid) {
            e.preventDefault();
            WasteWise.showNotification('Please fill in all required fields correctly.', 'error');
        }
    },

    // Email validation
    isValidEmail: function(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    },

    // Notification system
    showNotification: function(message, type = 'info', duration = 5000) {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(notification);
        
        // Auto-remove after duration
        setTimeout(() => {
            if (notification.parentNode) {
                const bsAlert = new bootstrap.Alert(notification);
                bsAlert.close();
            }
        }, duration);
    },

    // Sensor data updates
    updateSensorData: function() {
        const sensorCards = document.querySelectorAll('.sensor-card[data-bin-id]');
        
        sensorCards.forEach(card => {
            // Simulate random sensor updates
            const fillLevel = Math.floor(Math.random() * 100);
            const temperature = (Math.random() * 15 + 15).toFixed(1); // 15-30°C
            const battery = Math.floor(Math.random() * 40 + 60); // 60-100%
            
            // Update fill level
            const fillIndicator = card.querySelector('.fill-level');
            const fillText = card.querySelector('.fill-level .text-center');
            
            if (fillIndicator && fillText) {
                fillIndicator.style.height = `${fillLevel}%`;
                fillText.textContent = `${fillLevel}%`;
                
                // Update color based on level
                fillIndicator.className = `fill-level ${WasteWise.getFillLevelClass(fillLevel)}`;
            }
            
            // Update temperature
            const tempElement = card.querySelector('.bi-thermometer-half + small');
            if (tempElement) {
                tempElement.textContent = `${temperature}°C`;
            }
            
            // Update battery
            const batteryElement = card.querySelector('[class*="bi-battery"] + small');
            if (batteryElement) {
                batteryElement.textContent = `${battery}%`;
            }
        });
    },

    // Get fill level CSS class
    getFillLevelClass: function(level) {
        if (level < 30) return 'low';
        if (level < 60) return 'medium';
        if (level < 80) return 'high';
        return 'critical';
    },

    // Update relative timestamps
    updateTimestamps: function() {
        const timestamps = document.querySelectorAll('[data-timestamp]');
        
        timestamps.forEach(element => {
            const timestamp = new Date(element.getAttribute('data-timestamp'));
            const now = new Date();
            const diff = now - timestamp;
            
            element.textContent = WasteWise.formatRelativeTime(diff);
        });
    },

    // Format relative time
    formatRelativeTime: function(diff) {
        const seconds = Math.floor(diff / 1000);
        const minutes = Math.floor(seconds / 60);
        const hours = Math.floor(minutes / 60);
        const days = Math.floor(hours / 24);
        
        if (days > 0) return `${days} day${days > 1 ? 's' : ''} ago`;
        if (hours > 0) return `${hours} hour${hours > 1 ? 's' : ''} ago`;
        if (minutes > 0) return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
        return 'Just now';
    },

    // Local storage utilities
    storage: {
        set: function(key, value) {
            try {
                localStorage.setItem(`wastewise_${key}`, JSON.stringify(value));
            } catch (e) {
                console.warn('LocalStorage not available');
            }
        },
        
        get: function(key) {
            try {
                const item = localStorage.getItem(`wastewise_${key}`);
                return item ? JSON.parse(item) : null;
            } catch (e) {
                console.warn('LocalStorage not available');
                return null;
            }
        },
        
        remove: function(key) {
            try {
                localStorage.removeItem(`wastewise_${key}`);
            } catch (e) {
                console.warn('LocalStorage not available');
            }
        }
    },

    // Chart utilities
    charts: {
        defaultColors: [
            '#28a745', '#007bff', '#ffc107', '#dc3545', 
            '#6f42c1', '#20c997', '#fd7e14', '#6c757d'
        ],
        
        createLineChart: function(canvasId, data, options = {}) {
            const ctx = document.getElementById(canvasId);
            if (!ctx) return null;
            
            const defaultOptions = {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            };
            
            return new Chart(ctx.getContext('2d'), {
                type: 'line',
                data: data,
                options: { ...defaultOptions, ...options }
            });
        },
        
        createDoughnutChart: function(canvasId, data, options = {}) {
            const ctx = document.getElementById(canvasId);
            if (!ctx) return null;
            
            const defaultOptions = {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            };
            
            return new Chart(ctx.getContext('2d'), {
                type: 'doughnut',
                data: data,
                options: { ...defaultOptions, ...options }
            });
        }
    },

    // API utilities
    api: {
        baseUrl: '/api/',
        
        request: function(endpoint, options = {}) {
            const defaultOptions = {
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': WasteWise.getCSRFToken()
                },
                credentials: 'same-origin'
            };
            
            return fetch(this.baseUrl + endpoint, { ...defaultOptions, ...options })
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.json();
                });
        },
        
        get: function(endpoint) {
            return this.request(endpoint, { method: 'GET' });
        },
        
        post: function(endpoint, data) {
            return this.request(endpoint, {
                method: 'POST',
                body: JSON.stringify(data)
            });
        },
        
        put: function(endpoint, data) {
            return this.request(endpoint, {
                method: 'PUT',
                body: JSON.stringify(data)
            });
        },
        
        delete: function(endpoint) {
            return this.request(endpoint, { method: 'DELETE' });
        }
    },

    // Get CSRF token
    getCSRFToken: function() {
        const tokenElement = document.querySelector('[name=csrfmiddlewaretoken]');
        return tokenElement ? tokenElement.value : '';
    },

    // Modern features initialization
    initializeModernFeatures: function() {
        this.initializeTypingAnimation();
        this.setupHoverEffects();
        this.initializeParallaxEffect();
        this.setupCardAnimations();
        this.initializeLoadingAnimations();
        this.setupTiltEffect();
    },

    // Typing animation for hero text
    initializeTypingAnimation: function() {
        const typingElements = document.querySelectorAll('[data-typing]');
        
        typingElements.forEach(element => {
            const text = element.getAttribute('data-typing');
            const speed = parseInt(element.getAttribute('data-typing-speed')) || 100;
            element.textContent = '';
            
            let i = 0;
            const typeWriter = () => {
                if (i < text.length) {
                    element.textContent += text.charAt(i);
                    i++;
                    setTimeout(typeWriter, speed);
                }
            };
            
            // Start typing when element is visible
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        setTimeout(typeWriter, 500);
                        observer.unobserve(element);
                    }
                });
            });
            
            observer.observe(element);
        });
    },

    // Enhanced hover effects
    setupHoverEffects: function() {
        // Magnetic effect for buttons
        const magneticElements = document.querySelectorAll('.btn-modern, .card-modern');
        
        magneticElements.forEach(element => {
            element.addEventListener('mousemove', (e) => {
                const rect = element.getBoundingClientRect();
                const x = e.clientX - rect.left - rect.width / 2;
                const y = e.clientY - rect.top - rect.height / 2;
                
                element.style.transform = `translate(${x * 0.1}px, ${y * 0.1}px) scale(1.05)`;
            });
            
            element.addEventListener('mouseleave', () => {
                element.style.transform = 'translate(0px, 0px) scale(1)';
            });
        });

        // Glowing effect for interactive elements
        const glowElements = document.querySelectorAll('.stats-card, .sensor-card');
        
        glowElements.forEach(element => {
            element.addEventListener('mouseenter', () => {
                element.style.boxShadow = '0 0 30px rgba(17, 153, 142, 0.6)';
                element.style.transition = 'all 0.3s ease';
            });
            
            element.addEventListener('mouseleave', () => {
                element.style.boxShadow = '';
            });
        });
    },

    // Parallax scrolling effect
    initializeParallaxEffect: function() {
        const parallaxElements = document.querySelectorAll('[data-parallax]');
        
        if (parallaxElements.length > 0) {
            window.addEventListener('scroll', () => {
                const scrolled = window.pageYOffset;
                
                parallaxElements.forEach(element => {
                    const rate = scrolled * (element.getAttribute('data-parallax') || -0.5);
                    element.style.transform = `translateY(${rate}px)`;
                });
            });
        }
    },

    // Card animations on scroll
    setupCardAnimations: function() {
        const cards = document.querySelectorAll('.card, .stats-card, .dashboard-card');
        
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const cardObserver = new IntersectionObserver((entries) => {
            entries.forEach((entry, index) => {
                if (entry.isIntersecting) {
                    setTimeout(() => {
                        entry.target.style.opacity = '1';
                        entry.target.style.transform = 'translateY(0) scale(1)';
                        entry.target.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
                    }, index * 100);
                    
                    cardObserver.unobserve(entry.target);
                }
            });
        }, observerOptions);
        
        cards.forEach(card => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(30px) scale(0.95)';
            cardObserver.observe(card);
        });
    },

    // Loading animations
    initializeLoadingAnimations: function() {
        // Skeleton loading for dynamic content
        const skeletonElements = document.querySelectorAll('.skeleton');
        
        setTimeout(() => {
            skeletonElements.forEach(skeleton => {
                skeleton.classList.add('loaded');
            });
        }, 1000);

        // Progressive image loading
        const images = document.querySelectorAll('img[data-src]');
        
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.getAttribute('data-src');
                    img.classList.add('loaded');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
    },

    // 3D tilt effect
    setupTiltEffect: function() {
        const tiltElements = document.querySelectorAll('[data-tilt]');
        
        tiltElements.forEach(element => {
            element.addEventListener('mousemove', (e) => {
                const rect = element.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                
                const centerX = rect.width / 2;
                const centerY = rect.height / 2;
                
                const rotateX = (y - centerY) / centerY * -10;
                const rotateY = (x - centerX) / centerX * 10;
                
                element.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.05, 1.05, 1.05)`;
                element.style.transition = 'transform 0.1s ease';
            });
            
            element.addEventListener('mouseleave', () => {
                element.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) scale3d(1, 1, 1)';
                element.style.transition = 'transform 0.3s ease';
            });
        });
    },

    // Particle system for background
    setupParticleSystem: function() {
        const particleContainer = document.getElementById('particles');
        if (!particleContainer) return;
        
        const particleCount = 50;
        
        for (let i = 0; i < particleCount; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.cssText = `
                position: absolute;
                width: 4px;
                height: 4px;
                background: rgba(255, 255, 255, 0.3);
                border-radius: 50%;
                pointer-events: none;
                animation: float ${Math.random() * 3 + 2}s ease-in-out infinite;
                animation-delay: ${Math.random() * 2}s;
                left: ${Math.random() * 100}%;
                top: ${Math.random() * 100}%;
            `;
            
            particleContainer.appendChild(particle);
        }
    },

    // Scroll-triggered animations
    initializeScrollAnimations: function() {
        // Reveal elements on scroll
        const revealElements = document.querySelectorAll('[data-reveal]');
        
        const revealObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const element = entry.target;
                    const animationType = element.getAttribute('data-reveal');
                    
                    switch (animationType) {
                        case 'fade-up':
                            element.style.animation = 'fadeInUp 0.8s ease forwards';
                            break;
                        case 'fade-left':
                            element.style.animation = 'fadeInLeft 0.8s ease forwards';
                            break;
                        case 'fade-right':
                            element.style.animation = 'fadeInRight 0.8s ease forwards';
                            break;
                        case 'zoom':
                            element.style.animation = 'zoomIn 0.8s ease forwards';
                            break;
                        default:
                            element.style.animation = 'fadeIn 0.8s ease forwards';
                    }
                    
                    revealObserver.unobserve(element);
                }
            });
        }, { threshold: 0.1 });
        
        revealElements.forEach(element => {
            element.style.opacity = '0';
            revealObserver.observe(element);
        });

        // Add CSS keyframes dynamically
        this.addAnimationKeyframes();
    },

    // Add CSS animation keyframes
    addAnimationKeyframes: function() {
        const style = document.createElement('style');
        style.textContent = `
            @keyframes fadeInUp {
                from { opacity: 0; transform: translateY(30px); }
                to { opacity: 1; transform: translateY(0); }
            }
            @keyframes fadeInLeft {
                from { opacity: 0; transform: translateX(-30px); }
                to { opacity: 1; transform: translateX(0); }
            }
            @keyframes fadeInRight {
                from { opacity: 0; transform: translateX(30px); }
                to { opacity: 1; transform: translateX(0); }
            }
            @keyframes zoomIn {
                from { opacity: 0; transform: scale(0.8); }
                to { opacity: 1; transform: scale(1); }
            }
            @keyframes float {
                0%, 100% { transform: translateY(0) rotate(0deg); }
                50% { transform: translateY(-20px) rotate(180deg); }
            }
        `;
        document.head.appendChild(style);
    },

    // Enhanced chart creation with animations
    createAnimatedChart: function(canvasId, type, data, options = {}) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return null;
        
        const defaultOptions = {
            responsive: true,
            maintainAspectRatio: false,
            animation: {
                duration: 2000,
                easing: 'easeInOutQuart'
            },
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        usePointStyle: true,
                        padding: 20
                    }
                }
            }
        };
        
        return new Chart(ctx.getContext('2d'), {
            type: type,
            data: data,
            options: { ...defaultOptions, ...options }
        });
    },

    // Smooth number counting animation
    animateValue: function(element, start, end, duration = 2000) {
        const range = end - start;
        const startTime = performance.now();
        
        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            // Easing function
            const easeOutQuart = 1 - Math.pow(1 - progress, 4);
            
            const current = Math.floor(start + (range * easeOutQuart));
            element.textContent = current.toLocaleString();
            
            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };
        
        requestAnimationFrame(animate);
    },

    // Interactive notifications with better styling
    showModernNotification: function(message, type = 'info', duration = 5000) {
        const notification = document.createElement('div');
        const icon = this.getNotificationIcon(type);
        
        notification.className = `modern-notification ${type}`;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
            min-width: 300px;
            max-width: 400px;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border-radius: 15px;
            padding: 1rem 1.5rem;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            border-left: 4px solid var(--${type}-color, #17a2b8);
            transform: translateX(100%);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        `;
        
        notification.innerHTML = `
            <div style="display: flex; align-items: center; gap: 0.75rem;">
                <i class="${icon}" style="font-size: 1.25rem; color: var(--${type}-color, #17a2b8);"></i>
                <span style="flex: 1; font-weight: 500;">${message}</span>
                <button onclick="this.parentElement.parentElement.remove()" 
                        style="background: none; border: none; font-size: 1.25rem; cursor: pointer; opacity: 0.7;">
                    ×
                </button>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);
        
        // Auto-remove
        setTimeout(() => {
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.remove();
                }
            }, 400);
        }, duration);
    },

    // Get notification icon
    getNotificationIcon: function(type) {
        const icons = {
            success: 'bi bi-check-circle-fill',
            error: 'bi bi-exclamation-triangle-fill',
            warning: 'bi bi-exclamation-circle-fill',
            info: 'bi bi-info-circle-fill'
        };
        return icons[type] || icons.info;
    }
};

// Pickup scheduling utilities
WasteWise.PickupScheduler = {
    currentStep: 1,
    totalSteps: 4,
    
    nextStep: function() {
        if (this.currentStep < this.totalSteps) {
            this.currentStep++;
            this.updateDisplay();
        }
    },
    
    previousStep: function() {
        if (this.currentStep > 1) {
            this.currentStep--;
            this.updateDisplay();
        }
    },
    
    updateDisplay: function() {
        // Hide all step contents
        document.querySelectorAll('.step-content').forEach(content => {
            content.style.display = 'none';
        });
        
        // Show current step
        const currentContent = document.getElementById(`step${this.currentStep}Content`);
        if (currentContent) {
            currentContent.style.display = 'block';
        }
        
        // Update step indicators
        document.querySelectorAll('.step').forEach((step, index) => {
            step.classList.remove('active', 'completed');
            if (index + 1 < this.currentStep) {
                step.classList.add('completed');
            } else if (index + 1 === this.currentStep) {
                step.classList.add('active');
            }
        });
        
        // Update navigation buttons
        const prevBtn = document.getElementById('prevBtn');
        const nextBtn = document.getElementById('nextBtn');
        const submitBtn = document.getElementById('submitBtn');
        
        if (prevBtn) prevBtn.style.display = this.currentStep > 1 ? 'block' : 'none';
        if (nextBtn) nextBtn.style.display = this.currentStep < this.totalSteps ? 'block' : 'none';
        if (submitBtn) submitBtn.style.display = this.currentStep === this.totalSteps ? 'block' : 'none';
    }
};

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    WasteWise.init();
});

// Export for use in other scripts
window.WasteWise = WasteWise;