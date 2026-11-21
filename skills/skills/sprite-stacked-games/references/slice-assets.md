# Slice assets

A horizontal slice is a top-down image of one height. Stack all layers around the same ground pivot, draw from ground to roof, and rotate every layer by the object's heading. Apply camera squash after rotation, then lift each layer in screen space. Source art pixels and final display pixels are different units.

For original vehicles, author the wheel, chassis, body, cabin and roof layers directly. Keep wide color clusters and aligned features. The Switchback starter faces +x; a supplied strip may face another direction, so declare and test its forward axis.

For a PNG strip, require positive integer dimensions and a width evenly divisible by the layer count. Preserve alpha. Reject an empty strip, non-finite options and missing layer metadata with an actionable error. Keep the source file intact. A voxel-editor layer export is also a suitable input when its provenance allows use.

Four orthographic views can estimate a visual hull, but hidden cavities cannot be recovered from silhouettes. View alignment and scale are prerequisites. Show the result, keep a manual slice correction path, and treat image generation as an optional user-authorized source.

Compare zero rotation, camera squash 1 and spacing 1 with direct bottom-to-top compositing. Use a visibly asymmetric marker to catch a flipped axis. Inspect 45-degree edges and a complete turn. Draw an outline around the finished stack when needed, rather than outlining every layer.

Cache static props. Keep vehicle stacks dynamic. Store an asset's source, palette, authoring command and license with its manifest.

Technique reference: https://www.spritecook.ai/blog/sprite-stacking-pixel-art
Additional implementation reference: https://github.com/danielwh2/sprite-stacking
These are research references. Their sample media are not bundled game assets.
