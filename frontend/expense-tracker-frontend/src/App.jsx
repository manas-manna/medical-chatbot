import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import UserList from "./pages/UserList";
import CreateUser from "./pages/CreateUser";
import AddExpense from "./pages/AddExpense";


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<UserList />} />
        <Route path="/create-user" element={<CreateUser />} />
        <Route path="/add-expense" element={<AddExpense />} />
      </Routes>
    </Router>
  );
}

export default App;
