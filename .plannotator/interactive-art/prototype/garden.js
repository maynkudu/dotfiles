const WORLD = { width: 1000, height: 680 };
const TAU = Math.PI * 2;
const clamp = (value, low = 0, high = 1) => Math.max(low, Math.min(high, value));
const mix = (a, b, amount) => a + (b - a) * amount;
const smooth = value => { const t = clamp(value); return t * t * (3 - 2 * t); };

function randomSource(seed) {
  let state = seed >>> 0;
  return () => {
    state = (Math.imul(state, 1664525) + 1013904223) >>> 0;
    return state / 4294967296;
  };
}

function colour(from, to, amount, alpha = 1) {
  return `rgba(${from.map((channel, index) => Math.round(mix(channel, to[index], amount))).join(',')},${alpha})`;
}

const PLANTS = [
  { x: 115, height: 235, radius: 34, lean: -.24, delay: -30, duration: 75, shade: 'violet' },
  { x: 278, height: 290, radius: 49, lean: -.16, delay: -38, duration: 72, shade: 'ivory' },
  { x: 438, height: 207, radius: 38, lean: -.08, delay: 0, duration: 72, shade: 'rose' },
  { x: 578, height: 370, radius: 63, lean: .12, delay: -44, duration: 78, shade: 'ivory' },
  { x: 744, height: 250, radius: 43, lean: .15, delay: -12, duration: 68, shade: 'violet' },
  { x: 902, height: 285, radius: 39, lean: .2, delay: 12, duration: 85, shade: 'rose' },
];

function createPlant(definition, index) {
  return { ...definition, id: `flower-${index + 1}`, rootY: 594 + (index % 2) * 18,
    growth: 0, bloom: 0, headAngle: 0, headVelocity: 0,
    nodes: Array.from({ length: 9 }, () => ({ x: definition.x, y: 600, previousX: definition.x, previousY: 600 })) };
}

function restPoint(plant, index) {
  const progress = index / (plant.nodes.length - 1);
  const height = plant.height * mix(.26, 1, plant.growth);
  return { x: plant.x + Math.sin(progress * 1.35) * height * plant.lean,
    y: plant.rootY - height * progress };
}

function placeAtRest(plant) {
  plant.nodes.forEach((node, index) => {
    const point = restPoint(plant, index);
    node.x = node.previousX = point.x;
    node.y = node.previousY = point.y;
  });
  const a = plant.nodes.at(-2), b = plant.nodes.at(-1);
  plant.headAngle = Math.atan2(b.y - a.y, b.x - a.x) + Math.PI / 2;
  plant.headVelocity = 0;
}

function updateGrowth(plant, elapsed) {
  plant.growth = smooth((elapsed - plant.delay) / plant.duration);
  plant.bloom = smooth((plant.growth - .48) / .52);
}

function boundedTarget(plant, point) {
  const rest = restPoint(plant, plant.nodes.length - 1);
  const dx = point.x - rest.x, dy = point.y - rest.y;
  const limit = plant.height * .34;
  const distance = Math.hypot(dx, dy);
  const ratio = distance > limit ? limit / distance : 1;
  return { x: rest.x + dx * ratio, y: rest.y + dy * ratio };
}

