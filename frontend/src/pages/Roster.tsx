import { useState } from "react";
import { fetchRoster, upsertRoster } from "../api/roster";

export default function Roster() {
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [roster, setRoster] = useState<any[]>([]);

  const loadRoster = async () => {
    const data = await fetchRoster(startDate, endDate);
    setRoster(data);
  };

  return (
    <div>
      <h1>Roster</h1>

      <div style={{ marginBottom: 20 }}>
        <input
          type="date"
          value={startDate}
          onChange={(e) => setStartDate(e.target.value)}
        />
        <input
          type="date"
          value={endDate}
          onChange={(e) => setEndDate(e.target.value)}
        />
        <button onClick={loadRoster}>Load</button>
      </div>

      <pre>{JSON.stringify(roster, null, 2)}</pre>
    </div>
  );
}