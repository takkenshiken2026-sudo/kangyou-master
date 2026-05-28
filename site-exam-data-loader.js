/**
 * 過去問・実践・一問一答の大容量 JS を初回描画後に順次読み込む。
 * index.html のゲスト起動は whenExamSiteDataReady() で待つ。
 */
(function (global) {
  var VERSION = (global.__SITE_ASSET_VERSION__ || "").toString();
  var FILES = [
    "site-config.js",
    "exam-site-data-practice.js",
    "exam-site-data-past.js",
    "exam-site-data-ichimondou.js",
  ];
  var ready = false;
  var loading = false;
  var waiters = [];

  function verUrl(path) {
    if (!VERSION) return path;
    return path + (path.indexOf("?") >= 0 ? "&" : "?") + "v=" + encodeURIComponent(VERSION);
  }

  function notify() {
    ready = true;
    var q = waiters.slice();
    waiters = [];
    q.forEach(function (fn) {
      try {
        fn();
      } catch (e) {
        console.error("[exam-data-loader]", e);
      }
    });
  }

  function loadScript(src) {
    return new Promise(function (resolve, reject) {
      var s = document.createElement("script");
      s.src = src;
      s.async = false;
      s.onload = function () {
        resolve();
      };
      s.onerror = function () {
        reject(new Error("Failed to load " + src));
      };
      (document.head || document.documentElement).appendChild(s);
    });
  }

  function loadAll() {
    if (ready) return Promise.resolve();
    if (loading) {
      return new Promise(function (resolve) {
        waiters.push(resolve);
      });
    }
    loading = true;
    var chain = Promise.resolve();
    FILES.forEach(function (f) {
      chain = chain.then(function () {
        return loadScript(verUrl(f));
      });
    });
    return chain
      .then(function () {
        if (typeof applyCsvImportedQuestions === "function") {
          applyCsvImportedQuestions();
        }
        notify();
      })
      .catch(function (err) {
        loading = false;
        console.error("[exam-data-loader]", err);
        notify();
      });
  }

  global.whenExamSiteDataReady = function (cb) {
    if (typeof cb !== "function") return;
    if (ready) {
      cb();
      return;
    }
    waiters.push(cb);
    scheduleLoad();
  };

  function scheduleLoad() {
    if (loading || ready) return;
    var run = function () {
      loadAll();
    };
    var kick = function () {
      if ("requestIdleCallback" in global) {
        global.requestIdleCallback(run, { timeout: 2000 });
      } else {
        setTimeout(run, 0);
      }
    };
    if (document.readyState === "loading") {
      document.addEventListener(
        "DOMContentLoaded",
        function () {
          global.requestAnimationFrame(kick);
        },
        { once: true }
      );
    } else {
      global.requestAnimationFrame(kick);
    }
  }

  scheduleLoad();
})(typeof window !== "undefined" ? window : this);
