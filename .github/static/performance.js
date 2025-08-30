// Performance monitoring utilities
(function() {
  'use strict';

  // Core Web Vitals monitoring
  function observeWebVitals() {
    // Only measure in production
    if (location.hostname === 'localhost' || location.hostname === '127.0.0.1') {
      return;
    }

    // Largest Contentful Paint (LCP)
    if ('PerformanceObserver' in window) {
      const lcpObserver = new PerformanceObserver((entryList) => {
        const entries = entryList.getEntries();
        const lastEntry = entries[entries.length - 1];
        console.log('LCP:', lastEntry.startTime);
      });
      try {
        lcpObserver.observe({ entryTypes: ['largest-contentful-paint'] });
      } catch (e) {
        // Fallback for older browsers
      }

      // First Input Delay (FID)
      const fidObserver = new PerformanceObserver((entryList) => {
        const entries = entryList.getEntries();
        entries.forEach((entry) => {
          console.log('FID:', entry.processingStart - entry.startTime);
        });
      });
      try {
        fidObserver.observe({ entryTypes: ['first-input'] });
      } catch (e) {
        // Fallback for older browsers
      }

      // Cumulative Layout Shift (CLS)
      let clsValue = 0;
      const clsObserver = new PerformanceObserver((entryList) => {
        const entries = entryList.getEntries();
        entries.forEach((entry) => {
          if (!entry.hadRecentInput) {
            clsValue += entry.value;
          }
        });
        console.log('CLS:', clsValue);
      });
      try {
        clsObserver.observe({ entryTypes: ['layout-shift'] });
      } catch (e) {
        // Fallback for older browsers
      }
    }
  }

  // Memory usage monitoring
  function monitorMemoryUsage() {
    if ('memory' in performance) {
      const memory = performance.memory;
      console.log('Memory Usage:', {
        used: Math.round(memory.usedJSHeapSize / 1024 / 1024) + ' MB',
        total: Math.round(memory.totalJSHeapSize / 1024 / 1024) + ' MB',
        limit: Math.round(memory.jsHeapSizeLimit / 1024 / 1024) + ' MB'
      });
    }
  }

  // Resource loading performance
  function analyzeResourcePerformance() {
    if ('getEntriesByType' in performance) {
      const resources = performance.getEntriesByType('resource');
      const criticalResources = resources.filter(resource => 
        resource.name.includes('style.css') || 
        resource.name.includes('main.js') ||
        resource.name.includes('MathJax') ||
        resource.name.includes('mermaid')
      );

      criticalResources.forEach(resource => {
        console.log(`${resource.name.split('/').pop()}: ${Math.round(resource.duration)}ms`);
      });
    }
  }

  // Initialize monitoring
  function initPerformanceMonitoring() {
    // Wait for page load to complete
    window.addEventListener('load', () => {
      setTimeout(() => {
        observeWebVitals();
        monitorMemoryUsage();
        analyzeResourcePerformance();
      }, 1000);
    });
  }

  // Auto-initialize in development mode
  if (location.hostname === 'localhost' || location.hostname === '127.0.0.1' || location.search.includes('debug=true')) {
    initPerformanceMonitoring();
  }

  // Export for manual use
  window.performanceMonitor = {
    init: initPerformanceMonitoring,
    memory: monitorMemoryUsage,
    resources: analyzeResourcePerformance
  };
})();
