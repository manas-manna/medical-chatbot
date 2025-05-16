import React from 'react';

const ExpenseSummary = ({ data }) => (
  <div className="mt-6">
    <h3 className="text-xl font-semibold mb-2">Category Summary</h3>
    <ul className="list-disc pl-6">
      {Object.entries(data).map(([category, amount]) => (
        <li key={category}>{category}: ₹{amount.toFixed(2)}</li>
      ))}
    </ul>
  </div>
);

export default ExpenseSummary;
