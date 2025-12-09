"use client";

import { useState, useEffect } from "react";
import Link from "next/link";

interface CalendarEvent {
  id: number;
  title: string;
  description?: string;
  start_time: string;
  end_time?: string;
  location?: string;
  attendees?: string;
  category?: string;
  is_recurring: string;
  recurrence_frequency?: string;
  status: string;
  reminders?: Array<{ minutes: number }>;
  created_at: string;
  updated_at: string;
}

export default function CalendarPage() {
  const [events, setEvents] = useState<CalendarEvent[]>([]);
  const [todayEvents, setTodayEvents] = useState<CalendarEvent[]>([]);
  const [upcomingEvents, setUpcomingEvents] = useState<CalendarEvent[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [view, setView] = useState<"today" | "upcoming" | "all">("today");
  const [newEvent, setNewEvent] = useState({
    title: "",
    description: "",
    start_time: "",
    end_time: "",
    location: "",
    attendees: "",
    category: "",
    is_recurring: "no",
    recurrence_frequency: "weekly",
    reminders: [] as Array<{ minutes: number }>,
  });

  const getApiUrl = () => {
    if (typeof window !== "undefined") {
      return `${window.location.protocol}//${window.location.hostname}:8000`;
    }
    return "http://localhost:8000";
  };

  const fetchTodaySummary = async () => {
    try {
      const response = await fetch(`${getApiUrl()}/calendar/today/summary`);
      if (response.ok) {
        const data = await response.json();
        setTodayEvents(data.today_events || []);
        setUpcomingEvents(data.upcoming_events || []);
      }
    } catch (err) {
      // Summary is optional
    }
  };

  const fetchEvents = async () => {
    try {
      let url = `${getApiUrl()}/calendar`;
      if (view === "today") {
        url = `${getApiUrl()}/calendar/upcoming?days=1`;
      } else if (view === "upcoming") {
        url = `${getApiUrl()}/calendar/upcoming?days=7`;
      }

      const response = await fetch(url);
      if (!response.ok) throw new Error("Failed to fetch events");
      const data = await response.json();
      setEvents(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load events");
    } finally {
      setLoading(false);
    }
  };

  const createEvent = async () => {
    if (!newEvent.title.trim() || !newEvent.start_time) return;

    try {
      const response = await fetch(`${getApiUrl()}/calendar`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ...newEvent,
          start_time: newEvent.start_time ? new Date(newEvent.start_time).toISOString() : null,
          end_time: newEvent.end_time ? new Date(newEvent.end_time).toISOString() : null,
          is_recurring: newEvent.is_recurring,
          recurrence_frequency: newEvent.is_recurring === "yes" ? newEvent.recurrence_frequency : null,
          reminders: newEvent.reminders.length > 0 ? newEvent.reminders : null,
        }),
      });

      if (!response.ok) throw new Error("Failed to create event");

      setNewEvent({
        title: "",
        description: "",
        start_time: "",
        end_time: "",
        location: "",
        attendees: "",
        category: "",
        is_recurring: "no",
        recurrence_frequency: "weekly",
        reminders: [],
      });
      setShowCreateForm(false);
      await fetchEvents();
      await fetchTodaySummary();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create event");
    }
  };

  const updateEvent = async (eventId: number, updates: Partial<CalendarEvent>) => {
    try {
      const response = await fetch(`${getApiUrl()}/calendar/${eventId}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(updates),
      });

      if (!response.ok) throw new Error("Failed to update event");
      await fetchEvents();
      await fetchTodaySummary();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to update event");
    }
  };

  useEffect(() => {
    fetchEvents();
    fetchTodaySummary();
  }, [view]);

  const formatDateTime = (dateString: string) => {
    const date = new Date(dateString);
    return {
      date: date.toLocaleDateString(),
      time: date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      full: date.toLocaleString(),
    };
  };

  const getEventsToDisplay = () => {
    if (view === "today") return todayEvents;
    if (view === "upcoming") return upcomingEvents;
    return events;
  };

  const addReminder = () => {
    const minutes = prompt("Reminder minutes before event:");
    if (minutes && !isNaN(Number(minutes))) {
      setNewEvent({
        ...newEvent,
        reminders: [...newEvent.reminders, { minutes: Number(minutes) }],
      });
    }
  };

  if (loading) {
    return (
      <div style={{ padding: "2rem", textAlign: "center" }}>
        <p>Loading calendar...</p>
      </div>
    );
  }

  const displayEvents = getEventsToDisplay();

  return (
    <div style={{ padding: "1rem", maxWidth: "1200px", margin: "0 auto" }}>
      <div style={{ marginBottom: "1rem", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <h1 style={{ fontSize: "1.75rem", margin: 0 }}>Calendar</h1>
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
            {showCreateForm ? "Cancel" : "+ New Event"}
          </button>
        </div>
      </div>

      <div style={{ marginBottom: "1rem", display: "flex", gap: "0.5rem", flexWrap: "wrap" }}>
        <button
          onClick={() => setView("today")}
          style={{
            padding: "0.5rem 1rem",
            backgroundColor: view === "today" ? "#0070f3" : "#f0f0f0",
            color: view === "today" ? "white" : "black",
            border: "none",
            borderRadius: "4px",
            cursor: "pointer",
          }}
        >
          Today
        </button>
        <button
          onClick={() => setView("upcoming")}
          style={{
            padding: "0.5rem 1rem",
            backgroundColor: view === "upcoming" ? "#0070f3" : "#f0f0f0",
            color: view === "upcoming" ? "white" : "black",
            border: "none",
            borderRadius: "4px",
            cursor: "pointer",
          }}
        >
          Next 7 Days
        </button>
        <button
          onClick={() => setView("all")}
          style={{
            padding: "0.5rem 1rem",
            backgroundColor: view === "all" ? "#0070f3" : "#f0f0f0",
            color: view === "all" ? "white" : "black",
            border: "none",
            borderRadius: "4px",
            cursor: "pointer",
          }}
        >
          All Events
        </button>
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
          <h3 style={{ marginTop: 0 }}>Create New Event</h3>
          <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
            <div>
              <label style={{ display: "block", marginBottom: "0.5rem", fontWeight: "bold" }}>
                Title *
              </label>
              <input
                type="text"
                value={newEvent.title}
                onChange={(e) => setNewEvent({ ...newEvent, title: e.target.value })}
                style={{
                  width: "100%",
                  padding: "0.5rem",
                  border: "1px solid #ccc",
                  borderRadius: "4px",
                }}
                placeholder="Event title"
              />
            </div>
            <div>
              <label style={{ display: "block", marginBottom: "0.5rem", fontWeight: "bold" }}>
                Description
              </label>
              <textarea
                value={newEvent.description}
                onChange={(e) => setNewEvent({ ...newEvent, description: e.target.value })}
                style={{
                  width: "100%",
                  padding: "0.5rem",
                  border: "1px solid #ccc",
                  borderRadius: "4px",
                  minHeight: "80px",
                }}
                placeholder="Event description"
              />
            </div>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "1rem" }}>
              <div>
                <label style={{ display: "block", marginBottom: "0.5rem", fontWeight: "bold" }}>
                  Start Time *
                </label>
                <input
                  type="datetime-local"
                  value={newEvent.start_time}
                  onChange={(e) => setNewEvent({ ...newEvent, start_time: e.target.value })}
                  style={{
                    width: "100%",
                    padding: "0.5rem",
                    border: "1px solid #ccc",
                    borderRadius: "4px",
                  }}
                />
              </div>
              <div>
                <label style={{ display: "block", marginBottom: "0.5rem", fontWeight: "bold" }}>
                  End Time
                </label>
                <input
                  type="datetime-local"
                  value={newEvent.end_time}
                  onChange={(e) => setNewEvent({ ...newEvent, end_time: e.target.value })}
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
                  Location
                </label>
                <input
                  type="text"
                  value={newEvent.location}
                  onChange={(e) => setNewEvent({ ...newEvent, location: e.target.value })}
                  style={{
                    width: "100%",
                    padding: "0.5rem",
                    border: "1px solid #ccc",
                    borderRadius: "4px",
                  }}
                  placeholder="Event location"
                />
              </div>
              <div>
                <label style={{ display: "block", marginBottom: "0.5rem", fontWeight: "bold" }}>
                  Category
                </label>
                <input
                  type="text"
                  value={newEvent.category}
                  onChange={(e) => setNewEvent({ ...newEvent, category: e.target.value })}
                  style={{
                    width: "100%",
                    padding: "0.5rem",
                    border: "1px solid #ccc",
                    borderRadius: "4px",
                  }}
                  placeholder="work, personal, family, etc."
                />
              </div>
            </div>
            <div>
              <label style={{ display: "block", marginBottom: "0.5rem", fontWeight: "bold" }}>
                Attendees
              </label>
              <input
                type="text"
                value={newEvent.attendees}
                onChange={(e) => setNewEvent({ ...newEvent, attendees: e.target.value })}
                style={{
                  width: "100%",
                  padding: "0.5rem",
                  border: "1px solid #ccc",
                  borderRadius: "4px",
                }}
                placeholder="Comma-separated list of attendees"
              />
            </div>
            <div>
              <label style={{ display: "flex", alignItems: "center", gap: "0.5rem", marginBottom: "0.5rem" }}>
                <input
                  type="checkbox"
                  checked={newEvent.is_recurring === "yes"}
                  onChange={(e) =>
                    setNewEvent({ ...newEvent, is_recurring: e.target.checked ? "yes" : "no" })
                  }
                />
                <span style={{ fontWeight: "bold" }}>Recurring Event</span>
              </label>
              {newEvent.is_recurring === "yes" && (
                <select
                  value={newEvent.recurrence_frequency}
                  onChange={(e) => setNewEvent({ ...newEvent, recurrence_frequency: e.target.value })}
                  style={{
                    width: "100%",
                    padding: "0.5rem",
                    border: "1px solid #ccc",
                    borderRadius: "4px",
                    marginTop: "0.5rem",
                  }}
                >
                  <option value="daily">Daily</option>
                  <option value="weekly">Weekly</option>
                  <option value="monthly">Monthly</option>
                  <option value="yearly">Yearly</option>
                </select>
              )}
            </div>
            <div>
              <label style={{ display: "block", marginBottom: "0.5rem", fontWeight: "bold" }}>
                Reminders
              </label>
              <div style={{ display: "flex", gap: "0.5rem", alignItems: "center", flexWrap: "wrap" }}>
                {newEvent.reminders.map((r, idx) => (
                  <span
                    key={idx}
                    style={{
                      padding: "0.25rem 0.5rem",
                      backgroundColor: "#e3f2fd",
                      borderRadius: "4px",
                      fontSize: "0.85rem",
                    }}
                  >
                    {r.minutes} min before
                    <button
                      onClick={() => {
                        setNewEvent({
                          ...newEvent,
                          reminders: newEvent.reminders.filter((_, i) => i !== idx),
                        });
                      }}
                      style={{
                        marginLeft: "0.5rem",
                        background: "none",
                        border: "none",
                        cursor: "pointer",
                        color: "#666",
                      }}
                    >
                      ×
                    </button>
                  </span>
                ))}
                <button
                  onClick={addReminder}
                  style={{
                    padding: "0.25rem 0.5rem",
                    backgroundColor: "#2196f3",
                    color: "white",
                    border: "none",
                    borderRadius: "4px",
                    cursor: "pointer",
                    fontSize: "0.85rem",
                  }}
                >
                  + Add Reminder
                </button>
              </div>
            </div>
            <button
              onClick={createEvent}
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
              Create Event
            </button>
          </div>
        </div>
      )}

      {displayEvents.length === 0 ? (
        <div style={{ padding: "2rem", textAlign: "center", color: "#666" }}>
          <p>No events found.</p>
        </div>
      ) : (
        <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
          {displayEvents.map((event) => {
            const start = formatDateTime(event.start_time);
            const end = event.end_time ? formatDateTime(event.end_time) : null;
            return (
              <div
                key={event.id}
                style={{
                  padding: "1rem",
                  backgroundColor: "white",
                  border: "1px solid #ddd",
                  borderRadius: "4px",
                  borderLeft: "4px solid #2196f3",
                }}
              >
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "start", marginBottom: "0.5rem" }}>
                  <div>
                    <h3 style={{ margin: 0, fontSize: "1.1rem" }}>{event.title}</h3>
                    <div style={{ fontSize: "0.9rem", color: "#666", marginTop: "0.25rem" }}>
                      📅 {start.date} at {start.time}
                      {end && ` - ${end.time}`}
                    </div>
                  </div>
                  {event.status === "cancelled" && (
                    <span
                      style={{
                        padding: "0.25rem 0.5rem",
                        backgroundColor: "#ffebee",
                        color: "#c62828",
                        borderRadius: "4px",
                        fontSize: "0.8rem",
                        fontWeight: "bold",
                      }}
                    >
                      CANCELLED
                    </span>
                  )}
                </div>
                {event.description && (
                  <p style={{ margin: "0.5rem 0", fontSize: "0.9rem", color: "#666" }}>{event.description}</p>
                )}
                <div style={{ display: "flex", gap: "0.5rem", flexWrap: "wrap", marginBottom: "0.5rem" }}>
                  {event.location && (
                    <span
                      style={{
                        padding: "0.25rem 0.5rem",
                        backgroundColor: "#f3e5f5",
                        borderRadius: "4px",
                        fontSize: "0.8rem",
                      }}
                    >
                      📍 {event.location}
                    </span>
                  )}
                  {event.category && (
                    <span
                      style={{
                        padding: "0.25rem 0.5rem",
                        backgroundColor: "#e3f2fd",
                        borderRadius: "4px",
                        fontSize: "0.8rem",
                      }}
                    >
                      {event.category}
                    </span>
                  )}
                  {event.is_recurring === "yes" && (
                    <span
                      style={{
                        padding: "0.25rem 0.5rem",
                        backgroundColor: "#fff3e0",
                        borderRadius: "4px",
                        fontSize: "0.8rem",
                      }}
                    >
                      🔄 {event.recurrence_frequency}
                    </span>
                  )}
                  {event.attendees && (
                    <span
                      style={{
                        padding: "0.25rem 0.5rem",
                        backgroundColor: "#e8f5e9",
                        borderRadius: "4px",
                        fontSize: "0.8rem",
                      }}
                    >
                      👥 {event.attendees}
                    </span>
                  )}
                </div>
                {event.reminders && event.reminders.length > 0 && (
                  <div style={{ fontSize: "0.85rem", color: "#999", marginTop: "0.25rem" }}>
                    🔔 Reminders: {event.reminders.map((r) => `${r.minutes} min`).join(", ")} before
                  </div>
                )}
                {event.status !== "cancelled" && (
                  <div style={{ marginTop: "0.75rem", display: "flex", gap: "0.5rem" }}>
                    <button
                      onClick={() => updateEvent(event.id, { status: "cancelled" })}
                      style={{
                        padding: "0.5rem 1rem",
                        backgroundColor: "#f44336",
                        color: "white",
                        border: "none",
                        borderRadius: "4px",
                        cursor: "pointer",
                        fontSize: "0.9rem",
                      }}
                    >
                      Cancel Event
                    </button>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}

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
            Ask Otto to create an event
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
        <p style={{ marginTop: "0.5rem", fontSize: "0.9rem", color: "#666" }}>
          💡 <strong>Google Calendar Integration:</strong> Coming soon! For now, events are stored locally. Future versions will sync with Google Calendar.
        </p>
      </div>
    </div>
  );
}

