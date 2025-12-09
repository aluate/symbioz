"""
Otto Memory API - Long-term memory management
Phase 3 Extension — CONTROL_OTTO_LONG_TERM_MEMORY.md
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict
from pydantic import BaseModel
from datetime import datetime

from database import get_db
from models import OttoMemory, OttoMemoryHistory, OttoMemoryLink
from otto.context import get_default_context

router = APIRouter(prefix="/otto/memory", tags=["otto_memory"])


class MemoryCreate(BaseModel):
    category: str
    content: str
    tags: Optional[List[str]] = None
    source: str = "user"  # "user", "otto_inference", "task", or "system"
    confidence_score: float = 1.0


class MemoryUpdate(BaseModel):
    content: Optional[str] = None
    tags: Optional[List[str]] = None
    confidence_score: Optional[float] = None
    expires_at: Optional[datetime] = None  # Phase 4
    is_stale: Optional[bool] = None  # Phase 4
    stale_reason: Optional[str] = None  # Phase 4


class MemoryResponse(BaseModel):
    id: int
    household_id: int
    category: str
    content: str
    tags: Optional[List[str]]
    source: str
    created_at: datetime
    updated_at: datetime
    last_used_at: Optional[datetime]
    usage_count: int
    confidence_score: float
    version: int
    expires_at: Optional[datetime] = None  # Phase 4
    is_stale: bool = False  # Phase 4
    stale_reason: Optional[str] = None  # Phase 4
    
    class Config:
        from_attributes = True


class MemoryUseRequest(BaseModel):
    id: Optional[int] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None


@router.post("", response_model=MemoryResponse)
def create_memory(
    memory: MemoryCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new memory entry.
    
    Safety: Tier 2 (requires approval if source is "otto_inference")
    """
    otto_context = get_default_context(db)
    
    new_memory = OttoMemory(
        household_id=otto_context.household_id,
        category=memory.category,
        content=memory.content,
        tags=memory.tags,
        source=memory.source,
        confidence_score=memory.confidence_score,
        version=1
    )
    
    db.add(new_memory)
    db.commit()
    db.refresh(new_memory)
    
    return new_memory


