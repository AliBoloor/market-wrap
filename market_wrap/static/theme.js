(function () {
  "use strict";

  var root = document.documentElement;
  var toggle = document.querySelector(".theme-toggle");
  var systemDark = window.matchMedia("(prefers-color-scheme: dark)");

  function currentTheme() {
    return root.dataset.theme || (systemDark.matches ? "dark" : "light");
  }

  function updateControl() {
    if (!toggle) return;
    var nextTheme = currentTheme() === "dark" ? "light" : "dark";
    toggle.setAttribute("aria-label", "Switch to " + nextTheme + " theme");
  }

  if (toggle) {
    toggle.addEventListener("click", function () {
      var nextTheme = currentTheme() === "dark" ? "light" : "dark";
      root.dataset.theme = nextTheme;
      localStorage.setItem("market-wrap-theme", nextTheme);
      updateControl();
    });
  }

  systemDark.addEventListener("change", function () {
    if (!root.dataset.theme) updateControl();
  });

  updateControl();
}());
