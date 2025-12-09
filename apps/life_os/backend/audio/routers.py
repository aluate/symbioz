"""
Audiobook Studio API routes
"""

from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pathlib import Path

from .models import Book, AudioControl, Chapter, RenderRequest, RenderStatus
from .service import AudioBookService

router = APIRouter(prefix="/audio", tags=["audio"])

# Initialize service
# In production, this would use environment variable or config
CONTENT_ROOT = Path(__file__).resolve().parents[4] / "residential_repo" / "content"
audio_service = AudioBookService(content_root=str(CONTENT_ROOT))


@router.get("/books")
async def list_books() -> List[Book]:
    """List all available books"""
    return audio_service.list_books()


@router.get("/books/{book_slug}")
async def get_book(book_slug: str) -> Book:
    """Get book metadata"""
    book = audio_service.get_book(book_slug)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.get("/books/{book_slug}/control")
async def get_audio_control(book_slug: str) -> AudioControl:
    """Get audio control configuration for a book"""
    control = audio_service.get_audio_control(book_slug)
    if not control:
        raise HTTPException(status_code=404, detail="Audio control not found")
    return control


@router.post("/books/{book_slug}/control")
async def update_audio_control(book_slug: str, control: AudioControl) -> dict:
    """Update audio control configuration"""
    success = audio_service.update_audio_control(book_slug, control)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to update audio control")
    return {"success": True, "message": "Audio control updated"}


@router.get("/books/{book_slug}/script")
async def get_script(book_slug: str) -> dict:
    """Get tagged script content"""
    script = audio_service.get_tagged_script(book_slug)
    if script is None:
        raise HTTPException(status_code=404, detail="Script not found")
    return {"content": script}


@router.get("/books/{book_slug}/chapters")
async def list_chapters(book_slug: str) -> List[Chapter]:
    """List all chapters for a book"""
    chapters = audio_service.get_chapters(book_slug)
    if not chapters:
        raise HTTPException(status_code=404, detail="No chapters found")
    return chapters


@router.get("/books/{book_slug}/chapters/{chapter_id}")
async def get_chapter(book_slug: str, chapter_id: str) -> Chapter:
    """Get a specific chapter"""
    chapter = audio_service.get_chapter(book_slug, chapter_id)
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return chapter


@router.post("/books/{book_slug}/render/{chapter_id}")
async def trigger_render(book_slug: str, chapter_id: str) -> RenderStatus:
    """Trigger audio render for a chapter"""
    return audio_service.trigger_render(book_slug, chapter_id)


@router.get("/books/{book_slug}/renders/{chapter_id}")
async def get_render_status(book_slug: str, chapter_id: str) -> RenderStatus:
    """Get render status and file info"""
    return audio_service.check_render_status(book_slug, chapter_id)


@router.get("/books/{book_slug}/renders/{chapter_id}/file")
async def get_render_file(book_slug: str, chapter_id: str):
    """Serve the rendered audio file"""
    from fastapi.responses import FileResponse
    
    status = audio_service.check_render_status(book_slug, chapter_id)
    if status.status != "done" or not status.file_path:
        raise HTTPException(status_code=404, detail="Render not found or not complete")
    
    file_path = Path(status.file_path)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Audio file not found")
    
    return FileResponse(
        path=file_path,
        media_type="audio/mpeg",
        filename=f"{chapter_id}.mp3"
    )

