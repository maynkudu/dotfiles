# Driving and rules

The vehicle state uses world-space velocity and a separate heading. Project velocity onto forward and sideways axes. Throttle and braking affect forward speed. Capped lateral grip permits slip; surface grip and handbrake change that cap. Steering response depends on speed and wheelbase. Tune with a repeatable turn and braking distance rather than transferring force constants from a different engine.

## Circuit

Use the same track geometry for drawing, road-surface queries and checkpoint gates. Require ordered, directional crossings near the road. Cross the actual finish line only after every gate. Test skipping a gate, reversing, cutting off-road and crossing at high speed. Reset the race clock, inputs, contacts, checkpoints and lap recorder together.

## Drift

Score sustained, controlled lateral slip above a speed threshold, inside a driving zone. End a chain on contact, stopping or leaving the zone. Show the conditions in the scoring feedback. Test a straight run, a clean drift and a wall impact. Drift scoring belongs to the game and uses the existing vehicle state.

## Delivery

Keep a small list of destinations with acceptance radii and stopping-speed limits. A delivery completes only at the active destination while moving slowly enough. Test driving through too fast, visiting destinations out of order, completing one and restarting. Keep destination rules outside the vehicle and renderer.

Reference for capped lateral correction and varying surfaces: https://www.iforce2d.net/b2dtut/top-down-car
Reference for a bounded fixed-step accumulator: https://gafferongames.com/post/fix_your_timestep/
The original game's units and handling constants require their own tuning.
