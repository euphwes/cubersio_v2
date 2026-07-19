<!--
@component
The cubers.io logo: a single 3x3 cube face. Original, I know.

Sticker colors are chosen by hashing today's date, so the face is
static every day but rescrambles daily.
-->

<script lang="ts">
  import { hashObject } from '$lib/utils.js';

  // Tile geometry; the face spans 3 tiles + 2 gaps = 204 viewBox units
  const TILE = 66;
  const GAP = 4;
  const STEP = TILE + GAP;
  const FACE = 3 * TILE + 2 * GAP;

  // Backing square behind the stickers; PAD is how far it extends beyond the
  // face on each side (8 units is roughly 2px at the default 50px icon size)
  const PAD = 6;
  const BG_RADIUS = 10;

  // The old cubers.io scramble renderer drew 30px stickers; radii below are in
  // that coordinate space and get scaled up to TILE-sized tiles here
  const SCALE = TILE / 30;

  // Per-corner radii [UL, DL, DR, UR] for each tile, indexed [row][col].
  type CornerRadii = [number, number, number, number];
  const RADII: CornerRadii[][] = [
    [
      [2, 2, 6, 2],
      [2, 8, 8, 2],
      [2, 6, 2, 2]
    ],
    [
      [2, 2, 8, 8],
      [12, 12, 12, 12],
      [8, 8, 2, 2]
    ],
    [
      [2, 2, 2, 6],
      [8, 2, 2, 8],
      [6, 2, 2, 2]
    ]
  ];

  // Sticker color CSS variables, defined globally in app.css
  const COLORS = [
    'var(--cube-white)',
    'var(--cube-red)',
    'var(--cube-blue)',
    'var(--cube-green)',
    'var(--cube-yellow)',
    'var(--cube-orange)'
  ];

  // Today's date as yyyy/mm/dd, used as the hash input below so the sticker
  // colors change on a daily basis.
  const now = new Date();
  const dateKey = [
    now.getFullYear(),
    String(now.getMonth() + 1).padStart(2, '0'),
    String(now.getDate()).padStart(2, '0')
  ].join('/');

  /**
   * Picks today's sticker colors by shuffling an array holding three copies
   * of each color, and picking the first 9, so a color can only appear up to
   * three times, ensuring a little variety each day.
   */
  function dailyFills(): string[][] {
    const deck = [...COLORS, ...COLORS, ...COLORS];
    for (let i = deck.length - 1; i > 0; i--) {
      const j = hashObject({ date: dateKey, salt: i }, i);
      [deck[i], deck[j]] = [deck[j], deck[i]];
    }
    return [deck.slice(0, 3), deck.slice(3, 6), deck.slice(6, 9)];
  }

  // Sticker colors, indexed [row][col]
  const FILLS: string[][] = dailyFills();

  /**
   * Builds the path for the tile at grid position (col, row): a square traced
   * UL -> DL -> DR -> UR with a quadratic curve through each corner, the same
   * shape the old canvas renderer produced with quadraticCurveTo.
   */
  function tilePath(col: number, row: number): string {
    const [ul, dl, dr, ur] = RADII[row][col].map(
      (r) => Math.round(r * SCALE * 10) / 10
    ) as CornerRadii;
    const x = col * STEP;
    const y = row * STEP;
    const s = TILE;
    return [
      `M ${x} ${y + ul}`,
      `L ${x} ${y + s - dl}`,
      `Q ${x} ${y + s} ${x + dl} ${y + s}`,
      `L ${x + s - dr} ${y + s}`,
      `Q ${x + s} ${y + s} ${x + s} ${y + s - dr}`,
      `L ${x + s} ${y + ur}`,
      `Q ${x + s} ${y} ${x + s - ur} ${y}`,
      `L ${x + ul} ${y}`,
      `Q ${x} ${y} ${x} ${y + ul}`,
      'Z'
    ].join(' ');
  }
</script>

<div class="icon">
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="{-PAD} {-PAD} {FACE + 2 * PAD} {FACE + 2 * PAD}"
    width="100%"
    height="100%"
  >
    <rect
      x={-PAD}
      y={-PAD}
      width={FACE + 2 * PAD}
      height={FACE + 2 * PAD}
      rx={BG_RADIUS}
      fill="var(--cube-innard)"
    />

    <g stroke="var(--cube-innard)">
      {#each FILLS as rowFills, row (row)}
        {#each rowFills as fill, col (col)}
          <path d={tilePath(col, row)} {fill} />
        {/each}
      {/each}
    </g>
  </svg>
</div>

<style>
  .icon {
    width: var(--icon-size, 50px);
    height: var(--icon-size, 50px);
    cursor: pointer;
  }
</style>
