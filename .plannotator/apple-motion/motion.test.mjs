import assert from 'node:assert/strict';
import test from 'node:test';
import { advanceSpring, rubberband, rubberbandSlope, project, nearestDetent, previewDetent, smoothUnion } from './motion.mjs';

const near = (actual, expected, tolerance = 1e-8) => assert.ok(Math.abs(actual - expected) <= tolerance, `${actual} differs from ${expected}`);

test('the spring trajectory is independent of frame partition, including interrupted targets', () => {
  for (const dampingRatio of [0.3, 0.85, 1, 1.5, 4]) {
    const configuration = { position: 80, velocity: -140, target: 0, omega: 20, dampingRatio };
    for (const fps of [30, 60, 120]) {
      let state = configuration;
      for (let frame = 0; frame < fps; frame++) state = { ...configuration, ...advanceSpring(state, 1 / fps) };
      const direct = advanceSpring(configuration, 1);
      near(state.position, direct.position);
      near(state.velocity, direct.velocity);
      const retargeted = { ...state, target: 120 };
      const atChange = advanceSpring(retargeted, 0);
      near(atChange.position, state.position);
      near(atChange.velocity, state.velocity);
    }
  }
});

test('spring position derivative agrees with its returned velocity', () => {
  for (const dampingRatio of [0.3, 1, 1.5]) {
    const state = { position: 80, velocity: 320, target: 0, omega: 20, dampingRatio };
    const t = 0.17;
    const h = 1e-6;
    const difference = (advanceSpring(state, t + h).position - advanceSpring(state, t - h).position) / (2 * h);
    near(difference, advanceSpring(state, t).velocity, 1e-5);
  }
});

test('latent spring release stays visually bounded and carries mapped velocity', () => {
  const initial = { position: 300, velocity: 5000, target: 0, omega: 20, dampingRatio: 0.85 };
  for (let frame = 0; frame <= 240; frame++) {
    const state = advanceSpring(initial, frame / 120);
    assert.ok(Math.abs(rubberband(state.position, 48)) < 48);
  }
  const dt = 1e-7;
  const mappedDifference = (rubberband(advanceSpring(initial, dt).position, 48) - rubberband(initial.position, 48)) / dt;
  near(mappedDifference, rubberbandSlope(initial.position, 48) * initial.velocity, 0.002);
});

test('snap projection responds to flick direction and selection hysteresis prevents midpoint chatter', () => {
  const detents = [0, 100, 200];
  assert.equal(nearestDetent(project(60, 600, 0.2), detents), 2);
  assert.equal(nearestDetent(project(60, -600, 0.2), detents), 0);
  let index = 0;
  for (const position of [49, 51, 48, 54]) index = previewDetent(position, detents, index, 5);
  assert.equal(index, 0);
  index = previewDetent(56, detents, index, 5);
  assert.equal(index, 1);
  assert.equal(previewDetent(49, detents, index, 5), 1);
  assert.equal(previewDetent(44, detents, index, 5), 0);
});

test('a smooth-union bridge separates at the derived equal-circle distance', () => {
  const radius = 30;
  const k = 24;
  const threshold = 2 * radius + k / 2;
  const midpoint = distance => smoothUnion(distance / 2 - radius, distance / 2 - radius, k);
  assert.ok(midpoint(threshold - 1) < 0);
  near(midpoint(threshold), 0);
  assert.ok(midpoint(threshold + 1) > 0);
  near(smoothUnion(-10, 20, 0), -10);
});
