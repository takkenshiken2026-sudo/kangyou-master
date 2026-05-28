(function () {
  if (!("serviceWorker" in navigator)) return;
  var version = (window.__SITE_ASSET_VERSION__ || "").toString();
  window.addEventListener(
    "load",
    function () {
      navigator.serviceWorker
        .register("sw.js")
        .then(function (reg) {
          if (!version || !reg.active) return;
          reg.active.postMessage({ type: "SET_CACHE_VERSION", version: version });
        })
        .catch(function () {});
    },
    { once: true }
  );
})();
