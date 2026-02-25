import { create } from "zustand";

interface AppState {
  loading: boolean;
  setLoading: (value: boolean) => void;

  selectedMonth: number;
  selectedYear: number;
  setPayrollPeriod: (month: number, year: number) => void;
}

export const useAppStore = create<AppState>((set) => ({
  loading: false,
  setLoading: (value) => set({ loading: value }),

  selectedMonth: new Date().getMonth() + 1,
  selectedYear: new Date().getFullYear(),

  setPayrollPeriod: (month, year) =>
    set({
      selectedMonth: month,
      selectedYear: year,
    }),
}));