# Portable fluid motion mechanisms

Retrieved on 2026-11-09. This is isolated implementation research for web, Android, Flutter, React Native and motion graphics. The equations below are my proposed model. They do not recover Apple's private spring constants, gesture thresholds, material parameters or Liquid Glass shaders.

Use a stateful gesture and spring model for control behavior. Give the shell its own geometry. Draw readable content as a separate rigid layer. For a small set of merging controls, use a smooth union of distance fields. Use a fluid solver only when the intended behavior requires simulated flow, conserved mass or capillary forces.

## Coordinate and state contract

Choose one length unit for each driver. A web driver can use CSS pixels, an Android driver can use drawing pixels, and a Flutter or React Native driver can use logical pixels. Convert at the adapter boundary. Never mix device pixels with logical pixels in the same velocity calculation.

Use seconds for elapsed time and length units per second for velocity. Millisecond pointer timestamps need division by 1000. Normalized slider velocity has units 1/s. Angular velocity needs a declared radians/s or degrees/s convention.

Keep these quantities separate:

| Quantity | Meaning | Units |
| --- | --- | --- |
| X | Raw drag or spring coordinate | length |
| v | Time derivative of X | length/s |
| a, b | Valid track endpoints | length |
| V | Published control value | domain units |
| r | Selected destination for the spring | length |
| Y | Rendered position after resistance | length |
| e | Shell extension or compression | length |

During direct manipulation, the pointer owns X. On release, a spring owns X. A new pointer gesture takes ownership immediately. Reuse the current state and establish a new pointer offset so a regrab does not reset the appearance.

Publish the value derived from the input and valid range. After release, publish the chosen committed target for a snapping control. Do not publish decorative spring overshoot as new control input. Whether a continuous control commits on release or updates during dragging is a product decision that the implementation must state.

## Capped semantics and bounded rubber-banding

Let L = b - a, with L > 0. For a continuous slider with domain bounds Vmin and Vmax:

```text
u = clamp((X - a) / L, 0, 1)
V = Vmin + u * (Vmax - Vmin)
```

V is always valid. Visual resistance does not expand the numeric range.

Let R > 0 be the maximum visual extension, in the same length unit as X. Use this piecewise mapping:

```text
f(X) = a - R * tanh((a - X) / R)    when X < a
f(X) = X                           when a <= X <= b
f(X) = b + R * tanh((X - b) / R)    when X > b
Y = f(X)
```

The extension approaches R as raw drag distance grows. The value and first derivative agree at both bounds. The second derivative also approaches zero at the bounds. This avoids a slope change when the pointer first crosses an endpoint.

Let d = max(a - X, X - b, 0). With fixed a, b and R:

```text
f'(X) = 1 - tanh(d / R)^2
vY = f'(X) * v
```

Inside the range, vY = v. Outside the range, resistance reduces the rendered velocity. The derivative is dimensionless. Multiplying it by raw velocity preserves length/s.

For example, with b = 300 px, X = 324 px, R = 24 px and v = 800 px/s, the rendered release velocity is about 335.98 px/s. Starting a spring in Y coordinates with 800 px/s would introduce a velocity discontinuity.

The general release rule for a changing transform is the chain rule:

```text
Y = F(X, p)
dY/dt = (partial F / partial X) * v
        + (partial F / partial p) * dp/dt
```

p can contain bounds, cap size or layout dimensions. Freeze these parameters across the release handoff, or include their derivatives. Resizing the track while treating its bounds as fixed invalidates the simple velocity formula.

For moving upper bound b and cap R, let z = (X - b)/R and Q = 1 - tanh(z)^2:

```text
vY = db/dt + Q * (v - db/dt) + (tanh(z) - z * Q) * dR/dt
```

For the lower overflow, let z = (a - X)/R. The cap term changes sign:

```text
vY = da/dt + Q * (v - da/dt) - (tanh(z) - z * Q) * dR/dt
```

Every term has units length/s. The simpler fixed-layout formula follows when both parameter derivatives are zero.

A common rational alternative for nonnegative overflow is:

