import pkg from 'svg-round-corners';
const { roundCorners } = pkg;

const path = process.argv[2];
const radius = process.argv[3];

const result = roundCorners(path, radius, 2);
console.log(result.path);