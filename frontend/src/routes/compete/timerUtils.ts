export type TimerMode = 'waiting' | 'inspection' | 'running' | 'stopped' | 'dnf';

export function getHintText(mode: TimerMode): string {
  switch (mode) {
    case 'waiting':
      return 'Press Space to begin inspection';
    case 'inspection':
      return 'Press Space to start - Esc to cancel';
    case 'dnf':
      return 'DNF - press any key to record';
    case 'running':
      return 'Press any key to stop';
    case 'stopped':
      return 'Press Space for next solve';
  }
}

export function getMobileHintText(mode: TimerMode): string {
  switch (mode) {
    case 'waiting':
      return 'Tap to begin inspection';
    case 'inspection':
      return 'Tap to start timer';
    case 'dnf':
      return 'DNF - tap to record';
    case 'running':
      return 'Tap to stop';
    case 'stopped':
      return 'Tap for next solve';
  }
}
