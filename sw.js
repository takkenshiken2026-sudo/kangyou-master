/* Service Worker: 静的アセットの長期キャッシュ（GitHub Pages の短い max-age=600 を補完） */
var CACHE_PREFIX = "kangyou-master";
var VERSION = "5e02c839cbf0";
var CACHE_NAME = CACHE_PREFIX + "-" + VERSION;

var PRECACHE = [
  "./site-theme.css",
  "./site-config.js",
  "./site-pages.css",
  "./site-analytics.js",
  "./site-exam-data-loader.js",
];

function isExamDataRequest(url) {
  return /\/exam-site-data-(past|practice|ichimondou)\.js(\?|$)/.test(url.pathname);
}

function isStaticAsset(url) {
  if (url.origin !== self.location.origin) return false;
  if (isExamDataRequest(url)) return true;
  return /\.(js|css|woff2?|png|jpe?g|webp|svg|ico)(\?|$)/i.test(url.pathname);
}

self.addEventListener("install", function (event) {
  event.waitUntil(
    caches
      .open(CACHE_NAME)
      .then(function (cache) {
        return cache.addAll(PRECACHE).catch(function () {});
      })
      .then(function () {
        return self.skipWaiting();
      })
  );
});

self.addEventListener("activate", function (event) {
  event.waitUntil(
    caches
      .keys()
      .then(function (keys) {
        return Promise.all(
          keys
            .filter(function (k) {
              return k.indexOf(CACHE_PREFIX + "-") === 0 && k !== CACHE_NAME;
            })
            .map(function (k) {
              return caches.delete(k);
            })
        );
      })
      .then(function () {
        return self.clients.claim();
      })
  );
});

self.addEventListener("message", function (event) {
  var data = event.data;
  if (!data || data.type !== "SET_CACHE_VERSION") return;
  var next = String(data.version || "").trim();
  if (!next || next === VERSION) return;
  VERSION = next;
  CACHE_NAME = CACHE_PREFIX + "-" + VERSION;
  event.waitUntil(
    caches
      .open(CACHE_NAME)
      .then(function (cache) {
        return cache.addAll(PRECACHE).catch(function () {});
      })
      .then(function () {
        return self.skipWaiting();
      })
  );
});

self.addEventListener("fetch", function (event) {
  var req = event.request;
  if (req.method !== "GET") return;
  var url;
  try {
    url = new URL(req.url);
  } catch (_e) {
    return;
  }
  if (!isStaticAsset(url)) return;

  event.respondWith(
    caches.open(CACHE_NAME).then(function (cache) {
      return cache.match(req).then(function (cached) {
        var network = fetch(req)
          .then(function (res) {
            if (res && res.ok) {
              cache.put(req, res.clone());
            }
            return res;
          })
          .catch(function () {
            return cached;
          });
        return cached || network;
      });
    })
  );
});
