# Apple fluid interaction research

Research date: 2026-11-09 UTC. Scope: earlier iOS fluid interaction principles and iOS 26 Liquid Glass, for a reusable animation skill that can be implemented on other platforms.

Apple publicly describes enough behavior to support continuous dragging, elastic boundaries, momentum preserving release and retargeting, and geometry driven merging. The inspected sources do not disclose the deformation law of an iOS 26 slider, the private Liquid Glass shader, the constants used by individual system controls, or a liquid simulation that explains the material.

The strongest direct statement about the requested slider behavior is in WWDC25 session 284 at 18:07. Apple says sliders have Liquid Glass effects on their thumb and "preserve momentum and stretch when they are moved." The session does not specify that the stretch is exclusively caused by dragging beyond the slider's bounds. Earlier iOS rubberbanding explains continued visual response at boundaries. Combining those behaviors into a slider that stretches beyond its range is a proposed portable design, with a clear Apple precedent for each behavior, rather than a recovered specification of Apple's slider.

## How to read the evidence

- **Public mechanism** means an Apple transcript or API document explicitly states the behavior or implementation relationship.
- **Apple demonstration narration** means a speaker describes a demonstration. The transcript supports that description, but this research did not play the video, inspect its frames, or operate the control.
- **Proposed reconstruction** means a portable implementation recommendation derived from the principles. It is not evidence of Apple's private implementation.

Ten substantive sources are cited below. Raw HTML, documentation JSON, timecoded transcripts, selected excerpts, session code snippets where available, and retrieval metadata are saved in [apple-primary-sources/](apple-primary-sources/). [manifest.json](apple-primary-sources/manifest.json) records exact URLs, retrieval timestamps, and file paths. The Apple video catalogs and three incidentally retrieved icon pages are discovery records. The icon pages do not support the synthesis.

The parent already completed BLANK discovery. Before retrieving named SwiftUI API documentation, this research ran Context7 `library SwiftUI` with the full research question and selected `/websites/developer_apple_swiftui`, then ran `docs` with the same question. Both commands succeeded without a quota error. The document results are preserved in [ctx7-swiftui.txt](apple-primary-sources/ctx7-swiftui.txt). The direct Apple documentation JSON was retrieved afterward.

The final Markdown edit was initially blocked because the installed edit hook did not recognize the parent's BLANK search in this session. Recovery ran `blank registry-search 'spring slider glass'`, then `blank search 'fluid slider motion'`. The registry search returned no installables. Discovery returned fluid simulation references and reported that reranking was unavailable. These references do not provide first-party Apple evidence and were not used in the synthesis. The search responses are saved as [registry recovery](apple-primary-sources/blank-registry-recovery.txt) and [discovery recovery](apple-primary-sources/blank-discovery-recovery.txt). The edit succeeded after those searches.

## What carries across earlier iOS and Liquid Glass

### Input remains active while the interface moves

WWDC 2018 session 803 explains that people change their intention during an interaction. The interface should respond to the new intention immediately. Its iPhone X examples allow changing between home, multitasking, and app switching during one gesture, interrupting an app launch, and interacting with an app while it launches. At 09:16 the speaker explicitly says the demonstration's physics has been slowed down. Its visible timing cannot establish production timing. [S1, 06:59](https://developer.apple.com/videos/play/wwdc2018/803/?time=419)

This is a behavioral requirement. A portable control should accept another drag, another destination, or cancellation while it is settling. A motion duration is not a period during which input becomes unavailable. This recommendation follows Apple's examples; the sources do not prescribe one cross-platform event handling architecture.

The same session describes using the finger's acceleration to detect the pause that opens multitasking, instead of waiting on a timer. This is evidence that Apple used changes in input motion to infer intent in that specific interaction. It does not establish an acceleration detector or threshold for all controls. [S1, 10:38](https://developer.apple.com/videos/play/wwdc2018/803/?time=638)

### Tracking is direct, with a meaningful change at a boundary

