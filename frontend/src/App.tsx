import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider, useAuth } from "./auth/AuthProvider";
import Products from "./pages/Products";
import Login from "./pages/Login";
import TestLogin from "./pages/TestLogin";
import Orders from "./pages/Orders";

function PrivateRoute({ children }: { children: React.ReactElement }) {
  const { tokens } = useAuth();
  return tokens ? children : <Navigate to="/login" replace />;
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/" element={<PrivateRoute><Products /></PrivateRoute>} />
          <Route path="/test-login" element={<TestLogin />} />
          <Route path="/orders" element={<PrivateRoute><Orders /></PrivateRoute>} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