function simulatePlant(plant, dt, elapsed, wind, target) {
  const damping = Math.exp(-(target ? 11 : 5.8) * dt);
  const root = plant.nodes[0];
  root.x = root.previousX = plant.x;
  root.y = root.previousY = plant.rootY;
  for (let index = 1; index < plant.nodes.length; index++) {
    const node = plant.nodes[index], rest = restPoint(plant, index);
    const progress = index / (plant.nodes.length - 1);
    const velocityX = (node.x - node.previousX) * damping;
    const velocityY = (node.y - node.previousY) * damping;
    node.previousX = node.x; node.previousY = node.y;
    const gust = (Math.sin(elapsed * .85 + plant.x * .006) * 22 + Math.sin(elapsed * 1.9 + progress) * 6) * wind * progress;
    let goalX = rest.x, goalY = rest.y;
    if (target) {
      const weight = progress ** 2;
      const tipRest = restPoint(plant, plant.nodes.length - 1);
      goalX += (target.x - tipRest.x) * weight;
      goalY += (target.y - tipRest.y) * weight;
    }
    const stiffness = target ? 105 : 48;
    const forceX = (goalX - node.x) * stiffness + gust;
    const forceY = (goalY - node.y) * stiffness;
    node.x += velocityX + forceX * dt * dt;
    node.y += velocityY + forceY * dt * dt;
  }
  // Length constraints distribute a pull along the stem while its root stays anchored.
  for (let pass = 0; pass < 10; pass++) {
    for (let index = 1; index < plant.nodes.length; index++) {
      const a = plant.nodes[index - 1], b = plant.nodes[index];
      const ra = restPoint(plant, index - 1), rb = restPoint(plant, index);
      const length = Math.hypot(rb.x - ra.x, rb.y - ra.y);
      const dx = b.x - a.x, dy = b.y - a.y;
      const distance = Math.max(.001, Math.hypot(dx, dy));
      const correction = (distance - length) / distance;
      const share = index === 1 ? 1 : .5;
      if (index > 1) { a.x += dx * correction * .5; a.y += dy * correction * .5; }
      b.x -= dx * correction * share; b.y -= dy * correction * share;
    }
    const tip = plant.nodes.at(-1), bounded = boundedTarget(plant, tip);
    tip.x = bounded.x; tip.y = bounded.y;
  }
  const a = plant.nodes.at(-2), b = plant.nodes.at(-1);
  const angle = Math.atan2(b.y - a.y, b.x - a.x) + Math.PI / 2;
  plant.headVelocity += ((angle - plant.headAngle) * 42 - plant.headVelocity * 7.8) * dt;
  plant.headAngle += plant.headVelocity * dt;
}

function petalPath(context, width, height, bend = 0) {
  context.beginPath();
  context.moveTo(0, 7);
  context.bezierCurveTo(-width, -height * .2, -width * .92 + bend, -height * .74, bend, -height);
  context.bezierCurveTo(width * .94 + bend, -height * .68, width, -height * .18, 0, 7);
  context.closePath();
}

function drawLeaf(context, x, y, size, rotation, daylight) {
  context.save(); context.translate(x, y); context.rotate(rotation);
  petalPath(context, size * .27, size, size * .12);
  const gradient = context.createLinearGradient(-size * .2, 0, size * .3, -size);
  gradient.addColorStop(0, colour([23, 58, 65], [36, 90, 69], daylight));
  gradient.addColorStop(1, colour([44, 91, 97], [100, 144, 108], daylight));
  context.fillStyle = gradient; context.fill();
  context.strokeStyle = '#1f3443'; context.lineWidth = 1.5; context.stroke();
  context.strokeStyle = colour([109, 148, 127], [176, 189, 121], daylight, .8);
  context.lineWidth = .7;
  context.beginPath(); context.moveTo(0, 4); context.quadraticCurveTo(size * .03, -size * .5, size * .12, -size * .96); context.stroke();
  for (let index = 1; index < 7; index++) {
    const p = index / 8;
    const width = Math.sin(p * Math.PI) * size * .19;
    context.beginPath(); context.moveTo(size * p * .08, -size * p);
    context.quadraticCurveTo(-width * .7, -size * (p + .04), -width, -size * (p + .12));
    context.moveTo(size * p * .08, -size * p);
    context.quadraticCurveTo(width * .7, -size * (p + .04), width + size * .06, -size * (p + .12)); context.stroke();
  }
  context.restore();
}

function drawPetal(context, rotation, width, height, palette, daylight, texture, bend = 0) {
  context.save(); context.rotate(rotation);
  petalPath(context, width, height, bend);
  const gradient = context.createLinearGradient(-width, 5, width * .6, -height);
  gradient.addColorStop(0, colour(palette[0], palette[1], daylight));
  gradient.addColorStop(.64, colour(palette[1], palette[2], daylight));
  gradient.addColorStop(1, colour(palette[2], palette[3], daylight));
  context.fillStyle = gradient; context.fill();
  context.save(); context.clip(); context.globalAlpha = .095; context.fillStyle = texture;
  context.fillRect(-width * 2, -height - 4, width * 4, height + 16); context.restore();
  context.strokeStyle = colour([25, 37, 65], [47, 56, 71], daylight); context.lineWidth = 1.45; context.stroke();
  context.strokeStyle = colour([114, 118, 119], [186, 165, 116], daylight, .78); context.lineWidth = .65;
  context.beginPath(); context.moveTo(0, 4); context.quadraticCurveTo(bend * .4, -height * .43, bend, -height * .94); context.stroke();
  for (let index = 1; index < 5; index++) {
    const p = index / 6, w = Math.sin(p * Math.PI) * width * .66;
    context.beginPath(); context.moveTo(bend * p * .4, -height * p);
    context.quadraticCurveTo(-w * .5, -height * (p + .06), -w + bend * p, -height * (p + .17));
    context.moveTo(bend * p * .4, -height * p);
    context.quadraticCurveTo(w * .5, -height * (p + .06), w + bend * p, -height * (p + .17)); context.stroke();
  }
  context.restore();
}

