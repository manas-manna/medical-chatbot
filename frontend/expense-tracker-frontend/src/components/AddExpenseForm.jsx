import React, { useState } from 'react';
import axios from 'axios';
import toast from 'react-hot-toast';

const AddExpenseForm = ({ onExpenseAdded }) => {
  const [formData, setFormData] = useState({
    title: '',
    amount: '',
    category: '',
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:8080/api/expenses/manas@gmail.com', {
        ...formData
      });
      toast.success("Expense added!");
      setFormData({ title: '', amount: '', category: '' });
      onExpenseAdded(); // refresh dashboard
    } catch (error) {
      toast.error("Failed to add expense!");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white p-6 rounded-xl shadow-md space-y-4">
      <h2 className="text-xl font-semibold">Add New Expense</h2>

      <input
        name="title"
        value={formData.title}
        onChange={handleChange}
        placeholder="Title"
        className="w-full p-2 border rounded"
        required
      />
      <input
        name="amount"
        type="number"
        value={formData.amount}
        onChange={handleChange}
        placeholder="Amount"
        className="w-full p-2 border rounded"
        required
      />
      <select
        name="category"
        value={formData.category}
        onChange={handleChange}
        required
        className="w-full p-2 border rounded"
      >
        <option value="">Select Category</option>
        <option value="Stationary">Stationary</option>
        <option value="Electronics">Electronics</option>
        <option value="Food">Food</option>
        <option value="Travel">Travel</option>
      </select>

      <button
        type="submit"
        className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded"
      >
        Add Expense
      </button>
    </form>
  );
};

export default AddExpenseForm;
