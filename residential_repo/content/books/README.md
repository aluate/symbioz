# Audiobook Content Directory

This directory contains book manuscripts, tagged scripts, and audio renders for the Audiobook Studio system.

## Structure

Each book gets its own folder named with a slug (e.g., `example_book`, `dark_cda_world`, etc.).

### Book Folder Contents

- `manuscript.md` - Raw manuscript text (no tags)
- `script_tagged.md` - Role-tagged script with stage directions
- `audio_control.yaml` - Voice model mappings and configuration
- `notes.md` - Editing notes taken while listening
- `renders/` - Generated audio files (MP3s per chapter)

## Example Book

The `example_book/` folder contains a template showing the expected format and structure.

## Adding a New Book

1. Create a new folder: `content/books/<book_slug>/`
2. Copy the structure from `example_book/`
3. Add your `manuscript.md`
4. Use Otto or manual editing to create `script_tagged.md`
5. Configure `audio_control.yaml` with your voice models
6. Start rendering chapters via Life OS Audiobook Studio

## Integration

This content is used by:
- **Life OS Audiobook Studio** - Web interface for managing books and renders
- **Otto** - Automation for script tagging and processing
- **Audio Engine** - Backend service for generating audio files

