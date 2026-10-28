# Stage C2 geometry coverage research

The operator approved **100 sourced geometry checks selected for coverage, with popularity unverified**. This packet must not be described as a popularity-ranked top 100.

Records identify exact existing cohort IDs. A source for one model is never propagated to the rest of its family. Aliases removed by C2 are excluded from the final selected cohort. The geometry facts are static visual candidates, not build-property evidence or runtime promotion; human review remains pending.

## Accepted evidence methods

- Explicit camera-cutout geometry in a first-hand technical review (GSMArena or equivalent).
- Exact-model manufacturer hardware / keys-and-parts drawing, visually inspected in a browser. The camera must actually be shown inside the screen at the stated location; a camera in the bezel means `none` / `none`.
- Manufacturer/operator product drawings, with the visual inference explicitly labeled.

Drawings support the coarse cutout type and location only. They do not establish exact pixel dimensions or device runtime identity. Foldable Google models were excluded because a single notch field cannot safely conflate the inner and cover displays.

## Popularity investigation

Counterpoint's public 2025 report supports a limited global top-ten sales list, not a complete top-100 ranking for this Android cohort. GSMArena's public home page exposes ten daily-interest models; the individual Galaxy S25 Ultra page exposes hits, but one device's hits cannot establish a cohort ranking.

The public GSMArena phone-finder form was read successfully. It defines `nOrder=0` as Popularity (`1` is Price, `2` is Weight), and `idDisplayNotch=1` as No, `2` as Yes, `3` as Punch hole. Result pages state that only 70 devices are shown. Direct filtered requests returned HTTP 200 Turnstile checks, not result content. **No models or notch facts were accepted from those challenge pages.** Automated extraction stopped when the challenge was identified; no CAPTCHA bypass was attempted.

Smartprix's generic "no notch" filter was rejected as a source of `none`: it includes known punch-hole Asus models. Individual first-hand reviews with explicit geometry remain usable.

Sources investigated:

- https://counterpointresearch.com/en/insights/iphone-16-worlds-best-selling-smartphone-in-2025-apple-takes-7-spots-in-top-10-models
- https://www.gsmarena.com/
- https://www.gsmarena.com/search.php3
- https://www.gsmarena.com/results.php3?nOrder=2
- https://www.gsmarena.com/samsung_galaxy_s25_ultra-13322.php
- https://support.google.com/pixelphone/answer/7157629?hl=en
- https://www.smartprix.com/mobiles/asus-brand/with-no_notch

Zero paid services, MobileAPI calls, or cloud resources were used for this research.

## Final packet

`notch-candidates.json` contains exactly 100 retained IDs with both notch type and position supported, plus seven additional candidates (including type-only records). Every rank remains null. Selected records cover 11 brands: 39 Nokia, 19 Google, 11 OnePlus, 13 Sony, 5 Asus, 5 Samsung, 3 Nothing, 2 Motorola, and one each from Realme, Vivo, and Xiaomi. This is a sourced geometry coverage sample, not a brand-balanced sample or a sales ranking.

The HMD checks used the **front product render**, not just the schematic camera marker: 41 correct-model pages yielded interpretable renders. Two redirects to the generic HMD support page were rejected even though a product image was present. Missing / redirected pages were not treated as evidence. `notch-hmd-observations.json` preserves the exact source title, resolved URL, image URL, and diagram URL for replay. Manufacturer render screenshots were inspected locally; OEM artwork was not added to the simulator or committed.

Camera shapes connected to the screen's upper edge are mapped to the schema's coarse `teardrop` category; isolated round cutouts map to `punch_hole`; camera hardware entirely outside the display maps to `none`. No center position was inferred merely from the word "notch". Six type-only sources remain outside the selected 100 because a location was not independently established.

All 100 selected records remain human-review pending. Geometry sourcing does not certify every other specification in the corresponding profile or promote any runtime profile.

A later carrier-family collapse retires Nokia8V into8.3. The independently sourced NokiaXR20 replaces it in the selected100; no geometry was transferred between those models.
