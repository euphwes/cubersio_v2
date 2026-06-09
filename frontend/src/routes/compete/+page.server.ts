import type { WeeklyCompetitionRecord } from './types.js';

export const load = async ({ fetch }) => {
  const response = await fetch('/api/competition/current');
  const data: WeeklyCompetitionRecord = await response.json();
  return data;
};
