import { useEffect, useState } from "react";
import { fetchStaff } from "../api/staff";
import { fetchPayrollPeriods } from "../api/payroll";

export default function Dashboard() {
  const [staffCount, setStaffCount] = useState(0);
  const [payrollCount, setPayrollCount] = useState(0);

  useEffect(() => {
    const load = async () => {
      const staff = await fetchStaff();
      const payrolls = await fetchPayrollPeriods();

      setStaffCount(staff.length);
      setPayrollCount(payrolls.length);
    };

    load();
  }, []);

  return (
    <div>
      <h1>Dashboard</h1>

      <div style={{ display: "flex", gap: "20px", marginTop: "20px" }}>
        <div
          style={{
            background: "#1e293b",
            padding: "20px",
            borderRadius: "8px",
            width: "200px",
          }}
        >
          <h3>Total Staff</h3>
          <p style={{ fontSize: "24px" }}>{staffCount}</p>
        </div>

        <div
          style={{
            background: "#1e293b",
            padding: "20px",
            borderRadius: "8px",
            width: "200px",
          }}
        >
          <h3>Payroll Periods</h3>
          <p style={{ fontSize: "24px" }}>{payrollCount}</p>
        </div>
      </div>
    </div>
  );
}