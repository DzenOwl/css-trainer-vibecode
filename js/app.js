/* ============================================
   Логика задачника: поле CSS -> предпросмотр
   Каждая задача рендерит свой HTML-фрагмент
   внутри <iframe>, куда подставляется CSS
   пользователя по кнопке «Применить».
   ============================================ */
(function () {
  "use strict";

  var STORAGE_KEY = "css-tasks-v2";

  /* Базовые стили документа-предпросмотра:
     нейтральные, чтобы решения задач было видно чисто */
  var FRAME_BASE_CSS = [
    "html { color-scheme: light; }",
    "body {",
    "  margin: 10px;",
    "  font-family: 'Segoe UI', Arial, sans-serif;",
    "  font-size: 16px;",
    "  line-height: 1.5;",
    "  color: #222;",
    "  background: #fff;",
    "}",
    "img { max-width: 100%; }",
    "table { border-collapse: collapse; }",
    "td, th { padding: 4px 8px; }"
  ].join("\n");

  function taskNumber(card) {
    // id="task-1.2" -> "1.2"
    return (card.id || "").replace(/^task-/, "");
  }

  /* ---------- Предпросмотр ---------- */

  function buildDoc(htmlFragment, cssText) {
    return (
      "<!DOCTYPE html><html lang='ru'><head><meta charset='utf-8'>" +
      "<style>" + FRAME_BASE_CSS + "</style>" +
      "<style>" + cssText + "</style>" +
      "</head><body>" + htmlFragment + "</body></html>"
    );
  }

  function renderPreview(card) {
    var frame = card.querySelector(".preview-frame");
    var srcEl = card.querySelector(".html-src code");
    var input = card.querySelector(".css-input");
    if (!frame || !srcEl || !input) return;

    var fragment = srcEl.textContent;
    var css = input.value;

    try {
      frame.srcdoc = buildDoc(fragment, css);
      frame.classList.remove("error");
    } catch (e) {
      // fallback для старых браузеров без srcdoc
      var doc = frame.contentDocument;
      if (doc) {
        doc.open();
        doc.write(buildDoc(fragment, css));
        doc.close();
      }
    }
  }

  /* ---------- Кнопка «Применить» ---------- */

  function applyTask(card) {
    renderPreview(card);
    saveCode(card);

    var btn = card.querySelector(".apply-btn");
    if (!btn) return;
    btn.textContent = "Готово ✓";
    btn.classList.add("ok");
    setTimeout(function () {
      btn.textContent = "Применить ▶";
      btn.classList.remove("ok");
    }, 900);
  }

  /* ---------- Сохранение кода в localStorage ---------- */

  function saveCode(card) {
    try {
      var data = JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}");
      var input = card.querySelector(".css-input");
      if (input) data[taskNumber(card)] = input.value;
      localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
    } catch (e) {
      /* localStorage может быть недоступен — не критично */
    }
  }

  function restoreCode() {
    var data = {};
    try {
      data = JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}");
    } catch (e) {
      data = {};
    }
    document.querySelectorAll(".task-card").forEach(function (card) {
      var num = taskNumber(card);
      var input = card.querySelector(".css-input");
      if (input && typeof data[num] === "string") {
        input.value = data[num];
      }
    });
  }

  /* ---------- Инициализация ---------- */

  function initCard(card) {
    var input = card.querySelector(".css-input");
    var btn = card.querySelector(".apply-btn");

    // Стартовый рендер: HTML без пользовательского CSS
    renderPreview(card);

    if (btn) {
      btn.addEventListener("click", function () {
        applyTask(card);
      });
    }

    if (input) {
      // Ctrl+Enter / Cmd+Enter применяет код
      input.addEventListener("keydown", function (e) {
        if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
          e.preventDefault();
          applyTask(card);
        }
      });

      // Tab вставляет два пробела, а не уходит к кнопке
      input.addEventListener("keydown", function (e) {
        if (e.key === "Tab") {
          e.preventDefault();
          var start = input.selectionStart;
          var end = input.selectionEnd;
          input.value =
            input.value.slice(0, start) + "  " + input.value.slice(end);
          input.selectionStart = input.selectionEnd = start + 2;
        }
      });

      // Автосохранение при наборе (без перерисовки preview)
      var timer = null;
      input.addEventListener("input", function () {
        clearTimeout(timer);
        timer = setTimeout(function () {
          saveCode(card);
        }, 400);
      });
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    restoreCode();
    document.querySelectorAll(".task-card").forEach(initCard);
  });
})();
