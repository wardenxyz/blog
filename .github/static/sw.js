// Enhanced Service Worker for caching and offline support
const CACHE_VERSION = 'v2';
const STATIC_CACHE = 'blog-static-' + CACHE_VERSION;
const PAGE_CACHE = 'blog-pages-' + CACHE_VERSION;

const STATIC_ASSETS = [
  './style.css',
  './main.js',
  './favicon.svg',
  '../index.html',
  '../categories.html',
  '../tags.html',
  '../search.json'
];

const STATIC_ROOT = new URL('./', self.location).pathname; // e.g. /blog/static/
const INDEX_URL = new URL('../index.html', self.location).href;

self.addEventListener('install', event => {
  event.waitUntil((async () => {
    const cache = await caches.open(STATIC_CACHE);
    await Promise.all(
      STATIC_ASSETS.map(async asset => {
        try {
          await cache.add(asset);
        } catch (err) {
          console.warn('[SW] Skip asset during install:', asset, err);
        }
      })
    );
    self.skipWaiting();
  })());
});

self.addEventListener('activate', event => {
  event.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(
      keys
        .filter(name => name !== STATIC_CACHE && name !== PAGE_CACHE)
        .map(name => caches.delete(name))
    );
    self.clients.claim();
  })());
});

function cacheFirst(request) {
  return caches.open(STATIC_CACHE).then(cache =>
    cache.match(request).then(cached => {
      if (cached) {
        return cached;
      }
      return fetch(request).then(response => {
        if (response && response.ok) {
          cache.put(request, response.clone());
        }
        return response;
      });
    })
  );
}

function networkFirst(request) {
  return fetch(request)
    .then(response => {
      if (response && response.ok) {
        const copy = response.clone();
        caches.open(PAGE_CACHE).then(cache => cache.put(request, copy));
      }
      return response;
    })
    .catch(() => caches.match(request).then(match => match || caches.match(INDEX_URL)));
}

function staleWhileRevalidate(request) {
  return caches.open(STATIC_CACHE).then(cache =>
    cache.match(request).then(cached => {
      const fetchPromise = fetch(request)
        .then(response => {
          if (response && response.ok) {
            cache.put(request, response.clone());
          }
          return response;
        })
        .catch(() => cached);
      return cached || fetchPromise;
    })
  );
}

self.addEventListener('fetch', event => {
  const { request } = event;
  if (request.method !== 'GET') return;

  const url = new URL(request.url);
  if (url.origin !== self.location.origin) return;

  if (url.pathname.startsWith(STATIC_ROOT)) {
    event.respondWith(cacheFirst(request));
    return;
  }

  if (url.pathname.endsWith('/search.json') || url.pathname.endsWith('search.json')) {
    event.respondWith(staleWhileRevalidate(request));
    return;
  }

  const accept = request.headers.get('accept') || '';
  if (request.mode === 'navigate' || accept.includes('text/html')) {
    event.respondWith(networkFirst(request));
    return;
  }

  if (request.destination === 'image' || request.destination === 'style' || request.destination === 'script' || request.destination === 'font') {
    event.respondWith(staleWhileRevalidate(request));
  }
});
