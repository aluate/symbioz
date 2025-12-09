# Audiobook Studio Module

Multi-actor voice system for Life OS.

## Features

- Book management
- Role/voice configuration
- Tagged script parsing
- Chapter management
- Audio render triggering (TTS integration in Phase 2)

## API Endpoints

### Books
- `GET /audio/books` - List all books
- `GET /audio/books/{book_slug}` - Get book metadata

### Audio Control
- `GET /audio/books/{book_slug}/control` - Get voice configuration
- `POST /audio/books/{book_slug}/control` - Update voice configuration

### Scripts
- `GET /audio/books/{book_slug}/script` - Get tagged script content
- `GET /audio/books/{book_slug}/chapters` - List all chapters
- `GET /audio/books/{book_slug}/chapters/{chapter_id}` - Get specific chapter

### Rendering
- `POST /audio/books/{book_slug}/render/{chapter_id}` - Trigger render
- `GET /audio/books/{book_slug}/renders/{chapter_id}` - Get render status
- `GET /audio/books/{book_slug}/renders/{chapter_id}/file` - Download audio file

## Data Structure

Books are stored in `residential_repo/content/books/{book_slug}/`:
- `manuscript.md` - Raw manuscript
- `script_tagged.md` - Role-tagged script
- `audio_control.yaml` - Voice configuration
- `notes.md` - Editing notes
- `renders/` - Generated audio files

## Usage Example

```python
from audio.service import AudioBookService

service = AudioBookService()

# List books
books = service.list_books()

# Get chapters
chapters = service.get_chapters("example_book")

# Get audio control
control = service.get_audio_control("example_book")

# Trigger render
status = service.trigger_render("example_book", "chapter-1")
```

## Integration

This module integrates with:
- **Life OS Backend** - Main API server
- **Life OS Frontend** - Audiobook Studio UI
- **Otto** - Automation for script tagging (Phase 2)
- **TTS API** - Audio generation (Phase 2)

## Phase 2 Features

- TTS API integration (ElevenLabs, etc.)
- Audio file stitching
- Real-time render progress
- Batch rendering
- Voice model management

