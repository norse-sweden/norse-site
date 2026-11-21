/* Minimal JS: mobile nav, gallery lightbox, contact form. */
(function () {
  "use strict";

  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    nav.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () {
        nav.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  /* Lightbox with prev/next, arrow keys and swipe */
  var boxes = Array.prototype.slice.call(document.querySelectorAll("[data-lightbox]"));
  if (boxes.length) {
    var overlay = document.createElement("div");
    overlay.className = "lightbox";
    overlay.setAttribute("role", "dialog");
    overlay.setAttribute("aria-modal", "true");
    overlay.setAttribute("aria-label", "Image preview");
    overlay.innerHTML =
      '<button type="button" class="lightbox-close" aria-label="Close">&times;</button>' +
      '<button type="button" class="lightbox-nav lightbox-prev" aria-label="Previous">&#8249;</button>' +
      '<img alt="">' +
      '<button type="button" class="lightbox-nav lightbox-next" aria-label="Next">&#8250;</button>' +
      '<div class="lightbox-count"></div>';
    document.body.appendChild(overlay);
    var img = overlay.querySelector("img");
    var closeBtn = overlay.querySelector(".lightbox-close");
    var prevBtn = overlay.querySelector(".lightbox-prev");
    var nextBtn = overlay.querySelector(".lightbox-next");
    var count = overlay.querySelector(".lightbox-count");
    var group = [], idx = 0;

    function srcOf(el) { return el.getAttribute("href") || (el.querySelector("img") || {}).src; }
    function show(i) {
      idx = (i + group.length) % group.length;
      var el = group[idx];
      img.src = srcOf(el);
      img.alt = ((el.querySelector("img") || {}).alt) || "";
      count.textContent = group.length > 1 ? (idx + 1) + " / " + group.length : "";
      var multi = group.length > 1;
      prevBtn.style.display = nextBtn.style.display = multi ? "" : "none";
      var n = new Image(); n.src = srcOf(group[(idx + 1) % group.length]);
    }
    function isOpen() { return overlay.classList.contains("is-open"); }
    function close() { overlay.classList.remove("is-open"); img.removeAttribute("src"); }

    boxes.forEach(function (el) {
      el.addEventListener("click", function (e) {
        e.preventDefault();
        var parent = el.closest(".gallery") || document;
        group = Array.prototype.slice.call(parent.querySelectorAll("[data-lightbox]"));
        show(group.indexOf(el));
        overlay.classList.add("is-open");
        closeBtn.focus();
      });
    });
    prevBtn.addEventListener("click", function (e) { e.stopPropagation(); show(idx - 1); });
    nextBtn.addEventListener("click", function (e) { e.stopPropagation(); show(idx + 1); });
    overlay.addEventListener("click", function (e) {
      if (e.target === overlay || e.target === closeBtn) close();
    });
    document.addEventListener("keydown", function (e) {
      if (!isOpen()) return;
      if (e.key === "Escape") close();
      else if (e.key === "ArrowRight") { e.preventDefault(); show(idx + 1); }
      else if (e.key === "ArrowLeft") { e.preventDefault(); show(idx - 1); }
    });
    var x0 = null;
    overlay.addEventListener("touchstart", function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    overlay.addEventListener("touchend", function (e) {
      if (x0 === null) return;
      var dx = e.changedTouches[0].clientX - x0; x0 = null;
      if (Math.abs(dx) > 40) show(idx + (dx < 0 ? 1 : -1));
    });
  }

  /* Auto-advancing sliders (home news/reviews and product ribbon). */
  function initSlider(root) {
    var slides = Array.prototype.slice.call(root.querySelectorAll(".slide"));
    if (!slides.length) return;
    var dotsBox = root.querySelector(".slider-dots");
    var prevBtn = root.querySelector(".slider-prev");
    var nextBtn = root.querySelector(".slider-next");
    var i = 0;
    var timer = null;
    var interval = parseInt(root.getAttribute("data-interval") || "7000", 10);
    var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    if (dotsBox) {
      dotsBox.innerHTML = "";
      slides.forEach(function (_, n) {
        var b = document.createElement("button");
        b.type = "button";
        b.setAttribute("aria-label", "Go to slide " + (n + 1));
        b.addEventListener("click", function () { go(n, true); });
        dotsBox.appendChild(b);
      });
    }

    function go(n, user) {
      i = (n + slides.length) % slides.length;
      slides.forEach(function (s, k) {
        s.classList.toggle("is-active", k === i);
      });
      if (dotsBox) {
        Array.prototype.forEach.call(dotsBox.querySelectorAll("button"), function (b, k) {
          if (k === i) b.setAttribute("aria-current", "true");
          else b.removeAttribute("aria-current");
        });
      }
      if (user || !reduce) restart();
    }
    function stop() {
      if (timer) { clearInterval(timer); timer = null; }
    }
    function restart() {
      stop();
      if (reduce || slides.length < 2) return;
      timer = setInterval(function () { go(i + 1, false); }, interval);
    }

    if (prevBtn) prevBtn.addEventListener("click", function () { go(i - 1, true); });
    if (nextBtn) nextBtn.addEventListener("click", function () { go(i + 1, true); });
    root.addEventListener("mouseenter", stop);
    root.addEventListener("mouseleave", restart);
    root.addEventListener("focusin", stop);
    root.addEventListener("focusout", function (e) {
      if (!root.contains(e.relatedTarget)) restart();
    });
    var x0 = null;
    root.addEventListener("touchstart", function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    root.addEventListener("touchend", function (e) {
      if (x0 === null) return;
      var dx = e.changedTouches[0].clientX - x0; x0 = null;
      if (Math.abs(dx) > 40) go(i + (dx < 0 ? 1 : -1), true);
    });
    document.addEventListener("visibilitychange", function () {
      if (document.hidden) stop(); else restart();
    });
    go(0, false);
  }
  document.querySelectorAll("[data-slider]").forEach(initSlider);

  /* Contact form → Web3Forms (or Formspree if the action is changed). */
  var form = document.querySelector("form[data-contact]");
  if (!form) return;

  var status = form.querySelector(".form-status");
  var submit = form.querySelector("[type=submit]");
  var PLACEHOLDER = "YOUR_WEB3FORMS_ACCESS_KEY";

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var keyInput = form.querySelector("[name=access_key]");
    var key = keyInput ? keyInput.value.trim() : "";
    if (!key || key === PLACEHOLDER) {
      if (status) {
        status.className = "form-status err";
        status.textContent =
          "The form is not connected yet. Replace YOUR_WEB3FORMS_ACCESS_KEY in contact/index.html with a free key from web3forms.com.";
      }
      return;
    }

    if (submit) submit.disabled = true;
    if (status) {
      status.className = "form-status";
      status.textContent = "Sending…";
    }

    var data = new FormData(form);
    fetch(form.action, {
      method: "POST",
      body: data,
      headers: { Accept: "application/json" }
    })
      .then(function (res) {
        return res.json().catch(function () { return { ok: res.ok }; });
      })
      .then(function (json) {
        var ok = json.success === true || json.ok === true || json.ok === "true";
        if (ok) {
          form.reset();
          if (status) {
            status.className = "form-status ok";
            status.textContent = "Thank you. Your message has been sent.";
          }
        } else {
          throw new Error((json && (json.message || json.error)) || "Could not send.");
        }
      })
      .catch(function (err) {
        if (status) {
          status.className = "form-status err";
          status.textContent =
            "The message could not be sent. Please try again later. " +
            (err && err.message ? "(" + err.message + ")" : "");
        }
      })
      .finally(function () {
        if (submit) submit.disabled = false;
      });
  });
})();
