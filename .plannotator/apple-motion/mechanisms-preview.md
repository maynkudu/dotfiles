# Proposed skill chapter. Stretching a brightness control

This chapter describes a portable reconstruction. It does not identify Apple's private brightness-control implementation or reproduce its exact geometry.

## What the interaction does

Dragging changes a bounded brightness value. After the finger moves beyond an endpoint, the control's shell stretches with increasing resistance. Releasing returns the shell to its resting shape. The label and icon remain legible throughout.

The input is displacement. A large pull does not establish that a device measures force or pressure. Add pressure only for a product that actually has and uses a pressure-capable input.

## Keep separate state

Use a semantic value `value` in `[0, 1]`, a raw gesture coordinate `q`, a latent overshoot `d`, and an explicit phase such as `idle`, `tracking`, or `settling`.

For an upward-increasing track of height `H`, compute `q = qAtGrab + (pointerYAtGrab - pointerY)`. Set `value = clamp(q / H, 0, 1)`. Preserve the grab offset, including the current presentation state when a settling control is grabbed again.

At the upper endpoint, `d = max(q - H, 0)`. At the lower endpoint, `d = max(-q, 0)`. Remember which endpoint owns the stretch. During return, a negative spring displacement compresses that same shell instead of switching its anchor to the other endpoint.

## Add resistance

For a signed latent displacement `d`, a maximum visual displacement `L`, and dimensionless resistance parameter `c`, use:

```text
f(d) = L c d / (L + c |d|)
f'(d) = c L² / (L + c |d|)²
```

Lengths use the same unit throughout. The slope starts at `c` and decreases as the pull grows. The visual displacement stays strictly within `(-L, L)` for finite input.

The resistance is a chosen input mapping. It is not a surface-tension calculation or a measurement of Apple's control.

## Carry the correct velocity

Estimate the raw pointer velocity from timestamped samples. Convert milliseconds to seconds once. A release after a stationary hold should have zero velocity even if an earlier move was fast.

The rendered velocity is `vVisual = f'(d) vRaw`. Passing raw pointer velocity to a spring that owns visual displacement creates a speed discontinuity.

One reliable solution is to spring the latent `d` toward zero and apply `f` on every frame. The visual velocity then follows the chain rule automatically, and the maximum stretch holds even when outward release velocity initially extends the control further.

## Return without restarting

Use a damped spring with current position and velocity:

```text
x'' + 2 ζ ω x' + ω² (x - target) = 0
```

`ω` is angular frequency in radians per second. `ζ` is dimensionless damping ratio. For a stationary target change, retain the current `x` and `x'`; change only `target`. Position and velocity stay continuous. Acceleration can change immediately.

Critical damping does not guarantee that every trajectory stays on one side of its target. Sufficient initial velocity can cross the target even when `ζ = 1`.

Choose the endpoint before settling. Brightness remains at its endpoint while the decorative shape returns. Another drag takes control of the current shape immediately.

## Deform the shell

Let the signed visual extension be `e = f(d)`, with `L < H`. An illustrative area-preserving mapping is:

```text
newHeight = H + e
newWidth = W H / newHeight
```

Anchor the opposite endpoint. Update the shell path and its shadow together. Render the icon and label in separate unscaled layers. This preserves rectangle area, not the true volume of a simulated material. Rounded outlines require their own area calculation if exact area conservation matters.

Use a continuous native corner shape when available. A web superellipse is an explicit approximation, not an extracted Apple corner formula.

## Verify the interaction

Pull beyond both endpoints, release while still moving, hold before release, reverse direction, re-grab during return, cancel pointer capture, and use keyboard increments and endpoint keys. Check that brightness stays bounded and the label stays unscaled.

With reduced motion, retain the brightness interaction and its selected state, and remove decorative stretch and oscillation. Stop frame work at rest and when hidden. Handle a preference change during a drag or return.
