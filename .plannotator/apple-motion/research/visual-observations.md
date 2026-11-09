# Primary-source visual observations

Inspected on 2026-11-09. These are frames from Apple's published WWDC25 session 284, not recordings of a control operated on this machine.

## Slider movement, 18:05 to 18:15

Source: https://developer.apple.com/videos/play/wwdc2025/284/?time=1085

The extracted clip shows a horizontal slider changing from a compact resting thumb to a wider glass thumb during interaction. Blue illumination surrounds the moving thumb. At the right end, the surrounding track and endpoint symbol also visibly shift before returning. The thumb returns to its compact resting shape.

This supports deformation during movement and an elastic return. These frames do not identify the finger's pressure, the deformation equation, the event threshold, the brightness control's exact behavior, or the values used by Apple's animation engine.

The five-column frame strip samples every 0.5 seconds. This cadence can show distinct shapes and positions but cannot establish frame-to-frame velocity continuity or small transient timing. The clip has its original frame rate and a ten-second duration.

Artifacts: `apple-slider-clip.mp4` and `apple-slider-frames.png` beside this note.

## Container merging and splitting, 24:05 to 24:41

Source: https://developer.apple.com/videos/play/wwdc2025/284/?time=1445

The extracted clip shows two glass shapes over one photograph. Changes in the container's spacing cause the shapes to connect at a larger separation. Overlapping frames become a common shape. The split demonstration creates two views at the same initial frame and moves them apart. This agrees with the published UIKit example and narration.

The four-column frame strip samples every 2.5 seconds. It shows before and after states and changing code. It is too sparse to characterize the narrow connection during breakup. No rupture distance, curvature profile, timing constant, or fluid force was measured.

Artifacts: `apple-merge-clip.mp4` and `apple-merge-frames.png` beside this note.

## Capture conditions

The remote SD MP4 was read with FFmpeg using source timestamps 1085 and 1445 seconds. Clips were encoded locally with H.264 and no audio. Frame strips scale each frame to 320 pixels wide. These media are research evidence in the isolated preview directory, not redistributed skill assets.

Remote media source: https://devstreaming-cdn.apple.com/videos/wwdc/2025/284/4/afb20876-65b2-4aeb-bd50-66e4df1b2281/downloads/wwdc2025-284_sd.mp4?dl=1

The new repository will cite the original session and carry this observation summary. It will not claim native-device verification, a pressure measurement, or exact Apple fidelity.
