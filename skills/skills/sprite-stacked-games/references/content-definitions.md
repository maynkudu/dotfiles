# Cars and circuits

The example's content is in `game/racer-content.ts`. `createRaceSession({map, car})` accepts a circuit definition and a car definition. The renderer and vehicle integrator stay shared.

## Add a car

Define the name, art dimensions, layer count, palette, slice recipe and handling. Author an original silhouette and cabin position. A shape change belongs in `game/garage-artwork.ts`; it does not require changing the renderer. Keep the forward axis +x and the declared pivot consistent with the engine. The provided hatchback, three-box coupe, wedge, GT, rounded sports car and pickup show different bodies. The pickup directly represents an open bed, without inferring a closed hull from four views.

Use `createGarageCarStack(definition)` to render the asset. Inspect its full rotation, separated layers and garage thumbnail. Fit the inspector to the actual layer count so tall vehicles cannot clip. Verify heading while reversing and the visual bounds in scenery.

Tune acceleration, braking, forward/reverse speed, grip, handbrake grip, wheelbase and steering lock through the definition. These are game units and choices, not manufacturer specifications. The example's brand-inspired cars are original low-resolution drawings; reference photographs are research inputs rather than shipped textures.

## Add a circuit

Define a closed list of world-space centerline points, road width, surface grip, palette, scenery theme and seed. Drawing, nearest-road queries and checkpoints consume the same sampled geometry. Keep road branches far enough apart for an unambiguous nearest segment. Put the grid and painted finish on the actual race origin. When moving that origin, rerun the complete-lap tests.

The included forest, coast, alpine, harbor and desert circuits use different geometry and scenery. A new biome belongs in `game/race-artwork.ts`. Cache its static terrain and props. Keep changing car and circuit selection local to the menu, reset the race coherently, and release old resources if a production runtime evicts cached artwork.

## Verify the combination

Run the full car/circuit matrix with the actual vehicle simulation and directional gates. A recording controller must slow for corners instead of teleporting between points. This checks the simulation's finish path; separately drive the game with real inputs.

Store best time and sampled ghost under a versioned key containing both map and car identifiers. Changing either selection must load its own record or an honest empty state. Corrupt or unavailable storage must preserve play.
