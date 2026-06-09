import type { EventSlug } from '$lib/types.js';
import type { EventFormat } from './types.js';

export function getImagePath(eventSlug: EventSlug, solved: boolean) {
  return solved ? `/images/${eventSlug}s.svg` : `/images/${eventSlug}.svg`;
}

// Word describing the overall result; best-of formats rank by the single time.
export const RESULT_LABEL_BY_FORMAT: Record<EventFormat, string> = {
  ao5: 'average',
  mo3: 'mean',
  bo3: 'single',
  bo5: 'single',
  bo1: 'single'
};
