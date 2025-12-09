"use client";

import { useState, useEffect } from "react";
import Link from "next/link";

interface Book {
  slug: string;
  title: string;
  updated_at?: string;
}

interface Chapter {
  id: string;
  title?: string;
  segments: any[];
}

export default function AudioStudio() {
  const [books, setBooks] = useState<Book[]>([]);
  const [selectedBook, setSelectedBook] = useState<string | null>(null);
  const [chapters, setChapters] = useState<Chapter[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadBooks();
  }, []);

  useEffect(() => {
    if (selectedBook) {
      loadChapters(selectedBook);
    }
  }, [selectedBook]);

  const getApiUrl = (endpoint: string) => {
    if (typeof window !== 'undefined') {
      return `${window.location.protocol}//${window.location.hostname}:8000${endpoint}`;
    }
    return `http://localhost:8000${endpoint}`;
  };

  const loadBooks = async () => {
    try {
      const response = await fetch(getApiUrl("/audio/books"));
      if (!response.ok) throw new Error("Failed to load books");
      const data = await response.json();
      setBooks(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load books");
    }
  };

  const loadChapters = async (bookSlug: string) => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(getApiUrl(`/audio/books/${bookSlug}/chapters`));
      if (!response.ok) throw new Error("Failed to load chapters");
      const data = await response.json();
      setChapters(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load chapters");
    } finally {
      setLoading(false);
    }
  };

  const handleRender = async (bookSlug: string, chapterId: string) => {
    try {
      const response = await fetch(
        getApiUrl(`/audio/books/${bookSlug}/render/${chapterId}`),
        { method: "POST" }
      );
      if (!response.ok) throw new Error("Failed to trigger render");
      const data = await response.json();
      alert(`Render status: ${data.status}\n${data.error || "Render queued"}`);
    } catch (err) {
      alert(`Error: ${err instanceof Error ? err.message : "Unknown error"}`);
    }
  };

  return (
    <div style={{ padding: "2rem", maxWidth: "1200px", margin: "0 auto" }}>
      <div style={{ marginBottom: "2rem" }}>
        <Link
          href="/"
          style={{ color: "#81D8D0", textDecoration: "none", marginBottom: "1rem", display: "block" }}
        >
          ← Back to Life OS
        </Link>
        <h1 style={{ fontSize: "2.5rem", marginBottom: "0.5rem" }}>Audiobook Studio</h1>
        <p style={{ color: "#666" }}>
          Manage books, configure voices, and render audio chapters
        </p>
      </div>

      {error && (
        <div
          style={{
            padding: "1rem",
            backgroundColor: "#fee",
            border: "1px solid #fcc",
            borderRadius: "4px",
            color: "#c00",
            marginBottom: "1rem",
          }}
        >
          <strong>Error:</strong> {error}
        </div>
      )}

      <div style={{ display: "grid", gridTemplateColumns: "300px 1fr", gap: "2rem" }}>
        {/* Sidebar - Book List */}
        <div style={{ backgroundColor: "#fff", padding: "1.5rem", borderRadius: "8px", boxShadow: "0 2px 4px rgba(0,0,0,0.1)" }}>
          <h2 style={{ fontSize: "1.5rem", marginBottom: "1rem" }}>Books</h2>
          {books.length === 0 ? (
            <p style={{ color: "#666" }}>No books found</p>
          ) : (
            <div style={{ display: "flex", flexDirection: "column", gap: "0.5rem" }}>
              {books.map((book) => (
                <button
                  key={book.slug}
                  onClick={() => setSelectedBook(book.slug)}
                  style={{
                    padding: "0.75rem",
                    textAlign: "left",
                    border: selectedBook === book.slug ? "2px solid #81D8D0" : "1px solid #ddd",
                    borderRadius: "4px",
                    backgroundColor: selectedBook === book.slug ? "#f0f9f8" : "#fff",
                    cursor: "pointer",
                  }}
                >
                  {book.title}
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Main Content - Chapters */}
        <div style={{ backgroundColor: "#fff", padding: "1.5rem", borderRadius: "8px", boxShadow: "0 2px 4px rgba(0,0,0,0.1)" }}>
          {!selectedBook ? (
            <p style={{ color: "#666" }}>Select a book to view chapters</p>
          ) : loading ? (
            <p>Loading chapters...</p>
          ) : chapters.length === 0 ? (
            <p style={{ color: "#666" }}>No chapters found</p>
          ) : (
            <div>
              <h2 style={{ fontSize: "1.5rem", marginBottom: "1rem" }}>Chapters</h2>
              <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
                {chapters.map((chapter) => (
                  <div
                    key={chapter.id}
                    style={{
                      border: "1px solid #ddd",
                      borderRadius: "4px",
                      padding: "1rem",
                    }}
                  >
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "0.5rem" }}>
                      <h3 style={{ fontSize: "1.25rem", fontWeight: "bold" }}>
                        {chapter.title || chapter.id}
                      </h3>
                      <button
                        onClick={() => handleRender(selectedBook, chapter.id)}
                        style={{
                          padding: "0.5rem 1rem",
                          backgroundColor: "#81D8D0",
                          color: "white",
                          border: "none",
                          borderRadius: "4px",
                          cursor: "pointer",
                          fontSize: "0.9rem",
                        }}
                      >
                        Render
                      </button>
                    </div>
                    <p style={{ color: "#666", fontSize: "0.9rem" }}>
                      {chapter.segments?.length || 0} segments
                    </p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      <div style={{ marginTop: "2rem", padding: "1rem", backgroundColor: "#f9f9f9", borderRadius: "4px" }}>
        <h3 style={{ marginTop: 0 }}>Quick Tips:</h3>
        <ul style={{ margin: "0.5rem 0", paddingLeft: "1.5rem" }}>
          <li>Select a book to view its chapters</li>
          <li>Click "Render" to generate audio for a chapter</li>
          <li>TTS API integration coming in Phase 2</li>
          <li>Books are stored in <code>residential_repo/content/books/</code></li>
        </ul>
      </div>
    </div>
  );
}

