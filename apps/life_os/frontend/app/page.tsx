"use client";

import { useState } from "react";
import Link from "next/link";

export default function Home() {
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const sendPrompt = async () => {
    if (!prompt.trim()) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      // Use current host (works on localhost and network IP)
      const apiUrl = typeof window !== 'undefined' 
        ? `${window.location.protocol}//${window.location.hostname}:8000/otto/prompt`
        : "http://localhost:8000/otto/prompt";
      
      const response = await fetch(apiUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          prompt: prompt,
          source: "life_os_web",
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setResult(data);
      setPrompt(""); // Clear input on success
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to send prompt");
    } finally {
      setLoading(false);
    }
  };

  const checkOttoHealth = async () => {
    try {
      const apiUrl = typeof window !== 'undefined'
        ? `${window.location.protocol}//${window.location.hostname}:8000/otto/health`
        : "http://localhost:8000/otto/health";
      
      const response = await fetch(apiUrl);
      const data = await response.json();
      alert(`Otto Status: ${data.status}\n${data.otto_status ? JSON.stringify(data.otto_status, null, 2) : data.error || ""}`);
    } catch (err) {
      alert(`Error checking Otto: ${err instanceof Error ? err.message : "Unknown error"}`);
    }
  };

  return (
    <div style={{ padding: "1rem", maxWidth: "800px", margin: "0 auto" }}>
      <h1 style={{ fontSize: "1.75rem", marginBottom: "1rem" }}>Life OS - Otto Prompt Interface</h1>
      
      <div style={{ marginBottom: "2rem" }}>
        <button
          onClick={checkOttoHealth}
          style={{
            padding: "0.5rem 1rem",
            backgroundColor: "#4CAF50",
            color: "white",
            border: "none",
            borderRadius: "4px",
            cursor: "pointer",
            marginBottom: "1rem",
          }}
        >
          Check Otto Connection
        </button>
      </div>

      <div style={{ marginBottom: "1rem" }}>
        <label style={{ display: "block", marginBottom: "0.5rem", fontWeight: "bold" }}>
          Send Prompt to Otto:
        </label>
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Enter your prompt here... (e.g., 'List the repository structure', 'Audit the Otto repo')"
          style={{
            width: "100%",
            minHeight: "150px",
            padding: "0.75rem",
            border: "1px solid #ccc",
            borderRadius: "4px",
            fontSize: "16px", // Prevents zoom on iOS
            fontFamily: "inherit",
            resize: "vertical",
          }}
          onKeyDown={(e) => {
            if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) {
              e.preventDefault();
              sendPrompt();
            }
          }}
        />
      </div>

      <button
        onClick={sendPrompt}
        disabled={loading || !prompt.trim()}
        style={{
          width: "100%",
          padding: "1rem 1.5rem",
          backgroundColor: loading ? "#ccc" : "#0070f3",
          color: "white",
          border: "none",
          borderRadius: "4px",
          cursor: loading ? "not-allowed" : "pointer",
          fontSize: "1.1rem",
          fontWeight: "bold",
          minHeight: "48px", // Better touch target for mobile
        }}
      >
        {loading ? "Sending..." : "Send to Otto"}
      </button>

      {error && (
        <div
          style={{
            marginTop: "1rem",
            padding: "1rem",
            backgroundColor: "#fee",
            border: "1px solid #fcc",
            borderRadius: "4px",
            color: "#c00",
          }}
        >
          <strong>Error:</strong> {error}
        </div>
      )}

      {result && (
        <div
          style={{
            marginTop: "1rem",
            padding: "1rem",
            backgroundColor: "#f0f0f0",
            border: "1px solid #ccc",
            borderRadius: "4px",
          }}
        >
          <h3 style={{ marginTop: 0 }}>Result:</h3>
          <pre style={{ whiteSpace: "pre-wrap", wordBreak: "break-word" }}>
            {JSON.stringify(result, null, 2)}
          </pre>
        </div>
      )}

      <div style={{ marginTop: "2rem", padding: "1rem", backgroundColor: "#f9f9f9", borderRadius: "4px" }}>
        <h3 style={{ marginTop: 0 }}>Quick Tips:</h3>
        <ul>
          <li>Press Cmd/Ctrl + Enter to send</li>
          <li>Try: "List repository structure" or "Audit Otto repo"</li>
          <li>Make sure Otto API is running on port 8001</li>
        </ul>
      </div>

      <div style={{ marginTop: "2rem", padding: "1rem", backgroundColor: "#e8f4f3", borderRadius: "4px", border: "1px solid #81D8D0" }}>
        <h3 style={{ marginTop: 0, color: "#81D8D0" }}>Life OS Modules:</h3>
        <div style={{ display: "flex", gap: "1rem", marginTop: "0.5rem", flexWrap: "wrap" }}>
          <Link
            href="/audio"
            style={{
              padding: "0.5rem 1rem",
              backgroundColor: "#81D8D0",
              color: "white",
              textDecoration: "none",
              borderRadius: "4px",
              fontSize: "0.9rem",
            }}
          >
            Audiobook Studio
          </Link>
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
            Otto Console
          </Link>
          <Link
            href="/otto/memory"
            style={{
              padding: "0.5rem 1rem",
              backgroundColor: "#81D8D0",
              color: "white",
              textDecoration: "none",
              borderRadius: "4px",
              fontSize: "0.9rem",
            }}
          >
            Memory Console
          </Link>
          <Link
            href="/tasks"
            style={{
              padding: "0.5rem 1rem",
              backgroundColor: "#81D8D0",
              color: "white",
              textDecoration: "none",
              borderRadius: "4px",
              fontSize: "0.9rem",
            }}
          >
            Tasks
          </Link>
          <Link
            href="/bills"
            style={{
              padding: "0.5rem 1rem",
              backgroundColor: "#81D8D0",
              color: "white",
              textDecoration: "none",
              borderRadius: "4px",
              fontSize: "0.9rem",
            }}
          >
            Bills
          </Link>
          <Link
            href="/calendar"
            style={{
              padding: "0.5rem 1rem",
              backgroundColor: "#81D8D0",
              color: "white",
              textDecoration: "none",
              borderRadius: "4px",
              fontSize: "0.9rem",
            }}
          >
            Calendar
          </Link>
        </div>
      </div>
    </div>
  );
}

