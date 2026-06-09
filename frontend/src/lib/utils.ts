/**
 * Accepts an object, hashes it, and maps it to an integer in the range [0, n] inclusive.
 */
export function hashObject(value: unknown, n: number): number {
  if (n <= 0) {
    throw new Error('n must be positive');
  }

  const json = JSON.stringify(sortKeys(value));

  let hash = 0x811c9dc5; // FNV-1a 32-bit offset basis
  for (let i = 0; i < json.length; i++) {
    hash ^= json.charCodeAt(i);
    hash = Math.imul(hash, 0x01000193); // FNV prime
  }

  return (hash >>> 0) % (n + 1); // maps to [0, n]
}

/**
 * Utility method to take an object and sort its keys (recursively when needed)
 * so it is hashed consistently.
 */
function sortKeys(value: unknown): unknown {
  if (Array.isArray(value)) {
    return value.map(sortKeys);
  }

  if (value && typeof value === 'object') {
    return Object.fromEntries(
      Object.entries(value as Record<string, unknown>)
        .sort(([a], [b]) => a.localeCompare(b))
        .map(([k, v]) => [k, sortKeys(v)])
    );
  }

  return value;
}