@router.get("", response_model=List[MemoryResponse])
def list_memories(
    category: Optional[str] = Query(None, description="Filter by category"),
    tags: Optional[str] = Query(None, description="Comma-separated tags"),
    source: Optional[str] = Query(None, description="Filter by source"),
    is_stale: Optional[bool] = Query(None, description="Filter by stale status"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """List memories with optional filters"""
    otto_context = get_default_context(db)
    
    query = db.query(OttoMemory).filter(
        OttoMemory.household_id == otto_context.household_id
    )
    
    if category:
        query = query.filter(OttoMemory.category == category)
    
    if tags:
        tag_list = [t.strip() for t in tags.split(",")]
        # Filter by tags (tags is JSON array)
        for tag in tag_list:
            query = query.filter(OttoMemory.tags.contains([tag]))
    
    if source:
        query = query.filter(OttoMemory.source == source)
    
    if is_stale is not None:
        query = query.filter(OttoMemory.is_stale == is_stale)
    
    memories = query.order_by(OttoMemory.created_at.desc()).offset(offset).limit(limit).all()
    return memories


@router.get("/search", response_model=List[MemoryResponse])
def search_memories(
    q: Optional[str] = Query(None, description="Text search in content"),
    category: Optional[str] = Query(None, description="Filter by category"),
    tag: Optional[str] = Query(None, description="Filter by single tag"),
    source: Optional[str] = Query(None, description="Filter by source"),
    is_stale: Optional[bool] = Query(None, description="Filter by stale status"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """
    Search memories with simple SQL-based text search.
    
    Phase 4 — Simple search, no embeddings/vector search.
    """
    otto_context = get_default_context(db)
    
    query = db.query(OttoMemory).filter(
        OttoMemory.household_id == otto_context.household_id
    )
    
    # Text search on content
    if q:
        query = query.filter(OttoMemory.content.contains(q))
    
    if category:
        query = query.filter(OttoMemory.category == category)
    
    if tag:
        query = query.filter(OttoMemory.tags.contains([tag]))
    
    if source:
        query = query.filter(OttoMemory.source == source)
    
    if is_stale is not None:
        query = query.filter(OttoMemory.is_stale == is_stale)
    
    memories = query.order_by(OttoMemory.created_at.desc()).offset(offset).limit(limit).all()
    return memories


@router.get("/{memory_id}", response_model=MemoryResponse)
def get_memory(
    memory_id: int,
    db: Session = Depends(get_db)
):
    """Get a single memory entry by ID"""
    otto_context = get_default_context(db)
    
    memory = db.query(OttoMemory).filter(
        OttoMemory.id == memory_id,
        OttoMemory.household_id == otto_context.household_id
    ).first()
    
    if not memory:
        raise HTTPException(status_code=404, detail=f"Memory {memory_id} not found")
    
    return memory


@router.patch("/{memory_id}", response_model=MemoryResponse)
def update_memory(
    memory_id: int,
    updates: MemoryUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a memory entry.
    
    Behavior:
    - Increments version
    - Updates updated_at
    - Optionally archives previous version (Phase 4)
    
    Safety: Tier 2 (requires approval)
    """
    otto_context = get_default_context(db)
    
    memory = db.query(OttoMemory).filter(
        OttoMemory.id == memory_id,
        OttoMemory.household_id == otto_context.household_id
    ).first()
    
    if not memory:
        raise HTTPException(status_code=404, detail=f"Memory {memory_id} not found")
    
    # Phase 4: Create history entry before updating
    history_entry = OttoMemoryHistory(
        memory_id=memory.id,
        household_id=memory.household_id,
        version=memory.version,
        category=memory.category,
        content=memory.content,
        tags=memory.tags,
        source=memory.source,
        changed_by="API"  # Could be enhanced with user context
    )
    db.add(history_entry)
    
    # Update fields
    if updates.content is not None:
        memory.content = updates.content
    if updates.tags is not None:
        memory.tags = updates.tags
    if updates.confidence_score is not None:
        memory.confidence_score = updates.confidence_score
    if updates.expires_at is not None:
        memory.expires_at = updates.expires_at
    if updates.is_stale is not None:
        memory.is_stale = updates.is_stale
    if updates.stale_reason is not None:
        memory.stale_reason = updates.stale_reason
    
    # Increment version
    memory.version += 1
    memory.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(memory)
    
    return memory


@router.post("/use", response_model=List[MemoryResponse])
def mark_memory_used(
    request: MemoryUseRequest,
    db: Session = Depends(get_db)
):
    """
    Mark memory as "used".
    
    Behavior:
    - Increments usage_count
    - Sets last_used_at to now
    - Updates all matching entries if query-based
    
    Safety: Tier 1 (read-only operation, just tracking)
    """
    otto_context = get_default_context(db)
    
    query = db.query(OttoMemory).filter(
        OttoMemory.household_id == otto_context.household_id
    )
    
    if request.id:
        query = query.filter(OttoMemory.id == request.id)
    if request.category:
        query = query.filter(OttoMemory.category == request.category)
    if request.tags:
        for tag in request.tags:
            query = query.filter(OttoMemory.tags.contains([tag]))
    
    memories = query.all()
    
    now = datetime.utcnow()
    for memory in memories:
        memory.usage_count += 1
        memory.last_used_at = now
    
    db.commit()
    
    return memories


@router.delete("/{memory_id}")
def delete_memory(
    memory_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a memory entry.
    
    Phase 4: Creates final history entry before deletion.
    
    Safety: Tier 2 (requires approval)
    """
    otto_context = get_default_context(db)
    
    memory = db.query(OttoMemory).filter(
        OttoMemory.id == memory_id,
        OttoMemory.household_id == otto_context.household_id
    ).first()
    
    if not memory:
        raise HTTPException(status_code=404, detail=f"Memory {memory_id} not found")
    
    # Phase 4: Create final history entry before deletion
    history_entry = OttoMemoryHistory(
        memory_id=memory.id,
        household_id=memory.household_id,
        version=memory.version,
        category=memory.category,
        content=memory.content,
        tags=memory.tags,
        source=memory.source,
        changed_by="API"
    )
    db.add(history_entry)
    
    db.delete(memory)
    db.commit()
    
    return {"message": f"Memory {memory_id} deleted"}


@router.get("/{memory_id}/history", response_model=List[Dict])
def get_memory_history(
    memory_id: int,
    db: Session = Depends(get_db)
):
    """
    Get version history for a memory entry.
    
    Phase 4 — Returns list of historical versions.
    """
    otto_context = get_default_context(db)
    
    # Verify memory exists and belongs to household
    memory = db.query(OttoMemory).filter(
        OttoMemory.id == memory_id,
        OttoMemory.household_id == otto_context.household_id
    ).first()
    
    if not memory:
        raise HTTPException(status_code=404, detail=f"Memory {memory_id} not found")
    
    # Get history entries
    history = db.query(OttoMemoryHistory).filter(
        OttoMemoryHistory.memory_id == memory_id
    ).order_by(OttoMemoryHistory.version.desc()).all()
    
    return [
        {
            "id": h.id,
            "version": h.version,
            "category": h.category,
            "content": h.content,
            "tags": h.tags,
            "source": h.source,
            "created_at": h.created_at.isoformat(),
            "changed_by": h.changed_by
        }
        for h in history
    ]


@router.get("/{memory_id}/history/{version}", response_model=Dict)
def get_memory_history_version(
    memory_id: int,
    version: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific historical version of a memory entry.
    
    Phase 4 — Returns single historical version.
    """
    otto_context = get_default_context(db)
    
    # Verify memory exists and belongs to household
    memory = db.query(OttoMemory).filter(
        OttoMemory.id == memory_id,
        OttoMemory.household_id == otto_context.household_id
    ).first()
    
    if not memory:
        raise HTTPException(status_code=404, detail=f"Memory {memory_id} not found")
    
    # Get specific history entry
    history = db.query(OttoMemoryHistory).filter(
        OttoMemoryHistory.memory_id == memory_id,
        OttoMemoryHistory.version == version
    ).first()
    
    if not history:
        raise HTTPException(status_code=404, detail=f"Version {version} not found for memory {memory_id}")
    
    return {
        "id": history.id,
        "memory_id": history.memory_id,
        "version": history.version,
        "category": history.category,
        "content": history.content,
        "tags": history.tags,
        "source": history.source,
        "created_at": history.created_at.isoformat(),
        "changed_by": history.changed_by
    }


class MemoryLinkCreate(BaseModel):
    to_memory_id: Optional[int] = None
    target_type: str  # "task", "bill", "transaction", "event", "memory"
    target_id: int
    relationship_type: str  # "supports", "contradicts", "refines", "applies_to", etc.
    notes: Optional[str] = None


class MemoryLinkResponse(BaseModel):
    id: int
    from_memory_id: int
    to_memory_id: Optional[int]
    target_type: str
    target_id: int
    relationship_type: str
    notes: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


@router.post("/{memory_id}/links", response_model=MemoryLinkResponse)
def create_memory_link(
    memory_id: int,
    link: MemoryLinkCreate,
    db: Session = Depends(get_db)
):
    """
    Create a link from a memory to another memory or domain object.
    
    Phase 4 — Memory relationships.
    """
    otto_context = get_default_context(db)
    
    # Verify memory exists and belongs to household
    memory = db.query(OttoMemory).filter(
        OttoMemory.id == memory_id,
        OttoMemory.household_id == otto_context.household_id
    ).first()
    
    if not memory:
        raise HTTPException(status_code=404, detail=f"Memory {memory_id} not found")
    
    # If linking to another memory, set to_memory_id
    to_memory_id = link.to_memory_id
    if link.target_type == "memory":
        to_memory_id = link.target_id
    
    new_link = OttoMemoryLink(
        from_memory_id=memory_id,
        to_memory_id=to_memory_id,
        target_type=link.target_type,
        target_id=link.target_id,
        relationship_type=link.relationship_type,
        notes=link.notes
    )
    
    db.add(new_link)
    db.commit()
    db.refresh(new_link)
    
    return new_link


@router.get("/{memory_id}/links", response_model=List[MemoryLinkResponse])
def get_memory_links(
    memory_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all links from a memory entry.
    
    Phase 4 — Memory relationships.
    """
    otto_context = get_default_context(db)
    
    # Verify memory exists and belongs to household
    memory = db.query(OttoMemory).filter(
        OttoMemory.id == memory_id,
        OttoMemory.household_id == otto_context.household_id
    ).first()
    
    if not memory:
        raise HTTPException(status_code=404, detail=f"Memory {memory_id} not found")
    
    links = db.query(OttoMemoryLink).filter(
        OttoMemoryLink.from_memory_id == memory_id
    ).all()
    
    return links


@router.delete("/links/{link_id}")
def delete_memory_link(
    link_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a memory link.
    
    Phase 4 — Memory relationships.
    """
    otto_context = get_default_context(db)
    
    link = db.query(OttoMemoryLink).filter(
        OttoMemoryLink.id == link_id
    ).first()
    
    if not link:
        raise HTTPException(status_code=404, detail=f"Link {link_id} not found")
    
    # Verify memory belongs to household
    memory = db.query(OttoMemory).filter(
        OttoMemory.id == link.from_memory_id,
        OttoMemory.household_id == otto_context.household_id
    ).first()
    
    if not memory:
        raise HTTPException(status_code=404, detail=f"Memory not found or access denied")
    
    db.delete(link)
    db.commit()
    
    return {"message": f"Link {link_id} deleted"}

