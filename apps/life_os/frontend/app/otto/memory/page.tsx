"use client";

import { useState, useEffect } from "react";
import Link from "next/link";

interface Memory {
  id: number;
  category: string;
  content: string;
  tags: string[] | null;
  source: string;
  created_at: string;
  updated_at: string;
  last_used_at: string | null;
  usage_count: number;
  confidence_score: number;
  version: number;
  expires_at: string | null;
  is_stale: boolean;
  stale_reason: string | null;
}

interface MemoryHistory {
  id: number;
  version: number;
  category: string;
  content: string;
  tags: string[] | null;
  source: string;
  created_at: string;
  changed_by: string | null;
}

interface MemoryLink {
  id: number;
  from_memory_id: number;
  to_memory_id: number | null;
  target_type: string;
  target_id: number;
  relationship_type: string;
  notes: string | null;
  created_at: string;
}

export default function MemoryConsole() {
  const [memories, setMemories] = useState<Memory[]>([]);
  const [activeMemory, setActiveMemory] = useState<Memory | null>(null);
  const [history, setHistory] = useState<MemoryHistory[]>([]);
  const [links, setLinks] = useState<MemoryLink[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  // Filters
  const [searchQuery, setSearchQuery] = useState("");
  const [categoryFilter, setCategoryFilter] = useState<string>("");
  const [tagFilter, setTagFilter] = useState<string>("");
  const [sourceFilter, setSourceFilter] = useState<string>("");
  const [staleFilter, setStaleFilter] = useState<string>(""); // "all", "active", "stale"
  
  // Edit mode
  const [isEditing, setIsEditing] = useState(false);
  const [editContent, setEditContent] = useState("");
  const [editTags, setEditTags] = useState("");

  // Get API base URL
  const getApiUrl = () => {
    if (typeof window !== "undefined") {
      return `${window.location.protocol}//${window.location.hostname}:8000`;
    }
    return "http://localhost:8000";
  };

  // Fetch memories with filters
  const fetchMemories = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const params = new URLSearchParams();
      if (searchQuery) params.append("q", searchQuery);
      if (categoryFilter) params.append("category", categoryFilter);
      if (tagFilter) params.append("tag", tagFilter);
      if (sourceFilter) params.append("source", sourceFilter);
      if (staleFilter === "active") params.append("is_stale", "false");
      if (staleFilter === "stale") params.append("is_stale", "true");
      params.append("limit", "100");
      
      const url = searchQuery 
        ? `${getApiUrl()}/otto/memory/search?${params.toString()}`
        : `${getApiUrl()}/otto/memory?${params.toString()}`;
      
      const response = await fetch(url);
      if (!response.ok) throw new Error("Failed to fetch memories");
      const data = await response.json();
      setMemories(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to fetch memories");
    } finally {
      setLoading(false);
    }
  };

  // Fetch memory details (history + links)
  const fetchMemoryDetails = async (memoryId: number) => {
    try {
      // Fetch history
      const historyResponse = await fetch(`${getApiUrl()}/otto/memory/${memoryId}/history`);
      if (historyResponse.ok) {
        const historyData = await historyResponse.json();
        setHistory(historyData);
      }
      
      // Fetch links
      const linksResponse = await fetch(`${getApiUrl()}/otto/memory/${memoryId}/links`);
      if (linksResponse.ok) {
        const linksData = await linksResponse.json();
        setLinks(linksData);
      }
    } catch (err) {
      console.error("Error fetching memory details:", err);
    }
  };

  // Update memory
  const updateMemory = async () => {
    if (!activeMemory) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const tagsArray = editTags.split(",").map(t => t.trim()).filter(t => t);
      
      const response = await fetch(`${getApiUrl()}/otto/memory/${activeMemory.id}`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          content: editContent,
          tags: tagsArray.length > 0 ? tagsArray : null,
        }),
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to update memory");
      }
      
      const updated = await response.json();
      setActiveMemory(updated);
      setIsEditing(false);
      await fetchMemories();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to update memory");
    } finally {
      setLoading(false);
    }
  };

  // Mark memory as stale
  const markStale = async (memoryId: number, reason: string) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch(`${getApiUrl()}/otto/actions`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          actions: [{
            type: "memory.mark_stale",
            payload: {
              memory_id: memoryId,
              reason: reason,
            },
          }],
        }),
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to mark memory as stale");
      }
      
      await fetchMemories();
      if (activeMemory?.id === memoryId) {
        await fetchMemoryDetails(memoryId);
        const updated = memories.find(m => m.id === memoryId);
        if (updated) setActiveMemory({ ...updated, is_stale: true, stale_reason: reason });
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to mark memory as stale");
    } finally {
      setLoading(false);
    }
  };

  // Set expiration
  const setExpiration = async (memoryId: number, expiresAt: string) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch(`${getApiUrl()}/otto/actions`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          actions: [{
            type: "memory.set_expiration",
            payload: {
              memory_id: memoryId,
              expires_at: expiresAt,
            },
          }],
        }),
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to set expiration");
      }
      
      await fetchMemories();
      if (activeMemory?.id === memoryId) {
        await fetchMemoryDetails(memoryId);
        const updated = memories.find(m => m.id === memoryId);
        if (updated) setActiveMemory({ ...updated, expires_at: expiresAt });
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to set expiration");
    } finally {
      setLoading(false);
    }
  };

  // Handle memory selection
  const handleMemorySelect = (memory: Memory) => {
    setActiveMemory(memory);
    setIsEditing(false);
    fetchMemoryDetails(memory.id);
  };

  // Start editing
  const handleEdit = () => {
    if (activeMemory) {
      setEditContent(activeMemory.content);
      setEditTags(activeMemory.tags?.join(", ") || "");
      setIsEditing(true);
    }
  };

  // Initial load
  useEffect(() => {
    fetchMemories();
  }, []);

  // Format timestamp
  const formatTime = (timestamp: string) => {
    const date = new Date(timestamp);
    return date.toLocaleString();
  };

  return (
    <div style={{ padding: "1rem", maxWidth: "1600px", margin: "0 auto" }}>
      <div style={{ marginBottom: "1rem", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <h1 style={{ fontSize: "1.75rem", margin: 0 }}>Otto Memory Console</h1>
        <Link
          href="/otto"
          style={{
            padding: "0.5rem 1rem",
            backgroundColor: "#81D8D0",
            color: "white",
            textDecoration: "none",
            borderRadius: "4px",
            fontSize: "0.9rem",
          }}
        >
          ← Back to Otto Console
        </Link>
      </div>

      {error && (
        <div
          style={{
            marginBottom: "1rem",
            padding: "0.75rem",
            backgroundColor: "#ffebee",
            border: "1px solid #f44336",
            borderRadius: "4px",
            color: "#c62828",
          }}
        >
          {error}
        </div>
      )}

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "minmax(300px, 1fr) minmax(500px, 2fr)",
          gap: "1rem",
          minHeight: "600px",
        }}
      >
        {/* Left column: Filters + Memory list */}
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            gap: "1rem",
          }}
        >
          {/* Filters */}
          <div
            style={{
              border: "1px solid #ccc",
              borderRadius: "4px",
              padding: "1rem",
              backgroundColor: "#f9f9f9",
            }}
          >
            <h3 style={{ marginTop: 0, fontSize: "1rem" }}>Filters</h3>
            
            <div style={{ marginBottom: "0.75rem" }}>
              <label style={{ display: "block", fontSize: "0.85rem", marginBottom: "0.25rem" }}>Search:</label>
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search content..."
                style={{
                  width: "100%",
                  padding: "0.5rem",
                  border: "1px solid #ccc",
                  borderRadius: "4px",
                }}
              />
            </div>
            
            <div style={{ marginBottom: "0.75rem" }}>
              <label style={{ display: "block", fontSize: "0.85rem", marginBottom: "0.25rem" }}>Category:</label>
              <input
                type="text"
                value={categoryFilter}
                onChange={(e) => setCategoryFilter(e.target.value)}
                placeholder="e.g., preference"
                style={{
                  width: "100%",
                  padding: "0.5rem",
                  border: "1px solid #ccc",
                  borderRadius: "4px",
                }}
              />
            </div>
            
            <div style={{ marginBottom: "0.75rem" }}>
              <label style={{ display: "block", fontSize: "0.85rem", marginBottom: "0.25rem" }}>Tag:</label>
              <input
                type="text"
                value={tagFilter}
                onChange={(e) => setTagFilter(e.target.value)}
                placeholder="e.g., reminder_pattern"
                style={{
                  width: "100%",
                  padding: "0.5rem",
                  border: "1px solid #ccc",
                  borderRadius: "4px",
                }}
              />
            </div>
            
            <div style={{ marginBottom: "0.75rem" }}>
              <label style={{ display: "block", fontSize: "0.85rem", marginBottom: "0.25rem" }}>Source:</label>
              <input
                type="text"
                value={sourceFilter}
                onChange={(e) => setSourceFilter(e.target.value)}
                placeholder="e.g., user"
                style={{
                  width: "100%",
                  padding: "0.5rem",
                  border: "1px solid #ccc",
                  borderRadius: "4px",
                }}
              />
            </div>
            
            <div style={{ marginBottom: "0.75rem" }}>
              <label style={{ display: "block", fontSize: "0.85rem", marginBottom: "0.25rem" }}>Status:</label>
              <select
                value={staleFilter}
                onChange={(e) => setStaleFilter(e.target.value)}
                style={{
                  width: "100%",
                  padding: "0.5rem",
                  border: "1px solid #ccc",
                  borderRadius: "4px",
                }}
              >
                <option value="all">All</option>
                <option value="active">Active Only</option>
                <option value="stale">Stale Only</option>
              </select>
            </div>
            
            <button
              onClick={fetchMemories}
              disabled={loading}
              style={{
                width: "100%",
                padding: "0.5rem",
                backgroundColor: loading ? "#ccc" : "#0070f3",
                color: "white",
                border: "none",
                borderRadius: "4px",
                cursor: loading ? "not-allowed" : "pointer",
              }}
            >
              {loading ? "Loading..." : "Apply Filters"}
            </button>
          </div>

          {/* Memory list */}
          <div
            style={{
              border: "1px solid #ccc",
              borderRadius: "4px",
              padding: "1rem",
              backgroundColor: "#f9f9f9",
              overflowY: "auto",
              flex: 1,
              maxHeight: "60vh",
            }}
          >
            <h3 style={{ marginTop: 0, fontSize: "1rem" }}>Memories ({memories.length})</h3>
            {memories.length === 0 ? (
              <p style={{ color: "#666", fontSize: "0.9rem" }}>No memories found. Try adjusting filters.</p>
            ) : (
              <div style={{ display: "flex", flexDirection: "column", gap: "0.5rem" }}>
                {memories.map((memory) => (
                  <div
                    key={memory.id}
                    onClick={() => handleMemorySelect(memory)}
                    style={{
                      padding: "0.75rem",
                      border: "1px solid #ddd",
                      borderRadius: "4px",
                      backgroundColor: activeMemory?.id === memory.id ? "#e3f2fd" : "white",
                      cursor: "pointer",
                      transition: "background-color 0.2s",
                    }}
                  >
                    <div style={{ fontSize: "0.75rem", color: "#666", marginBottom: "0.25rem" }}>
                      {memory.category} {memory.is_stale && <span style={{ color: "#f44336" }}>• STALE</span>}
                    </div>
                    <div
                      style={{
                        fontSize: "0.85rem",
                        color: "#333",
                        overflow: "hidden",
                        textOverflow: "ellipsis",
                        whiteSpace: "nowrap",
                      }}
                    >
                      {memory.content.substring(0, 80)}
                      {memory.content.length > 80 ? "..." : ""}
                    </div>
                    <div style={{ fontSize: "0.7rem", color: "#999", marginTop: "0.25rem" }}>
                      Used {memory.usage_count}x • v{memory.version}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Right column: Memory details */}
        <div
          style={{
            border: "1px solid #ccc",
            borderRadius: "4px",
            padding: "1rem",
            backgroundColor: "white",
            overflowY: "auto",
            maxHeight: "80vh",
          }}
        >
          {activeMemory ? (
            <>
              <div style={{ marginBottom: "1rem", display: "flex", justifyContent: "space-between", alignItems: "start" }}>
                <div>
                  <h2 style={{ margin: 0, fontSize: "1.2rem" }}>Memory #{activeMemory.id}</h2>
                  <div style={{ fontSize: "0.8rem", color: "#666", marginTop: "0.25rem" }}>
                    {formatTime(activeMemory.created_at)}
                    {activeMemory.is_stale && (
                      <span style={{ color: "#f44336", marginLeft: "0.5rem" }}>
                        • Stale: {activeMemory.stale_reason || "Unknown reason"}
                      </span>
                    )}
                  </div>
                </div>
                {!isEditing && (
                  <button
                    onClick={handleEdit}
                    style={{
                      padding: "0.5rem 1rem",
                      backgroundColor: "#0070f3",
                      color: "white",
                      border: "none",
                      borderRadius: "4px",
                      cursor: "pointer",
                      fontSize: "0.85rem",
                    }}
                  >
                    Edit
                  </button>
                )}
              </div>

              {isEditing ? (
                <div style={{ marginBottom: "1rem" }}>
                  <label style={{ display: "block", marginBottom: "0.5rem", fontWeight: "bold" }}>Content:</label>
                  <textarea
                    value={editContent}
                    onChange={(e) => setEditContent(e.target.value)}
                    style={{
                      width: "100%",
                      minHeight: "150px",
                      padding: "0.75rem",
                      border: "1px solid #ccc",
                      borderRadius: "4px",
                      fontSize: "0.9rem",
                      fontFamily: "inherit",
                    }}
                  />
                  
                  <label style={{ display: "block", marginTop: "1rem", marginBottom: "0.5rem", fontWeight: "bold" }}>Tags (comma-separated):</label>
                  <input
                    type="text"
                    value={editTags}
                    onChange={(e) => setEditTags(e.target.value)}
                    placeholder="reminder_pattern, scheduling"
                    style={{
                      width: "100%",
                      padding: "0.5rem",
                      border: "1px solid #ccc",
                      borderRadius: "4px",
                    }}
                  />
                  
                  <div style={{ display: "flex", gap: "0.5rem", marginTop: "1rem" }}>
                    <button
                      onClick={updateMemory}
                      disabled={loading}
                      style={{
                        padding: "0.5rem 1rem",
                        backgroundColor: loading ? "#ccc" : "#4CAF50",
                        color: "white",
                        border: "none",
                        borderRadius: "4px",
                        cursor: loading ? "not-allowed" : "pointer",
                      }}
                    >
                      Save
                    </button>
                    <button
                      onClick={() => setIsEditing(false)}
                      style={{
                        padding: "0.5rem 1rem",
                        backgroundColor: "#9E9E9E",
                        color: "white",
                        border: "none",
                        borderRadius: "4px",
                        cursor: "pointer",
                      }}
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              ) : (
                <>
                  <div style={{ marginBottom: "1rem" }}>
                    <h3 style={{ fontSize: "0.9rem", color: "#666", marginBottom: "0.5rem" }}>Content:</h3>
                    <div
                      style={{
                        padding: "0.75rem",
                        backgroundColor: "#f5f5f5",
                        borderRadius: "4px",
                        whiteSpace: "pre-wrap",
                        wordBreak: "break-word",
                      }}
                    >
                      {activeMemory.content}
                    </div>
                  </div>

                  <div style={{ marginBottom: "1rem" }}>
                    <h3 style={{ fontSize: "0.9rem", color: "#666", marginBottom: "0.5rem" }}>Metadata:</h3>
                    <div style={{ fontSize: "0.85rem" }}>
                      <div><strong>Category:</strong> {activeMemory.category}</div>
                      <div><strong>Source:</strong> {activeMemory.source}</div>
                      <div><strong>Tags:</strong> {activeMemory.tags?.join(", ") || "None"}</div>
                      <div><strong>Version:</strong> {activeMemory.version}</div>
                      <div><strong>Usage Count:</strong> {activeMemory.usage_count}</div>
                      {activeMemory.last_used_at && (
                        <div><strong>Last Used:</strong> {formatTime(activeMemory.last_used_at)}</div>
                      )}
                      {activeMemory.expires_at && (
                        <div><strong>Expires:</strong> {formatTime(activeMemory.expires_at)}</div>
                      )}
                      <div><strong>Confidence:</strong> {activeMemory.confidence_score.toFixed(2)}</div>
                    </div>
                  </div>

                  {/* History */}
                  {history.length > 0 && (
                    <div style={{ marginBottom: "1rem" }}>
                      <h3 style={{ fontSize: "0.9rem", color: "#666", marginBottom: "0.5rem" }}>Version History:</h3>
                      <div style={{ maxHeight: "200px", overflowY: "auto" }}>
                        {history.map((h) => (
                          <div
                            key={h.id}
                            style={{
                              padding: "0.5rem",
                              border: "1px solid #ddd",
                              borderRadius: "4px",
                              marginBottom: "0.5rem",
                              fontSize: "0.8rem",
                            }}
                          >
                            <div><strong>v{h.version}</strong> • {formatTime(h.created_at)}</div>
                            <div style={{ color: "#666", marginTop: "0.25rem" }}>
                              {h.content.substring(0, 100)}
                              {h.content.length > 100 ? "..." : ""}
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Links */}
                  {links.length > 0 && (
                    <div style={{ marginBottom: "1rem" }}>
                      <h3 style={{ fontSize: "0.9rem", color: "#666", marginBottom: "0.5rem" }}>Links:</h3>
                      <div style={{ fontSize: "0.85rem" }}>
                        {links.map((link) => (
                          <div
                            key={link.id}
                            style={{
                              padding: "0.5rem",
                              border: "1px solid #ddd",
                              borderRadius: "4px",
                              marginBottom: "0.5rem",
                            }}
                          >
                            <div>
                              <strong>{link.relationship_type}</strong> → {link.target_type} #{link.target_id}
                            </div>
                            {link.notes && (
                              <div style={{ color: "#666", fontSize: "0.8rem", marginTop: "0.25rem" }}>
                                {link.notes}
                              </div>
                            )}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Actions */}
                  <div style={{ marginTop: "1rem", paddingTop: "1rem", borderTop: "1px solid #ddd" }}>
                    <h3 style={{ fontSize: "0.9rem", color: "#666", marginBottom: "0.5rem" }}>Actions:</h3>
                    <div style={{ display: "flex", flexDirection: "column", gap: "0.5rem" }}>
                      {!activeMemory.is_stale && (
                        <button
                          onClick={() => {
                            const reason = prompt("Reason for marking as stale:");
                            if (reason) markStale(activeMemory.id, reason);
                          }}
                          style={{
                            padding: "0.5rem",
                            backgroundColor: "#FF9800",
                            color: "white",
                            border: "none",
                            borderRadius: "4px",
                            cursor: "pointer",
                            fontSize: "0.85rem",
                          }}
                        >
                          Mark as Stale
                        </button>
                      )}
                      <button
                        onClick={() => {
                          const dateStr = prompt("Expiration date (YYYY-MM-DD):");
                          if (dateStr) {
                            const expiresAt = new Date(dateStr).toISOString();
                            setExpiration(activeMemory.id, expiresAt);
                          }
                        }}
                        style={{
                          padding: "0.5rem",
                          backgroundColor: "#2196F3",
                          color: "white",
                          border: "none",
                          borderRadius: "4px",
                          cursor: "pointer",
                          fontSize: "0.85rem",
                        }}
                      >
                        Set Expiration
                      </button>
                    </div>
                  </div>
                </>
              )}
            </>
          ) : (
            <div
              style={{
                textAlign: "center",
                color: "#666",
                padding: "2rem",
              }}
            >
              Select a memory from the list to view details
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

