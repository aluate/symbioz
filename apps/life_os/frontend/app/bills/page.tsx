"use client";

import { useState, useEffect } from "react";
import Link from "next/link";

interface Bill {
  id: number;
  name: string;
  amount: string;
  due_date: string;
  paid: "yes" | "no" | "partial";
  category?: string;
  payee?: string;
  account_number?: string;
  notes?: string;
  is_recurring: string;
  recurrence_frequency?: string;
  next_due_date?: string;
  created_at: string;
  updated_at: string;
  paid_at?: string;
}

export default function BillsPage() {
  const [bills, setBills] = useState<Bill[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [filter, setFilter] = useState<"all" | "upcoming" | "overdue" | "paid">("all");
  const [summary, setSummary] = useState<{
    upcoming_count: number;
    total_amount: string;
    overdue_count: number;
  } | null>(null);
  const [newBill, setNewBill] = useState({
    name: "",
    amount: "",
    due_date: "",
    category: "",
    payee: "",
    account_number: "",
    notes: "",
    is_recurring: "no",
    recurrence_frequency: "monthly",
  });

  const getApiUrl = () => {
    if (typeof window !== "undefined") {
      return `${window.location.protocol}//${window.location.hostname}:8000`;
    }
    return "http://localhost:8000";
  };

  const fetchBills = async () => {
    try {
      const params = new URLSearchParams();
      if (filter === "upcoming") {
        params.append("upcoming", "true");
      } else if (filter === "overdue") {
        params.append("overdue", "true");
      } else if (filter === "paid") {
        params.append("paid", "yes");
      } else {
        params.append("paid", "no");
      }

      const response = await fetch(`${getApiUrl()}/bills?${params.toString()}`);
      if (!response.ok) throw new Error("Failed to fetch bills");
      const data = await response.json();
      setBills(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load bills");
    } finally {
      setLoading(false);
    }
  };

  const fetchSummary = async () => {
    try {
      const response = await fetch(`${getApiUrl()}/bills/upcoming/summary?days=30`);
      if (response.ok) {
        const data = await response.json();
        setSummary({
          upcoming_count: data.upcoming_count,
          total_amount: data.total_amount,
          overdue_count: data.overdue_count,
        });
      }
    } catch (err) {
      // Summary is optional, don't fail if it errors
    }
  };

  const createBill = async () => {
    if (!newBill.name.trim() || !newBill.amount.trim() || !newBill.due_date) return;

    try {
      const response = await fetch(`${getApiUrl()}/bills`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ...newBill,
          due_date: newBill.due_date ? new Date(newBill.due_date).toISOString() : null,
          is_recurring: newBill.is_recurring,
          recurrence_frequency: newBill.is_recurring === "yes" ? newBill.recurrence_frequency : null,
        }),
      });

      if (!response.ok) throw new Error("Failed to create bill");

      setNewBill({
        name: "",
        amount: "",
        due_date: "",
        category: "",
        payee: "",
        account_number: "",
        notes: "",
        is_recurring: "no",
        recurrence_frequency: "monthly",
      });
      setShowCreateForm(false);
      await fetchBills();
      await fetchSummary();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create bill");
    }
  };

  const updateBill = async (billId: number, updates: Partial<Bill>) => {
    try {
      const response = await fetch(`${getApiUrl()}/bills/${billId}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(updates),
      });

      if (!response.ok) throw new Error("Failed to update bill");
      await fetchBills();
      await fetchSummary();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to update bill");
    }
  };

  useEffect(() => {
    fetchBills();
    fetchSummary();
  }, [filter]);

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString();
  };

  const isOverdue = (dueDate: string, paid: string) => {
    if (paid === "yes") return false;
    const due = new Date(dueDate);
    const now = new Date();
    return due < now;
  };

  const isUpcoming = (dueDate: string, paid: string) => {
    if (paid === "yes") return false;
    const due = new Date(dueDate);
    const now = new Date();
    const daysUntilDue = Math.ceil((due.getTime() - now.getTime()) / (1000 * 60 * 60 * 24));
    return daysUntilDue >= 0 && daysUntilDue <= 7;
  };

  if (loading) {
    return (
      <div style={{ padding: "2rem", textAlign: "center" }}>
        <p>Loading bills...</p>
      </div>
    );
  }

  return (
    <div style={{ padding: "1rem", maxWidth: "1200px", margin: "0 auto" }}>
      <div style={{ marginBottom: "1rem", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <h1 style={{ fontSize: "1.75rem", margin: 0 }}>Bills</h1>
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
            {showCreateForm ? "Cancel" : "+ New Bill"}
          </button>
        </div>
      </div>

      {summary && (
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
            gap: "1rem",
            marginBottom: "2rem",
          }}
        >
          <div style={{ padding: "1rem", backgroundColor: "#e3f2fd", borderRadius: "4px", border: "1px solid #2196f3" }}>
            <div style={{ fontSize: "0.9rem", color: "#666", marginBottom: "0.25rem" }}>Upcoming Bills</div>
            <div style={{ fontSize: "1.5rem", fontWeight: "bold", color: "#2196f3" }}>
              {summary.upcoming_count}
            </div>
          </div>
          <div style={{ padding: "1rem", backgroundColor: "#fff3e0", borderRadius: "4px", border: "1px solid #ff9800" }}>
            <div style={{ fontSize: "0.9rem", color: "#666", marginBottom: "0.25rem" }}>Total Amount</div>
            <div style={{ fontSize: "1.5rem", fontWeight: "bold", color: "#ff9800" }}>
              {summary.total_amount}
            </div>
          </div>
          <div style={{ padding: "1rem", backgroundColor: "#ffebee", borderRadius: "4px", border: "1px solid #f44336" }}>
            <div style={{ fontSize: "0.9rem", color: "#666", marginBottom: "0.25rem" }}>Overdue</div>
            <div style={{ fontSize: "1.5rem", fontWeight: "bold", color: "#f44336" }}>
              {summary.overdue_count}
            </div>
          </div>
        </div>
      )}

      <div style={{ marginBottom: "1rem", display: "flex", gap: "0.5rem", flexWrap: "wrap" }}>
        <button
          onClick={() => setFilter("all")}
          style={{
            padding: "0.5rem 1rem",
            backgroundColor: filter === "all" ? "#0070f3" : "#f0f0f0",
            color: filter === "all" ? "white" : "black",
            border: "none",
            borderRadius: "4px",
            cursor: "pointer",
          }}
        >
          All Unpaid
        </button>
        <button
          onClick={() => setFilter("upcoming")}
          style={{
            padding: "0.5rem 1rem",
            backgroundColor: filter === "upcoming" ? "#0070f3" : "#f0f0f0",
            color: filter === "upcoming" ? "white" : "black",
            border: "none",
            borderRadius: "4px",
            cursor: "pointer",
          }}
        >
          Upcoming
        </button>
        <button
          onClick={() => setFilter("overdue")}
          style={{
            padding: "0.5rem 1rem",
            backgroundColor: filter === "overdue" ? "#0070f3" : "#f0f0f0",
            color: filter === "overdue" ? "white" : "black",
            border: "none",
            borderRadius: "4px",
            cursor: "pointer",
          }}
        >
          Overdue
        </button>
        <button
          onClick={() => setFilter("paid")}
          style={{
            padding: "0.5rem 1rem",
            backgroundColor: filter === "paid" ? "#0070f3" : "#f0f0f0",
            color: filter === "paid" ? "white" : "black",
            border: "none",
            borderRadius: "4px",
            cursor: "pointer",
          }}
        >
          Paid
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
          <h3 style={{ marginTop: 0 }}>Create New Bill</h3>
          <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
            <div>
              <label style={{ display: "block", marginBottom: "0.5rem", fontWeight: "bold" }}>
                Bill Name *
              </label>
              <input
                type="text"
                value={newBill.name}
                onChange={(e) => setNewBill({ ...newBill, name: e.target.value })}
                style={{
                  width: "100%",
                  padding: "0.5rem",
                  border: "1px solid #ccc",
                  borderRadius: "4px",
                }}
                placeholder="Electric Bill"
              />
            </div>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "1rem" }}>
              <div>
                <label style={{ display: "block", marginBottom: "0.5rem", fontWeight: "bold" }}>
                  Amount *
                </label>
                <input
                  type="text"
                  value={newBill.amount}
                  onChange={(e) => setNewBill({ ...newBill, amount: e.target.value })}
                  style={{
                    width: "100%",
                    padding: "0.5rem",
                    border: "1px solid #ccc",
                    borderRadius: "4px",
                  }}
                  placeholder="$150.00"
                />
              </div>
              <div>
                <label style={{ display: "block", marginBottom: "0.5rem", fontWeight: "bold" }}>
                  Due Date *
                </label>
                <input
                  type="date"
                  value={newBill.due_date}
                  onChange={(e) => setNewBill({ ...newBill, due_date: e.target.value })}
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
                  Payee
                </label>
                <input
                  type="text"
                  value={newBill.payee}
                  onChange={(e) => setNewBill({ ...newBill, payee: e.target.value })}
                  style={{
                    width: "100%",
                    padding: "0.5rem",
                    border: "1px solid #ccc",
                    borderRadius: "4px",
                  }}
                  placeholder="Company name"
                />
              </div>
              <div>
                <label style={{ display: "block", marginBottom: "0.5rem", fontWeight: "bold" }}>
                  Category
                </label>
                <input
                  type="text"
                  value={newBill.category}
                  onChange={(e) => setNewBill({ ...newBill, category: e.target.value })}
                  style={{
                    width: "100%",
                    padding: "0.5rem",
                    border: "1px solid #ccc",
                    borderRadius: "4px",
                  }}
                  placeholder="utilities, subscription, etc."
                />
              </div>
            </div>
            <div>
              <label style={{ display: "block", marginBottom: "0.5rem", fontWeight: "bold" }}>
                Account Number
              </label>
              <input
                type="text"
                value={newBill.account_number}
                onChange={(e) => setNewBill({ ...newBill, account_number: e.target.value })}
                style={{
                  width: "100%",
                  padding: "0.5rem",
                  border: "1px solid #ccc",
                  borderRadius: "4px",
                }}
                placeholder="Account number"
              />
            </div>
            <div>
              <label style={{ display: "flex", alignItems: "center", gap: "0.5rem", marginBottom: "0.5rem" }}>
                <input
                  type="checkbox"
                  checked={newBill.is_recurring === "yes"}
                  onChange={(e) =>
                    setNewBill({ ...newBill, is_recurring: e.target.checked ? "yes" : "no" })
                  }
                />
                <span style={{ fontWeight: "bold" }}>Recurring Bill</span>
              </label>
              {newBill.is_recurring === "yes" && (
                <select
                  value={newBill.recurrence_frequency}
                  onChange={(e) => setNewBill({ ...newBill, recurrence_frequency: e.target.value })}
                  style={{
                    width: "100%",
                    padding: "0.5rem",
                    border: "1px solid #ccc",
                    borderRadius: "4px",
                    marginTop: "0.5rem",
                  }}
                >
                  <option value="monthly">Monthly</option>
                  <option value="quarterly">Quarterly</option>
                  <option value="yearly">Yearly</option>
                </select>
              )}
            </div>
            <div>
              <label style={{ display: "block", marginBottom: "0.5rem", fontWeight: "bold" }}>
                Notes
              </label>
              <textarea
                value={newBill.notes}
                onChange={(e) => setNewBill({ ...newBill, notes: e.target.value })}
                style={{
                  width: "100%",
                  padding: "0.5rem",
                  border: "1px solid #ccc",
                  borderRadius: "4px",
                  minHeight: "80px",
                }}
                placeholder="Additional notes"
              />
            </div>
            <button
              onClick={createBill}
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
              Create Bill
            </button>
          </div>
        </div>
      )}

      {bills.length === 0 ? (
        <div style={{ padding: "2rem", textAlign: "center", color: "#666" }}>
          <p>No bills found.</p>
        </div>
      ) : (
        <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
          {bills.map((bill) => (
            <div
              key={bill.id}
              style={{
                padding: "1rem",
                backgroundColor: "white",
                border: "1px solid #ddd",
                borderRadius: "4px",
                borderLeft: isOverdue(bill.due_date, bill.paid)
                  ? "4px solid #f44336"
                  : isUpcoming(bill.due_date, bill.paid)
                  ? "4px solid #ff9800"
                  : "4px solid #4caf50",
              }}
            >
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "start", marginBottom: "0.5rem" }}>
                <div>
                  <h3 style={{ margin: 0, fontSize: "1.1rem" }}>{bill.name}</h3>
                  {bill.payee && (
                    <p style={{ margin: "0.25rem 0", fontSize: "0.9rem", color: "#666" }}>
                      Payee: {bill.payee}
                    </p>
                  )}
                </div>
                <div style={{ textAlign: "right" }}>
                  <div style={{ fontSize: "1.25rem", fontWeight: "bold", color: "#0070f3" }}>
                    {bill.amount}
                  </div>
                  <div style={{ fontSize: "0.85rem", color: "#666" }}>
                    Due: {formatDate(bill.due_date)}
                  </div>
                </div>
              </div>
              <div style={{ display: "flex", gap: "0.5rem", flexWrap: "wrap", marginBottom: "0.5rem" }}>
                {bill.category && (
                  <span
                    style={{
                      padding: "0.25rem 0.5rem",
                      backgroundColor: "#e3f2fd",
                      borderRadius: "4px",
                      fontSize: "0.8rem",
                    }}
                  >
                    {bill.category}
                  </span>
                )}
                {bill.is_recurring === "yes" && (
                  <span
                    style={{
                      padding: "0.25rem 0.5rem",
                      backgroundColor: "#f3e5f5",
                      borderRadius: "4px",
                      fontSize: "0.8rem",
                    }}
                  >
                    🔄 {bill.recurrence_frequency}
                  </span>
                )}
                {isOverdue(bill.due_date, bill.paid) && (
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
                    OVERDUE
                  </span>
                )}
                {bill.paid === "yes" && (
                  <span
                    style={{
                      padding: "0.25rem 0.5rem",
                      backgroundColor: "#e8f5e9",
                      color: "#2e7d32",
                      borderRadius: "4px",
                      fontSize: "0.8rem",
                      fontWeight: "bold",
                    }}
                  >
                    ✓ PAID
                  </span>
                )}
              </div>
              {bill.notes && (
                <p style={{ margin: "0.5rem 0", fontSize: "0.9rem", color: "#666" }}>{bill.notes}</p>
              )}
              {bill.account_number && (
                <p style={{ margin: "0.25rem 0", fontSize: "0.85rem", color: "#999" }}>
                  Account: {bill.account_number}
                </p>
              )}
              {bill.paid !== "yes" && (
                <div style={{ marginTop: "0.75rem", display: "flex", gap: "0.5rem" }}>
                  <button
                    onClick={() => updateBill(bill.id, { paid: "yes" })}
                    style={{
                      padding: "0.5rem 1rem",
                      backgroundColor: "#4caf50",
                      color: "white",
                      border: "none",
                      borderRadius: "4px",
                      cursor: "pointer",
                      fontSize: "0.9rem",
                    }}
                  >
                    Mark as Paid
                  </button>
                </div>
              )}
            </div>
          ))}
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
            Ask Otto to check bills
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

