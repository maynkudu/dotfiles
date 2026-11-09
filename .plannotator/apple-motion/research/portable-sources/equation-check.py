"""Check the portable equations. This is research evidence, not product QA."""

import json
import math
from pathlib import Path


def visual(x, a=0.0, b=300.0, cap=24.0):
    if x < a:
        return a - cap * math.tanh((a - x) / cap)
    if x > b:
        return b + cap * math.tanh((x - b) / cap)
    return x


def slope(x, a=0.0, b=300.0, cap=24.0):
    distance = max(a - x, x - b, 0.0)
    return 1.0 - math.tanh(distance / cap) ** 2


def critical(t, start, velocity, target, omega):
    displacement = start - target
    coefficient = velocity + omega * displacement
    decay = math.exp(-omega * t)
    return (
        target + (displacement + coefficient * t) * decay,
        (velocity - omega * coefficient * t) * decay,
    )


def smooth_union(a, b, width):
    weight = min(max(0.5 + 0.5 * (b - a) / width, 0.0), 1.0)
    return b * (1.0 - weight) + a * weight - width * weight * (1.0 - weight)


def select(projected, current, sites, margin):
    while current < len(sites) - 1:
        midpoint = (sites[current] + sites[current + 1]) / 2.0
        if projected <= midpoint + margin:
            break
        current += 1
    while current > 0:
        midpoint = (sites[current - 1] + sites[current]) / 2.0
        if projected >= midpoint - margin:
            break
        current -= 1
    return current


positions = [-10000.0, -24.0, -1.0, 0.0, 1.0, 299.0, 300.0, 301.0, 324.0, 10000.0]
epsilon = 1e-4
errors = []
for position in positions:
    finite_difference = (visual(position + epsilon) - visual(position - epsilon)) / (2 * epsilon)
    errors.append(abs(finite_difference - slope(position)))
    assert -24.0 <= visual(position) <= 324.0
    assert 0 <= slope(position) <= 1
assert max(errors) < 1e-7

release_raw_position = 324.0
release_raw_velocity = 800.0
release_visual_velocity = slope(release_raw_position) * release_raw_velocity
assert 335 < release_visual_velocity < 337

position, velocity = critical(0.073, 40.0, 500.0, 240.0, 18.0)
retarget_position, retarget_velocity = critical(0.0, position, velocity, 0.0, 18.0)
assert retarget_position == position
assert retarget_velocity == velocity

sites = [0.0, 100.0, 200.0]
assert all(select(projected, 0, sites, 8.0) == 0 for projected in [49, 51, 57.9])
assert select(58.1, 0, sites, 8.0) == 1
assert all(select(projected, 1, sites, 8.0) == 1 for projected in [49, 51, 42.1])
assert select(41.9, 1, sites, 8.0) == 0

width = 32.0
assert smooth_union(7.0, 7.0, width) < 0
assert smooth_union(8.0, 8.0, width) == 0
assert smooth_union(9.0, 9.0, width) > 0

maximum_area_error = 0.0
for stretch in [-10000.0, -1.0, 0.0, 1.0, 10000.0]:
    strain_limit = 0.12
    strain = strain_limit * math.tanh(stretch / 40.0 / strain_limit)
    scale_x, scale_y = math.exp(strain), math.exp(-strain)
    maximum_area_error = max(maximum_area_error, abs(scale_x * scale_y - 1.0))
    assert math.exp(-strain_limit) <= scale_x <= math.exp(strain_limit)

results = {
    "status": "passed",
    "evidence_scope": "Numeric equations only. No rendered UI or framework execution.",
    "maximum_finite_difference_error": max(errors),
    "release_example": {
        "raw_position_px": release_raw_position,
        "raw_velocity_px_per_s": release_raw_velocity,
        "visual_velocity_px_per_s": release_visual_velocity,
        "cap_px": 24,
    },
    "critical_retarget_position_error": retarget_position - position,
    "critical_retarget_velocity_error": retarget_velocity - velocity,
    "maximum_area_ratio_error": maximum_area_error,
    "hysteresis_threshold_px": {"forward": 58, "backward": 42},
    "smooth_union_midpoint_touch_gap_px": width / 2,
}
Path(__file__).with_name("equation-check-results.json").write_text(json.dumps(results, indent=2) + "\n")
print(json.dumps(results, indent=2))
