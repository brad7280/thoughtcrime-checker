#!/usr/bin/env python3
"""
Generate a static `banned-words.html` file from `banned-words.js`.

Usage:
  python3 scripts/generate_banned_html.py

This script extracts the JS array from `banned-words.js`, then writes
an HTML file that contains the same table as the dynamic page. This is
useful when you want a pre-rendered, distributable `banned-words.html`.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BANNED_JS = ROOT / 'banned-words.js'
OUT_HTML = ROOT / 'banned-words.html'

def read_banned_words():
    txt = BANNED_JS.read_text(encoding='utf-8')
    m = re.search(r"window\.BANNED_WORDS\s*=\s*\[([\s\S]*?)\];", txt)
    if not m:
        raise SystemExit('Could not find window.BANNED_WORDS array in banned-words.js')
    array_text = m.group(1)
    # Find all double-quoted strings. This is robust enough for this file.
    words = re.findall(r'"([^"]*)"', array_text)
    return words

TEMPLATE_HEAD = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Banned Words List</title>
  <style>
    body { font-family: Arial, sans-serif; background-color: #7a1519; color: white; text-align: center; }
    .container { max-width: 800px; margin: 40px auto; padding: 20px; }
    table { width: 100%; border-collapse: collapse; background: white; color: black; margin-top: 20px; }
    th, td { border: 1px solid black; padding: 10px; }
    a { color: #ffcc00; text-decoration: none; font-weight: bold; }
  </style>
</head>
<body>
<div class="container">
  <nav>
    <a href="index.html">Home</a>
    <a href="banned-words.html">Banned Words List</a>
    <a href="replacer.html">Replacer Tool</a>
  </nav>
  <h2>Banned Words List</h2>
  <table>
    <thead><tr><th>Banned Words</th></tr></thead>
    <tbody id="bannedWordsBody">
'''

TEMPLATE_TAIL = '''
    </tbody>
  </table>
</div>
</body>
</html>
'''

def main():
    words = read_banned_words()
    rows = '\n'.join(f'      <tr><td>{w}</td></tr>' for w in words)
    OUT_HTML.write_text(TEMPLATE_HEAD + rows + TEMPLATE_TAIL, encoding='utf-8')
    print(f'Wrote {OUT_HTML} ({len(words)} words)')

if __name__ == '__main__':
    main()
