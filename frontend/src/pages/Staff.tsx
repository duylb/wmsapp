import { useEffect, useState } from "react";
import {
  fetchStaff,
  createStaff,
  updateStaff,
  deleteStaff,
  Staff as StaffType,
} from "../api/staff";

export default function Staff() {
  const [staff, setStaff] = useState<StaffType[]>([]);
  const [form, setForm] = useState<Partial<StaffType>>({});

  const loadStaff = async () => {
    const data = await fetchStaff();
    setStaff(data);
  };

  useEffect(() => {
    loadStaff();
  }, []);

  const handleCreate = async () => {
    await createStaff(form);
    setForm({});
    loadStaff();
  };

  const handleDelete = async (id: number) => {
    await deleteStaff(id);
    loadStaff();
  };

  return (
    <div>
      <h1>Staff</h1>

      <div style={{ marginBottom: 20 }}>
        <input
          placeholder="Full Name"
          value={form.full_name || ""}
          onChange={(e) => setForm({ ...form, full_name: e.target.value })}
        />
        <input
          placeholder="Position"
          value={form.position || ""}
          onChange={(e) => setForm({ ...form, position: e.target.value })}
        />
        <select
          value={form.salary_type || ""}
          onChange={(e) => setForm({ ...form, salary_type: e.target.value })}
        >
          <option value="">Salary Type</option>
          <option value="hourly">Hourly</option>
          <option value="package">Package</option>
        </select>

        <button onClick={handleCreate}>Add</button>
      </div>

      <table width="100%" border={1} cellPadding={8}>
        <thead>
          <tr>
            <th>Name</th>
            <th>Position</th>
            <th>Salary Type</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {staff.map((s) => (
            <tr key={s.id}>
              <td>{s.full_name}</td>
              <td>{s.position}</td>
              <td>{s.salary_type}</td>
              <td>
                <button onClick={() => handleDelete(s.id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}