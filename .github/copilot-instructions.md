<!-- Copilot / AI Agent Instructions for `thoughtcrime-checker` -->
# Project overview

This repository is a small, static, client-side web app that highlights and optionally replaces words/phrases from a curated list. It is intentionally simple: no build toolchain, no server-side code, and all processing happens in the browser for privacy.

Key files:
- `index.html` — main editor. Uses `contenteditable`, caret helpers, and highlights matches from the shared list.
- `replacer.html` — replacement tool: tokenizes matches and substitutes approved phrases.
- `banned-words.js` — canonical global list assigned to `window.BANNED_WORDS` and consumed by pages.
- `banned-words.html` — a browsable table that duplicates the banned list as a local `bannedWords` array (keep in sync with `banned-words.js`).
- `CNAME` — indicates this repo is served with a custom domain (GitHub Pages).

What to know about the code and conventions
- Global list pattern: `banned-words.js` sets `window.BANNED_WORDS = [...]`. Pages assume this global exists and do not import modules.
- No build step: edit HTML/JS directly and test in-browser. Use a simple local static server for reliable testing (`python3 -m http.server`), see Testing section.
- Highlighting approach: pages create RegExps per banned entry with word boundaries (e.g. `new RegExp(`\\b(${word})\\b`, 'gi')`). Because of this:
  - Entries are expected as lowercase strings or phrases. Case-insensitive matching is used.
  - Word-boundary semantics may not match across punctuation or some Unicode; multi-word phrases work but watch for punctuation or slashes in list items.
- Escaping differences:
 - Escaping differences:
  - Both `replacer.html` and `index.html` escape list entries and prefer a combined regex sorted by length (longer-first) to avoid partial matches. This ensures multi-word phrases (e.g. `"climate change"`) are matched before their substrings (e.g. `"climate"`).
- Caret preservation: both `index.html` and `replacer.html` implement `getCaretCharacterOffsetWithin` and `setCaretPosition` by character index — follow that pattern when editing or refactoring the editor logic.
- HTML escaping: pages call an `escapeHTML` helper before injecting spans; keep this behavior when modifying the rendering path to avoid XSS and preserve plain-text caret offsets.

Maintenance & patterns to follow
- Single source of truth: `banned-words.js` is the intended shared list. `banned-words.html` currently duplicates the list — update both when changing words, or consolidate by loading `banned-words.js` inside `banned-words.html` (preferred).
 - Single source of truth: `banned-words.js` is the intended shared list. `banned-words.html` previously duplicated the list — prefer loading `banned-words.js` at runtime (the repo now does this).
 - If you need a pre-rendered static `banned-words.html` for distribution, run the generator: `python3 scripts/generate_banned_html.py` (it reads `banned-words.js` and writes a static HTML file).
- Update cadence: entries are simple strings. When adding phrases, add them as lower-case strings (e.g. `"new phrase example"`). Avoid regex markup inside list entries because some pages do not escape entries before building regexes.
- Replacements: `replacer.html` uses tokenization to ensure highlighted preview and plain-text output match. If you change replacement behavior, keep the token-first approach to preserve exact replacements.

Testing & debugging
- Local dev: serve the repo root and open pages in a browser.
  - Command (from project root):
    `python3 -m http.server 8000`
  - Then open `http://localhost:8000/index.html` (or other pages).
- Use the browser console to inspect `window.BANNED_WORDS` and verify regex creation. If highlighting fails, check for regex special characters inside list entries.

Common small tasks & examples
- Add a banned phrase: open `banned-words.js`, add a new string to the array (keep trailing comma formatting consistent). Then update `banned-words.html`'s array (or remove the duplicate and load the JS file instead).
- Add an approved replacement (replacer tool): edit the `APPROVED_OPTIONS` array in `replacer.html`.
- Preserve caret behavior: when changing the editor DOM, ensure you still save/restore caret by character offset using the existing helpers.

Integration & deployment notes
- Deployment is static: push to `main` and use GitHub Pages (this project already includes a `CNAME`). No CI/build configured.
- Privacy: the app is explicitly client-side only; do not add server-side analytics without updating the README and privacy notice.

If anything is missing or unclear (for example, where the canonical list should live long-term, or if you want to remove duplication between `banned-words.html` and `banned-words.js`), tell me which approach you prefer and I can either:
- consolidate the list into a single file and update pages to import it, or
- keep duplication but add a small script to generate `banned-words.html` from `banned-words.js`.

Files referenced in examples: `index.html`, `replacer.html`, `banned-words.js`, `banned-words.html`, `CNAME`, `README.md`.

— End of copilot instructions —
