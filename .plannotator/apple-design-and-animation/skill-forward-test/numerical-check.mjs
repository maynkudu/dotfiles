import assert from 'node:assert/strict';
import { readFile, writeFile } from 'node:fs/promises';
import { compileTimeline, sampleTimeline, toCsv } from '/home/maynkudu/Code/Projects/apple-design-and-animation-system/skills/apple-design-and-animation/scripts/sample-motion.mjs';
import { advanceSpring } from '/home/maynkudu/Code/Projects/apple-design-and-animation-system/skills/apple-design-and-animation/scripts/motion.mjs';

const input = JSON.parse(await readFile(new URL('./input-timeline.json', import.meta.url), 'utf8'));
const result = sampleTimeline(input), compiled = compileTimeline(input), checks = [];
assert.equal(result.samples.length, 241);
assert.equal(result.fps, 120);
assert.equal(result.samples[0].position, 1);
assert.equal(result.samples.at(-1).time, 2);
assert.ok(Math.abs(result.samples.at(-1).position - 2) < 1e-8);
checks.push('241 finite samples at exact frameIndex / 120 timestamps, including 0 and 2 seconds.');
for (let index = 1; index < compiled.segments.length; index++) {
  const current = compiled.segments[index], previous = compiled.segments[index - 1];
  const before = advanceSpring(previous.state, current.time - previous.time);
  assert.ok(Math.abs(before.position - current.state.position) < 1e-12);
  assert.ok(Math.abs(before.velocity - current.state.velocity) < 1e-12);
  checks.push(`Position and velocity retained at exact retarget time ${current.time}s. Velocity ${before.velocity.toFixed(6)} intervals/s.`);
}
for (const time of [.09, .19, .55, .91]) {
  const epsilon = 1e-6;
  const derivative = (compiled.evaluate(time + epsilon).position - compiled.evaluate(time - epsilon).position) / (2 * epsilon);
  assert.ok(Math.abs(derivative - compiled.evaluate(time).velocity) < 1e-7);
}
checks.push('Returned velocity agrees with independent central finite differences within 1e-7 intervals/s.');
for (const fps of [30, 60]) {
  const other = sampleTimeline({ ...input, fps });
  other.samples.forEach((sample, index) => {
    assert.ok(Math.abs(sample.position - result.samples[index * 120 / fps].position) < 1e-12);
    assert.ok(Math.abs(sample.velocity - result.samples[index * 120 / fps].velocity) < 1e-12);
  });
}
checks.push('30, 60 and 120 fps exports agree at all shared timestamps within 1e-12.');
const csv = toCsv(result);
await writeFile(new URL('./placement-120fps.csv', import.meta.url), csv);
const parsed = (await readFile(new URL('./placement-120fps.csv', import.meta.url), 'utf8')).trim().split('\n');
assert.equal(parsed.length, 242);
assert.equal(parsed[0], 'time,position,velocity,target');
assert.ok(parsed.slice(1).every(line => line.split(',').every(value => Number.isFinite(Number(value)))));
checks.push('Written CSV read back. Header and 241 numeric data rows verified.');
await writeFile(new URL('./numerical-evidence.json', import.meta.url), JSON.stringify({ passed: true, checks }, null, 2) + '\n');
console.log(checks.join('\n'));
