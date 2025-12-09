# CONTROL – Audiobook Engine / Multi-Actor Voice System

**Owner:** Karl  
**Depends on:** Life OS app, Otto automation, external TTS/voice-clone API (e.g. ElevenLabs)  
**Status:** v0.1 – scaffolding

---

## 1. Purpose

Build an **Audiobook Studio** inside the Life OS app that can:

1. Convert my manuscripts into **role-tagged scripts** with stage directions.
2. Map each role (NARRATOR, DAD, BAD_GUY, MOM, LITTLE_GIRL, etc.) to a **voice model**.
3. Call an external **TTS / voice cloning API** to render audio per chapter.
4. Let me **listen while I edit**, drop notes, and re-render specific scenes/sections.
5. Support a future upgrade path to:
   - hybrid human + AI narration
   - pro studio production using the same script markup.

This is primarily an **editing tool** and Life OS feature first, and an eventual **distribution pipeline** second.

---

## 2. High-Level Architecture

### 2.1 Components

- **Life OS frontend**
  - New section: `Audiobook Studio`
  - Features:
    - Book picker
    - Role/character manager
    - Tagged script editor/viewer
    - Audio player w/ notes

- **Life OS backend**
  - API endpoints for:
    - listing books & chapters
    - reading/writing tagged scripts
    - reading/writing `audio_control.yaml`
    - triggering audio renders
    - serving rendered audio files

- **Audio Engine (service/module)**
  - Can live inside Life OS backend as a module.
  - Responsibilities:
    - Parse tagged script
    - For each line:
      - resolve role → voice model
      - send text + metadata to TTS API
    - Stitch segments into chapter-level MP3
    - Save to `content/books/<book_slug>/renders/`

- **Otto**
  - Automation + control-doc brain:
    - Turn raw manuscripts into role-tagged scripts.
    - Maintain `audio_control.yaml` skeletons per book.
    - Provide scripts to:
      - "Render all changed scenes since last edit"
      - "Update role tags based on character list"

---

## 3. Folder Structure

Target structure (within `residential_repo`):

```
residential_repo/
  control/
    CONTROL.md
    CONTROL_AUDIO.md

  apps/
    life_os/
      backend/
        # (Python/FastAPI or similar)
      frontend/
        # (Next/React – Life OS UI)
      ...

  content/
    books/
      example_book/
        manuscript.md          # raw text (no tags)
        script_tagged.md       # role-tagged & staged script
        audio_control.yaml     # role → voice mapping + defaults
        notes.md               # edit notes while listening (optional)
        renders/
          ch01.mp3
          ch02.mp3
          ...
```

`example_book` is a template folder. Each real book gets its own slug folder.

---

## 4. Data Formats

### 4.1 audio_control.yaml (per book)

Defines roles and their default voice models + behavior.

Separates content (script) from performance (voices, tone, pacing).

See template in `content/books/example_book/audio_control.yaml`.

### 4.2 script_tagged.md (per book)

Markdown script with inline role tags and optional stage directions.

Format guidelines:

- Each speech line starts with `[ROLE]` or `[ROLE, modifiers...]`
- Narration uses `[NARRATOR]`
- Stage directions in modifiers or on their own lines.

Example snippet:
```
[NARRATOR]
The wind curled around the ridge like a slow exhale.

[DAD, calm, slower]
"Son, you don't build a cabin to escape life. You build it to face it."

[BAD_GUY, low, cold]
"You really think you're still in control?"
```

---

## 5. Life OS – Audiobook Studio Features

### 5.1 MVP Features

**Book selection**
- List folders under `content/books/`
- CRUD basic book metadata (title, slug)

**Character / Role manager**
- Read/write `audio_control.yaml`
- Add/edit roles (NARRATOR, DAD, BAD_GUY, MOM, LITTLE_GIRL, etc.)
- Assign each role to:
  - a voice_model_id (from voice API)
  - default tone/pacing (optional)

**Script view**
- Load `script_tagged.md`
- Show segments grouped by chapter / scene
- (Nice to have) Simple editing UI for tags & directions

**Render controls**
- Button: "Render Chapter X"
- Button: "Re-render selected section"
- Show status: Pending → Rendering → Done
- When done, expose chapter MP3 URL to the frontend player

**Listening + Notes**
- Player for each rendered chapter
- Text area / comments tied to timestamps
- Append notes to `notes.md` or a per-book notes store in backend DB

---

## 6. Audio Engine Requirements

### 6.1 External API (initial assumption)

Use something like ElevenLabs (or similar TTS/voice clone API).

Config via environment variables:
- `AUDIO_API_BASE_URL`
- `AUDIO_API_KEY`

### 6.2 Rendering Pipeline (per chapter)

Backend receives request:
- `book_slug`
- `chapter_id` (or index)

Load:
- `content/books/<book_slug>/script_tagged.md`
- `content/books/<book_slug>/audio_control.yaml`

Extract relevant chapter section.

Parse line by line:
- Get role + modifiers + text.
- Resolve role → voice_model_id (with defaults from YAML).

For each line / chunk:
- Call TTS API to generate audio snippet.

Stitch snippets into a single chapter MP3.

Save as:
- `content/books/<book_slug>/renders/chXX.mp3`

Return metadata for frontend:
- file path / URL
- duration
- optional markers per line/segment

---

## 7. Otto Integration

Otto tasks to implement later:

**Manuscript → script_tagged.md**
- Input: `manuscript.md` or Google Doc export
- Output:
  - `script_tagged.md` with [NARRATOR] and character tags
  - initial `audio_control.yaml` with discovered roles

**Smart tagging**
- Use dialogue patterns ("..." + "he said") to infer roles.
- Insert [DAD], [BAD_GUY], etc. based on a character map.

**Selective re-render**
- Track changed scenes/lines
- Trigger the audio engine only for those sections
- Update per-chapter renders incrementally

---

## 8. Constraints / Decisions

- Primary goal: internal listening and editing, not immediate retail distribution.
- Synthetic narration is fine internally and for direct/private distribution.
- If/when we target Audible/ACX:
  - We can re-use the same scripts + stage directions
  - Swap the "renderer" from TTS → human studio.

---

## 9. Dev Instructions for Cursor

When running in Cursor:

**Create file structure:**
- Ensure `content/books/example_book/` exists with:
  - `manuscript.md`
  - `script_tagged.md`
  - `audio_control.yaml`
  - `renders/` folder

**Life OS backend:**
- Add endpoints under something like `/api/audio`:
  - `GET /api/audio/books` – list books
  - `GET /api/audio/books/{book_slug}` – get book metadata & roles
  - `GET /api/audio/books/{book_slug}/script` – fetch tagged script
  - `POST /api/audio/books/{book_slug}/render/{chapter_id}` – trigger render
  - `GET /api/audio/books/{book_slug}/renders/{chapter_id}` – get audio file URL / metadata

**Audio engine module:**
- Implement an internal `audio_engine` module:
  - Parse `script_tagged.md`
  - Resolve roles from `audio_control.yaml`
  - Call TTS API (mock for now if no API key)
  - Stitch audio segments
  - Save MP3 files

**For now:**
- Have a mock that just creates silent audio or placeholder files first.
- Focus on the data model and API structure.
- TTS integration can come later when API keys are available.

Follow the design and intent of this control document. Do not overbuild; this is v0.1 scaffolding for internal use.

