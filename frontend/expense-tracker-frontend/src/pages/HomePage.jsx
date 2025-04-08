import React, { useEffect, useState } from "react";
import axios from "axios";
import AddExpenseForm from "../components/AddExpenseForm";
import TimeFilter from "../components/TimeFilter";
import CategoryPieChart from "../components/CategoryPieChart";
import ExpenseSummary from "../components/ExpenseSummary";

const HomePage = () => {
  const [range, setRange] = useState("7d");
  const [summary, setSummary] = useState({});

  const fetchSummary = async () => {
    const res = await axios.get(
      `http://localhost:8080/api/expenses/manas@gmail.com/summary?range=${range}`
    );
    setSummary(res.data);
  };

  useEffect(() => {
    fetchSummary();
  }, [range]);

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-4xl mx-auto space-y-8">
        <h1 className="text-3xl font-bold text-center">
          💸 Expense Tracker Dashboard
        </h1>

        <AddExpenseForm onExpenseAdded={fetchSummary} />
        <TimeFilter selectedRange={range} onRangeChange={setRange} />
        <div className="flex flex-col md:flex-row gap-8 items-start justify-between">
          <CategoryPieChart data={summary} />
          <ExpenseSummary data={summary} />
        </div>
      </div>
    </div>
  );
};

export default HomePage;
