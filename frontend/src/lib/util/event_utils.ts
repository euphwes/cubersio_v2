import type { EventSlug } from '$lib/types.js';

export const nameByEventSlug: Record<EventSlug, string> = {
  '222': '2x2',
  '333': '3x3',
  '444': '4x4',
  '555': '5x5',
  '666': '6x6',
  '777': '7x7',
  '888': '8x8',
  '999': '9x9',
  '10x': '10x10',
  fto: 'FTO',
  '3bld': '3x3 Blindfolded',
  '4bld': '4x4 Blindfolded',
  '5bld': '5x5 Blindfolded',
  '332': '3x3x2',
  '223': '2x2x3',
  '334': '3x3x4',
  '335': '3x3x5',
  skewb: 'Skewb',
  clock: 'Clock',
  sq1: 'Square-1',
  pyra: 'Pyraminx',
  mega: 'Megaminx',
  kilo: 'Kilominx',
  mbld: '3x3 Multi-Blind',
  rex: 'Rex Cube',
  bicube: 'BiCube',
  dino: 'Dino Cube',
  redi: 'Redi Cube',
  bump: 'Mirror Blocks',
  '3oh': '3x3 One-Handed',
  '15puzzle': '15 Puzzle',
  fmc: '3x3 Fewest Moves',
  '234relay': '2-3-4 Relay'
};

export const descriptionsByEventSlug: Record<EventSlug, string> = {
  '333':
    "The 3x3 is the iconic puzzle that started it all.\nWhether you're just getting started or chasing records, this is where legends are made.",
  '222':
    "The 2x2 is a miniature version of the classic puzzle.\nWith only corners to solve, it's a fast-paced event. Don't blink, or you'll miss the solve!",
  '444':
    'The 4x4 adds an extra layer of complexity with its center building and edge pairing.\nOLL and PLL parity can trip up even experienced solvers.',
  '555': 'The 5x5 ups the ante.\nCenter building and edge pairing become a true challenge.',
  '666':
    'The 6x6 is a beast of a puzzle.\nWith many opportunities for parity, this event is not for the faint of heart!',
  '777':
    'The 7x7 is the largest NxN in competition.\nSolvers must stay focused during this marathon of an event.',
  skewb:
    "The Skewb is a corner-turning puzzle that scrambles quickly and solves even faster.\nSimple to learn but difficult to master, it's a crowd favorite.",
  pyra: "The Pyraminx is a tetrahedral puzzle that's fairly intuitive to solve.\nIs it corner-turning or face-turning? That's an ongoing debate.",
  mega: 'The Megaminx is a dodecahedral puzzle with twelve faces.\nWhile the solve process is similar to a 3x3, the higher piece count makes for a longer solve.',
  fto: 'Face-Turning Octahedron (FTO) is a twisty puzzle with triangular faces.\nIts recent surge in popularity has led to better hardware, and a bid for a place in the WCA.',
  sq1: 'Square-1 is a shape-shifting puzzle that can quickly turn into a jumbled mess.\nSolvers must restore both shape and color, making it a unique challenge.',
  clock:
    "Rubik's Clock is a mechanical puzzle with nine clocks to align on each side.\nIt's a race against time!",
  fmc: '3x3 Fewest Moves is a battle of efficiency.\nSolvers have one hour to find the shortest possible solution to a given scramble.',
  '3oh':
    "This is exactly what it sounds like — solve the 3x3 using only one hand!\nDexterity is key, but don't be afraid to use the table, too.",
  '3bld':
    '3x3 Blindfolded is the classic memory challenge.\nCompetitors memorize the cube, don a blindfold, and solve it without peeking.',
  '4bld':
    '4x4 Blindfolded takes the blindfolded challenge to the next level.\nMore pieces, more memorization, and more opportunities for error.',
  '5bld':
    '5x5 Blindfolded is a true test of memory and technique.\nWith hundreds of pieces to track, you better start learning about memory palaces.',
  mbld: '3x3 Multi-Blind is the ultimate memory test.\nSolve as many 3x3 cubes as possible, all blindfolded, in one sitting.',
  kilo: "Kilominx is a smaller, simpler version of the Megaminx.\nIt's a fun and approachable corners-only dodecahedral challenge.",
  bump: 'Mirror Blocks, aka Bump Cube, is probably the most well-known 3x3 shape mod.\nAll pieces are the same color, and solvers must instead rely on shape and size.',
  redi: 'The Redi Cube is a simple corner-turning puzzle.\nMany can solve this intuitively, but solving it efficiently takes practice.',
  dino: "The Dino Cube is an interesting corner-turning puzzle.\nIt's one of only a few puzzles with multiple solved states!",
  rex: 'The Rex Cube is a corner-turning puzzle with petal-shaped pieces.\nIts unique mechanism and patterns make for a visually striking and enjoyable solve.',
  '15puzzle':
    'The 15 Puzzle is a sliding tile classic.\nArrange the numbers in order by sliding tiles into the empty space.',
  '234relay':
    "The 2-3-4 Relay is a race to solve cubing's most popular events in quick succession.\nSolve the 2x2, 3x3, and 4x4 in a single sitting as fast as possible!",
  '223':
    'The 2x2x3 cuboid is a quick but quirky solve.\nWhile it looks hardly more difficult than a 2x2, cuboids are truly their own sort of challenge.',
  '332':
    'The 3x3x2 is a great introduction into the world of cuboid puzzles.\nIts simple appearance belies a somewhat tricky solving experience.',
  '334':
    'The 3x3x4 cuboid adds a couple additional layers to the 3x3x2.\nThis introduces a new type of parity!',
  '335':
    'The 3x3x5 cuboid is a tall twisty tower with a fun twist.\nThis is the first 3x3xN cuboid that introduces shape-shifting!',
  bicube:
    "The BiCube is a bandaged 3x3 that looks simple but can be surprisingly tricky.\nIt's a fun twist on the classic cube shape.",
  '888':
    'The 8x8 is not part of official competitions, but it offers a satisfying test of control and precision.\nHardware quality becomes critical to avoid lockups during long solves.',
  '999':
    'The 9x9 is the ultimate test of patience and perseverance.\nAt this size, solving becomes more about rhythm and endurance than raw speed.',
  '10x':
    "Is tHaT a TeN bY tEn?\nThe 10x10 pushes beyond most solvers' regular routines. It's often tackled for the satisfaction of completion rather than competition, emphasizing consistency and error management."
};

export function getImagePath(eventSlug: EventSlug, solved: boolean) {
  return solved ? `/images/${eventSlug}s.svg` : `/images/${eventSlug}.svg`;
}
