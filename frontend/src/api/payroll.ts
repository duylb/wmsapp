import { apiClient } from "./client";

export interface PayrollRecord {
  staff_id: number;
  total_hours: number;
  salary_amount: number;
}

export interface PayrollPeriod {
  id: number;
  month: number;
  year: number;
  is_locked: boolean;
  generated_at: string;
  records: PayrollRecord[];
}

export const generatePayroll = async (month: number, year: number) => {
  const response = await apiClient.post("/payroll/generate", {
    month,
    year,
  });
  return response.data;
};

export const fetchPayrollPeriods = async (): Promise<PayrollPeriod[]> => {
  const response = await apiClient.get("/payroll");
  return response.data;
};