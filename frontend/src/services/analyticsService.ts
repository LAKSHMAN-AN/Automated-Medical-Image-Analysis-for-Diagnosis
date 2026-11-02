import { api } from './api';
import { AnalyticsSummary } from '../types';

export const analyticsService = {
  async getSummary(): Promise<AnalyticsSummary> {
    const res = await api.get<AnalyticsSummary>('/analytics/summary');
    return res.data;
  }
};