const PALETTES = {
  ivory: [[145, 157, 157], [211, 216, 204], [243, 236, 212], [255, 248, 224]],
  violet: [[77, 71, 112], [120, 102, 150], [169, 156, 191], [213, 207, 220]],
  rose: [[101, 66, 98], [164, 108, 137], [219, 170, 185], [246, 216, 212]],
};

function drawFlower(context, plant, daylight, texture, selected) {
  const tip = plant.nodes.at(-1);
  const radius = plant.radius * mix(.53, 1, plant.growth);
  const bloom = plant.bloom;
  context.save(); context.translate(tip.x, tip.y); context.rotate(plant.headAngle * .85);
  if (selected) {
    context.save(); context.globalAlpha = .35; context.strokeStyle = '#e6d39c'; context.lineWidth = 1;
    context.setLineDash([2, 6]); context.beginPath(); context.ellipse(0, -radius * .35, radius * 1.4, radius * 1.1, 0, 0, TAU); context.stroke(); context.restore();
  }
  const unfolding = smooth((bloom - .04) / .16);
  if (unfolding < 1) {
    context.save(); context.globalAlpha *= 1 - unfolding;
    drawPetal(context, -.1, radius * .32, radius * 1.05, PALETTES[plant.shade], daylight, texture, radius * .03);
    drawPetal(context, .13, radius * .21, radius * 1.06, PALETTES[plant.shade], daylight, texture, -radius * .04);
    drawLeaf(context, -2, 8, radius * .57, -.34, daylight);
    drawLeaf(context, 2, 8, radius * .52, .4, daylight);
    context.restore();
  }
  if (unfolding > 0) {
    context.save(); context.globalAlpha *= unfolding;
    const open = smooth((bloom - .04) / .96);
    for (let index = -4; index <= 4; index++) {
      drawPetal(context, index * .34 * mix(.3, 1, open), radius * mix(.17, .33, open), radius * (1.38 - Math.abs(index) * .048), PALETTES[plant.shade], daylight, texture, index * 1.1);
    }
    for (let index = -3; index <= 3; index++) {
      drawPetal(context, index * .45 * mix(.2, 1, open), radius * mix(.17, .34, open), radius * (.98 - Math.abs(index) * .035), PALETTES[plant.shade], daylight, texture, -index * .7);
    }
    context.save(); context.scale(1, .54);
    context.fillStyle = colour([163, 137, 68], [226, 192, 95], daylight); context.strokeStyle = '#8c7548'; context.lineWidth = 1;
    context.beginPath(); context.ellipse(0, -radius * .07, radius * .3 * open, radius * .25 * open, 0, 0, TAU); context.fill(); context.stroke();
    for (let index = 0; index < 31; index++) {
      const a = index * 2.399, r = Math.sqrt(index / 31) * radius * .28 * open;
      context.fillStyle = index % 3 ? '#dfc988' : '#776344';
      context.beginPath(); context.arc(Math.cos(a) * r, -radius * .07 + Math.sin(a) * r, .9, 0, TAU); context.fill();
    }
    context.restore();
    for (let index = -2; index <= 2; index++) {
      drawPetal(context, index * .76 * open + Math.PI * .17 * Math.sign(index), radius * .29, radius * (.6 - Math.abs(index) * .035), PALETTES[plant.shade], daylight, texture, index);
    }
    context.restore();
  }
  context.restore();
}

