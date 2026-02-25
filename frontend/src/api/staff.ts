import { apiClient } from "./client";

export interface Staff {
  id: number;
  full_name: string;
  position: string;
  phone?: string;
  email?: string;
  address?: string;
  salary_type: string;
  hourly_rate?: number;
  package_salary?: number;
  is_active: boolean;
}

export const fetchStaff = async (): Promise<Staff[]> => {
  const response = await apiClient.get("/staff");
  return response.data;
};

export const createStaff = async (data: Partial<Staff>) => {
  const response = await apiClient.post("/staff", data);
  return response.data;
};

export const updateStaff = async (id: number, data: Partial<Staff>) => {
  const response = await apiClient.put(`/staff/${id}`, data);
  return response.data;
};

export const deleteStaff = async (id: number) => {
  const response = await apiClient.delete(`/staff/${id}`);
  return response.data;
};