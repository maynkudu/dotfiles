import { test } from 'node:test';
import assert from 'node:assert/strict';
import { advanceSpring, estimateVelocity, nearestDetent, previewDetent, rubberband, validateDetents } from '/home/maynkudu/Code/Projects/modulo-snap-rail/motion';
test('only finite ordered detents with stable unique IDs are accepted', () => {
  validateDetents([{id:'only',label:'Only',position:7}]);
  for (const detents of [[],[{id:'a',label:'A',position:NaN}],[{id:'a',label:'A',position:0},{id:'a',label:'B',position:1}],[{id:'a',label:'A',position:1},{id:'b',label:'B',position:0}],[{id:'a',label:'',position:0}]]) assert.throws(()=>validateDetents(detents));
});
test('release projection chooses a destination once with stable midpoint ties', () => {
  assert.equal(nearestDetent(40+600*.12,[0,100,200]),1); assert.equal(nearestDetent(100,[0,200]),0);
  assert.equal(nearestDetent(-500,[0,100,200]),0); assert.equal(nearestDetent(800,[0,100,200]),2);
});
test('preview hysteresis avoids changes while hovering around a midpoint', () => {
  assert.equal(previewDetent(51,[0,100,200],0,8),0); assert.equal(previewDetent(59,[0,100,200],0,8),1);
  assert.equal(previewDetent(45,[0,100,200],1,8),1); assert.equal(previewDetent(41,[0,100,200],1,8),0);
  assert.equal(previewDetent(10,[0,10],0,100),1);
});
test('release velocity is px/s and a held pointer cannot reuse its earlier flick', () => {
  const samples=[{position:0,time:0},{position:40,time:40}];
  assert.equal(estimateVelocity(samples,40,40),1000); assert.equal(estimateVelocity(samples,40,121),0);
  assert.equal(estimateVelocity([{position:0,time:0}],null,20),0);
});
test('spring retargeting retains opposing velocity in all damping regimes', () => {
  for(const dampingRatio of [.85,1,2]) {
    const initial={position:100,velocity:600,target:0,omega:20,dampingRatio};
    const at=advanceSpring(initial,0);assert.ok(Math.abs(at.position-100)<1e-9);assert.ok(Math.abs(at.velocity-600)<1e-9);
    assert.ok(advanceSpring(initial,.0001).position>100);
  }
});
test('spring trajectory agrees when elapsed time is split at different frame rates', () => {
  for(const dampingRatio of [.85,1,2]) {
    const initial={position:100,velocity:600,target:0,omega:20,dampingRatio};
    const direct=advanceSpring(initial,.2);let state=initial;
    for(let i=0;i<24;i++)state={...state,...advanceSpring(state,1/120)};
    assert.ok(Math.abs(state.position-direct.position)<1e-8);assert.ok(Math.abs(state.velocity-direct.velocity)<1e-8);
  }
});
test('one detent remains selectable at any projected point', () => { assert.equal(nearestDetent(500,[100]),0);assert.equal(previewDetent(-500,[100],0,8),0); });
test('visual overshoot stays inside its finite rubberband cap', () => { for(const distance of [-10000,-100,0,100,10000])assert.ok(Math.abs(rubberband(distance))<32); });
