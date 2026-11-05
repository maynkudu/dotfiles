# Constructing the artwork

Read this when choosing forms, composition, material, or layer boundaries for a
new scene. The current request and its references determine the result.

## Read the reference as drawing

Record the traits that change construction. A lotus reference may depend on
pointed overlapping petals, dark contours, visible veins, ivory and violet
flowers, and gold seed detail. Paisley can depend on a curved teardrop outline,
smaller repeated shapes inside it, and alternating dense and open areas. A
radial medallion needs deliberate symmetry, ring spacing, and edge detail.

Choose which traits belong in this scene. The garden demonstrates lotus drawing;
its subject and palette are not defaults for every request. Preserve explicit
reproduction requirements when the task calls for an exact copy.

Draw the silhouette first at the final display size. Add major internal divisions,
then secondary ornament, veins, and material texture. Check both the isolated
object and its surroundings. Fine detail that disappears at the intended size
does not improve the visible result.

## Parts and attachment

Separate parts where their behavior or occlusion differs. A stem can deform
along a chain while its leaves follow local tangents and its head lags behind.
Give each part a pivot in common world coordinates. Keep shapes long enough to
overlap their attachment so bending does not expose a gap.

The bundled garden uses procedural paths for stems, leaves, petals, and pads.
Its seed fixes grass, stars, pads, and texture. The draw functions in
`assets/scenes/garden.ts` show pointed petals with curved veins, stacked petal
rows, and growth-dependent opening. Preserve these mechanisms when extending
this garden. Construct different geometry when the subject changes.

Painted parts can use transparent PNG or WebP assets. Keep original resolution,
alpha edges, pivots, and the hidden margins needed by the animation. A petal that
needs to curl requires changing geometry or mesh coordinates. Translation of a
flat cutout only moves it rigidly.

## Depth and lighting

Define the layer order before adding effects. Use overlap, scale, contour weight,
and color to separate foreground from distance. Keep decoration from obscuring
interactive objects and their focus indicators.

Day and night should change the same scene coherently. Update sky, plants, ground,
and celestial objects from one phase. Test the cycle boundary as well as day and
night endpoints. Stars, glow, or particles should have a purpose and a bounded
count.

## Judge the result

Compare the actual render with the traits selected from the reference. Name the
concrete gap before revising it: too few petal rows, uniform contours, a missing
inner pattern, poor overlap, or insufficient contrast between adjacent forms.
Keep successful parts intact while fixing that gap.

The bundled garden is procedural ornament. A request for the texture of painted
fabric needs separate material work and visual verification. Do not claim that
procedural noise recreates the texture of a supplied image.
