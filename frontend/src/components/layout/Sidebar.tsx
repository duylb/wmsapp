import { useAuthStore } from "../../store/authStore";

export default function Navbar() {
  const logout = useAuthStore((state) => state.logout);

  return (
    <div
      style={{
        height: "60px",
        background: "#0f172a",
        color: "white",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "0 24px",
        borderBottom: "1px solid #1e293b",
      }}
    >
      <h3 style={{ margin: 0 }}>RosMan WMS</h3>

      <button
        onClick={logout}
        style={{
          background: "#dc2626",
          border: "none",
          color: "white",
          padding: "8px 16px",
          borderRadius: "6px",
          cursor: "pointer",
        }}
      >
        Logout
      </button>
    </div>
  );
}