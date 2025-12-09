# 📘 Universal Book Repo Bootstrap – Cursor Prompt

You are an AI inside Cursor.
Your job is to **create a complete, generic book-writing repository structure** using ONLY the parameters I give you.

This template must work for **any** book, regardless of genre, tone, or structure.

---

## 📌 INPUT PARAMETERS
I will provide these when running this template:

- **BOOK_SLUG** — folder-safe name (e.g., `ironforge`, `mountain-systems`)
- **BOOK_TITLE** — display title
- **CHAPTER_COUNT** — integer (e.g., 12, 17, 24)

You MUST generate everything from these three values only.

---

## 📦 ROOT DIRECTORY
Create:

```
books/
  {{BOOK_SLUG}}/
```

Everything goes inside that folder.

---

## 📚 1. CORE (Foundational Thinking)

Create:

```
books/{{BOOK_SLUG}}/core/
```

Inside it, create these EMPTY or minimally initialized generic files:

- `concept.md`
- `audience.md`
- `working-outline.md`
- `global-beats.md`
- `voice-guide.md`
- `metaphor-guide.md`
- `story-bank.md`
- `reference-notes.md`

Each file should contain ONLY:

```
# <Human-readable Title>
(Empty template – fill during book development)
```

---

## 🧩 2. CHAPTERS (Automated by CHAPTER_COUNT)

Create:

```
books/{{BOOK_SLUG}}/chapters/
```

Then generate folders:

- `intro/`
- `outro/`
- AND a numbered series based on CHAPTER_COUNT
  (`ch01/`, `ch02/`, … up to the count)

Inside *each* chapter folder, create:

- `beats.md`
- `scaffold.md`
- `draft.md`
- `revisions.md`
- `notes.md`

Each file contains ONLY:

```
# <File Title>
(Empty template)
```

---

## 🎭 3. JOKES (Optional Humor Assets)

```
books/{{BOOK_SLUG}}/jokes/
  one-liners.md
  callbacks.md
  ideas.md
```

Each file:

```
# <Title>
(Empty)
```

---

## 🪦 4. BONEYARD (Cut Material)

```
books/{{BOOK_SLUG}}/boneyard/
  paragraphs.md
  sections.md
  ideas.md
  experiments.md
```

Each file:

```
# <Title>
(Empty)
```

---

## 🏷️ 5. PUBLISHING (External-Facing Materials)

```
books/{{BOOK_SLUG}}/publishing/
  synopsis.md
  long-synopsis.md
  query-letter.md
  comps.md
  marketing-plan.md
  formatting-notes.md
  proposal.md
```

All empty templates.

---

## 🗂️ 6. ADMIN (Process, Logs, Meta)

```
books/{{BOOK_SLUG}}/admin/
  punchlist.md
  revision-log.md
  version-history.md
  meeting-notes.md
```

All empty templates.

---

## 🎨 7. ASSETS (Visuals)

```
books/{{BOOK_SLUG}}/assets/
  diagrams/
  illustrations/
  mockups/
```

Folders only.

---

## 🧰 8. PROMPTS (Reusable AI Helpers)

```
books/{{BOOK_SLUG}}/prompts/
  chapter-from-beats.prompt.md
  beat-to-scaffold.prompt.md
  voice-check.prompt.md
  metaphor-inject.prompt.md
```

Each file contains:

```
# <Prompt Template>
(Empty – user will fill in)
```

---

## 🛠️ 9. TOOLS (Optional Utility Scripts)

```
books/{{BOOK_SLUG}}/tools/
  combine-book.py
  extract-beats.py
  revision-diff.py
```

Each script begins with:

```python
"""
Utility script template.
Book: {{BOOK_TITLE}} ({{BOOK_SLUG}})
Empty stub.
"""
```

---

## ✔️ FINAL ACTIONS

When all generation is complete:

1. Print a final **directory tree** of everything created
2. List any files that already existed and were skipped
3. Do **not** invent additional files or structure
4. Do **not** add book-specific content
5. Follow the structure exactly