```text
rubber(d) = c * d * R / (R + c * d)
rubber'(d) = c * R^2 / (R + c * d)^2
```

c is dimensionless. Its slope at d = 0 is c, so c must equal 1 to join an unchanged interior mapping with continuous slope. This formula is an alternative proposed mapping. It is not evidence for an Apple implementation or constant.

### Where the release spring runs

The simplest guarantee of a hard visual cap is to keep the spring in X coordinates and render f(X) during both dragging and settling. Supply the spring with raw release v. Its initial rendered velocity follows the chain rule automatically. Even if the latent spring overshoots, f keeps the rendered extension within R.

A spring directly in Y coordinates needs vY at release. Its later overshoot can exceed the initial visual cap. Clamping the resulting Y then creates a new derivative discontinuity. If a hard cap is required throughout the return, retain the latent coordinate or apply another differentiable bounded mapping throughout the animation.

Do not estimate raw velocity by dividing rendered velocity by f'(X) near saturation. The denominator approaches zero and amplifies noise. Track raw input samples before the resistance mapping.

## Velocity-preserving spring retargeting

For a fixed target r, use the damped spring equation:

```text
m * X'' + c * X' + k * (X - r) = 0
omega0 = sqrt(k / m)
zeta = c / (2 * sqrt(k * m))
```

m is a positive mass parameter, k has units mass/s^2, c has units mass/s, omega0 has units 1/s, and zeta is dimensionless. These are animation model units. Forces in pixel coordinates are not forces in Newtons until length is converted to meters.

For 0 <= zeta < 1, let omegaD = omega0 * sqrt(1 - zeta^2), z0 = X0 - r, and B = (v0 + zeta * omega0 * z0) / omegaD:

```text
X(t) = r + exp(-zeta * omega0 * t)
           * (z0 * cos(omegaD * t) + B * sin(omegaD * t))

v(t) = exp(-zeta * omega0 * t)
       * (-zeta * omega0 * (z0 * cos(omegaD * t) + B * sin(omegaD * t))
          - z0 * omegaD * sin(omegaD * t)
          + B * omegaD * cos(omegaD * t))
```

For zeta = 1, let C = v0 + omega0 * z0:

```text
X(t) = r + (z0 + C * t) * exp(-omega0 * t)
v(t) = (v0 - omega0 * C * t) * exp(-omega0 * t)
```

At retarget time, evaluate the old spring's current X and v. Set the new target and use that X and v as its initial state. Do not restart from the original start or reset velocity. Changing the target changes acceleration immediately, but position and velocity remain continuous.

Preserving velocity during a reversal means an object can briefly continue away from the new target before turning. An engine that zeros this outward velocity makes a different interaction choice. It does not satisfy strict velocity continuity.

Use separate stop tolerances for position error in length units and velocity in length/s. Do not reuse one scalar epsilon for both. Analytic evaluation avoids the instability of an explicit Euler spring under variable frame duration. If an existing engine integrates the spring, verify its pause, large-frame-delta and interruption behavior.

## Projected snapping with hysteresis

Project from raw X and v, or from Y and vY if the decision is intentionally in rendered coordinates. Declare the choice. Do not combine a compressed position with raw velocity accidentally.

For exponential drag v' = -lambda * v, lambda > 0 has units 1/s. The projected position at horizon T seconds is:

```text
tau = (1 - exp(-lambda * T)) / lambda
Xprojected = X + tau * v
```

As T approaches infinity, the projection becomes X + v/lambda. This is the integral of the decay model, not an arbitrary pixel multiplier. If using a framework's native decay, use that decay's own target prediction instead. Different decay models produce different destinations.

For valid snap sites s0 < s1 < ... < sn, clamp Xprojected to the valid track. Let midpoint mi = (si + si+1) / 2. Remember the current selected index j. A positive hysteresis margin hi is measured in track length units:

```text
move from j to j + 1 only when Xprojected > mj + hj
move from j to j - 1 only when Xprojected < mj-1 - hj-1
```

