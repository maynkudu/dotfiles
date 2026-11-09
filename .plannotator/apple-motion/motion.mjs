/** Advance a spring with a constant target by elapsed seconds. Position and velocity share length units. */
export function advanceSpring({ position, velocity, target, omega, dampingRatio }, seconds) {
  const y = position - target;
  const z = dampingRatio;
  const decay = Math.exp(-z * omega * seconds);
  if (Math.abs(z - 1) < 1e-8) {
    const b = velocity + omega * y;
    return {
      position: target + decay * (y + b * seconds),
      velocity: decay * (velocity - omega * b * seconds),
    };
  }
  if (z < 1) {
    const frequency = omega * Math.sqrt(1 - z * z);
    const cosine = Math.cos(frequency * seconds);
    const sine = Math.sin(frequency * seconds);
    return {
      position: target + decay * (y * cosine + (velocity + z * omega * y) * sine / frequency),
      velocity: decay * (velocity * cosine - (z * omega * velocity + omega * omega * y) * sine / frequency),
    };
  }
  const root = Math.sqrt(z * z - 1);
  const slow = -omega / (z + root);
  const fast = -omega * (z + root);
  const a = (velocity - fast * y) / (slow - fast);
  const b = y - a;
  return {
    position: target + a * Math.exp(slow * seconds) + b * Math.exp(fast * seconds),
    velocity: slow * a * Math.exp(slow * seconds) + fast * b * Math.exp(fast * seconds),
  };
}

/** Map latent displacement to a bounded visual displacement. limit is a length; resistance is dimensionless. */
export function rubberband(displacement, limit, resistance = 0.55) {
  return limit * resistance * displacement / (limit + resistance * Math.abs(displacement));
}

export function rubberbandSlope(displacement, limit, resistance = 0.55) {
  return resistance * limit * limit / (limit + resistance * Math.abs(displacement)) ** 2;
}

/** Continuous exponential-decay projection. decaySeconds is a time constant, not a tween duration. */
export function project(position, velocity, decaySeconds) {
  return position + velocity * decaySeconds;
}

export function nearestDetent(position, detents) {
  let index = 0;
  for (let i = 1; i < detents.length; i++) {
    if (Math.abs(position - detents[i]) < Math.abs(position - detents[index])) index = i;
  }
  return index;
}

/** A Schmitt trigger for the previewed selection. Supply sorted detents and retain the returned index. */
export function previewDetent(position, detents, currentIndex, hysteresis) {
  let index = currentIndex;
  while (index < detents.length - 1 && position > (detents[index] + detents[index + 1]) / 2 + hysteresis) index++;
  while (index > 0 && position < (detents[index] + detents[index - 1]) / 2 - hysteresis) index--;
  return index;
}

/** Polynomial smooth minimum for negative-inside signed fields. blendRadius has length units. */
export function smoothUnion(a, b, blendRadius) {
  if (blendRadius <= 0) return Math.min(a, b);
  const h = Math.max(blendRadius - Math.abs(a - b), 0) / blendRadius;
  return Math.min(a, b) - h * h * blendRadius / 4;
}
