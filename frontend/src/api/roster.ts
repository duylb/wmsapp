import { apiClient } from "./client";

export interface RosterEntry {
  id: number;
  staff_id: number;
  date: string;
  morning_shift_id?: number;
  afternoon_shift_id?: number;
}

export const fetchRoster = async (
  start_date: string,
  end_date: string
): Promise<RosterEntry[]> => {
  const response = await apiClient.get("/roster", {
    params: { start_date, end_date },
  });
  return response.data;
};

export const upsertRoster = async (data: {
  staff_id: number;
  date: string;
  morning_shift_id?: number;
  afternoon_shift_id?: number;
}) => {
  const response = await apiClient.post("/roster", data);
  return response.data;
};