Repeat the checks to allow a deliberate fast fling to cross multiple sites. Keep hi smaller than half the local site spacing. At equality, retain the existing selection. The forward and backward thresholds differ, so pointer noise near a midpoint does not alternate the selection.

With sites at 0 and 100 px and h = 8 px, the forward threshold is 58 px and the backward threshold is 42 px. These are demonstration values, not prescribed tuning.

Hysteresis chooses a destination. The spring animates toward that destination. Combining these into a per-frame nearest-site calculation makes a settling control repeatedly change its target.

On pointer cancellation, avoid treating the last measured velocity as a fling. Return to the appropriate valid state without a new activation. Keyboard and assistive input should select the same sites directly without synthesizing a high-velocity gesture.

## Deform the shell while keeping labels rigid

Use at least two independently rendered layers:

```text
stable hit region and semantics
    shell geometry, shadow and material
    label and icon with rigid translation
```

The label can translate with the shell's center. It should not inherit shell scale, shear, path deformation or refraction. A sibling layer is simpler than compensating text for every deformation. If inverse scaling is needed for an existing hierarchy, it must exactly cancel both axes and account for transform origin. It does not automatically cancel clipping or shader distortion.

For a simple deformation, let e be shell extension in length units, H > 0 a reference shell height, and Smax > 0 a maximum dimensionless logarithmic strain:

```text
q = e / H
s = Smax * tanh(q / Smax)
scaleX = exp(s)
scaleY = exp(-s)
```

scaleX * scaleY = 1. This preserves the area of the affine shell, not the volume or perceived area of its shadow. Both scales remain between exp(-Smax) and exp(Smax). Keep Smax small enough for the control's content and visual role. It is a local design parameter.

With fixed H and Smax:

```text
ds/dt = (1 - tanh(q / Smax)^2) * (de/dt) / H
d(scaleX)/dt = scaleX * ds/dt
d(scaleY)/dt = -scaleY * ds/dt
```

These derivatives give the correct handoff when deformation itself gets a spring. A bounded geometry mapping must remain in the render path for the entire settle if its cap is a hard requirement.

For an endpoint response, anchor the shell deformation at the endpoint or contact edge. Scaling around the shell's center moves both ends and communicates a different mechanism. If affine scaling distorts corner curvature, draw a changing rounded path or distance-field shape with an explicitly retained corner radius instead.

The hit region can remain stable while the shell extends. This avoids moving the pointer target away from the finger. Keep the label and actual control in the accessibility tree. Mark duplicate decorative shells as noninteractive and hidden from assistive technology.

## Liquid merge and separation

### Smooth union of distance fields

For a circle, d(p) = length(p - center) - radius. Distances and coordinates use the same length unit. Negative values are inside.

For two distances A and B and blend width w > 0:

```text
h = clamp(0.5 + 0.5 * (B - A) / w, 0, 1)
D = mix(B, A, h) - w * h * (1 - h)
```

This is the original quadratic polynomial smooth-minimum printed by Inigo Quilez. The current article also prints normalized variants. In the formula above, the maximum field inflation is w/4. Do not copy a normalized variant's parameter while assuming the original w convention.

Render the zero contour of D as one common mask. Draw the common shadow and rim from that mask. Separate shadows underneath overlapping circles expose the construction and produce doubled dark regions.

The derivation gives a useful calibration. At the midpoint between equal circles with an edge gap g, A = B = g/2, so D = g/2 - w/4. The midpoint becomes interior when g < w/2. At g = w/2 the neck pinches to zero. This is a geometric blend threshold, not a material's physical rupture distance.

In the blend region, with fixed w:

```text
gradient(D) = h * gradient(A) + (1 - h) * gradient(B)
```

The derivatives through h cancel in this expression. The resulting gradient usually has length below 1. D is not an exact signed distance in the blend region. Use screen derivatives for antialiasing, rather than interpreting each unit of D as an exact pixel everywhere. For example, use an antialias width based on fwidth(D), with a nonzero minimum appropriate to the shader's coordinate scale.

