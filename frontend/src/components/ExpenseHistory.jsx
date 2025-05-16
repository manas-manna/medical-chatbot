import React from "react";

const ExpenseHistory = ({ expenses }) => {
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold mb-4">🧾 Expense History</h2>
      {expenses.map((exp, index) => (
        <div
          key={index}
          className="p-4 bg-white rounded shadow flex justify-between items-center"
        >
          <div>
            <p>
              <strong>Category:</strong> {exp.category}
            </p>
            <p>
              <strong>Amount:</strong> ₹{exp.amount}
            </p>
            <p>
              <strong>Date:</strong>{" "}
              {new Date(exp.timestamp).toLocaleString()}
            </p>
          </div>
          {exp.fraud && (
            <span className="text-red-600 font-semibold text-lg">
              ⚠️ Fraud
            </span>
          )}
        </div>
      ))}
    </div>
  );
};

export default ExpenseHistory;
