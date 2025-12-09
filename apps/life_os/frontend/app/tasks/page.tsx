"use client";

import { useState, useEffect } from "react";
import Link from "next/link";

interface LifeOSTask {
  id: number;
  title: string;
  description?: string;
  status: "todo" | "in_progress" | "done" | "blocked";
  assignee?: string;
  due_date?: string;
  priority?: "low" | "medium" | "high";
  category?: string;
  created_at: string;
  updated_at: string;
  completed_at?: string;
}

export default function TasksPage() {
  const [tasks, setTasks] = useState<LifeOSTask[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [newTask, setNewTask] = useState({
    title: "",
    description: "",
    assignee: "",
    due_date: "",
    priority: "medium" as "low" | "medium" | "high",
    category: "",
  });

  const getApiUrl = () => {
    if (typeof window !== "undefined") {
      return `${window.location.protocol}//${window.location.hostname}:8000`;
    }
    return "http://localhost:8000";
  };

  const fetchTasks = async () => {
    try {
      const response = await fetch(`${getApiUrl()}/life_os/tasks`);
      if (!response.ok) throw new Error("Failed to fetch tasks");
      const data = await response.json();
      setTasks(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load tasks");
    } finally {
      setLoading(false);
    }
  };

  const createTask = async () => {
    if (!newTask.title.trim()) return;

    try {
      const response = await fetch(`${getApiUrl()}/life_os/tasks`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ...newTask,
          due_date: newTask.due_date || null,
        }),
      });

      if (!response.ok) throw new Error("Failed to create task");
      
      setNewTask({
        title: "",
        description: "",
        assignee: "",
        due_date: "",
        priority: "medium",
        category: "",
      });
      setShowCreateForm(false);
      await fetchTasks();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create task");
    }
  };

  const updateTaskStatus = async (taskId: number, newStatus: string) => {
    try {
      const response = await fetch(`${getApiUrl()}/life_os/tasks/${taskId}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status: newStatus }),
      });

      if (!response.ok) throw new Error("Failed to update task");
      await fetchTasks();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to update task");
    }
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  const formatDate = (dateString?: string) => {
    if (!dateString) return null;
    const date = new Date(dateString);
    return date.toLocaleDateString();
  };

  const getPriorityColor = (priority?: string) => {
    switch (priority) {
      case "high":
        return "#f44336";
      case "medium":
        return "#ff9800";
      case "low":
        return "#4caf50";
      default:
        return "#9e9e9e";
    }
  };

  const columns = [
    { id: "todo", title: "To Do", status: "todo" as const },
    { id: "in_progress", title: "In Progress", status: "in_progress" as const },
    { id: "done", title: "Done", status: "done" as const },
  ];

  const getTasksByStatus = (status: string) => {
    return tasks.filter((t) => t.status === status);
  };

  if (loading) {
    return (
      <div style={{ padding: "2rem", textAlign: "center" }}>
        <p>Loading tasks...</p>
      </div>
    );
  }

  return (
    <div style={{ padding: "1rem", maxWidth: "1400px", margin: "0 auto" }}>
      <div style={{ marginBottom: "1rem", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <h1 style={{ fontSize: "1.75rem", margin: 0 }}>Life OS Tasks</h1>
        <div style={{ display: "flex", gap: "0.5rem" }}>
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
          <button
            onClick={() => setShowCreateForm(!showCreateForm)}
            style={{
              padding: "0.5rem 1rem",
              backgroundColor: "#0070f3",
              color: "white",
              border: "none",
              borderRadius: "4px",
              cursor: "pointer",
              fontSize: "0.9rem",
            }}
          >
            {showCreateForm ? "Cancel" : "+ New Task"}
          </button>
        </div>
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

      {showCreateForm && (
        <div
          style={{
            marginBottom: "2rem",
            padding: "1.5rem",
            border: "1px solid #ccc",
            borderRadius: "4px",
            backgroundColor: "#f9f9f9",
          }}
        >
          <h3 style={{ marginTop: 0 }}>Create New Task</h3>
          <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
            <div>
              <label style={{ display: "block", marginBottom: "0.5rem", fontWeight: "bold" }}>
                Title *
              </label>
              <input
                type="text"
                value={newTask.title}
                onChange={(e) => setNewTask({ ...newTask, title: e.target.value })}
                style={{
                  width: "100%",
                  padding: "0.5rem",
                  border: "1px solid #ccc",
                  borderRadius: "4px",
                }}
                placeholder="Task title"
              />
            </div>
            <div>
              <label style={{ display: "block", marginBottom: "0.5rem", fontWeight: "bold" }}>
                Description
              </label>
              <textarea
                value={newTask.description}
                onChange={(e) => setNewTask({ ...newTask, description: e.target.value })}
                style={{
                  width: "100%",
                  padding: "0.5rem",
                  border: "1px solid #ccc",
                  borderRadius: "4px",
                  minHeight: "80px",
                }}
                placeholder="Task description"
              />
            </div>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "1rem" }}>
              <div>
                <label style={{ display: "block", marginBottom: "0.5rem", fontWeight: "bold" }}>
                  Assignee
                </label>
                <input
                  type="text"
                  value={newTask.assignee}
                  onChange={(e) => setNewTask({ ...newTask, assignee: e.target.value })}
                  style={{
                    width: "100%",
                    padding: "0.5rem",
                    border: "1px solid #ccc",
                    borderRadius: "4px",
                  }}
                  placeholder="Karl, Brit, etc."
                />
              </div>
              <div>
                <label style={{ display: "block", marginBottom: "0.5rem", fontWeight: "bold" }}>
                  Due Date
                </label>
                <input
                  type="date"
                  value={newTask.due_date}
                  onChange={(e) => setNewTask({ ...newTask, due_date: e.target.value })}
                  style={{
                    width: "100%",
                    padding: "0.5rem",
                    border: "1px solid #ccc",
                    borderRadius: "4px",
                  }}
                />
              </div>
            </div>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "1rem" }}>
              <div>
                <label style={{ display: "block", marginBottom: "0.5rem", fontWeight: "bold" }}>
                  Priority
                </label>
                <select
                  value={newTask.priority}
                  onChange={(e) => setNewTask({ ...newTask, priority: e.target.value as any })}
                  style={{
                    width: "100%",
                    padding: "0.5rem",
                    border: "1px solid #ccc",
                    borderRadius: "4px",
                  }}
                >
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                </select>
              </div>
              <div>
                <label style={{ display: "block", marginBottom: "0.5rem", fontWeight: "bold" }}>
                  Category
                </label>
                <input
                  type="text"
                  value={newTask.category}
                  onChange={(e) => setNewTask({ ...newTask, category: e.target.value })}
                  style={{
                    width: "100%",
                    padding: "0.5rem",
                    border: "1px solid #ccc",
                    borderRadius: "4px",
                  }}
                  placeholder="bills, household, work, etc."
                />
              </div>
            </div>
            <button
              onClick={createTask}
              style={{
                padding: "0.75rem 1.5rem",
                backgroundColor: "#0070f3",
                color: "white",
                border: "none",
                borderRadius: "4px",
                cursor: "pointer",
                fontSize: "1rem",
                fontWeight: "bold",
              }}
            >
              Create Task
            </button>
          </div>
        </div>
      )}

      {/* Kanban Board */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(3, 1fr)",
          gap: "1rem",
          minHeight: "500px",
        }}
      >
        {columns.map((column) => {
          const columnTasks = getTasksByStatus(column.status);
          return (
            <div
              key={column.id}
              style={{
                border: "1px solid #ccc",
                borderRadius: "4px",
                padding: "1rem",
                backgroundColor: "#f9f9f9",
              }}
            >
              <h3 style={{ marginTop: 0, marginBottom: "1rem" }}>
                {column.title} ({columnTasks.length})
              </h3>
              <div style={{ display: "flex", flexDirection: "column", gap: "0.5rem" }}>
                {columnTasks.length === 0 ? (
                  <p style={{ color: "#666", fontSize: "0.9rem", fontStyle: "italic" }}>
                    No tasks
                  </p>
                ) : (
                  columnTasks.map((task) => (
                    <div
                      key={task.id}
                      style={{
                        padding: "0.75rem",
                        backgroundColor: "white",
                        border: "1px solid #ddd",
                        borderRadius: "4px",
                        cursor: "pointer",
                      }}
                      onClick={() => {
                        // Cycle through statuses: todo -> in_progress -> done -> todo
                        const nextStatus =
                          task.status === "todo"
                            ? "in_progress"
                            : task.status === "in_progress"
                            ? "done"
                            : "todo";
                        updateTaskStatus(task.id, nextStatus);
                      }}
                    >
                      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "start", marginBottom: "0.5rem" }}>
                        <h4 style={{ margin: 0, fontSize: "1rem" }}>{task.title}</h4>
                        {task.priority && (
                          <span
                            style={{
                              display: "inline-block",
                              width: "8px",
                              height: "8px",
                              borderRadius: "50%",
                              backgroundColor: getPriorityColor(task.priority),
                            }}
                            title={task.priority}
                          />
                        )}
                      </div>
                      {task.description && (
                        <p style={{ margin: "0.25rem 0", fontSize: "0.85rem", color: "#666" }}>
                          {task.description.substring(0, 60)}
                          {task.description.length > 60 ? "..." : ""}
                        </p>
                      )}
                      <div style={{ fontSize: "0.75rem", color: "#666", marginTop: "0.5rem" }}>
                        {task.assignee && <span>👤 {task.assignee}</span>}
                        {task.due_date && (
                          <span style={{ marginLeft: "0.5rem" }}>
                            📅 {formatDate(task.due_date)}
                          </span>
                        )}
                        {task.category && (
                          <span style={{ marginLeft: "0.5rem" }}>🏷️ {task.category}</span>
                        )}
                      </div>
                      <div style={{ fontSize: "0.7rem", color: "#999", marginTop: "0.25rem" }}>
                        Click to change status
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          );
        })}
      </div>

      <div style={{ marginTop: "2rem", padding: "1rem", backgroundColor: "#e8f4f3", borderRadius: "4px", border: "1px solid #81D8D0" }}>
        <h3 style={{ marginTop: 0, color: "#81D8D0" }}>Quick Actions:</h3>
        <div style={{ display: "flex", gap: "1rem", marginTop: "0.5rem", flexWrap: "wrap" }}>
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
            Ask Otto to create a task
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
            Back to Life OS
          </Link>
        </div>
      </div>
    </div>
  );
}