Normalizing this gradient requires a guard near zero magnitude. At a symmetric pinch point, the two gradients can cancel. Smooth-union topology change can therefore create a lighting singularity. A normal guard and a controlled rim treatment solve the render defect. They do not make the pinch a fluid simulation.

Keep blend order stable for multiple shapes. Polynomial smooth union is not associative. Reordering the same objects during interaction can change the silhouette without any geometric movement.

A distance-driven blend can use a bounded contact weight that changes w continuously. Do not toggle w between zero and a finite value when a gap crosses one threshold. If w becomes zero, branch to ordinary min to avoid division by zero.

### Metaball fields

Metaballs sum scalar fields and render an isocontour. One portable compact field choice is:

```text
distanceRatio = length(p - center_i) / supportRadius_i
phi_i(p) = amplitude_i * max(1 - distanceRatio^2, 0)^3
Phi(p) = sum(phi_i(p))
inside when Phi(p) >= threshold
```

The amplitudes, total field and threshold are dimensionless. Support radii are length units. This cubic compact kernel is a proposed choice, not a quotation of Blinn's Gaussian or the Wyvill polynomial. It has zero contribution beyond the support radius and avoids the infinite influence of a Gaussian or inverse-square field.

Changing threshold, support radius or contributor count changes the apparent volume. Preserve the intended silhouette by calibration, or use a solver if conservation matters. A field can merge smoothly as centers approach while still having no simulated pressure, viscosity or surface tension.

Paul Bourke's 1997 explanation describes the inverse-square example and attributes the earlier Gaussian model to Jim Blinn. His page is an inspected implementation explanation and historical secondary source. Blinn's original 1982 paper is listed there but was not retrieved in this pass. Do not cite it as directly inspected evidence.

### Actual surface tension

Muller, Charypar and Gross's 2003 SPH paper provides a fluid model and a separate reconstruction method. In their notation:

```text
cS(p) = sum((mass_i / density_i) * W(p - p_i, supportRadius))
n = gradient(cS)
curvature = -laplacian(cS) / length(n)
surfaceForceDensity = sigma * curvature * n
```

In three-dimensional SI units, cS is dimensionless, n has units 1/m, curvature has units 1/m, and sigma has units N/m. The resulting force density has units N/m^3. The normal points into the fluid in this convention. The paper evaluates the force only where the normal magnitude exceeds a threshold because division near zero is unstable.

A solver then updates particle positions and velocities under pressure, viscosity, surface tension and external forces. Rendering the color-field isosurface is a separate operation. The presence of an isosurface renderer does not show whether its centers came from a solver or an authored trajectory.

For controls that must follow a user's finger, a calibrated geometric model gives more predictable behavior. A physical solver introduces timestep, resolution, parameter and collision choices. In motion graphics, use actual simulation when the brief requires sloshing, droplets, capillary oscillation or mass conservation. Do not call an authored bridge or smooth minimum a surface-tension simulation.

### Shape and glass optics are separate

The merged mask describes geometry. It does not implement the complete Liquid Glass material. Blur, color adaptation, refraction, highlights, rim lighting, shadow and contrast treatment need their own rendering decisions.

An approximation can use field gradients to shift samples from a backdrop texture. This requires an actual texture of the intended backdrop in the renderer. A web shader cannot assume that it can sample the live DOM behind its canvas. CSS backdrop blur alone does not provide arbitrary shader refraction of that DOM. In a controlled scene, render the background into a texture, then sample it through the common shape. Keep text outside that sampling path.

Document the material as an approximation unless a pinned source and comparisons establish fidelity. This research did not compare any renderer against Apple's output.

## Framework mapping and API evidence

These are implementation mappings, not completed ports. No framework app, browser, simulator or device ran in this pass.

