"use client";

import { useState, useEffect } from "react";
import Link from "next/link";

interface OttoRun {
  id: number;
  created_at: string;
  updated_at: string;
  status: "pending" | "running" | "success" | "error";
  source: string;
  input_text: string;
  input_payload?: any;
  output_text?: string;
  output_payload?: any;
  logs?: string;
}

export default function OttoConsole() {
  const [runs, setRuns] = useState<OttoRun[]>([]);
  const [activeRun, setActiveRun] = useState<OttoRun | null>(null);
  const [inputText, setInputText] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Get API base URL
  const getApiUrl = () => {
    if (typeof window !== "undefined") {
      return `${window.location.protocol}//${window.location.hostname}:8000`;
    }
    return "http://localhost:8000";
  };

  // Fetch runs list
  const fetchRuns = async () => {
    try {
      const response = await fetch(`${getApiUrl()}/otto/runs?limit=20`);
      if (!response.ok) throw new Error("Failed to fetch runs");
      const data = await response.json();
      setRuns(data);
      
      // If we have an active run, refresh its details
      if (activeRun) {
        const updatedRun = data.find((r: OttoRun) => r.id === activeRun.id);
        if (updatedRun) {
          setActiveRun(updatedRun);
          // If still pending/running, keep polling
          if (updatedRun.status === "pending" || updatedRun.status === "running") {
            setTimeout(fetchRuns, 2000);
          }
        }
      }
    } catch (err) {
      console.error("Error fetching runs:", err);
    }
  };

  // Fetch single run details
  const fetchRunDetails = async (runId: number) => {
    try {
      const response = await fetch(`${getApiUrl()}/otto/runs/${runId}`);
      if (!response.ok) throw new Error("Failed to fetch run details");
      const run = await response.json();
      setActiveRun(run);
      
      // If still pending/running, keep polling
      if (run.status === "pending" || run.status === "running") {
        setTimeout(() => fetchRunDetails(runId), 2000);
      }
    } catch (err) {
      console.error("Error fetching run details:", err);
    }
  };

  // Create new run
  const createRun = async () => {
    if (!inputText.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${getApiUrl()}/otto/runs`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          input_text: inputText,
          mode: "chat",
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to create run");
      }

      const newRun = await response.json();
      setInputText("");
      setActiveRun(newRun);
      
      // Refresh runs list
      await fetchRuns();
      
      // If pending/running, start polling
      if (newRun.status === "pending" || newRun.status === "running") {
        setTimeout(() => fetchRunDetails(newRun.id), 2000);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create run");
    } finally {
      setLoading(false);
    }
  };

  // Initial load
  useEffect(() => {
    fetchRuns();
  }, []);

  // Format timestamp
  const formatTime = (timestamp: string) => {
    const date = new Date(timestamp);
    return date.toLocaleString();
  };

  // Get status badge color
  const getStatusColor = (status: string) => {
    switch (status) {
      case "success":
        return "#4CAF50";
      case "error":
        return "#f44336";
      case "running":
        return "#2196F3";
      case "pending":
        return "#FF9800";
      default:
        return "#9E9E9E";
    }
  };

  return (
    <div style={{ padding: "1rem", maxWidth: "1400px", margin: "0 auto" }}>
      <div style={{ marginBottom: "1rem", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <h1 style={{ fontSize: "1.75rem", margin: 0 }}>Otto Console</h1>
        <div style={{ display: "flex", gap: "0.5rem" }}>
          <Link
            href="/otto/memory"
            style={{
              padding: "0.5rem 1rem",
              backgroundColor: "#4CAF50",
              color: "white",
              textDecoration: "none",
              borderRadius: "4px",
              fontSize: "0.9rem",
            }}
          >
            Memory Console
          </Link>
          <Link
            href="/"
            style={{
              padding: "0.5rem 1rem",
              backgroundColor: "#81D8D0",
              color: "white",
              textDecoration: "none",
              borderRadius: "4px",
              fontSize: "0.9rem",
            }}
          >
            ← Back to Life OS
          </Link>
        </div>
      </div>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "minmax(250px, 1fr) minmax(400px, 2fr)",
          gap: "1rem",
          minHeight: "600px",
        }}
      >
        {/* Left column: Runs list */}
        <div
          style={{
            border: "1px solid #ccc",
            borderRadius: "4px",
            padding: "1rem",
            backgroundColor: "#f9f9f9",
            overflowY: "auto",
            maxHeight: "80vh",
          }}
        >
          <h2 style={{ fontSize: "1.2rem", marginTop: 0, marginBottom: "1rem" }}>
            Recent Runs
          </h2>
          {runs.length === 0 ? (
            <p style={{ color: "#666" }}>No runs yet. Send a prompt to get started!</p>
          ) : (
            <div style={{ display: "flex", flexDirection: "column", gap: "0.5rem" }}>
              {runs.map((run) => (
                <div
                  key={run.id}
                  onClick={() => {
                    setActiveRun(run);
                    if (run.status === "pending" || run.status === "running") {
                      fetchRunDetails(run.id);
                    }
                  }}
                  style={{
                    padding: "0.75rem",
                    border: "1px solid #ddd",
                    borderRadius: "4px",
                    backgroundColor: activeRun?.id === run.id ? "#e3f2fd" : "white",
                    cursor: "pointer",
                    transition: "background-color 0.2s",
                  }}
                  onMouseEnter={(e) => {
                    if (activeRun?.id !== run.id) {
                      e.currentTarget.style.backgroundColor = "#f5f5f5";
                    }
                  }}
                  onMouseLeave={(e) => {
                    if (activeRun?.id !== run.id) {
                      e.currentTarget.style.backgroundColor = "white";
                    }
                  }}
                >
                  <div style={{ display: "flex", alignItems: "center", gap: "0.5rem", marginBottom: "0.25rem" }}>
                    <span
                      style={{
                        display: "inline-block",
                        width: "8px",
                        height: "8px",
                        borderRadius: "50%",
                        backgroundColor: getStatusColor(run.status),
                      }}
                    />
                    <span
                      style={{
                        fontSize: "0.75rem",
                        fontWeight: "bold",
                        textTransform: "uppercase",
                        color: getStatusColor(run.status),
                      }}
                    >
                      {run.status}
                    </span>
                    <span style={{ fontSize: "0.7rem", color: "#666", marginLeft: "auto" }}>
                      {formatTime(run.created_at).split(",")[0]}
                    </span>
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
                    {run.input_text.substring(0, 60)}
                    {run.input_text.length > 60 ? "..." : ""}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Right column: Active run details + input */}
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            gap: "1rem",
          }}
        >
          {/* Active run details */}
          {activeRun ? (
            <div
              style={{
                border: "1px solid #ccc",
                borderRadius: "4px",
                padding: "1rem",
                backgroundColor: "white",
                flex: 1,
                overflowY: "auto",
                maxHeight: "60vh",
              }}
            >
              <div style={{ marginBottom: "1rem" }}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "0.5rem" }}>
                  <h3 style={{ margin: 0 }}>Run #{activeRun.id}</h3>
                  <span
                    style={{
                      padding: "0.25rem 0.5rem",
                      borderRadius: "4px",
                      backgroundColor: getStatusColor(activeRun.status),
                      color: "white",
                      fontSize: "0.75rem",
                      fontWeight: "bold",
                      textTransform: "uppercase",
                    }}
                  >
                    {activeRun.status}
                  </span>
                </div>
                <div style={{ fontSize: "0.8rem", color: "#666" }}>
                  Created: {formatTime(activeRun.created_at)}
                  {activeRun.updated_at !== activeRun.created_at && (
                    <> • Updated: {formatTime(activeRun.updated_at)}</>
                  )}
                </div>
              </div>

              <div style={{ marginBottom: "1rem" }}>
                <h4 style={{ marginBottom: "0.5rem", fontSize: "0.9rem", color: "#666" }}>Input:</h4>
                <div
                  style={{
                    padding: "0.75rem",
                    backgroundColor: "#f5f5f5",
                    borderRadius: "4px",
                    whiteSpace: "pre-wrap",
                    wordBreak: "break-word",
                  }}
                >
                  {activeRun.input_text}
                </div>
              </div>

              {activeRun.output_text && (
                <div style={{ marginBottom: "1rem" }}>
                  <h4 style={{ marginBottom: "0.5rem", fontSize: "0.9rem", color: "#666" }}>Output:</h4>
                  <div
                    style={{
                      padding: "0.75rem",
                      backgroundColor: "#e8f5e9",
                      borderRadius: "4px",
                      whiteSpace: "pre-wrap",
                      wordBreak: "break-word",
                    }}
                  >
                    {activeRun.output_text}
                  </div>
                </div>
              )}

              {activeRun.logs && (
                <details style={{ marginTop: "1rem" }}>
                  <summary style={{ cursor: "pointer", fontSize: "0.9rem", color: "#666", marginBottom: "0.5rem" }}>
                    Logs (click to expand)
                  </summary>
                  <pre
                    style={{
                      padding: "0.75rem",
                      backgroundColor: "#f5f5f5",
                      borderRadius: "4px",
                      overflow: "auto",
                      fontSize: "0.8rem",
                      maxHeight: "200px",
                    }}
                  >
                    {activeRun.logs}
                  </pre>
                </details>
              )}

              {activeRun.status === "error" && (
                <div
                  style={{
                    marginTop: "1rem",
                    padding: "0.75rem",
                    backgroundColor: "#ffebee",
                    border: "1px solid #f44336",
                    borderRadius: "4px",
                    color: "#c62828",
                  }}
                >
                  <strong>Error:</strong> {activeRun.logs || "Unknown error occurred"}
                </div>
              )}
            </div>
          ) : (
            <div
              style={{
                border: "1px solid #ccc",
                borderRadius: "4px",
                padding: "2rem",
                backgroundColor: "#f9f9f9",
                textAlign: "center",
                color: "#666",
              }}
            >
              Select a run from the list to view details
            </div>
          )}

          {/* Input box */}
          <div
            style={{
              border: "1px solid #ccc",
              borderRadius: "4px",
              padding: "1rem",
              backgroundColor: "white",
            }}
          >
            <label style={{ display: "block", marginBottom: "0.5rem", fontWeight: "bold" }}>
              Talk to Otto:
            </label>
            <textarea
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="Enter your prompt here... (e.g., 'List the repository structure', 'Audit the Otto repo')"
              style={{
                width: "100%",
                minHeight: "100px",
                padding: "0.75rem",
                border: "1px solid #ccc",
                borderRadius: "4px",
                fontSize: "16px",
                fontFamily: "inherit",
                resize: "vertical",
                marginBottom: "0.5rem",
              }}
              onKeyDown={(e) => {
                if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) {
                  e.preventDefault();
                  createRun();
                }
              }}
            />
            {error && (
              <div
                style={{
                  marginBottom: "0.5rem",
                  padding: "0.5rem",
                  backgroundColor: "#ffebee",
                  border: "1px solid #f44336",
                  borderRadius: "4px",
                  color: "#c62828",
                  fontSize: "0.9rem",
                }}
              >
                {error}
              </div>
            )}
            <button
              onClick={createRun}
              disabled={loading || !inputText.trim()}
              style={{
                width: "100%",
                padding: "0.75rem 1.5rem",
                backgroundColor: loading ? "#ccc" : "#0070f3",
                color: "white",
                border: "none",
                borderRadius: "4px",
                cursor: loading ? "not-allowed" : "pointer",
                fontSize: "1rem",
                fontWeight: "bold",
              }}
            >
              {loading ? "Sending..." : "Send to Otto"}
            </button>
            <div style={{ marginTop: "0.5rem", fontSize: "0.8rem", color: "#666" }}>
              Press Cmd/Ctrl + Enter to send
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

