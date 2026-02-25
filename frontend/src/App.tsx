import { Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Staff from "./pages/Staff";
import Roster from "./pages/Roster";
import Payroll from "./pages/Payroll";
import Layout from "./components/layout/Layout";
import { useAuthStore } from "./store/authStore";

export default function App() {
  const token = useAuthStore((state) => state.token);

  if (!token) {
    return <Login />;
  }

  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/staff" element={<Staff />} />
        <Route path="/roster" element={<Roster />} />
        <Route path="/payroll" element={<Payroll />} />
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </Layout>
  );
}