| Renderer | Proposed implementation | Verified API evidence and limits |
| --- | --- | --- |
| Android Compose | Keep a Float Animatable in raw drawing coordinates. Use snapTo during dragging, animateTo with a spring at release, and initialVelocity from the raw tracker. Keep the clamp in published semantics and f in drawing. Use the framework decay's predicted target if using native fling behavior. Draw the shell separately from Text. | Official Compose docs and Context7 snippets explicitly support current-value/current-velocity interruption, snapTo, animateDecay and initialVelocity. Bounds stop the Animatable, so bounding the latent spring at the valid track would remove its overflow state. Canvas and shader adaptation remain design mappings here. No RuntimeShader API or Android version availability was checked. |
| Flutter | Keep the driver in one chosen coordinate unit. Start SpringSimulation from current position and velocity with a new target. Use animateWith to drive the controller. Paint the shell separately from the text. | Official SpringSimulation docs verify its explicit start, end and initial velocity plus an animateWith example. Automatic velocity inheritance on a new simulation was not established. Capture current velocity before resetting or stopping the owner. Whether to use AnimationController.unbounded and the exact controller clipping behavior must be verified against the project's installed version. CustomPainter and fragment-shader APIs were not verified in this pass. |
| Web with Motion | Numeric motion values hold raw X. The spring owns this value after release. A derived value maps it through f and drives the shell. Keep a sibling label. Use SVG or a GPU mask for merging. | Official Motion docs verify numeric getVelocity is per second and jump resets velocity and ends active animations. Context7's official animate excerpt says spring velocity defaults to current value velocity. Explicitly pass the correct release velocity when switching from gesture tracking. Rapid set calls and event cadence can affect the estimate, so raw timestamped pointer tracking remains useful. dragElastic and modifyTarget semantics were not independently verified. Do not infer capped domain semantics from drag constraints. |
| React Native with Reanimated | Shared values hold latent position and the derived shell shape. Gesture input supplies raw velocity. Assign withSpring only when its installed version meets the required interruption behavior. Use a custom analytic spring owner if strict reversal continuity is mandatory and the built-in owner clips it. | Official Context7 docs verify withSpring velocity and mutually exclusive physics/duration configuration, plus withDecay clamp, rubberBandEffect and rubberBandFactor. The pinned current main source additionally adds prior and configured velocity for a changed target, then zeros velocity pointing away from the destination. This branch therefore fails strict reversal continuity. This is a branch-specific finding, not a claim about all released versions. A 4.1.5 source URL returned 404, so that release was not inspected. Gesture-handler velocity units and Skia shader APIs remain unverified. |
| Offline motion graphics | Record or author timestamped input, releases and retargets. Evaluate the analytic model at frameTime = frameIndex / framesPerSecond. Bake position, rigid content transforms, shell paths and shader parameters. For actual fluid flow, bake the solver and render its reconstructed surface. | The math has numeric checks below. No After Effects, Blender, Houdini or export API was inspected or executed. Do not present package-specific expressions or node names as verified. Fixed-frame evaluation removes dependency on the interactive renderer's frame cadence, but does not replace export playback and image verification. |

For normalized animation coordinates, convert velocity explicitly. If z = (X - a)/L with fixed bounds, vz = v/L. If a or L changes, use the full derivative. Built-in animation parameters can use different units or precedence from this model. Read the installed engine's source or documentation before translating k, c, duration or bounce settings.

Do not add configured release velocity to an already inherited spring velocity. The pinned Reanimated implementation makes that addition explicitly. A zero configured velocity can be appropriate for pure retargeting, while a fresh gesture release needs its own measured velocity. The exact lifecycle must be checked in the project.

## Evidence log

Files below are in portable-sources/ beside this document. HTML and source bytes are retained. Fetch manifests include exact URLs and UTC retrieval timestamps. Context7 resolved each library before fetching docs. No quota error occurred.

