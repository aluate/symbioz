"""
Audiobook service - handles book management and audio operations
"""

from pathlib import Path
from typing import List, Optional, Dict, Any
import yaml
import re
from datetime import datetime

from .models import Book, Role, AudioControl, ScriptSegment, Chapter, RenderStatus


class AudioBookService:
    """Service for managing audiobooks"""
    
    def __init__(self, content_root: str = "residential_repo/content/books"):
        self.content_root = Path(content_root)
        self.books_dir = self.content_root / "books"
        self.books_dir.mkdir(parents=True, exist_ok=True)
    
    def list_books(self) -> List[Book]:
        """List all books"""
        books = []
        if not self.books_dir.exists():
            return books
        
        for book_dir in self.books_dir.iterdir():
            if book_dir.is_dir() and not book_dir.name.startswith('.'):
                # Try to read metadata or use directory name
                books.append(Book(
                    slug=book_dir.name,
                    title=book_dir.name.replace('-', ' ').title(),
                    updated_at=datetime.fromtimestamp(book_dir.stat().st_mtime)
                ))
        
        return books
    
    def get_book(self, book_slug: str) -> Optional[Book]:
        """Get book metadata"""
        book_dir = self.books_dir / book_slug
        if not book_dir.exists():
            return None
        
        return Book(
            slug=book_slug,
            title=book_slug.replace('-', ' ').title(),
            updated_at=datetime.fromtimestamp(book_dir.stat().st_mtime)
        )
    
    def get_audio_control(self, book_slug: str) -> Optional[AudioControl]:
        """Load audio control configuration"""
        control_file = self.books_dir / book_slug / "audio_control.yaml"
        if not control_file.exists():
            return None
        
        with open(control_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f) or {}
        
        roles = {}
        if 'roles' in data:
            for role_name, role_data in data['roles'].items():
                roles[role_name] = Role(
                    name=role_name,
                    **role_data
                )
        
        return AudioControl(
            roles=roles,
            modifiers=data.get('modifiers', {}),
            defaults=data.get('defaults', {})
        )
    
    def update_audio_control(self, book_slug: str, control: AudioControl) -> bool:
        """Update audio control configuration"""
        control_file = self.books_dir / book_slug / "audio_control.yaml"
        control_file.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            'roles': {
                name: role.dict(exclude={'name'}, exclude_none=True)
                for name, role in control.roles.items()
            },
            'modifiers': control.modifiers,
            'defaults': control.defaults
        }
        
        with open(control_file, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)
        
        return True
    
    def get_tagged_script(self, book_slug: str) -> Optional[str]:
        """Get the tagged script content"""
        script_file = self.books_dir / book_slug / "script_tagged.md"
        if not script_file.exists():
            return None
        
        with open(script_file, 'r', encoding='utf-8') as f:
            return f.read()
    
    def parse_script_segments(self, script_content: str) -> List[Chapter]:
        """Parse tagged script into chapters and segments"""
        chapters = []
        current_chapter = None
        current_segments = []
        line_number = 0
        
        for line in script_content.split('\n'):
            line_number += 1
            line = line.strip()
            
            # Check for chapter header
            if line.startswith('## '):
                # Save previous chapter
                if current_chapter:
                    current_chapter.segments = current_segments
                    chapters.append(current_chapter)
                
                # Start new chapter
                chapter_title = line[3:].strip()
                current_chapter = Chapter(
                    id=chapter_title.lower().replace(' ', '-'),
                    title=chapter_title,
                    segments=[]
                )
                current_segments = []
            
            # Check for role tag
            elif line.startswith('[') and ']' in line:
                role_match = re.match(r'\[([^\]]+)\]', line)
                if role_match:
                    role_spec = role_match.group(1)
                    parts = [p.strip() for p in role_spec.split(',')]
                    role = parts[0]
                    modifiers = parts[1:] if len(parts) > 1 else []
                    
                    # Get text after tag (next line or rest of line)
                    text = line[role_match.end():].strip()
                    if not text:
                        continue
                    
                    segment = ScriptSegment(
                        role=role,
                        modifiers=modifiers,
                        text=text,
                        line_number=line_number
                    )
                    current_segments.append(segment)
            
            # Regular text (narration continuation)
            elif line and current_segments:
                # Append to last segment if it exists
                if current_segments:
                    current_segments[-1].text += ' ' + line
        
        # Add last chapter
        if current_chapter:
            current_chapter.segments = current_segments
            chapters.append(current_chapter)
        
        return chapters
    
    def get_chapters(self, book_slug: str) -> List[Chapter]:
        """Get all chapters for a book"""
        script_content = self.get_tagged_script(book_slug)
        if not script_content:
            return []
        
        return self.parse_script_segments(script_content)
    
    def get_chapter(self, book_slug: str, chapter_id: str) -> Optional[Chapter]:
        """Get a specific chapter"""
        chapters = self.get_chapters(book_slug)
        return next((ch for ch in chapters if ch.id == chapter_id), None)
    
    def check_render_status(self, book_slug: str, chapter_id: str) -> RenderStatus:
        """Check if a chapter has been rendered"""
        render_file = self.books_dir / book_slug / "renders" / f"{chapter_id}.mp3"
        
        if render_file.exists():
            return RenderStatus(
                book_slug=book_slug,
                chapter_id=chapter_id,
                status="done",
                file_path=str(render_file),
                created_at=datetime.fromtimestamp(render_file.stat().st_mtime)
            )
        else:
            return RenderStatus(
                book_slug=book_slug,
                chapter_id=chapter_id,
                status="pending"
            )
    
    def trigger_render(self, book_slug: str, chapter_id: str) -> RenderStatus:
        """
        Trigger audio render for a chapter.
        For now, this is a placeholder that will be implemented with TTS API.
        """
        # In Phase 2, this will:
        # 1. Load script and audio_control
        # 2. Parse segments
        # 3. Call TTS API for each segment
        # 4. Stitch audio files
        # 5. Save to renders/ directory
        
        # For now, return pending status
        return RenderStatus(
            book_slug=book_slug,
            chapter_id=chapter_id,
            status="pending",
            error="TTS API integration coming in Phase 2"
        )

