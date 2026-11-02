# Stage F — interactive HTML chrome

Implemented mock status controls, editable time, keyboard/text input, portrait/landscape rotation and dark mode. Each existing simulator URL exposes **Enable interactive chrome**; static catalog cards retain their original appearance. All20brand shells reuse one shared JS/CSS implementation. Device draft/review labels and runtime eligibility remain separate from this mock interaction mode.

The current engineering checkout renders1022URLs:22reference profiles plus1000generated drafts. Interactive controls are available on each via the shared shell. This is a count of rendered artifacts, not a new claim about verified distinct devices: accepted C2/C2.1data integration remains a separate branch. No device was invented or duplicated for StageF and no generation eligibility flag was changed.

## Behavior

- Status panel shows explicitly simulated Wi-Fi/battery and no cellular service. Time is operator-editable; it is not a live connection to Android.
- Mock QWERTY keyboard edits a local text field, including space/backspace/done. Ordinary physical typing works; Escape hides the keyboard. Native buttons and labeled fields support keyboard focus.
- Rotation swaps the screen aspect ratio and retains entered text. Dark mode applies to the original mock UI; it is not the OEM OS.
- Disabling interaction restores the original illustration/status and accessibility role. Unknown hardware cutouts remain unknown; UI interaction does not infer their geometry.

A rotation/focus issue that could scroll the clipped screen and hide its status bar was corrected with non-scrolling clipping and an independently scrollable controls panel. A browser regression checks that the screen's scroll offset remains0.

## Verification

All26local browser tests passed, including7new interaction tests. Five sample profiles cover vivo, Samsung, Google, Huawei and Tecno; a separate traversal confirms controls for all20brands, and a mobile test checks typing, Escape, rotation and page overflow. Existing catalog/generated-page checks and frame/art snapshots also passed. Screenshots were visually inspected: `docs/proof/stage-f-keyboard.png` and five `stage-f-{profile}.png` pages.

A separate local warm-server traversal measured navigation-to-controls-ready for20brands; the maximum was **70ms**, below the5second target. This measures HTML control readiness, not Android/app time-to-interactive or a production/network performance guarantee. Raw per-brand timings are stored in ignored local evidence, `data/runtime/local/stage-f/readiness.json`.

No APKs, runtime containers, cloud services or paid APIs are invoked by the UI. No manufacturer logos/screenshots/wallpapers were added. Real Android still runs separately in the UTM VM.