| Source | Local artifact | Short evidence quote | Interpretation and limits |
| --- | --- | --- | --- |
| https://iquilezles.org/articles/distfunctions/ | iq-distance-functions.html and .txt | "a list of Signed Distance Field implementations for some basic 3D shapes" | Original author's geometric distance reference. Useful for base shapes. Shape mathematics alone does not establish Apple fidelity. |
| https://iquilezles.org/articles/smin/ | iq-smooth-minimum.html and .txt | "the order in which you blend objects matters" | Original quadratic code, normalization discussion and gradient limitations inspected. The article explicitly distinguishes conservative distance bounds from exact SDFs. Several displayed derivations are image assets and were not extracted; formulas used here derive from the printed code. |
| https://paulbourke.net/geometry/implicitsurf/ | bourke-implicit-surfaces.html and .txt | "The total field strength at any point in space is the sum of the field strengths due to each control point." | Author's explanation of field-sum modelling with references to Blinn and Wyvill. It supplies a contrasting construction, not dynamics or directly inspected original Blinn evidence. Several kernel formulas are images; the compact kernel above is my declared choice. |
| https://matthias-research.github.io/pages/publications/sca03.pdf | muller-2003-surface-tension.pdf and .md | "adding a term to model surface tension effects" | Original SPH fluid paper, particularly section 3.3, equations 15 through 19. Extracted locally using anydoc. Its numerical and hardware results are historical, not contemporary performance predictions. PDF layout was not visually rendered in this research pass. |
| https://developer.android.com/develop/ui/compose/animation/value-based | compose-value-based.html and .txt, compose-ctx7.txt | "the new animation starts from the current snapshot value with the current velocity" | Primary docs support interruption continuity. The Context7 file also retains official advanced gesture excerpts with initialVelocity and target prediction. No Compose runtime verified. |
| https://api.flutter.dev/flutter/physics/SpringSimulation-class.html | flutter-spring-simulation.html and .txt, flutter-ctx7.txt | "Models a particle attached to a spring that follows Hooke's law." | Explicit initial-state spring constructor verified. Controller bounds, stopping and renderer adaptation require further checks. |
| https://motion.dev/docs/react-motion-value | motion-react-values.html and .txt, motion-ctx7.txt | "This returns the velocity as calculated per second" | Numeric velocity units verified. jump intentionally breaks continuity. The spring velocity default is from the retained official animate excerpt in Context7, not an executed test. |
| https://raw.githubusercontent.com/software-mansion/react-native-reanimated/b66eb8c7dd3108b3ea39b9fe5b653498c91a0419/packages/react-native-reanimated/src/animation/spring/spring.ts | reanimated-spring-pinned.ts and reanimated-source-pin.json | "Inertia is only preserved when it already points toward toValue." | Actual onStart code inspected and pinned by commit. The corresponding code sets opposing velocity to zero. Timestamp conversion to seconds also appears in onFrame. This current main branch is not evidence for every released version. |
| https://docs.swmansion.com/react-native-reanimated/docs/animations/withSpring/ and https://docs.swmansion.com/react-native-reanimated/docs/animations/withDecay/ | reanimated-ctx7.txt | "Makes the animation bounce over the limit specified in clamp." | Official docs retrieved through Context7 establish config fields. A visual bounce does not establish valid published semantics or a hard stretch cap. The attempted tagged source URL is recorded in reanimated-tag-fetch.json. |

## Numeric experiment and missing runtime evidence

The standalone equation-check.py checks a bounded visual map and its derivative, the transformed release velocity, critical-spring retarget continuity, two-way hysteresis, equal-circle midpoint merge threshold and bounded area-preserving strain. It uses illustrative parameters only.

equation-check-results.json records a pass. The maximum finite-difference derivative error was 2.58e-10 for the selected positions and a 1e-4 px difference step. The retarget position and velocity errors at t = 0 were zero. These numbers show agreement of the implemented equations at the sampled cases. They do not measure interaction quality, rendering performance or visual fidelity.

Production acceptance still needs raw and rendered traces at release and reversal, out-of-range drags in both directions, cancellation and regrab, noisy midpoint input, multiple-site flings, resize and reduced motion. Rendered checks need rigid text, stable hit regions, merge/separation around the pinch and no duplicate shadows. For graphics exports, check playback at the requested frame rate and verify the final artifact.

Reduced motion should preserve values, selected states and activation. Remove decorative deformation and long oscillation, and choose a static or short settling path appropriate to the control. A stable opaque material fallback is needed when backdrop sampling or contrast treatment cannot be implemented. Those are explicit implementation paths, not claims that this research has verified them.
