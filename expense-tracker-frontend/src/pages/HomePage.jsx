import React, { useEffect, useState } from "react";
import axios from "axios";
import AddExpenseForm from "../components/AddExpenseForm";
import TimeFilter from "../components/TimeFilter";
import CategoryPieChart from "../components/CategoryPieChart";
import ExpenseSummary from "../components/ExpenseSummary";
import ExpenseHistory from "../components/ExpenseHistory";

const HomePage = () => {
  const [range, setRange] = useState("7d");
  const [summary, setSummary] = useState({});
  const [expenses, setExpenses] = useState([]);
  const [view, setView] = useState("summary"); // 'summary' or 'history'

  const fetchSummary = async () => {
    const res = await axios.get(
      `http://localhost:9000/api/expenses/manas@gmail.com/summary?range=${range}`
    );
    setSummary(res.data);
  };

  const fetchExpenses = async () => {
    const res = await axios.get(`http://localhost:9000/api/expenses/manas@gmail.com`);
    const sorted = res.data.sort(
      (a, b) => new Date(b.timestamp) - new Date(a.timestamp)
    );
    setExpenses(sorted);
  };

  const refreshAll = async () => {
    await fetchSummary();
    await fetchExpenses();
  };

  useEffect(() => {
    fetchSummary();
    fetchExpenses();
  }, [range]);

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-4xl mx-auto space-y-8">
        <h1 className="text-3xl font-bold text-center">
          💸 Expense Tracker Dashboard
        </h1>

        <div className="flex justify-center gap-4">
          <button
            onClick={() => setView("summary")}
            className={`px-4 py-2 rounded ${
              view === "summary"
                ? "bg-blue-600 text-white"
                : "bg-gray-300 text-black"
            }`}
          >
            Summary
          </button>
          <button
            onClick={() => setView("history")}
            className={`px-4 py-2 rounded ${
              view === "history"
                ? "bg-green-600 text-white"
                : "bg-gray-300 text-black"
            }`}
          >
            History
          </button>
        </div>

        <AddExpenseForm onExpenseAdded={refreshAll} />

        {view === "summary" ? (
          <>
            <TimeFilter selectedRange={range} onRangeChange={setRange} />
            <div className="flex flex-col md:flex-row gap-8 items-start justify-between">
              <CategoryPieChart data={summary} />
              <ExpenseSummary data={summary} />
            </div>
          </>
        ) : (
          <ExpenseHistory expenses={expenses} />
        )}
      </div>
    </div>
  );
};

export default HomePage;