function drawStem(context, plant, daylight) {
  const nodes = plant.nodes;
  context.beginPath(); context.moveTo(nodes[0].x, nodes[0].y);
  for (let index = 1; index < nodes.length - 1; index++) {
    const node = nodes[index], next = nodes[index + 1];
    context.quadraticCurveTo(node.x, node.y, (node.x + next.x) / 2, (node.y + next.y) / 2);
  }
  context.lineTo(nodes.at(-1).x, nodes.at(-1).y);
  context.lineCap = 'round'; context.strokeStyle = '#243b47'; context.lineWidth = 7; context.stroke();
  context.strokeStyle = colour([89, 116, 89], [177, 175, 113], daylight); context.lineWidth = 3.4; context.stroke();
  for (const [index, side] of [[3, -1], [5, 1]]) {
    const node = nodes[index], previous = nodes[index - 1];
    const angle = Math.atan2(node.y - previous.y, node.x - previous.x) + Math.PI / 2;
    const growth = smooth((plant.growth - .12 * index) / .44);
    drawLeaf(context, node.x, node.y, plant.radius * 1.4 * growth, angle + side * .98, daylight);
  }
}

function drawLilyPad(context, x, y, radius, rotation, daylight) {
  context.save(); context.translate(x, y); context.rotate(rotation); context.scale(1, .48);
  context.beginPath(); context.moveTo(0, 0); context.arc(0, 0, radius, -.28, TAU - .53); context.closePath();
  const gradient = context.createRadialGradient(-radius * .3, -radius * .3, 0, 0, 0, radius);
  gradient.addColorStop(0, colour([51, 95, 105], [126, 155, 108], daylight));
  gradient.addColorStop(1, colour([24, 52, 70], [55, 98, 88], daylight));
  context.fillStyle = gradient; context.fill(); context.strokeStyle = '#20384e'; context.lineWidth = 2; context.stroke();
  context.strokeStyle = colour([110, 147, 128], [174, 183, 127], daylight, .6); context.lineWidth = .8;
  for (let index = 1; index < 16; index++) {
    const a = index / 16 * TAU;
    context.beginPath(); context.moveTo(0, 0); context.quadraticCurveTo(Math.cos(a - .12) * radius * .48, Math.sin(a + .12) * radius * .48, Math.cos(a) * radius * .98, Math.sin(a) * radius * .98); context.stroke();
  }
  context.restore();
}

