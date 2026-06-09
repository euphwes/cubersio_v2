/**
 * Shared lock state for site navigation (navbar and compete sidebar).
 *
 * The compete view locks navigation while a solve is in progress and while a completed solve
 * is awaiting submit/discard, so the user can't switch events or routes mid-solve.
 */
export class NavigationLock {
  /** True during inspection and while the timer runs; owned by Timer. */
  timerActive = $state(false);

  /** True while a completed solve awaits submit/discard; owned by CompetitionTimerPanel. */
  solvePending = $state(false);

  get navigationAllowed(): boolean {
    return !this.timerActive && !this.solvePending;
  }
}
