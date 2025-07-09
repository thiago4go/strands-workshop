# Strands Workshop JavaScript Documentation

This document describes the comprehensive JavaScript functionality implemented for the AWS Strands Workshop website.

## Overview

The main JavaScript file (`main.js`) provides a complete interactive experience for the workshop website, including:

- **Copy-to-clipboard functionality** with visual feedback
- **Progress tracking system** using localStorage
- **Smooth scrolling navigation** with scroll spy
- **Mobile menu functionality** with hamburger toggle
- **Collapsible sections** and accordions
- **Interactive architecture diagrams** (prepared for future implementation)
- **Accessibility enhancements** and keyboard navigation
- **Performance optimizations** and lazy loading
- **Error handling** and graceful degradation

## Features

### 1. Copy-to-Clipboard (`ClipboardManager`)

Enhanced copy functionality for code blocks with:
- Visual feedback (success/error states)
- Fallback for older browsers
- Screen reader announcements
- Keyboard support

**Usage**: Automatically applied to all `.copy-btn` elements.

### 2. Progress Tracking (`ProgressTracker`)

Persistent progress tracking across sessions:
- Checkbox state persistence in localStorage
- Visual progress indicators
- Module-specific progress calculation
- Progress export functionality

**Usage**: Automatically applied to all `.progress-checkbox` elements with `data-module` and `data-step` attributes.

### 3. Navigation (`NavigationManager`)

Comprehensive navigation enhancements:
- Smooth scrolling to anchor links
- Active section highlighting (scroll spy)
- Mobile menu with hamburger toggle
- Dropdown menu keyboard navigation
- Focus management

**Usage**: Automatically applied to navigation elements.

### 4. Collapsible Sections (`CollapsibleManager`)

Interactive collapsible content:
- Smooth expand/collapse animations
- Keyboard accessibility
- ARIA attributes management
- Visual state indicators

**Usage**: Applied to elements with `.collapsible-header` and `.collapsible-content` classes.

### 5. Code Block Enhancements (`CodeBlockManager`)

Enhanced code presentation:
- Syntax highlighting integration (Prism.js)
- Language detection
- Line numbers
- Accessibility attributes

**Usage**: Automatically applied to all `pre code` elements.

### 6. Performance Optimizations (`PerformanceManager`)

Performance and accessibility features:
- Lazy loading with Intersection Observer
- Debounced scroll events
- Skip-to-content links
- Keyboard navigation shortcuts
- Screen reader support

### 7. Error Handling (`ErrorHandler`)

Robust error management:
- Global error catching
- User-friendly error messages
- Error logging for debugging
- Graceful degradation

### 8. Feature Detection (`FeatureDetection`)

Progressive enhancement:
- Feature detection for modern APIs
- Fallbacks for older browsers
- CSS class application based on support
- Polyfills where needed

## API Reference

### Global Object: `window.StrandsWorkshop`

The main application instance with the following methods:

#### `getProgress()`
Returns the current progress state for all modules.

```javascript
const progress = window.StrandsWorkshop.getProgress();
console.log(progress.overall.percentage); // Overall completion percentage
```

#### `clearProgress()`
Clears all saved progress and reloads the page.

```javascript
window.StrandsWorkshop.clearProgress();
```

#### `exportProgress()`
Downloads progress data as a JSON file.

```javascript
window.StrandsWorkshop.exportProgress();
```

### Debug Object: `window.StrandsWorkshopDebug` (localhost only)

Available debugging utilities when running on localhost:

```javascript
// Get current progress
window.StrandsWorkshopDebug.getProgress();

// Clear all progress
window.StrandsWorkshopDebug.clearProgress();

// Export progress
window.StrandsWorkshopDebug.exportProgress();

// Access storage utilities
window.StrandsWorkshopDebug.storage.get('key');
window.StrandsWorkshopDebug.storage.set('key', 'value');

// View configuration
console.log(window.StrandsWorkshopDebug.config);
```

## Configuration

The application uses a centralized configuration object:

```javascript
const CONFIG = {
    STORAGE_PREFIX: 'strands-workshop-',
    ANIMATION_DURATION: 300,
    SCROLL_OFFSET: 80,
    DEBOUNCE_DELAY: 100,
    COPY_FEEDBACK_DURATION: 2000,
    MOBILE_BREAKPOINT: 768
};
```

## Browser Support

- **Modern browsers**: Full functionality with all features
- **Older browsers**: Graceful degradation with fallbacks
- **No JavaScript**: Basic functionality remains available

### Feature Support:
- **localStorage**: Required for progress tracking (fallback to memory storage)
- **Clipboard API**: Enhanced copy functionality (fallback to execCommand)
- **Intersection Observer**: Lazy loading and scroll animations
- **CSS Custom Properties**: Enhanced styling
- **Flexbox/Grid**: Layout enhancements

## Accessibility Features

- **Keyboard Navigation**: Full keyboard support for all interactive elements
- **Screen Reader Support**: ARIA attributes and live announcements
- **Focus Management**: Visible focus indicators and logical tab order
- **High Contrast**: Support for high contrast mode
- **Reduced Motion**: Respects user's motion preferences
- **Skip Links**: Skip-to-content functionality

## Performance Features

- **Lazy Loading**: Images and heavy content loaded on demand
- **Debounced Events**: Optimized scroll and resize handlers
- **Passive Listeners**: Better scroll performance
- **Resource Preloading**: Critical resources loaded early
- **Efficient DOM Queries**: Cached selectors and minimal DOM manipulation

## Integration

### HTML Requirements

Include the JavaScript files in your HTML:

```html
<!-- Prism.js for syntax highlighting -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-core.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-bash.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-json.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-yaml.min.js"></script>

<!-- Main JavaScript functionality -->
<script src="scripts/main.js"></script>
```

### CSS Requirements

The corresponding CSS classes are defined in `styles/main.css` and are automatically applied by the JavaScript.

## Customization

### Adding New Progress Steps

```html
<div class="step-checkbox">
    <input type="checkbox" id="custom-step" class="progress-checkbox" 
           data-module="module1" data-step="custom">
    <label for="custom-step">Custom step description</label>
</div>
```

### Adding Collapsible Sections

```html
<div class="collapsible-section">
    <div class="collapsible-header" role="button" tabindex="0" 
         aria-expanded="false" aria-controls="custom-content">
        <h3>Section Title</h3>
        <span class="toggle-icon">▼</span>
    </div>
    <div class="collapsible-content" id="custom-content">
        <p>Collapsible content here...</p>
    </div>
</div>
```

### Adding Copy Buttons

```html
<div class="code-block">
    <pre><code>Your code here</code></pre>
    <button class="copy-btn">Copy</button>
</div>
```

## Troubleshooting

### Common Issues

1. **Progress not saving**: Check localStorage availability and browser settings
2. **Copy not working**: Verify HTTPS context for Clipboard API
3. **Smooth scrolling not working**: Browser may not support CSS scroll-behavior
4. **Mobile menu not appearing**: Check CSS media queries and viewport meta tag

### Debug Mode

Enable debug logging by setting:

```javascript
localStorage.setItem('strands-workshop-debug', 'true');
```

Then reload the page to see detailed console logs.

## Future Enhancements

The codebase is prepared for:
- Interactive architecture diagrams
- Advanced search functionality
- Real-time collaboration features
- Offline support with Service Workers
- Advanced analytics and tracking