/** Mount a self-contained garden. Its clock counts visible scene time, not background-tab time. */
export function createGarden(canvas, options = {}) {
  const context = canvas.getContext('2d');
  if (!context) throw new Error('The garden needs a Canvas 2D context.');
  const random = randomSource(options.seed ?? 1486);
  const config = { cycleSeconds: options.cycleSeconds ?? 120, timeScale: options.timeScale ?? 1, wind: options.wind ?? 1 };
  if (config.cycleSeconds <= 0 || config.timeScale < 0) throw new Error('Cycle length must be positive and time scale cannot be negative.');
  const plants = (options.plants ?? PLANTS).map(createPlant);
  const grass = Array.from({ length: 190 }, () => ({ x: random() * WORLD.width, y: 578 + random() * 108, height: 22 + random() * 75, lean: random() * 2 - 1, phase: random() * TAU }));
  const stars = Array.from({ length: 55 }, () => ({ x: 35 + random() * 930, y: 30 + random() * 250, radius: .45 + random() * 1.1 }));
  const pads = Array.from({ length: 13 }, () => ({ x: random() * WORLD.width, y: 454 + random() * 200, radius: 35 + random() * 72, rotation: random() * .6 - .3 }));
  const textureCanvas = document.createElement('canvas'); textureCanvas.width = textureCanvas.height = 96;
  const textureContext = textureCanvas.getContext('2d');
  const pixels = textureContext.createImageData(96, 96);
  for (let index = 0; index < pixels.data.length; index += 4) {
    const shade = Math.floor(random() * 255);
    pixels.data[index] = pixels.data[index + 1] = pixels.data[index + 2] = shade; pixels.data[index + 3] = 130;
  }
  textureContext.putImageData(pixels, 0, 0);
  const texture = context.createPattern(textureCanvas, 'repeat');
  const motionQuery = matchMedia('(prefers-reduced-motion: reduce)');
  const disposals = [];
  let elapsed = options.initialTime ?? 16, physicalTime = 0, paused = false, destroyed = false, inView = true;
  let frame = 0, last = 0, accumulator = 0, width = 1, height = 1, scale = 1, offsetX = 0;
  let pointer = null, drag = null, keyboardTarget = null, renderedFrames = 0;

  function listen(target, event, handler, settings) {
    target.addEventListener(event, handler, settings);
    disposals.push(() => target.removeEventListener(event, handler, settings));
  }

  function growthAt(time, resetPose = false) {
    plants.forEach(plant => { updateGrowth(plant, time); if (resetPose) placeAtRest(plant); });
  }
  growthAt(elapsed, true);

  function lighting() {
    const phase = (elapsed % config.cycleSeconds) / config.cycleSeconds;
    const daylight = smooth((Math.sin(phase * TAU) + .32) / .9);
    return { phase, daylight, name: daylight < .14 ? 'Night' : daylight < .64 ? 'Twilight' : 'Day' };
  }

  function render() {
    if (destroyed) return;
    const { phase, daylight } = lighting();
    context.setTransform(canvas.width / width, 0, 0, canvas.height / height, 0, 0);
    const sky = context.createLinearGradient(0, 0, 0, height);
    sky.addColorStop(0, colour([12, 25, 54], [89, 147, 171], daylight));
    sky.addColorStop(.65, colour([23, 46, 74], [173, 191, 174], daylight));
    sky.addColorStop(1, colour([24, 57, 66], [99, 147, 126], daylight));
    context.fillStyle = sky; context.fillRect(0, 0, width, height);
    context.translate(offsetX, 0); context.scale(scale, scale);
    context.save(); context.globalAlpha = 1 - daylight;
    context.fillStyle = '#dbd6b7';
    for (const star of stars) { context.beginPath(); context.arc(star.x, star.y, star.radius, 0, TAU); context.fill(); }
    context.restore();
    for (const [isSun, angle] of [[true, phase * TAU], [false, phase * TAU + Math.PI]]) {
      const orbX = 500 - Math.cos(angle) * 350, orbY = 415 - Math.sin(angle) * 330;
      const glow = context.createRadialGradient(orbX, orbY, 8, orbX, orbY, 108);
      glow.addColorStop(0, isSun ? 'rgba(255,228,167,.23)' : 'rgba(204,224,233,.12)'); glow.addColorStop(1, 'rgba(255,228,167,0)');
      context.fillStyle = glow; context.fillRect(orbX - 108, orbY - 108, 216, 216);
      context.fillStyle = isSun ? '#f5dda1' : '#d8dfdb'; context.beginPath(); context.arc(orbX, orbY, isSun ? 25 : 18, 0, TAU); context.fill();
      context.strokeStyle = 'rgba(220,205,149,.3)'; context.lineWidth = .7;
      for (let ring = 0; ring < 3; ring++) { context.beginPath(); context.arc(orbX, orbY, 31 + ring * 7, 0, TAU); context.stroke(); }
    }
    for (let index = 0; index < 3; index++) {
      context.beginPath(); context.moveTo(-50, 380 + index * 45);
      context.bezierCurveTo(160, 330 + index * 48, 208, 405 + index * 28, 480, 357 + index * 40);
      context.bezierCurveTo(692, 316 + index * 36, 830, 394 + index * 29, 1060, 328 + index * 36);
      context.lineTo(1060, 680); context.lineTo(-50, 680); context.closePath();
      context.fillStyle = colour([20 + index * 4, 47 + index * 5, 68 + index * 2], [75 - index * 11, 123 - index * 7, 113 - index * 8], daylight); context.fill();
      context.strokeStyle = colour([88, 116, 118], [170, 181, 129], daylight, .4); context.lineWidth = .8; context.stroke();
    }
    for (let index = 0; index < 22; index++) {
      const y = 437 + index * 8.5, x = ((index * 163) % 980) - 90;
      context.strokeStyle = colour([82, 131, 137], [170, 188, 150], daylight, .17); context.lineWidth = .9;
      context.beginPath(); context.moveTo(x, y); context.bezierCurveTo(x + 55, y - 7, x + 105, y + 7, x + 185, y); context.stroke();
    }
    for (const pad of pads) drawLilyPad(context, pad.x, pad.y, pad.radius, pad.rotation, daylight);
    for (const plant of [...plants].sort((a, b) => a.rootY - b.rootY)) {
      drawStem(context, plant, daylight);
      drawFlower(context, plant, daylight, texture, drag?.id === plant.id);
    }
    for (const blade of grass) {
      const sway = motionQuery.matches ? 0 : Math.sin(physicalTime * 1.4 + blade.phase) * 7 * config.wind;
      context.beginPath(); context.moveTo(blade.x, blade.y);
      context.bezierCurveTo(blade.x + blade.lean * 10, blade.y - blade.height * .34, blade.x + blade.lean * 17 + sway, blade.y - blade.height * .85, blade.x + blade.lean * 25 + sway, blade.y - blade.height);
      context.strokeStyle = colour([52, 91, 82], [114, 150, 95], daylight, .82); context.lineWidth = 1.3; context.stroke();
      if (blade.height > 70) {
        context.strokeStyle = colour([138, 147, 111], [211, 195, 129], daylight, .72); context.lineWidth = 2.6;
        context.beginPath(); context.moveTo(blade.x + blade.lean * 25 + sway, blade.y - blade.height);
        context.lineTo(blade.x + blade.lean * 24 + sway, blade.y - blade.height + 8); context.stroke();
      }
    }
    context.save(); context.globalAlpha = .045; context.fillStyle = texture; context.fillRect(0, 0, WORLD.width, WORLD.height); context.restore();
    renderedFrames++;
    if (options.onFrame) options.onFrame({ elapsed, ...lighting(), growth: plants.map(plant => plant.growth) });
  }

  function resize() {
    const rect = canvas.getBoundingClientRect(); width = Math.max(1, rect.width); height = Math.max(1, rect.height);
    const density = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = Math.round(width * density); canvas.height = Math.round(height * density);
    scale = height / WORLD.height; offsetX = (width - WORLD.width * scale) / 2;
    render();
  }

  function localPoint(event) {
    const rect = canvas.getBoundingClientRect();
    return { x: (event.clientX - rect.left - offsetX) / scale, y: (event.clientY - rect.top) / scale };
  }

  function nearest(point) {
    let result = null, distance = Infinity;
    for (const plant of plants) {
      const tip = plant.nodes.at(-1), centerY = tip.y - plant.radius * .4;
      const d = Math.hypot(point.x - tip.x, point.y - centerY);
      if (d < Math.max(plant.radius * 1.45, 24 / scale) && d < distance) { result = plant; distance = d; }
    }
    return result;
  }

  function clearDrag() {
    const id = drag?.pointerId; drag = null;
    if (id !== undefined && canvas.hasPointerCapture(id)) canvas.releasePointerCapture(id);
    canvas.style.cursor = 'default';
  }

  function step(dt) {
    elapsed += dt * config.timeScale; physicalTime += dt; growthAt(elapsed);
    for (const plant of plants) {
      let target = null;
      if (drag?.id === plant.id) target = boundedTarget(plant, drag.target);
      else if (keyboardTarget?.id === plant.id && physicalTime < keyboardTarget.until) target = boundedTarget(plant, keyboardTarget.target);
      else if (pointer) {
        const tip = plant.nodes.at(-1), distance = Math.hypot(pointer.x - tip.x, pointer.y - tip.y);
        if (distance < plant.radius * 2) {
          const rest = restPoint(plant, plant.nodes.length - 1), influence = smooth(1 - distance / (plant.radius * 2));
          target = { x: rest.x + (pointer.x > tip.x ? -1 : 1) * 27 * influence, y: rest.y + 4 * influence };
        }
      }
      simulatePlant(plant, dt, physicalTime, config.wind, target);
    }
  }

  const active = () => !destroyed && !paused && inView && !document.hidden && !motionQuery.matches;
  function tick(now) {
    frame = 0;
    if (!active()) return;
    const delta = last ? Math.min(.05, (now - last) / 1000) : 0; last = now; accumulator += delta;
    while (accumulator >= 1 / 120) { step(1 / 120); accumulator -= 1 / 120; }
    render(); if (active()) frame = requestAnimationFrame(tick);
  }

  function schedule() {
    cancelAnimationFrame(frame); frame = 0; last = 0; accumulator = 0;
    if (active()) frame = requestAnimationFrame(tick);
  }

  listen(canvas, 'pointermove', event => {
    if (!active()) return;
    const point = localPoint(event);
    if (drag?.pointerId === event.pointerId) {
      drag.target = { x: point.x - drag.offset.x, y: point.y - drag.offset.y }; event.preventDefault();
    }
    else if (event.pointerType !== 'touch') { pointer = point; canvas.style.cursor = nearest(point) ? 'grab' : 'default'; }
  });
  listen(canvas, 'pointerleave', () => { pointer = null; if (!drag) canvas.style.cursor = 'default'; });
  listen(canvas, 'pointerdown', event => {
    if (event.button !== 0 || drag || !active()) return;
    const point = localPoint(event), plant = nearest(point);
    if (!plant) return;
    const tip = plant.nodes.at(-1);
    drag = { id: plant.id, pointerId: event.pointerId, target: { x: tip.x, y: tip.y }, offset: { x: point.x - tip.x, y: point.y - tip.y } }; pointer = null;
    canvas.setPointerCapture(event.pointerId); canvas.style.cursor = 'grabbing'; event.preventDefault();
  });
  const release = event => { if (drag?.pointerId === event.pointerId) clearDrag(); };
  listen(canvas, 'pointerup', release); listen(canvas, 'pointercancel', release); listen(canvas, 'lostpointercapture', release);
  listen(document, 'visibilitychange', () => { if (document.hidden) { clearDrag(); pointer = null; } schedule(); });
  listen(motionQuery, 'change', () => { clearDrag(); pointer = null; if (motionQuery.matches) growthAt(elapsed, true); render(); schedule(); });
  const sizeObserver = new ResizeObserver(resize); sizeObserver.observe(canvas); disposals.push(() => sizeObserver.disconnect());
  const visibilityObserver = new IntersectionObserver(entries => {
    inView = entries[0].isIntersecting;
    if (!inView) { clearDrag(); pointer = null; }
    schedule();
  }, { threshold: .05 });
  visibilityObserver.observe(canvas); disposals.push(() => visibilityObserver.disconnect());
  resize(); schedule();

  return {
    pause() { paused = true; clearDrag(); pointer = null; keyboardTarget = null; schedule(); render(); },
    resume() { paused = false; schedule(); },
    setTimeScale(value) { if (!Number.isFinite(value) || value < 0) throw new Error('Time scale must be a nonnegative number.'); config.timeScale = value; },
    seek(seconds) {
      if (!Number.isFinite(seconds) || seconds < 0) throw new Error('Time must be a nonnegative number.');
      clearDrag(); pointer = null; keyboardTarget = null; elapsed = seconds; growthAt(elapsed, true); render();
    },
    bend(id = plants[3]?.id, direction = 1) {
      const plant = plants.find(item => item.id === id); if (!plant) return;
      const rest = restPoint(plant, plant.nodes.length - 1);
      if (!motionQuery.matches && active()) keyboardTarget = { id, target: { x: rest.x + direction * 65, y: rest.y + 12 }, until: physicalTime + .7 };
    },
    snapshot() {
      return { elapsed, ...lighting(), paused, reducedMotion: motionQuery.matches, running: Boolean(frame), destroyed, renderedFrames, drag: drag?.id ?? null,
        plants: plants.map(plant => ({ id: plant.id, growth: plant.growth, bloom: plant.bloom, root: { x: plant.nodes[0].x, y: plant.nodes[0].y },
          tip: { x: plant.nodes.at(-1).x, y: plant.nodes.at(-1).y }, rest: restPoint(plant, plant.nodes.length - 1),
          screen: { x: plant.nodes.at(-1).x * scale + offsetX, y: (plant.nodes.at(-1).y - plant.radius * .4) * scale },
          maxPull: plant.height * .34, maxSegmentError: Math.max(...plant.nodes.slice(1).map((node, index) => {
            const previous = plant.nodes[index], a = restPoint(plant, index), b = restPoint(plant, index + 1);
            return Math.abs(Math.hypot(node.x - previous.x, node.y - previous.y) / Math.hypot(b.x - a.x, b.y - a.y) - 1);
          })) })), width, height, scale, offsetX };
    },
    destroy() { if (destroyed) return; destroyed = true; cancelAnimationFrame(frame); frame = 0; clearDrag(); disposals.forEach(dispose => dispose()); },
  };
}