At 52:22 in session 803, Apple says the touch and dragged image should move together and the relative grab position should be preserved. The object should not jump so that its center becomes the dragging point. At 53:11, Apple observes that users notice when content stops tracking one to one, and that scrolling uses this change to communicate the end of content. [S1, 52:16](https://developer.apple.com/videos/play/wwdc2018/803/?time=3136)

Earlier in the talk, rubberbanding is described as softly indicating boundaries while still tracking the user. A hard stop can be indistinguishable from an unresponsive interface. The same principle applies when two parts of an interface hand tracking over to each other. [S1, 17:01](https://developer.apple.com/videos/play/wwdc2018/803/?time=1021)

A portable reconstruction should therefore keep ordinary in-range manipulation attached to input, then smoothly reduce its visual response beyond a boundary. The beyond-bound response should still change as the user continues dragging. Apple documents this purpose and its scrolling example. This source does not publish a universal rubberband equation, coefficient, maximum stretch, or slider boundary mapping.

### Release continues the motion, and another target can interrupt it

Session 803 describes scrolling as maintaining the momentum supplied by the user, using consistent friction, and coming to an imperceptible stop. Its elasticity model pulls a current displayed value toward a target and returns overscrolled content within the boundary after release. [S1, 28:49](https://developer.apple.com/videos/play/wwdc2018/803/?time=1729), [S1, 31:14](https://developer.apple.com/videos/play/wwdc2018/803/?time=1874)

WWDC23 session 10158 makes the continuity requirement explicit. Position and velocity should remain continuous. Its gesture example contrasts a fixed ease-in-and-out animation with a spring that can begin at the gesture's current velocity. At 05:57, Apple says SwiftUI now automatically tracks velocities when a gesture changes properties. At 14:53, it explains that a retargeted spring uses its existing velocity as the initial velocity toward the new destination. [S2, 02:12](https://developer.apple.com/videos/play/wwdc2023/10158/?time=132), [S2, 04:38](https://developer.apple.com/videos/play/wwdc2023/10158/?time=278), [S2, 14:53](https://developer.apple.com/videos/play/wwdc2023/10158/?time=893)

WWDC23 session 10156 provides the framework mechanism behind that explanation. A spring animation's `shouldMerge` incorporates the previous animation's state, and its `velocity` implementation makes velocity available when one animation merges with another. The current `Animation.spring(_:blendDuration:)` documentation explicitly says that successive spring and interactive spring animations on the same property preserve velocity. [S3, 18:11](https://developer.apple.com/videos/play/wwdc2023/10156/?time=1091), [S10](https://developer.apple.com/documentation/swiftui/animation/spring(_:blendduration:))

This guarantee has a scope. It describes compatible successive animations on the same property and SwiftUI's gesture integration. It does not mean that remounting an object, replacing its identity, switching to an arbitrary animation, or animating a different derived property automatically preserves the old motion. A portable implementation needs to retain the current displayed position and velocity for the state it actually animates.

### Snap destination reflects the gesture's direction and speed

Session 803 treats target selection as a separate problem from animating to that target. In its FaceTime picture-in-picture example, choosing the corner nearest the release position ignores the flick's momentum. Apple instead projects where the object would coast using its release velocity and a familiar scrolling deceleration rate, chooses the corner nearest that projected position, and retargets the object there. The projected position is hypothetical and is never displayed. [S1, 43:12](https://developer.apple.com/videos/play/wwdc2018/803/?time=2592), [S1, 45:15](https://developer.apple.com/videos/play/wwdc2018/803/?time=2715), [S1, 46:30](https://developer.apple.com/videos/play/wwdc2018/803/?time=2790)

A portable snapping interaction therefore has two decisions. It selects an allowed destination from the gesture's intent, then moves toward that destination while preserving current motion. Keeping velocity continuous cannot correct a destination that contradicts the flick. Conversely, selecting the intended destination cannot remove a velocity jump at release.

Projection is a documented mechanism for the FaceTime example, and Apple recommends it for other dragged or swiped properties. Applying it to a stepped slider is a proposed policy. A precision slider may need to keep the directly selected tick, whereas a movable panel may intentionally advance to a farther resting position after a flick. Define this semantic choice before tuning motion. This evidence does not establish the native slider's target selection rule or projection constant.

### Elasticity is useful without repeated bouncing

Session 803 recommends starting with 100 percent damping in its design terminology. It gives a specific Music example using no overshoot when opening Now Playing from a tap and 80 percent damping when a swipe dismisses it. These are historical examples, not iOS 26 slider constants or a universal recipe. [S1, 36:09](https://developer.apple.com/videos/play/wwdc2018/803/?time=2169)

Session 10158 similarly recommends starting with zero bounce, then tuning for the context. It says a gesture ending can justify bounce and warns that values above roughly 0.4 can look exaggerated. Its discussion distinguishes perceptual duration from settling duration. The mathematical spring tail continues past the perceptual duration, and user-facing work should not wait for the variable settling duration. [S2, 16:12](https://developer.apple.com/videos/play/wwdc2023/10158/?time=972), [S2, 20:32](https://developer.apple.com/videos/play/wwdc2023/10158/?time=1232)

The reusable skill should make pace and bounce independent choices. It should support a spring that moves quickly and settles smoothly with little visible oscillation. Tuning the interaction by increasing bounce alone would miss Apple's reason for using springs, which is continuous motion that can be redirected.

The terminology changed between the talks. The 2018 presentation exposes damping ratio and response, and avoids calling response a duration. The 2023 APIs expose perceptual duration and bounce. These are different parameterizations. Do not copy a numerical response into a duration field or interpret 80 percent damping as 80 percent bounce.

## Displacement, force, and pressure

Different quantities can produce a similar appearance of softness, but they have different input and state requirements.

| Quantity | What Apple explicitly documents | Portable implication |
| --- | --- | --- |
| Drag displacement | One-to-one movement with preserved grab position; continued tracking at scrolling boundaries. S1, 17:01 and 52:16. | Use position and displacement to drive a drag. Define a separate beyond-bound visual mapping. |
| Gesture velocity | Motion history contributes to release; a spring can inherit gesture velocity and retain velocity when retargeted. S1, 52:34. S2, 05:32 and 14:53. | Record velocity in the animated coordinate system and carry it into release and retargeting. |
| Actual touch pressure | The iPhone X flashlight button grows based on pressure and teaches that pressing harder activates it. S1, 53:58. | Treat pressure as an optional input capability for an explicitly pressure driven interaction. |
| Spring restoring force | Mass, stiffness, and damping determine a model that pulls current state toward a target. S1, 31:41. S2, 08:35. | A simulation can calculate force from displacement without receiving pressure from hardware. |
| Liquid Glass touch response | Immediate flexing and light feedback; interactive glass scales, bounces, and shimmers. S5, 03:38. S6, 19:21. | Describe the visible response and input trigger. These statements do not identify a pressure sensor or force law. |

The slider statement in session 284 refers to movement, momentum, and stretch. Neither that statement nor the Liquid Glass design session identifies pressure as the driver of slider stretching. An implementation based on ordinary pointer displacement can follow the documented drag principles without claiming equivalence to Apple's deformation law.

The flashlight example is useful evidence that pressure existed as a distinct input in earlier iOS. It does not justify making real pressure a dependency for an iOS 26 inspired slider, mouse control, or other platform's touch interaction. The inspected sources also do not equate contact area, press duration, and measured pressure.

If a portable prototype invents a force-like signal from excess displacement, velocity, or a held press, name the underlying signal. Calling this "pressure" would conceal a product choice and could make the skill impossible to reproduce on devices that expose different input data.

## Bounded slider value and visual elasticity

The evidence supports separating a control's meaning from its displayed deformation, but it stops short of publishing Apple's internal slider state.

Session 10156 describes animatable attributes as having model and presentation values. An animation calculates the current presentation value as the model changes. This is a public animation framework explanation. It is not a disclosure of the internal state fields of `UISlider`. [S3, 05:06](https://developer.apple.com/videos/play/wwdc2023/10156/?time=306)

Session 284 independently shows that a slider may restrict selection to five tick values, while also stating that sliders preserve momentum and stretch. It also describes a neutral value that anchors track fill. Session 323 describes stepped sliders, manually placed ticks, and neutral values. [S7, 18:07](https://developer.apple.com/videos/play/wwdc2025/284/?time=1087), [S6, 15:42](https://developer.apple.com/videos/play/wwdc2025/323/?time=942)

A proposed portable slider should maintain these separately:

- The selected domain value, restricted to the allowed range and any selected step policy.
- The pointer's raw position or displacement, which can continue beyond the range.
- The visual state of the thumb, track, or surrounding control, including stretch and its current motion.
- The resting target used on release, which must correspond to a valid value and a defined resting shape.

This separation lets a slider communicate a reached limit while still responding to further input. It also lets a control animate toward a valid discrete value without exposing intermediate presentation values as permitted selections. The precise policy for live value changes, committed changes, and cancellation belongs to the product. The research does not establish one Apple-wide commit rule for sliders.

Stretch can communicate speed as well as a boundary. Session 803 describes motion stretching as deforming content in each frame to convey velocity, and gives app launch and close transitions as examples. That is a separately documented purpose for visual deformation. A portable skill should name whether a particular stretch is driven by excess displacement, ongoing velocity, or a combination. Native slider stretching is not fully specified by any one of these examples. [S1, 20:00](https://developer.apple.com/videos/play/wwdc2018/803/?time=1200)

On release, continuing the rendered motion matters. When a nonlinear beyond-bound mapping has reduced thumb movement, the raw finger velocity and the rendered thumb velocity can differ. Carrying the raw finger velocity directly into a different visual coordinate can introduce a velocity jump. The proposed skill should transfer velocity consistently through its mapping or measure the resulting visual velocity. This follows the published continuity goal; Apple does not publish this calculation for its native slider.

Regrabbing a settling control also needs a distinction. Preserve the current displayed position and the grab offset to avoid a jump. Once direct manipulation takes over, the new input can determine movement. A guarantee that a retargeted spring preserves velocity is not a guarantee that a stationary finger must inherit all previous object velocity. The inspected material does not prescribe one catch behavior for every direct manipulation control.

## Liquid Glass merging, separation, and identity

Native glass containers coordinate geometry interaction.

| Public mechanism | Documented behavior | Meaning for a portable skill |
| --- | --- | --- |
| `GlassEffectContainer` | Renders child glass shapes together. As shapes approach, their paths blend. Higher container spacing begins blending sooner. S8 and S9. | Define an explicit group of shapes that can interact and a distance at which visual connection begins. |
| `UIGlassContainerEffect` | Child glass views merge as they approach and combine into one shape when their frames overlap. Its spacing property controls their interaction distance. S7, 23:53. | Separate placement animation from shape connection. Distance can drive the connection while positions remain ordinary animation state. |
| `glassEffectID(_:in:)` | Gives each effect an identity within a namespace. Together with a container, identity and geometry coordinate transitions as effects appear and disappear. S8. | Give components stable identities so interruption or insertion does not become an unrelated disappearance and reappearance. |
| `glassEffectUnion(id:namespace:)` | Multiple view geometries contribute to one glass shape at rest when they share the appropriate union ID and compatible shape and material. S8. | Distinguish a persistent shared background from a temporary connection produced by proximity. |
| `GlassEffectTransition` | Current docs distinguish `matchedGeometry` and `materialize`. Proximity within container spacing supports the default morph transition; distant insertion or removal can use materialization. S8. | Choose whether an element has a spatially related source. Use a separate appearance transition when a meaningful morph source is unavailable. |
| Interactive glass | SwiftUI `.interactive()` or UIKit `isInteractive = true` applies responsive scale and bounce feedback. S6 and S7. | Interaction feedback is a separate behavior from merging and from persistent grouping. |

Container spacing is an interaction distance, distinct from the layout spacing of an `HStack` or `VStack`. Current docs explicitly say that a container spacing greater than the interior layout spacing can make effects blend while at rest. The example describes morphing when the nearest edge is within the container's spacing. The docs do not publish the blending kernel or the precise path construction. [S8, "Combine multiple views with Liquid Glass containers"](https://developer.apple.com/documentation/swiftui/applying-liquid-glass-to-custom-views#Combine-multiple-views-with-Liquid-Glass-containers), [S9](https://developer.apple.com/documentation/swiftui/glasseffectcontainer)

Morph IDs and union IDs are not interchangeable. Apple's custom view example uses distinct `"pencil"` and `"eraser"` effect IDs. The WWDC25 badge example uses `badge.id` for each badge and `"badgeToggle"` for the button. These shapes can morph into or emerge from nearby shapes while retaining distinct identities. Giving every participant the same morph ID is not what these examples prescribe. The union example uses shared IDs deliberately to combine geometries into persistent backgrounds. [S6, 19:51](https://developer.apple.com/videos/play/wwdc2025/323/?time=1191), [S8](https://developer.apple.com/documentation/swiftui/applying-liquid-glass-to-custom-views)

The documented UIKit separation procedure is concrete. Add the glass views at the same position without animation, then animate them outward together. The container supplies the blending between the shapes. This gives a native split behavior without a public morph ID API in the demonstrated UIKit code. It does not establish that UIKit has no other identity APIs. [S7, 24:27](https://developer.apple.com/videos/play/wwdc2025/284/?time=1467)

A shared container also affects rendering correctness. Session 323 says glass samples an area larger than itself, cannot sample other glass, and uses the container to share a sampling region. Nearby glass in different containers can produce inconsistent results. The UIKit session says its container enforces uniform adaptation. These statements explain why unrelated isolated blur layers do not reproduce the documented composition. They reveal an architectural relationship, not the proprietary shader. [S6, 19:51](https://developer.apple.com/videos/play/wwdc2025/323/?time=1191), [S7, 24:46](https://developer.apple.com/videos/play/wwdc2025/284/?time=1486)

### What "surface tension" can mean in the skill

Apple's UIKit presenter compares approaching shapes to "small droplets of water." The Liquid Glass design session describes gel-like flexibility and lightweight liquid motion. These analogies support a connected shape that forms as elements approach and separates as they move apart. [S7, 24:07](https://developer.apple.com/videos/play/wwdc2025/284/?time=1447), [S5, 03:51](https://developer.apple.com/videos/play/wwdc2025/219/?time=231)

The sources do not state that Apple integrates a surface tension force, solves fluid flow, preserves liquid volume, or uses metaballs or signed distance fields. A portable implementation could choose a smooth union, an explicit connecting path, or another shape blending technique. Such a choice must be labeled a reconstruction. Its coefficients, neck shape, merge distance, and breakup timing remain implementation choices.

Keep the connection between meanings clear. A visible merged background can unite related controls without combining their semantic values or click targets. Session 356 explicitly recommends grouping related actions and warns that some combinations of symbols and text can be mistaken for one button. This supports purposeful grouping and readable boundaries. [S4, 09:01](https://developer.apple.com/videos/play/wwdc2025/356/?time=541)

The current docs use geometry and spacing to determine when and which shapes morph. They do not describe a universal arbitration rule for several equally eligible sources. A portable system should define ambiguous cases explicitly and avoid claiming its choice duplicates Apple's internal pairing logic.

## Shape, light, and accessibility are separate requirements

Session 219 describes the optical effect as lensing. Objects materialize by modulating light bending, interaction starts a glow at the contact point, and changes in size can produce deeper shadows and stronger lensing. The material is adaptive to its background. A uniform translucent fill with blur covers only part of that description. [S5, 01:55](https://developer.apple.com/videos/play/wwdc2025/219/?time=115), [S5, 07:02](https://developer.apple.com/videos/play/wwdc2025/219/?time=422), [S5, 12:05](https://developer.apple.com/videos/play/wwdc2025/219/?time=725)

For the requested animation skill, geometric continuity, responsive input, and semantic value constraints can be specified and implemented independently of exact refraction. The shader implementation, exact highlight calculation, adaptive contrast thresholds, and native slider material parameters remain unknown in this evidence set. A portable implementation should say which optical behaviors it actually implements.

Apple's reduced motion treatment is unusually relevant here. Session 219 says Reduced Motion decreases the intensity of some effects and "disables any elastic properties for the material." Reduced Transparency increases frosting, and Increased Contrast changes appearance and adds a contrasting border. These adaptations are automatic for native Liquid Glass. [S5, 18:15](https://developer.apple.com/videos/play/wwdc2025/219/?time=1095)

A portable reconstruction should support a reduced motion path that removes elastic deformation and excessive overshoot while retaining immediate input feedback, valid value changes, and clear state transitions. Exact native reduced motion behavior was not operated or measured in this research. The statement about native automatic accessibility adaptation is not a claim that a custom shader on another platform receives those adaptations automatically.

## Recommendations the parent can turn into reusable requirements

1. Define which input signal drives each response. Ordinary drag position, gesture velocity, measured pressure, and invented deformation signals must remain distinguishable.
2. Preserve the relative grab position. Respond continuously during manipulation and allow redirection while motion is in progress.
3. Keep a bounded domain value separate from visual overflow. Define how steps, neutral values, commits, and cancellation work for the product.
4. Treat release as a handoff from measured motion into a target driven behavior. Preserve position and velocity in the visual coordinate being animated.
5. Select an allowed snap target from the interaction's defined intent, then retarget the current motion state. Repeated snaps should not restart from an obsolete source value or an assumed zero velocity.
6. Expose pace and bounce as independent tuning choices. Begin with little or no bounce and tune to the interaction. Do not copy the historical Music values into all controls.
7. Define an interaction group for merging shapes. Keep proximity connection, persistent shared backgrounds, and identity based transitions as separate features.
8. Specify a distance based connection and separation behavior. Label the chosen geometry method and all numerical parameters as the portable implementation's choices.
9. Tie morphs to understandable spatial relationships. Maintain independent semantic controls even when their visual backgrounds join.
10. Provide reduced motion behavior that disables elastic deformation. Keep input response and state communication visible.

These are proposed requirements based on the evidence. They are not extracted native control constants, and they do not establish pixel or timing fidelity to iOS 26.

## Source record and brief evidence quotes

| ID | First-party source | Relevant timecodes or sections | Retrieved source |
| --- | --- | --- | --- |
| S1 | [Designing Fluid Interfaces, WWDC 2018, 803](https://developer.apple.com/videos/play/wwdc2018/803/) | 05:33 response. 06:59 interruption. 10:38 acceleration. 17:01 rubberbanding. 20:00 motion stretching. 28:49 momentum. 31:14 springs. 34:22 parameterization. 36:09 bounce. 42:06 to 47:47 endpoint intent. 52:16 tracking. 53:58 pressure. | [Raw HTML](apple-primary-sources/wwdc2018-803.html), [full transcript](apple-primary-sources/wwdc2018-803.transcript.txt), [excerpts](apple-primary-sources/wwdc2018-803.excerpts.txt) |
| S2 | [Animate with springs, WWDC 2023, 10158](https://developer.apple.com/videos/play/wwdc2023/10158/) | 02:12 position and velocity. 04:38 gesture handoff. 05:57 automatic velocity tracking. 08:35 model. 09:54 parameters. 14:53 retargeting. 16:12 completion. 17:29 presets. 20:32 tuning. | [Raw HTML](apple-primary-sources/wwdc2023-10158.html), [full transcript](apple-primary-sources/wwdc2023-10158.transcript.txt), [excerpts](apple-primary-sources/wwdc2023-10158.excerpts.txt), [published code](apple-primary-sources/wwdc2023-10158.code.json) |
| S3 | [Explore SwiftUI animation, WWDC 2023, 10156](https://developer.apple.com/videos/play/wwdc2023/10156/) | 05:06 model and presentation. 13:22 springs. 15:31 custom animation. 18:11 `shouldMerge` and velocity. | [Raw HTML](apple-primary-sources/wwdc2023-10156.html), [full transcript](apple-primary-sources/wwdc2023-10156.transcript.txt), [excerpts](apple-primary-sources/wwdc2023-10156.excerpts.txt), [published code](apple-primary-sources/wwdc2023-10156.code.json) |
| S4 | [Get to know the new design system, WWDC25, 356](https://developer.apple.com/videos/play/wwdc2025/356/) | 03:03 concentric shapes. 06:42 source relationships. 09:01 grouping. 13:34 cross-device continuity. 17:03 shared interactions. | [Raw HTML](apple-primary-sources/wwdc2025-356.html), [full transcript](apple-primary-sources/wwdc2025-356.transcript.txt), [excerpts](apple-primary-sources/wwdc2025-356.excerpts.txt) |
| S5 | [Meet Liquid Glass, WWDC25, 219](https://developer.apple.com/videos/play/wwdc2025/219/) | 01:55 lensing. 02:55 materialization. 03:38 flex. 04:10 transient glass. 04:43 morph. 07:02 size adaptation. 12:05 contact glow. 13:04 layering. 18:15 accessibility. | [Raw HTML](apple-primary-sources/wwdc2025-219.html), [full transcript](apple-primary-sources/wwdc2025-219.transcript.txt), [excerpts](apple-primary-sources/wwdc2025-219.excerpts.txt) |
| S6 | [Build a SwiftUI app with the new design, WWDC25, 323](https://developer.apple.com/videos/play/wwdc2025/323/) | 01:09 controls. 07:05 source zoom transitions. 15:42 sliders. 19:21 interactivity. 19:51 container sampling. 20:47 IDs. | [Raw HTML](apple-primary-sources/wwdc2025-323.html), [full transcript](apple-primary-sources/wwdc2025-323.transcript.txt), [excerpts](apple-primary-sources/wwdc2025-323.excerpts.txt), [published code](apple-primary-sources/wwdc2025-323.code.json) |
| S7 | [Build a UIKit app with the new design, WWDC25, 284](https://developer.apple.com/videos/play/wwdc2025/284/) | 18:07 slider momentum and stretch. 18:15 ticks. 20:29 materialize. 23:03 interactivity. 23:53 container. 24:18 spacing. 24:27 merge and split. | [Raw HTML](apple-primary-sources/wwdc2025-284.html), [full transcript](apple-primary-sources/wwdc2025-284.transcript.txt), [excerpts](apple-primary-sources/wwdc2025-284.excerpts.txt), [published code](apple-primary-sources/wwdc2025-284.code.json) |
| S8 | [Applying Liquid Glass to custom views, SwiftUI documentation](https://developer.apple.com/documentation/swiftui/applying-liquid-glass-to-custom-views) | Apply and configure Liquid Glass effects. Combine multiple views with Liquid Glass containers. Morph Liquid Glass effects during transitions. Optimize performance when using Liquid Glass effects. | [Raw DocC JSON](apple-primary-sources/doc-custom-liquid-glass.json), [readable extraction](apple-primary-sources/doc-custom-liquid-glass.text.txt) |
| S9 | [GlassEffectContainer, SwiftUI documentation](https://developer.apple.com/documentation/swiftui/glasseffectcontainer) | Abstract and Overview. Metadata lists introduction in iOS 26.0 and other supported platforms. | [Raw DocC JSON](apple-primary-sources/doc-glass-effect-container.json), [readable extraction](apple-primary-sources/doc-glass-effect-container.text.txt) |
| S10 | [Animation.spring(_:blendDuration:), SwiftUI documentation](https://developer.apple.com/documentation/swiftui/animation/spring(_:blendduration:)) | Discussion. Metadata lists introduction in iOS 17.0. | [Raw DocC JSON](apple-primary-sources/doc-spring-persistence.json), [readable extraction](apple-primary-sources/doc-spring-persistence.text.txt) |

The following short quotes are exact wording assembled from adjacent timecoded transcript spans, with line breaks removed. Ellipses identify omitted spans.

- **S1, 17:05 to 17:19.** "It means we're softly indicating boundaries of the interface." Later, "And, it's tracking you throughout."
- **S1, 52:28 to 52:32.** "We should respect the relative position, and never use the center of the image as the dragging point."
- **S1, 54:00 to 54:04.** "the size of button changes based on the pressure of my touch."
- **S2, 02:26 to 02:29.** "So one goal we have is to make our animations have continuous position and velocity."
- **S2, 05:57 to 06:02.** "SwiftUI will now automatically track velocities any time a gesture is changing properties, so you can get this behavior without any extra work."
- **S2, 15:00 to 15:10.** "When that happens, a spring animation uses the velocity it had when it was retargeted as the initial velocity towards its new destination and this same velocity preservation makes these kind of interruptions feel smooth and natural."
- **S3, 05:06 to 05:10.** "The first thing to notice is that animatable attributes conceptually have both model and presentation values."
- **S3, 19:21 to 19:28.** "Spring animations override shouldMerge to return true and incorporate the state of the previous animation. This allows them to preserve velocity and retarget to the new value,"
- **S4, 17:03 to 17:07.** "And even when structure shifts, behavior fills the gap. Components should always support the same set of core interactions."
- **S5, 03:38 to 03:41.** "To this effect, Liquid Glass responds to interaction by instantly flexing and energizing with light."
- **S5, 18:35 to 18:38.** "and Reduced Motion decreases the intensity of some effects and disables any elastic properties for the material."
- **S6, 19:31 to 19:38.** "Glass reacts to user interaction by scaling, bouncing, and shimmering, matching the effect provided by toolbar buttons and sliders."
- **S6, 20:15 to 20:29.** "However, glass can not sample other glass, so having nearby glass elements in different containers will result in inconsistent behavior. Using a glass container allows these elements to share their sampling region, providing a consistent visual result."
- **S7, 18:07 to 18:12.** "And with sliders, in addition to the liquid glass effects on the thumb, they now preserve momentum and stretch when they are moved."
- **S7, 24:12 to 24:15.** "Only if they get closer, they start merging like small droplets of water."
- **S7, 24:34 to 24:40.** "To split glass into multiple elements, first, add them to the same position without animation. Then, animate them out together!"
- **S8, Combine multiple views with Liquid Glass containers.** "The larger the spacing value on the container, the sooner the Liquid Glass effects behind views blend together and merge the shapes during a transition."
- **S8, Morph Liquid Glass effects during transitions.** "Associate each Liquid Glass effect with a unique identifier within a namespace that the Namespace property wrapper provides."
- **S9, Overview.** "As shapes near one another, their paths start to blend into one another. The higher the spacing, the sooner blending begins as the shapes approach each other."
- **S10, Discussion.** "When mixed with other `spring()` or `interactiveSpring()` animations on the same property, each animation will be replaced by their successor, preserving velocity from one animation to the next."

## Evidence limits and unresolved details

All ten substantive sources were retrieved on 2026-11-09 UTC. Session year and session identity come from Apple's published pages. The API documents are current snapshots retrieved after iOS 26's introduction. They can contain later additions or wording updates. This research does not establish that every statement in the current custom glass article was present during WWDC25.

No video frames, simulator, device, browser, or live native control were inspected. Demonstration geometry, deformation amplitude, snap timings, reduced motion rendering, and actual interaction fidelity remain unverified. The recorded timecodes locate Apple's explanations; they are not measurements of animation duration.

The source code snippets are published session examples. Some HTML stores literal newline escapes, and a conversion formula in S2's published code text warrants checking against the rendered slide before using it as mathematical authority. The raw text is retained without silently correcting it. The synthesis relies on the documented continuity and parameter concepts, not that formula.

The evidence does not establish:

- The precise mapping from raw drag displacement, speed, or excess displacement to native slider stretch.
- Whether an iOS 26 slider's specific deformation is generated by a spring, a geometry field, a shader, several coordinated models, or another private mechanism.
- Native slider stiffness, damping, mass, settling tolerance, snap thresholds, stretch cap, or filtering window.
- A global pressure dependency for Liquid Glass interactions.
- Native control semantic values temporarily exceeding their configured range because their appearance stretches.
- A fluid solver, surface tension equation, volume preservation rule, metaball field, signed distance field, or exact connection path inside Liquid Glass.
- The proprietary shader, background sampling kernel, blur radius, refraction index, highlight equation, or adaptive contrast thresholds.
- A general guarantee that every Liquid Glass topology change preserves every derivative of its geometry. The explicit velocity guarantees concern spring animation state.
- One exact portable algorithm that will reproduce Apple's output on every platform.

The reliable reusable content is the observable interaction contract and the public relationships between input, motion state, semantic constraints, grouping, and identity. Native implementation details should remain named gaps, and portable decisions should remain labeled reconstructions.
