import { apiClient } from "./client";

export interface LoginPayload {
  email: string;
  password: string;
}

export interface RegisterPayload {
  company_name: string;
  company_slug: string;
  full_name: string;
  email: string;
  password: string;
}

export const login = async (data: LoginPayload) => {
  const response = await apiClient.post("/auth/login", data);
  return response.data;
};

export const register = async (data: RegisterPayload) => {
  const response = await apiClient.post("/auth/register", data);
  return response.data;
};