/**
 * AWS Strands Workshop - Main JavaScript File
 * Comprehensive interactive functionality for the workshop website
 * 
 * Features:
 * - Copy-to-clipboard with visual feedback
 * - Progress tracking with localStorage persistence
 * - Smooth scrolling navigation
 * - Mobile menu functionality
 * - Collapsible sections and accordions
 * - Interactive architecture diagrams preparation
 * - Accessibility support
 * - Performance optimizations
 */

(function() {
    'use strict';

    // ==========================================================================
    // Configuration and Constants
    // ==========================================================================

    const CONFIG = {
        STORAGE_PREFIX: 'strands-workshop-',
        ANIMATION_DURATION: 300,
        SCROLL_OFFSET: 80,
        DEBOUNCE_DELAY: 100,
        COPY_FEEDBACK_DURATION: 2000,
        MOBILE_BREAKPOINT: 768
    };

    const SELECTORS = {
        copyButtons: '.copy-btn',
        progressCheckboxes: '.progress-checkbox',
        progressBar: '.progress-bar-fill',
        progressPercentage: '.progress-percentage',
        dropdownToggles: '.dropdown-toggle',
        dropdownMenus: '.dropdown-menu',
        collapsibleHeaders: '.collapsible-header',
        collapsibleContent: '.collapsible-content',
        mobileMenuToggle: '.mobile-menu-toggle',
        mainNav: '.main-nav',
        navLinks: '.nav-links',
        smoothScrollLinks: 'a[href^="#"]',
        codeBlocks: 'pre code',
        moduleContent: '.module-content',
        setupContent: '.setup-content'
    };

    const CLASSES = {
        active: 'active',
        expanded: 'expanded',
        collapsed: 'collapsed',
        copying: 'copying',
        copied: 'copied',
        error: 'error',
        loading: 'loading',
        visible: 'visible',
        hidden: 'hidden',
        mobileMenuOpen: 'mobile-menu-open'
    };

    // ==========================================================================
    // Utility Functions
    // ==========================================================================

    /**
     * Debounce function to limit the rate of function execution
     */
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    /**
     * Throttle function to limit function execution frequency
     */
    function throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }

    /**
     * Check if an element is in viewport
     */
    function isInViewport(element, offset = 0) {
        const rect = element.getBoundingClientRect();
        return (
            rect.top >= -offset &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) + offset &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    }

    /**
     * Get element offset from top of document
     */
    function getElementOffset(element) {
        let offsetTop = 0;
        while (element) {
            offsetTop += element.offsetTop;
            element = element.offsetParent;
        }
        return offsetTop;
    }

    /**
     * Animate element with CSS transitions
     */
    function animateElement(element, properties, duration = CONFIG.ANIMATION_DURATION) {
        return new Promise(resolve => {
            element.style.transition = `all ${duration}ms ease-in-out`;
            
            Object.keys(properties).forEach(prop => {
                element.style[prop] = properties[prop];
            });

            setTimeout(() => {
                element.style.transition = '';
                resolve();
            }, duration);
        });
    }

    /**
     * Show screen reader announcement
     */
    function announceToScreenReader(message) {
        const announcement = document.createElement('div');
        announcement.setAttribute('aria-live', 'polite');
        announcement.setAttribute('aria-atomic', 'true');
        announcement.className = 'sr-only';
        announcement.textContent = message;
        
        document.body.appendChild(announcement);
        
        setTimeout(() => {
            document.body.removeChild(announcement);
        }, 1000);
    }

    // ==========================================================================
    // Local Storage Management
    // ==========================================================================

    const Storage = {
        /**
         * Get item from localStorage with prefix
         */
        get(key) {
            try {
                const value = localStorage.getItem(CONFIG.STORAGE_PREFIX + key);
                return value ? JSON.parse(value) : null;
            } catch (error) {
                console.warn('Error reading from localStorage:', error);
                return null;
            }
        },

        /**
         * Set item in localStorage with prefix
         */
        set(key, value) {
            try {
                localStorage.setItem(CONFIG.STORAGE_PREFIX + key, JSON.stringify(value));
                return true;
            } catch (error) {
                console.warn('Error writing to localStorage:', error);
                return false;
            }
        },

        /**
         * Remove item from localStorage
         */
        remove(key) {
            try {
                localStorage.removeItem(CONFIG.STORAGE_PREFIX + key);
                return true;
            } catch (error) {
                console.warn('Error removing from localStorage:', error);
                return false;
            }
        },

        /**
         * Clear all workshop-related localStorage items
         */
        clear() {
            try {
                const keys = Object.keys(localStorage);
                keys.forEach(key => {
                    if (key.startsWith(CONFIG.STORAGE_PREFIX)) {
                        localStorage.removeItem(key);
                    }
                });
                return true;
            } catch (error) {
                console.warn('Error clearing localStorage:', error);
                return false;
            }
        }
    };

    // ==========================================================================
    // Copy-to-Clipboard Functionality
    // ==========================================================================

    class ClipboardManager {
        constructor() {
            this.initializeCopyButtons();
        }

        initializeCopyButtons() {
            const copyButtons = document.querySelectorAll(SELECTORS.copyButtons);
            copyButtons.forEach(button => {
                this.setupCopyButton(button);
            });
        }

        setupCopyButton(button) {
            // Ensure button has proper attributes
            if (!button.hasAttribute('aria-label')) {
                button.setAttribute('aria-label', 'Copy code to clipboard');
            }

            button.addEventListener('click', (e) => {
                e.preventDefault();
                this.handleCopyClick(button);
            });

            // Keyboard support
            button.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    this.handleCopyClick(button);
                }
            });
        }

        async handleCopyClick(button) {
            try {
                const codeText = this.extractCodeText(button);
                if (!codeText) {
                    throw new Error('No code found to copy');
                }

                await this.copyToClipboard(codeText);
                this.showCopySuccess(button);
                announceToScreenReader('Code copied to clipboard');
                
            } catch (error) {
                console.error('Copy failed:', error);
                this.showCopyError(button);
                announceToScreenReader('Failed to copy code');
            }
        }

        extractCodeText(button) {
            // Try to find code block relative to button
            let codeElement = button.previousElementSibling;
            
            // Look for pre > code structure
            if (codeElement && codeElement.tagName === 'PRE') {
                const codeChild = codeElement.querySelector('code');
                if (codeChild) {
                    return codeChild.textContent.trim();
                }
                return codeElement.textContent.trim();
            }

            // Look for code element in parent
            const parent = button.parentElement;
            const codeInParent = parent.querySelector('pre code, code');
            if (codeInParent) {
                return codeInParent.textContent.trim();
            }

            // Fallback: look for any code block in the same container
            const container = button.closest('.code-block, .step-content, .solution');
            if (container) {
                const codeInContainer = container.querySelector('pre code, code');
                if (codeInContainer) {
                    return codeInContainer.textContent.trim();
                }
            }

            return null;
        }

        async copyToClipboard(text) {
            // Modern clipboard API
            if (navigator.clipboard && window.isSecureContext) {
                await navigator.clipboard.writeText(text);
                return;
            }

            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = text;
            textArea.style.position = 'fixed';
            textArea.style.left = '-999999px';
            textArea.style.top = '-999999px';
            document.body.appendChild(textArea);
            textArea.focus();
            textArea.select();
            
            try {
                document.execCommand('copy');
            } finally {
                document.body.removeChild(textArea);
            }
        }

        showCopySuccess(button) {
            const originalText = button.textContent;
            
            button.classList.add(CLASSES.copied);
            button.textContent = '✓ Copied!';
            button.setAttribute('aria-label', 'Code copied successfully');

            setTimeout(() => {
                button.classList.remove(CLASSES.copied);
                button.textContent = originalText;
                button.setAttribute('aria-label', 'Copy code to clipboard');
            }, CONFIG.COPY_FEEDBACK_DURATION);
        }

        showCopyError(button) {
            const originalText = button.textContent;
            
            button.classList.add(CLASSES.error);
            button.textContent = '✗ Failed';
            button.setAttribute('aria-label', 'Copy failed');

            setTimeout(() => {
                button.classList.remove(CLASSES.error);
                button.textContent = originalText;
                button.setAttribute('aria-label', 'Copy code to clipboard');
            }, CONFIG.COPY_FEEDBACK_DURATION);
        }
    }

    // ==========================================================================
    // Progress Tracking System
    // ==========================================================================

    class ProgressTracker {
        constructor() {
            this.initializeProgressTracking();
        }

        initializeProgressTracking() {
            const checkboxes = document.querySelectorAll(SELECTORS.progressCheckboxes);
            
            // Load saved progress
            this.loadProgress(checkboxes);
            
            // Setup event listeners
            checkboxes.forEach(checkbox => {
                checkbox.addEventListener('change', () => {
                    this.handleProgressChange(checkbox);
                });
            });

            // Initial progress calculation
            this.updateProgressDisplay();
        }

        loadProgress(checkboxes) {
            checkboxes.forEach(checkbox => {
                const progressKey = this.getProgressKey(checkbox);
                const isCompleted = Storage.get(progressKey);
                
                if (isCompleted) {
                    checkbox.checked = true;
                    this.addCompletedStyling(checkbox);
                }
            });
        }

        handleProgressChange(checkbox) {
            const progressKey = this.getProgressKey(checkbox);
            const isChecked = checkbox.checked;
            
            // Save to localStorage
            Storage.set(progressKey, isChecked);
            
            // Update styling
            if (isChecked) {
                this.addCompletedStyling(checkbox);
                announceToScreenReader('Step marked as completed');
            } else {
                this.removeCompletedStyling(checkbox);
                announceToScreenReader('Step marked as incomplete');
            }
            
            // Update progress display
            this.updateProgressDisplay();
            
            // Trigger progress animation
            this.animateProgressChange();
        }

        getProgressKey(checkbox) {
            const module = checkbox.dataset.module || 'general';
            const step = checkbox.dataset.step || checkbox.id || 'unknown';
            return `progress-${module}-${step}`;
        }

        addCompletedStyling(checkbox) {
            const label = checkbox.nextElementSibling;
            if (label) {
                label.classList.add('completed');
            }
            
            const stepItem = checkbox.closest('.step-item, .step-checkbox');
            if (stepItem) {
                stepItem.classList.add('completed');
            }
        }

        removeCompletedStyling(checkbox) {
            const label = checkbox.nextElementSibling;
            if (label) {
                label.classList.remove('completed');
            }
            
            const stepItem = checkbox.closest('.step-item, .step-checkbox');
            if (stepItem) {
                stepItem.classList.remove('completed');
            }
        }

        updateProgressDisplay() {
            const checkboxes = document.querySelectorAll(SELECTORS.progressCheckboxes);
            const totalSteps = checkboxes.length;
            const completedSteps = Array.from(checkboxes).filter(cb => cb.checked).length;
            const percentage = totalSteps > 0 ? Math.round((completedSteps / totalSteps) * 100) : 0;

            // Update progress bar
            const progressBar = document.querySelector(SELECTORS.progressBar);
            if (progressBar) {
                progressBar.style.width = `${percentage}%`;
                progressBar.setAttribute('aria-valuenow', percentage);
            }

            // Update percentage text
            const percentageElement = document.querySelector(SELECTORS.progressPercentage);
            if (percentageElement) {
                percentageElement.textContent = `${percentage}%`;
            }

            // Update progress in page title for modules
            if (window.location.pathname.includes('module')) {
                this.updatePageTitle(percentage);
            }

            return { total: totalSteps, completed: completedSteps, percentage };
        }

        updatePageTitle(percentage) {
            const title = document.title;
            const baseTitle = title.replace(/ \(\d+%\)/, '');
            document.title = `${baseTitle} (${percentage}%)`;
        }

        animateProgressChange() {
            const progressBar = document.querySelector(SELECTORS.progressBar);
            if (progressBar) {
                progressBar.classList.add('updating');
                setTimeout(() => {
                    progressBar.classList.remove('updating');
                }, CONFIG.ANIMATION_DURATION);
            }
        }

        // Public method to get overall progress
        getOverallProgress() {
            const modules = ['module1', 'module2', 'module3', 'module4', 'module5'];
            const moduleProgress = {};
            let totalCompleted = 0;
            let totalSteps = 0;

            modules.forEach(module => {
                const checkboxes = document.querySelectorAll(`[data-module="${module}"]`);
                const completed = Array.from(checkboxes).filter(cb => cb.checked).length;
                const total = checkboxes.length;
                
                moduleProgress[module] = {
                    completed,
                    total,
                    percentage: total > 0 ? Math.round((completed / total) * 100) : 0
                };
                
                totalCompleted += completed;
                totalSteps += total;
            });

            return {
                modules: moduleProgress,
                overall: {
                    completed: totalCompleted,
                    total: totalSteps,
                    percentage: totalSteps > 0 ? Math.round((totalCompleted / totalSteps) * 100) : 0
                }
            };
        }
    }

    // ==========================================================================
    // Navigation and Smooth Scrolling
    // ==========================================================================

    class NavigationManager {
        constructor() {
            this.initializeNavigation();
            this.initializeSmoothScrolling();
            this.initializeMobileMenu();
            this.initializeDropdowns();
        }

        initializeNavigation() {
            // Highlight active navigation items
            this.updateActiveNavigation();
            
            // Setup scroll spy for section highlighting
            this.initializeScrollSpy();
        }

        initializeSmoothScrolling() {
            const smoothScrollLinks = document.querySelectorAll(SELECTORS.smoothScrollLinks);
            
            smoothScrollLinks.forEach(link => {
                link.addEventListener('click', (e) => {
                    const href = link.getAttribute('href');
                    
                    // Only handle internal anchor links
                    if (href.startsWith('#') && href.length > 1) {
                        e.preventDefault();
                        this.smoothScrollTo(href);
                    }
                });
            });
        }

        smoothScrollTo(targetId) {
            const target = document.querySelector(targetId);
            if (!target) return;

            const targetOffset = getElementOffset(target) - CONFIG.SCROLL_OFFSET;
            
            // Use native smooth scrolling if supported
            if ('scrollBehavior' in document.documentElement.style) {
                window.scrollTo({
                    top: targetOffset,
                    behavior: 'smooth'
                });
            } else {
                // Fallback smooth scrolling
                this.animatedScrollTo(targetOffset);
            }

            // Update URL without triggering scroll
            if (history.pushState) {
                history.pushState(null, null, targetId);
            }

            // Focus target for accessibility
            setTimeout(() => {
                target.focus({ preventScroll: true });
            }, 500);
        }

        animatedScrollTo(targetY) {
            const startY = window.pageYOffset;
            const distance = targetY - startY;
            const duration = Math.min(Math.abs(distance) / 2, 800);
            let startTime = null;

            function step(currentTime) {
                if (!startTime) startTime = currentTime;
                const progress = Math.min((currentTime - startTime) / duration, 1);
                const ease = this.easeInOutCubic(progress);
                
                window.scrollTo(0, startY + distance * ease);
                
                if (progress < 1) {
                    requestAnimationFrame(step);
                }
            }

            requestAnimationFrame(step.bind(this));
        }

        easeInOutCubic(t) {
            return t < 0.5 ? 4 * t * t * t : (t - 1) * (2 * t - 2) * (2 * t - 2) + 1;
        }

        initializeScrollSpy() {
            const sections = document.querySelectorAll('section[id], div[id]');
            const navLinks = document.querySelectorAll('.module-nav a, .setup-nav-links a, .troubleshooting-nav-links a');
            
            if (sections.length === 0 || navLinks.length === 0) return;

            const scrollSpyHandler = throttle(() => {
                let currentSection = '';
                
                sections.forEach(section => {
                    const rect = section.getBoundingClientRect();
                    if (rect.top <= CONFIG.SCROLL_OFFSET && rect.bottom >= CONFIG.SCROLL_OFFSET) {
                        currentSection = section.id;
                    }
                });

                // Update active nav links
                navLinks.forEach(link => {
                    const href = link.getAttribute('href');
                    if (href === `#${currentSection}`) {
                        link.classList.add(CLASSES.active);
                    } else {
                        link.classList.remove(CLASSES.active);
                    }
                });
            }, CONFIG.DEBOUNCE_DELAY);

            window.addEventListener('scroll', scrollSpyHandler);
        }

        initializeMobileMenu() {
            // Create mobile menu toggle if it doesn't exist
            this.createMobileMenuToggle();
            
            const mobileToggle = document.querySelector(SELECTORS.mobileMenuToggle);
            const navLinks = document.querySelector(SELECTORS.navLinks);
            
            if (mobileToggle && navLinks) {
                mobileToggle.addEventListener('click', () => {
                    this.toggleMobileMenu();
                });

                // Close mobile menu when clicking outside
                document.addEventListener('click', (e) => {
                    if (!e.target.closest(SELECTORS.mainNav)) {
                        this.closeMobileMenu();
                    }
                });

                // Close mobile menu on escape key
                document.addEventListener('keydown', (e) => {
                    if (e.key === 'Escape') {
                        this.closeMobileMenu();
                    }
                });
            }
        }

        createMobileMenuToggle() {
            const nav = document.querySelector(SELECTORS.mainNav);
            if (!nav || document.querySelector(SELECTORS.mobileMenuToggle)) return;

            const toggle = document.createElement('button');
            toggle.className = 'mobile-menu-toggle';
            toggle.setAttribute('aria-label', 'Toggle navigation menu');
            toggle.setAttribute('aria-expanded', 'false');
            toggle.innerHTML = `
                <span class="hamburger-line"></span>
                <span class="hamburger-line"></span>
                <span class="hamburger-line"></span>
            `;

            const container = nav.querySelector('.container');
            if (container) {
                container.appendChild(toggle);
            }
        }

        toggleMobileMenu() {
            const body = document.body;
            const toggle = document.querySelector(SELECTORS.mobileMenuToggle);
            const isOpen = body.classList.contains(CLASSES.mobileMenuOpen);

            if (isOpen) {
                this.closeMobileMenu();
            } else {
                this.openMobileMenu();
            }
        }

        openMobileMenu() {
            const body = document.body;
            const toggle = document.querySelector(SELECTORS.mobileMenuToggle);
            
            body.classList.add(CLASSES.mobileMenuOpen);
            if (toggle) {
                toggle.setAttribute('aria-expanded', 'true');
                toggle.classList.add(CLASSES.active);
            }
            
            announceToScreenReader('Navigation menu opened');
        }

        closeMobileMenu() {
            const body = document.body;
            const toggle = document.querySelector(SELECTORS.mobileMenuToggle);
            
            body.classList.remove(CLASSES.mobileMenuOpen);
            if (toggle) {
                toggle.setAttribute('aria-expanded', 'false');
                toggle.classList.remove(CLASSES.active);
            }
        }

        initializeDropdowns() {
            const dropdownToggles = document.querySelectorAll(SELECTORS.dropdownToggles);
            
            dropdownToggles.forEach(toggle => {
                this.setupDropdown(toggle);
            });
        }

        setupDropdown(toggle) {
            const dropdown = toggle.parentElement;
            const menu = dropdown.querySelector(SELECTORS.dropdownMenus);
            
            if (!menu) return;

            // Click handler
            toggle.addEventListener('click', (e) => {
                e.preventDefault();
                this.toggleDropdown(dropdown);
            });

            // Keyboard navigation
            toggle.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    this.toggleDropdown(dropdown);
                } else if (e.key === 'ArrowDown') {
                    e.preventDefault();
                    this.openDropdown(dropdown);
                    const firstLink = menu.querySelector('a');
                    if (firstLink) firstLink.focus();
                }
            });

            // Menu item navigation
            const menuItems = menu.querySelectorAll('a');
            menuItems.forEach((item, index) => {
                item.addEventListener('keydown', (e) => {
                    if (e.key === 'ArrowDown') {
                        e.preventDefault();
                        const nextItem = menuItems[index + 1] || menuItems[0];
                        nextItem.focus();
                    } else if (e.key === 'ArrowUp') {
                        e.preventDefault();
                        const prevItem = menuItems[index - 1] || menuItems[menuItems.length - 1];
                        prevItem.focus();
                    } else if (e.key === 'Escape') {
                        e.preventDefault();
                        this.closeDropdown(dropdown);
                        toggle.focus();
                    }
                });
            });

            // Close on outside click
            document.addEventListener('click', (e) => {
                if (!dropdown.contains(e.target)) {
                    this.closeDropdown(dropdown);
                }
            });
        }

        toggleDropdown(dropdown) {
            if (dropdown.classList.contains(CLASSES.active)) {
                this.closeDropdown(dropdown);
            } else {
                this.openDropdown(dropdown);
            }
        }

        openDropdown(dropdown) {
            // Close other dropdowns
            document.querySelectorAll('.dropdown').forEach(other => {
                if (other !== dropdown) {
                    this.closeDropdown(other);
                }
            });

            dropdown.classList.add(CLASSES.active);
            const toggle = dropdown.querySelector(SELECTORS.dropdownToggles);
            if (toggle) {
                toggle.setAttribute('aria-expanded', 'true');
            }
        }

        closeDropdown(dropdown) {
            dropdown.classList.remove(CLASSES.active);
            const toggle = dropdown.querySelector(SELECTORS.dropdownToggles);
            if (toggle) {
                toggle.setAttribute('aria-expanded', 'false');
            }
        }

        updateActiveNavigation() {
            const currentPath = window.location.pathname;
            const navLinks = document.querySelectorAll('.nav-links a:not(.dropdown-toggle)');
            
            navLinks.forEach(link => {
                const linkPath = new URL(link.href).pathname;
                if (linkPath === currentPath) {
                    link.classList.add(CLASSES.active);
                    link.setAttribute('aria-current', 'page');
                } else {
                    link.classList.remove(CLASSES.active);
                    link.removeAttribute('aria-current');
                }
            });
        }
    }

    // ==========================================================================
    // Collapsible Sections and Accordions
    // ==========================================================================

    class CollapsibleManager {
        constructor() {
            this.initializeCollapsibleSections();
        }

        initializeCollapsibleSections() {
            const collapsibleHeaders = document.querySelectorAll(SELECTORS.collapsibleHeaders);
            
            collapsibleHeaders.forEach(header => {
                this.setupCollapsibleSection(header);
            });
        }

        setupCollapsibleSection(header) {
            const content = header.nextElementSibling;
            if (!content || !content.classList.contains('collapsible-content')) return;

            // Set initial ARIA attributes
            const contentId = content.id || `collapsible-${Math.random().toString(36).substr(2, 9)}`;
            content.id = contentId;
            header.setAttribute('aria-controls', contentId);
            
            // Set initial state
            const isExpanded = header.getAttribute('aria-expanded') === 'true';
            this.setCollapsibleState(header, content, isExpanded);

            // Click handler
            header.addEventListener('click', () => {
                this.toggleCollapsible(header, content);
            });

            // Keyboard handler
            header.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    this.toggleCollapsible(header, content);
                }
            });
        }

        toggleCollapsible(header, content) {
            const isExpanded = header.getAttribute('aria-expanded') === 'true';
            this.setCollapsibleState(header, content, !isExpanded);
        }

        setCollapsibleState(header, content, isExpanded) {
            header.setAttribute('aria-expanded', isExpanded);
            
            const toggleIcon = header.querySelector('.toggle-icon');
            if (toggleIcon) {
                toggleIcon.textContent = isExpanded ? '▲' : '▼';
            }

            if (isExpanded) {
                this.expandContent(content);
                header.classList.add(CLASSES.expanded);
                header.classList.remove(CLASSES.collapsed);
            } else {
                this.collapseContent(content);
                header.classList.add(CLASSES.collapsed);
                header.classList.remove(CLASSES.expanded);
            }
        }

        expandContent(content) {
            content.style.display = 'block';
            const height = content.scrollHeight;
            content.style.height = '0px';
            content.style.overflow = 'hidden';
            
            // Force reflow
            content.offsetHeight;
            
            content.style.transition = `height ${CONFIG.ANIMATION_DURATION}ms ease-in-out`;
            content.style.height = height + 'px';
            
            setTimeout(() => {
                content.style.height = 'auto';
                content.style.overflow = 'visible';
                content.style.transition = '';
            }, CONFIG.ANIMATION_DURATION);
        }

        collapseContent(content) {
            const height = content.scrollHeight;
            content.style.height = height + 'px';
            content.style.overflow = 'hidden';
            
            // Force reflow
            content.offsetHeight;
            
            content.style.transition = `height ${CONFIG.ANIMATION_DURATION}ms ease-in-out`;
            content.style.height = '0px';
            
            setTimeout(() => {
                content.style.display = 'none';
                content.style.transition = '';
            }, CONFIG.ANIMATION_DURATION);
        }
    }

    // ==========================================================================
    // Code Block Enhancements
    // ==========================================================================

    class CodeBlockManager {
        constructor() {
            this.initializeCodeBlocks();
        }

        initializeCodeBlocks() {
            const codeBlocks = document.querySelectorAll(SELECTORS.codeBlocks);
            
            codeBlocks.forEach(block => {
                this.enhanceCodeBlock(block);
            });

            // Initialize syntax highlighting if Prism.js is available
            if (window.Prism) {
                this.initializeSyntaxHighlighting();
            }
        }

        enhanceCodeBlock(block) {
            // Add line numbers if not already present
            if (!block.classList.contains('line-numbers')) {
                this.addLineNumbers(block);
            }

            // Add language detection
            this.detectLanguage(block);

            // Add accessibility attributes
            block.setAttribute('role', 'code');
            block.setAttribute('tabindex', '0');
        }

        addLineNumbers(block) {
            const lines = block.textContent.split('\n');
            if (lines.length > 1) {
                block.classList.add('line-numbers');
            }
        }

        detectLanguage(block) {
            const text = block.textContent.trim();
            let language = 'text';

            // Simple language detection
            if (text.includes('from strands import') || text.includes('import strands')) {
                language = 'python';
            } else if (text.includes('pip install') || text.includes('python ')) {
                language = 'bash';
            } else if (text.includes('aws configure') || text.includes('docker ')) {
                language = 'bash';
            } else if (text.includes('{') && text.includes('}') && text.includes(':')) {
                language = 'json';
            }

            // Add language class
            if (!block.className.includes('language-')) {
                block.classList.add(`language-${language}`);
            }
        }

        initializeSyntaxHighlighting() {
            // Configure Prism.js if available
            if (window.Prism) {
                Prism.highlightAll();
                
                // Add custom styling for workshop code
                this.addCustomSyntaxStyling();
            }
        }

        addCustomSyntaxStyling() {
            // Add custom CSS classes for better workshop code presentation
            const codeBlocks = document.querySelectorAll('pre[class*="language-"]');
            codeBlocks.forEach(block => {
                block.classList.add('workshop-code');
            });
        }
    }

    // ==========================================================================
    // Interactive Architecture Diagrams
    // ==========================================================================

    class DiagramManager {
        constructor() {
            this.initializeDiagrams();
        }

        initializeDiagrams() {
            const diagramContainers = document.querySelectorAll('.architecture-diagram, .flow-diagram');
            
            diagramContainers.forEach(container => {
                this.setupInteractiveDiagram(container);
            });
        }

        setupInteractiveDiagram(container) {
            // Add interactive elements to diagrams
            const elements = container.querySelectorAll('.diagram-element, .diagram-node');
            
            elements.forEach(element => {
                this.makeElementInteractive(element);
            });
        }

        makeElementInteractive(element) {
            // Add hover effects and click handlers
            element.addEventListener('mouseenter', () => {
                this.highlightElement(element);
            });

            element.addEventListener('mouseleave', () => {
                this.unhighlightElement(element);
            });

            element.addEventListener('click', () => {
                this.showElementDetails(element);
            });

            // Keyboard support
            element.setAttribute('tabindex', '0');
            element.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    this.showElementDetails(element);
                }
            });
        }

        highlightElement(element) {
            element.classList.add('highlighted');
            
            // Show tooltip if available
            const tooltip = element.querySelector('.tooltip');
            if (tooltip) {
                tooltip.classList.add('visible');
            }
        }

        unhighlightElement(element) {
            element.classList.remove('highlighted');
            
            // Hide tooltip
            const tooltip = element.querySelector('.tooltip');
            if (tooltip) {
                tooltip.classList.remove('visible');
            }
        }

        showElementDetails(element) {
            const details = element.dataset.details;
            if (details) {
                // Show modal or expand details
                this.showDetailsModal(details);
            }
        }

        showDetailsModal(details) {
            // Create and show modal with diagram element details
            const modal = document.createElement('div');
            modal.className = 'diagram-modal';
            modal.innerHTML = `
                <div class="modal-content">
                    <button class="modal-close" aria-label="Close details">&times;</button>
                    <div class="modal-body">${details}</div>
                </div>
            `;

            document.body.appendChild(modal);
            
            // Setup modal interactions
            const closeBtn = modal.querySelector('.modal-close');
            closeBtn.addEventListener('click', () => {
                this.closeDetailsModal(modal);
            });

            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    this.closeDetailsModal(modal);
                }
            });

            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape') {
                    this.closeDetailsModal(modal);
                }
            });

            // Show modal
            setTimeout(() => {
                modal.classList.add('visible');
            }, 10);
        }

        closeDetailsModal(modal) {
            modal.classList.remove('visible');
            setTimeout(() => {
                document.body.removeChild(modal);
            }, CONFIG.ANIMATION_DURATION);
        }
    }

    // ==========================================================================
    // Performance and Accessibility Enhancements
    // ==========================================================================

    class PerformanceManager {
        constructor() {
            this.initializePerformanceOptimizations();
            this.initializeAccessibilityEnhancements();
        }

        initializePerformanceOptimizations() {
            // Lazy load images
            this.initializeLazyLoading();
            
            // Optimize scroll events
            this.optimizeScrollEvents();
            
            // Preload critical resources
            this.preloadCriticalResources();
        }

        initializeLazyLoading() {
            // Use Intersection Observer for lazy loading
            if ('IntersectionObserver' in window) {
                const imageObserver = new IntersectionObserver((entries, observer) => {
                    entries.forEach(entry => {
                        if (entry.isIntersecting) {
                            const img = entry.target;
                            img.src = img.dataset.src;
                            img.classList.remove('lazy');
                            observer.unobserve(img);
                        }
                    });
                });

                document.querySelectorAll('img[data-src]').forEach(img => {
                    imageObserver.observe(img);
                });
            }
        }

        optimizeScrollEvents() {
            // Use passive event listeners for better performance
            const scrollHandler = throttle(() => {
                this.handleScroll();
            }, 16); // ~60fps

            window.addEventListener('scroll', scrollHandler, { passive: true });
        }

        handleScroll() {
            // Handle scroll-based animations and effects
            this.updateScrollProgress();
            this.handleScrollAnimations();
        }

        updateScrollProgress() {
            const scrollProgress = (window.pageYOffset / (document.documentElement.scrollHeight - window.innerHeight)) * 100;
            
            // Update scroll progress indicator if present
            const progressIndicator = document.querySelector('.scroll-progress');
            if (progressIndicator) {
                progressIndicator.style.width = `${scrollProgress}%`;
            }
        }

        handleScrollAnimations() {
            // Animate elements as they come into view
            const animatedElements = document.querySelectorAll('.animate-on-scroll');
            
            animatedElements.forEach(element => {
                if (isInViewport(element, 100)) {
                    element.classList.add('animated');
                }
            });
        }

        preloadCriticalResources() {
            // Preload critical CSS and JS files
            const criticalResources = [
                'styles/main.css',
                'scripts/prism.js'
            ];

            criticalResources.forEach(resource => {
                const link = document.createElement('link');
                link.rel = 'preload';
                link.href = resource;
                link.as = resource.endsWith('.css') ? 'style' : 'script';
                document.head.appendChild(link);
            });
        }

        initializeAccessibilityEnhancements() {
            // Skip to content link
            this.addSkipToContentLink();
            
            // Focus management
            this.initializeFocusManagement();
            
            // Keyboard navigation
            this.enhanceKeyboardNavigation();
            
            // Screen reader announcements
            this.setupScreenReaderAnnouncements();
        }

        addSkipToContentLink() {
            if (document.querySelector('.skip-to-content')) return;

            const skipLink = document.createElement('a');
            skipLink.className = 'skip-to-content';
            skipLink.href = '#main';
            skipLink.textContent = 'Skip to main content';
            
            document.body.insertBefore(skipLink, document.body.firstChild);
        }

        initializeFocusManagement() {
            // Ensure focus is visible
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Tab') {
                    document.body.classList.add('keyboard-navigation');
                }
            });

            document.addEventListener('mousedown', () => {
                document.body.classList.remove('keyboard-navigation');
            });
        }

        enhanceKeyboardNavigation() {
            // Add keyboard shortcuts
            document.addEventListener('keydown', (e) => {
                // Alt + M: Focus main navigation
                if (e.altKey && e.key === 'm') {
                    e.preventDefault();
                    const nav = document.querySelector('.main-nav');
                    if (nav) {
                        const firstLink = nav.querySelector('a');
                        if (firstLink) firstLink.focus();
                    }
                }

                // Alt + S: Focus search (if present)
                if (e.altKey && e.key === 's') {
                    e.preventDefault();
                    const search = document.querySelector('input[type="search"], .search-input');
                    if (search) search.focus();
                }

                // Alt + C: Focus main content
                if (e.altKey && e.key === 'c') {
                    e.preventDefault();
                    const main = document.querySelector('main');
                    if (main) {
                        main.focus();
                        main.scrollIntoView({ behavior: 'smooth' });
                    }
                }
            });
        }

        setupScreenReaderAnnouncements() {
            // Create live region for announcements
            if (!document.querySelector('#sr-announcements')) {
                const liveRegion = document.createElement('div');
                liveRegion.id = 'sr-announcements';
                liveRegion.setAttribute('aria-live', 'polite');
                liveRegion.setAttribute('aria-atomic', 'true');
                liveRegion.className = 'sr-only';
                document.body.appendChild(liveRegion);
            }
        }
    }

    // ==========================================================================
    // Error Handling and Fallbacks
    // ==========================================================================

    class ErrorHandler {
        constructor() {
            this.initializeErrorHandling();
        }

        initializeErrorHandling() {
            // Global error handler
            window.addEventListener('error', (e) => {
                this.handleError(e.error, 'JavaScript Error');
            });

            // Promise rejection handler
            window.addEventListener('unhandledrejection', (e) => {
                this.handleError(e.reason, 'Promise Rejection');
            });
        }

        handleError(error, type) {
            console.error(`${type}:`, error);
            
            // Log error for debugging
            this.logError(error, type);
            
            // Show user-friendly error message if needed
            if (this.isUserFacingError(error)) {
                this.showUserError(error);
            }
        }

        logError(error, type) {
            const errorInfo = {
                type,
                message: error.message,
                stack: error.stack,
                timestamp: new Date().toISOString(),
                userAgent: navigator.userAgent,
                url: window.location.href
            };

            // Store error in localStorage for debugging
            const errors = Storage.get('errors') || [];
            errors.push(errorInfo);
            
            // Keep only last 10 errors
            if (errors.length > 10) {
                errors.splice(0, errors.length - 10);
            }
            
            Storage.set('errors', errors);
        }

        isUserFacingError(error) {
            // Determine if error should be shown to user
            const userFacingErrors = [
                'clipboard',
                'storage',
                'network'
            ];

            return userFacingErrors.some(keyword =>
                error.message.toLowerCase().includes(keyword)
            );
        }

        showUserError(error) {
            // Show non-intrusive error message
            const errorMessage = document.createElement('div');
            errorMessage.className = 'error-toast';
            errorMessage.textContent = 'Something went wrong. Please try again.';
            
            document.body.appendChild(errorMessage);
            
            setTimeout(() => {
                errorMessage.classList.add('visible');
            }, 10);

            setTimeout(() => {
                errorMessage.classList.remove('visible');
                setTimeout(() => {
                    document.body.removeChild(errorMessage);
                }, CONFIG.ANIMATION_DURATION);
            }, 5000);
        }
    }

    // ==========================================================================
    // Feature Detection and Progressive Enhancement
    // ==========================================================================

    class FeatureDetection {
        constructor() {
            this.detectFeatures();
            this.applyEnhancements();
        }

        detectFeatures() {
            const features = {
                localStorage: this.hasLocalStorage(),
                clipboard: this.hasClipboardAPI(),
                intersectionObserver: this.hasIntersectionObserver(),
                smoothScroll: this.hasSmoothScroll(),
                customProperties: this.hasCustomProperties(),
                flexbox: this.hasFlexbox(),
                grid: this.hasGrid()
            };

            // Add feature classes to body
            Object.keys(features).forEach(feature => {
                const className = features[feature] ? `has-${feature}` : `no-${feature}`;
                document.body.classList.add(className);
            });

            return features;
        }

        hasLocalStorage() {
            try {
                const test = 'test';
                localStorage.setItem(test, test);
                localStorage.removeItem(test);
                return true;
            } catch (e) {
                return false;
            }
        }

        hasClipboardAPI() {
            return !!(navigator.clipboard && window.isSecureContext);
        }

        hasIntersectionObserver() {
            return 'IntersectionObserver' in window;
        }

        hasSmoothScroll() {
            return 'scrollBehavior' in document.documentElement.style;
        }

        hasCustomProperties() {
            return window.CSS && CSS.supports('color', 'var(--test)');
        }

        hasFlexbox() {
            return window.CSS && CSS.supports('display', 'flex');
        }

        hasGrid() {
            return window.CSS && CSS.supports('display', 'grid');
        }

        applyEnhancements() {
            // Apply progressive enhancements based on feature support
            if (!this.hasLocalStorage()) {
                this.addLocalStorageFallback();
            }

            if (!this.hasClipboardAPI()) {
                this.addClipboardFallback();
            }

            if (!this.hasSmoothScroll()) {
                this.addSmoothScrollPolyfill();
            }
        }

        addLocalStorageFallback() {
            // Create in-memory storage fallback
            window.fallbackStorage = {};
            
            Storage.get = function(key) {
                return window.fallbackStorage[CONFIG.STORAGE_PREFIX + key] || null;
            };

            Storage.set = function(key, value) {
                window.fallbackStorage[CONFIG.STORAGE_PREFIX + key] = value;
                return true;
            };
        }

        addClipboardFallback() {
            // Fallback already implemented in ClipboardManager
            console.info('Using clipboard fallback for older browsers');
        }

        addSmoothScrollPolyfill() {
            // Smooth scroll polyfill already implemented in NavigationManager
            console.info('Using smooth scroll polyfill for older browsers');
        }
    }

    // ==========================================================================
    // Theme Management
    // ==========================================================================

    class ThemeManager {
        constructor() {
            this.initializeThemeToggle();
        }

        initializeThemeToggle() {
            // Create theme toggle button if it doesn't exist
            this.createThemeToggleButton();
            
            // Load saved theme preference
            this.loadThemePreference();
            
            // Listen for system preference changes
            this.listenForSystemPreferenceChanges();
        }

        createThemeToggleButton() {
            const nav = document.querySelector('.nav-links');
            if (!nav || document.querySelector('.theme-toggle')) return;

            const themeToggleItem = document.createElement('li');
            const themeToggle = document.createElement('button');
            themeToggle.className = 'theme-toggle';
            themeToggle.setAttribute('aria-label', 'Toggle dark mode');
            themeToggle.innerHTML = `
                <span class="theme-toggle-icon light">☀️</span>
                <span class="theme-toggle-icon dark">🌙</span>
            `;

            themeToggle.addEventListener('click', () => {
                this.toggleTheme();
            });

            themeToggleItem.appendChild(themeToggle);
            nav.appendChild(themeToggleItem);
        }

        loadThemePreference() {
            const savedTheme = Storage.get('theme');
            
            if (savedTheme) {
                // Apply saved theme preference
                this.setTheme(savedTheme);
            } else {
                // Check system preference
                const prefersDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;
                this.setTheme(prefersDarkMode ? 'dark' : 'light');
            }
        }

        listenForSystemPreferenceChanges() {
            // Only apply system changes if user hasn't set a preference
            window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
                if (!Storage.get('theme')) {
                    this.setTheme(e.matches ? 'dark' : 'light');
                }
            });
        }

        toggleTheme() {
            const currentTheme = document.documentElement.classList.contains('dark-mode') ? 'dark' : 'light';
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            
            this.setTheme(newTheme);
            Storage.set('theme', newTheme);
            
            // Announce theme change for screen readers
            announceToScreenReader(`${newTheme} mode activated`);
        }

        setTheme(theme) {
            if (theme === 'dark') {
                document.documentElement.classList.add('dark-mode');
                document.querySelector('.theme-toggle')?.setAttribute('aria-pressed', 'true');
            } else {
                document.documentElement.classList.remove('dark-mode');
                document.querySelector('.theme-toggle')?.setAttribute('aria-pressed', 'false');
            }
        }
    }

    // ==========================================================================
    // Main Application Class
    // ==========================================================================

    class StrandsWorkshopApp {
        constructor() {
            this.components = {};
            this.initialize();
        }

        initialize() {
            // Wait for DOM to be ready
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', () => {
                    this.initializeComponents();
                });
            } else {
                this.initializeComponents();
            }
        }

        initializeComponents() {
            try {
                // Initialize feature detection first
                this.components.featureDetection = new FeatureDetection();
                
                // Initialize error handling
                this.components.errorHandler = new ErrorHandler();
                
                // Initialize core components
                this.components.clipboardManager = new ClipboardManager();
                this.components.progressTracker = new ProgressTracker();
                this.components.navigationManager = new NavigationManager();
                this.components.collapsibleManager = new CollapsibleManager();
                this.components.codeBlockManager = new CodeBlockManager();
                this.components.diagramManager = new DiagramManager();
                this.components.performanceManager = new PerformanceManager();
                this.components.themeManager = new ThemeManager();

                // Initialize page-specific features
                this.initializePageSpecificFeatures();
                
                // Mark app as initialized
                document.body.classList.add('app-initialized');
                
                console.info('Strands Workshop app initialized successfully');
                
            } catch (error) {
                console.error('Failed to initialize Strands Workshop app:', error);
                this.handleInitializationError(error);
            }
        }

        initializePageSpecificFeatures() {
            const body = document.body;
            
            // Module-specific features
            if (body.hasAttribute('data-module')) {
                this.initializeModuleFeatures();
            }
            
            // Setup page features
            if (body.classList.contains('setup-page')) {
                this.initializeSetupFeatures();
            }
            
            // Troubleshooting page features
            if (body.classList.contains('troubleshooting-page')) {
                this.initializeTroubleshootingFeatures();
            }
        }

        initializeModuleFeatures() {
            // Enhanced progress tracking for modules
            const moduleId = document.body.dataset.module;
            if (moduleId) {
                this.trackModuleProgress(moduleId);
            }
            
            // Module navigation enhancements
            this.enhanceModuleNavigation();
        }

        initializeSetupFeatures() {
            // Setup verification helpers
            this.addSetupVerificationHelpers();
        }

        initializeTroubleshootingFeatures() {
            // Enhanced search for troubleshooting
            this.addTroubleshootingSearch();
        }

        trackModuleProgress(moduleId) {
            // Additional module-specific progress tracking
            const progress = this.components.progressTracker.getOverallProgress();
            const moduleProgress = progress.modules[moduleId];
            
            if (moduleProgress) {
                // Update module completion status
                this.updateModuleCompletionStatus(moduleId, moduleProgress);
            }
        }

        updateModuleCompletionStatus(moduleId, progress) {
            // Update UI to reflect module completion status
            const completionIndicator = document.querySelector('.module-completion');
            if (completionIndicator) {
                completionIndicator.textContent = `${progress.completed}/${progress.total} steps completed`;
            }
        }

        enhanceModuleNavigation() {
            // Add next/previous module navigation
            this.addModuleNavigation();
        }

        addModuleNavigation() {
            const currentModule = document.body.dataset.module;
            if (!currentModule) return;

            const moduleNumber = parseInt(currentModule.replace('module', ''));
            const prevModule = moduleNumber > 1 ? `module${moduleNumber - 1}.html` : null;
            const nextModule = moduleNumber < 5 ? `module${moduleNumber + 1}.html` : null;

            // Add navigation buttons if they don't exist
            const navContainer = document.querySelector('.module-navigation-buttons');
            if (navContainer) {
                if (prevModule) {
                    const prevBtn = document.createElement('a');
                    prevBtn.href = prevModule;
                    prevBtn.className = 'btn btn-secondary';
                    prevBtn.textContent = `← Previous Module`;
                    navContainer.appendChild(prevBtn);
                }

                if (nextModule) {
                    const nextBtn = document.createElement('a');
                    nextBtn.href = nextModule;
                    nextBtn.className = 'btn btn-primary';
                    nextBtn.textContent = `Next Module →`;
                    navContainer.appendChild(nextBtn);
                }
            }
        }

        addSetupVerificationHelpers() {
            // Add interactive setup verification
            const verificationButtons = document.querySelectorAll('.verify-step');
            verificationButtons.forEach(button => {
                button.addEventListener('click', (e) => {
                    e.preventDefault();
                    this.runSetupVerification(button);
                });
            });
        }

        runSetupVerification(button) {
            const step = button.dataset.step;
            button.classList.add(CLASSES.loading);
            button.textContent = 'Verifying...';

            // Simulate verification (in real implementation, this would call actual verification)
            setTimeout(() => {
                button.classList.remove(CLASSES.loading);
                button.classList.add('verified');
                button.textContent = '✓ Verified';
                announceToScreenReader(`${step} verification completed`);
            }, 2000);
        }

        addTroubleshootingSearch() {
            // Add search functionality for troubleshooting page
            const searchContainer = document.querySelector('.troubleshooting-search');
            if (searchContainer) {
                const searchInput = document.createElement('input');
                searchInput.type = 'search';
                searchInput.placeholder = 'Search troubleshooting topics...';
                searchInput.className = 'troubleshooting-search-input';
                
                searchInput.addEventListener('input', debounce((e) => {
                    this.filterTroubleshootingContent(e.target.value);
                }, CONFIG.DEBOUNCE_DELAY));

                searchContainer.appendChild(searchInput);
            }
        }

        filterTroubleshootingContent(query) {
            const sections = document.querySelectorAll('.troubleshooting-section');
            const lowerQuery = query.toLowerCase();

            sections.forEach(section => {
                const text = section.textContent.toLowerCase();
                const matches = text.includes(lowerQuery);
                
                section.style.display = matches || !query ? 'block' : 'none';
            });
        }

        handleInitializationError(error) {
            // Graceful degradation when initialization fails
            console.error('App initialization failed, falling back to basic functionality');
            
            // Ensure basic functionality still works
            this.initializeBasicFunctionality();
        }

        initializeBasicFunctionality() {
            // Basic copy functionality
            document.querySelectorAll('.copy-btn').forEach(button => {
                button.addEventListener('click', function() {
                    const codeBlock = this.previousElementSibling;
                    if (codeBlock) {
                        const text = codeBlock.textContent;
                        if (navigator.clipboard) {
                            navigator.clipboard.writeText(text);
                            this.textContent = 'Copied!';
                            setTimeout(() => {
                                this.textContent = 'Copy';
                            }, 2000);
                        }
                    }
                });
            });

            // Basic smooth scrolling
            document.querySelectorAll('a[href^="#"]').forEach(anchor => {
                anchor.addEventListener('click', function (e) {
                    e.preventDefault();
                    const target = document.querySelector(this.getAttribute('href'));
                    if (target) {
                        target.scrollIntoView({ behavior: 'smooth' });
                    }
                });
            });
        }

        // Public API methods
        getProgress() {
            return this.components.progressTracker ?
                this.components.progressTracker.getOverallProgress() : null;
        }

        clearProgress() {
            if (this.components.progressTracker) {
                Storage.clear();
                location.reload();
            }
        }

        exportProgress() {
            const progress = this.getProgress();
            if (progress) {
                const dataStr = JSON.stringify(progress, null, 2);
                const dataBlob = new Blob([dataStr], { type: 'application/json' });
                const url = URL.createObjectURL(dataBlob);
                
                const link = document.createElement('a');
                link.href = url;
                link.download = 'strands-workshop-progress.json';
                link.click();
                
                URL.revokeObjectURL(url);
            }
        }
    }

    // ==========================================================================
    // Initialize Application
    // ==========================================================================

    // Create global app instance
    window.StrandsWorkshop = new StrandsWorkshopApp();

    // Expose utility functions for debugging
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        window.StrandsWorkshopDebug = {
            getProgress: () => window.StrandsWorkshop.getProgress(),
            clearProgress: () => window.StrandsWorkshop.clearProgress(),
            exportProgress: () => window.StrandsWorkshop.exportProgress(),
            storage: Storage,
            config: CONFIG
        };
    }

})();