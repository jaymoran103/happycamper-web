/* The standard ESPO app header, made to actually work in a static prototype.
 *
 * Mirrors permit-desk src/app/components/theme-toggle.tsx and
 * src/components/kit/theme-accent.tsx:
 *   · theme is a MANAGED `.dark` class on <html>, never the OS media query
 *   · Light / Dark / System, plus the text-size bump (html.text-scale-lg)
 *   · the accent lands on <html> as data-accent and recolors --primary only
 * The app persists these in cookies; a file:// prototype uses localStorage.
 *
 * DARK IS THE DEFAULT HERE. The app defaults to "system"; these studies are
 * meant to be read dark, so an unset preference resolves to dark and the
 * markup ships with class="dark" so there is no flash before this runs.
 */
(function () {
  "use strict";

  var THEME = "espo-proto-theme";
  var SIZE = "espo-proto-textsize";
  var ACCENT = "espo-proto-accent";
  var DEFAULT_THEME = "dark";
  var DEFAULT_ACCENT = "teal";

  function get(k, fallback) {
    try {
      return localStorage.getItem(k) || fallback;
    } catch (e) {
      return fallback;
    }
  }
  function set(k, v) {
    try {
      localStorage.setItem(k, v);
    } catch (e) {
      /* private window: the preference simply does not persist */
    }
  }

  function prefersDark() {
    return window.matchMedia("(prefers-color-scheme: dark)").matches;
  }
  function resolveDark(theme) {
    return theme === "dark" || (theme === "system" && prefersDark());
  }

  function applyTheme(theme) {
    document.documentElement.classList.toggle("dark", resolveDark(theme));
  }
  function applySize(size) {
    document.documentElement.classList.toggle("text-scale-lg", size === "large");
  }
  function applyAccent(accent) {
    document.documentElement.setAttribute("data-accent", accent);
  }

  // Before paint.
  applyTheme(get(THEME, DEFAULT_THEME));
  applySize(get(SIZE, "default"));
  applyAccent(get(ACCENT, DEFAULT_ACCENT));

  // Follow the OS only while "system" is the choice.
  window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", function () {
    if (get(THEME, DEFAULT_THEME) === "system") applyTheme("system");
  });

  function ready(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }

  ready(function () {
    var menus = [].slice.call(document.querySelectorAll("[data-menu]"));

    function closeAll(except) {
      menus.forEach(function (m) {
        if (m !== except) m.removeAttribute("data-open");
      });
    }

    [].slice.call(document.querySelectorAll("[data-menu-trigger]")).forEach(function (btn) {
      btn.addEventListener("click", function (e) {
        e.stopPropagation();
        var id = btn.getAttribute("data-menu-trigger");
        var m = document.querySelector('[data-menu="' + id + '"]');
        if (!m) return;
        var open = m.hasAttribute("data-open");
        closeAll();
        if (!open) m.setAttribute("data-open", "");
        btn.setAttribute("aria-expanded", String(!open));
      });
    });

    document.addEventListener("click", function () {
      closeAll();
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") closeAll();
    });
    menus.forEach(function (m) {
      m.addEventListener("click", function (e) {
        e.stopPropagation();
      });
    });

    function markTheme() {
      var t = get(THEME, DEFAULT_THEME);
      [].slice.call(document.querySelectorAll("[data-theme-set]")).forEach(function (b) {
        b.setAttribute("aria-checked", String(b.getAttribute("data-theme-set") === t));
      });
      var icons = { light: "i-sun", dark: "i-moon", system: "i-monitor" };
      [].slice.call(document.querySelectorAll("[data-theme-icon] > svg")).forEach(function (s) {
        s.style.display = s.classList.contains(icons[t]) ? "" : "none";
      });
    }

    function markSize() {
      var s = get(SIZE, "default");
      [].slice.call(document.querySelectorAll("[data-size-toggle]")).forEach(function (b) {
        b.setAttribute("aria-checked", String(s === "large"));
        var lbl = b.querySelector("[data-size-label]");
        if (lbl) lbl.textContent = s === "large" ? "Text: large" : "Text: default";
      });
    }

    function markAccent() {
      var a = get(ACCENT, DEFAULT_ACCENT);
      [].slice.call(document.querySelectorAll("[data-accent-set]")).forEach(function (b) {
        b.setAttribute("aria-checked", String(b.getAttribute("data-accent-set") === a));
      });
    }

    [].slice.call(document.querySelectorAll("[data-theme-set]")).forEach(function (b) {
      b.addEventListener("click", function () {
        var v = b.getAttribute("data-theme-set");
        set(THEME, v);
        applyTheme(v);
        markTheme();
      });
    });

    [].slice.call(document.querySelectorAll("[data-size-toggle]")).forEach(function (b) {
      b.addEventListener("click", function () {
        var next = get(SIZE, "default") === "large" ? "default" : "large";
        set(SIZE, next);
        applySize(next);
        markSize();
      });
    });

    [].slice.call(document.querySelectorAll("[data-accent-set]")).forEach(function (b) {
      b.addEventListener("click", function () {
        var v = b.getAttribute("data-accent-set");
        set(ACCENT, v);
        applyAccent(v);
        markAccent();
      });
    });

    markTheme();
    markSize();
    markAccent();
  });
})();

/* ── ONE DISCLOSURE CONTROL ──────────────────────────────────────────────
 * Round 2. Every "there is more" in these studies is the same pair:
 *   <button class="disclose" data-disclose="ID" aria-expanded="false">
 *   <div class="detail" data-detail="ID">
 * so nothing supplemental is carried by a button's wording or by a hover
 * tooltip, and a reader learns one control rather than reading every label.
 */
(function () {
  "use strict";
  function ready(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }
  ready(function () {
    [].slice.call(document.querySelectorAll("[data-disclose]")).forEach(function (btn) {
      btn.addEventListener("click", function (e) {
        e.stopPropagation();
        var id = btn.getAttribute("data-disclose");
        var panel = document.querySelector('[data-detail="' + id + '"]');
        if (!panel) return;
        var open = panel.hasAttribute("data-open");
        if (open) panel.removeAttribute("data-open");
        else panel.setAttribute("data-open", "");
        btn.setAttribute("aria-expanded", String(!open));
      });
    });
  });
})();

/* ── ONE TAB MECHANISM ───────────────────────────────────────────────────
 * Round 3. Two things now switch in place: the document inside the source
 * panel, and the Checks / History region. Both are the same pair:
 *   <button data-tab="SET:key" aria-current>   <div data-panel="SET:key">
 * so a reader learns one control here too.
 */
(function () {
  "use strict";
  function ready(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }
  ready(function () {
    [].slice.call(document.querySelectorAll("[data-tab]")).forEach(function (btn) {
      btn.addEventListener("click", function (e) {
        e.preventDefault();
        var val = btn.getAttribute("data-tab");
        var set = val.split(":")[0];
        [].slice.call(document.querySelectorAll('[data-tab^="' + set + ':"]')).forEach(function (b) {
          if (b === btn) b.setAttribute("aria-current", "true");
          else b.removeAttribute("aria-current");
        });
        [].slice.call(document.querySelectorAll('[data-panel^="' + set + ':"]')).forEach(function (p) {
          p.hidden = p.getAttribute("data-panel") !== val;
        });
      });
    });
  });
})();
