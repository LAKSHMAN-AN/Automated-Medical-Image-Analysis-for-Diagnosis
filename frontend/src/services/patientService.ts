import { api } from './api';
import { Patient } from '../types';

export const patientService = {
  async getAll(): Promise<Patient[]> {
    const res = await api.get<Patient[]>('/patients/');
    return res.data;
  },
  async getById(id: string): Promise<Patient> {
    const res = await api.get<Patient>(`/patients/${id}`);
    return res.data;
  },
  async create(data: { patient_code: string; age: number; gender: string; medical_history?: string }): Promise<Patient> {
    const res = await api.post<Patient>('/patients/', data);
    return res.data;
  }
};
