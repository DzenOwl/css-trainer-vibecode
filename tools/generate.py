# -*- coding: utf-8 -*-
"""Генератор index.html из данных задач (tasks_data.py)."""
import html as H
import sys
from tasks_data import get_tasks

def esc(s):
    return H.escape(s, quote=False)

SECTIONS = [
    ("context", "Контекстные селекторы",
     "Контекстный (потомковый) селектор выбирает элементы внутри другого элемента: <code>main p</code>, <code>nav a</code>, <code>.card h3</code>. Напишите CSS так, чтобы стиль применился только к нужным элементам."),
    ("classes", "Классы",
     "Классы — самый частый инструмент верстальщика. Тренируем одиночные классы, связки «тег.класс», комбинированные селекторы без пробела, группировку через запятую и переопределение стилей."),
    ("hover", "Псевдокласс :hover",
     "Наведение курсора — интерактив без JavaScript. Меняем цвет, фон, рамку, тень, курсор и размер шрифта."),
    ("visited", "Псевдокласс :visited",
     ":visited стилизует уже посещённые ссылки. Помните про ограничения безопасности браузеров и порядок правил LVHA (:link → :visited → :hover → :active)."),
    ("first-child", "Псевдокласс :first-child",
     ":first-child выбирает элемент, который является ПЕРВЫМ ребёнком родителя, независимо от тега. Здесь прячутся главные ловушки новичков."),
    ("last-child", "Псевдокласс :last-child",
     ":last-child выбирает последнего ребёнка родителя. Классические приёмы: убрать рамку/отступ у последнего элемента, скруглить край группы кнопок."),
]

HEAD = '''<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CSS-задачник для начинающих верстальщиков</title>
  <link rel="stylesheet" href="css/style.css">
</head>
<body>

  <header class="site-header">
    <h1 class="site-title">CSS-задачник</h1>
    <p class="site-subtitle">Тренируем простые селекторы: контекстные, классы и псевдоклассы</p>
    <nav class="site-nav">
      <a href="#context">Контекстные селекторы</a>
      <a href="#classes">Классы</a>
      <a href="#hover">Псевдокласс :hover</a>
      <a href="#visited">Псевдокласс :visited</a>
      <a href="#first-child">Псевдокласс :first-child</a>
      <a href="#last-child">Псевдокласс :last-child</a>
    </nav>
    <p class="how-to">Как заниматься: слева — готовый HTML, в центре — поле для вашего CSS, справа — результат. Напишите стили и нажмите «Применить» (или Ctrl+Enter).</p>
  </header>

  <main class="content">

'''

FOOT = '''  </main>

  <footer class="site-footer">
    <nav class="site-nav">
      <a href="#context">Контекстные</a>
      <a href="#classes">Классы</a>
      <a href="#hover">:hover</a>
      <a href="#visited">:visited</a>
      <a href="#first-child">:first-child</a>
      <a href="#last-child">:last-child</a>
    </nav>
    <p class="footer-note">CSS-задачник · 60 задач · пишите код прямо на странице</p>
  </footer>

  <script src="js/app.js"></script>
</body>
</html>
'''

def main():
    tasks = get_tasks()
    out = [HEAD]
    for si, (sid, stitle, sdesc) in enumerate(SECTIONS, 1):
        out.append(f'    <section id="{sid}" class="section">\n')
        out.append(f'      <h2 class="section-title"><span class="num">{si}.</span> {stitle}</h2>\n')
        out.append(f'      <p class="section-desc">{sdesc}</p>\n\n')
        out.append('      <div class="task-list">\n')
        for j in range(10):
            num = f"{si}.{j + 1}"
            title, goal, snippet = tasks[(si - 1) * 10 + j]
            out.append(f'        <article class="task-card" id="task-{num}">\n')
            out.append(f'          <h3 class="task-title">{title}</h3>\n')
            out.append('          <div class="task-body">\n')
            out.append('            <div class="pane pane-html">\n')
            out.append('              <h4 class="pane-label">Дано (HTML)</h4>\n')
            out.append(f'              <pre class="html-src"><code>{esc(snippet)}</code></pre>\n')
            out.append('            </div>\n')
            out.append('            <div class="pane pane-css">\n')
            out.append('              <h4 class="pane-label">Ваш CSS</h4>\n')
            out.append('              <textarea class="css-input" rows="9" spellcheck="false" wrap="off" placeholder="/* Пишите CSS здесь */"></textarea>\n')
            out.append('              <button class="apply-btn" type="button">Применить ▶</button>\n')
            out.append('            </div>\n')
            out.append('            <div class="pane pane-preview">\n')
            out.append('              <h4 class="pane-label">Результат</h4>\n')
            out.append(f'              <iframe class="preview-frame" title="Предпросмотр задачи {num}" sandbox="allow-same-origin allow-popups allow-top-navigation-by-user-activation"></iframe>\n')
            out.append('            </div>\n')
            out.append('          </div>\n')
            out.append(f'          <p class="goal-text">Цель: {goal}</p>\n')
            out.append('        </article>\n\n')
        out.append('      </div>\n')
        out.append('    </section>\n\n')
    out.append(FOOT)

    path = sys.argv[1] if len(sys.argv) > 1 else "../index.html"
    with open(path, "w", encoding="utf-8") as f:
        f.write("".join(out))
    print("OK: written", len(tasks), "tasks ->", path)

if __name__ == "__main__":
    main()
