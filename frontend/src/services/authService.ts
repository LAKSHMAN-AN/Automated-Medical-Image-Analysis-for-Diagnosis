import { api } from './api';
import { User } from '../types';

export const authService = {
  async register(data: { email: string; password: string; full_name: string; role: string }): Promise<User> {
    const res = await api.post<User>('/auth/register', data);
    return res.data;
  },
  async getMe(): Promise<User> {
    const res = await api.get<User>('/users/me');
    return res.data;
  },
  async forgotPassword(email: string) {
    const res = await api.post('/auth/forgot-password', { email });
    return res.data;
  },
  async resetPassword(token: string, new_password: string) {
    const res = await api.post('/auth/reset-password', { token, new_password });
    return res.data;
  }
};
