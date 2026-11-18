# Timer 4 Kids downloadable scenes

Public delivery repository: https://github.com/andregiannini/timer-4-kids-scenes

Only approved scene packs, the public catalog, and publishing documentation belong
in that repository. App code, draft artwork, signing files, and credentials stay out.

The app reads `releases/download/catalog/catalog.json`, then fetches the immutable
release named `<scene-id>-r<revision>`. Each release contains `scene.json` and its
PNG/JPEG images. SHA-256 hashes and byte counts are verified before a scene appears.

## Publishing an approved scene

1. Design and approve the scene first. Export its layers and icon as PNG/JPEG.
2. Create `scene.json` using schema version 1. All positions and sizes are fractions
   of the declared canvas. Keep essential action above the timer controls.
3. Run the private app project's `scripts/package-scene.py SCENE --out NEW_OUTPUT`.
   This fills hashes and byte sizes and prints the catalog entry.
4. Validate the manifest with the app's scene-pack tests, and preview locally at 0%,
   50%, 100%, paused, and during the finale. Do not publish test fixtures.
5. Create release `<scene-id>-r<revision>` in this public repository and upload
   `scene.json` and exactly its referenced images. Do not overwrite published packs;
   make a higher revision for corrections.
6. Add or replace that scene's entry in `catalog.json`, retaining other scenes.
7. Update the existing `catalog` release's `catalog.json` asset **last**, after all
   scene assets are uploaded. Commit the matching catalog to this repository.

Example commands (run deliberately after reviewing the approved files):

```sh
gh release create christmas-r1 /path/to/pack/* --repo andregiannini/timer-4-kids-scenes --title 'Christmas revision 1' --notes 'Approved scene content'
gh release upload catalog catalog.json --clobber --repo andregiannini/timer-4-kids-scenes
```

## Format version 1

Required manifest fields:
- `schemaVersion`: 1
- `id`: lowercase letters, digits and hyphens; maximum 60 characters
- `revision`: positive integer
- `title`: scene picker name, maximum 40 characters
- `background`: six RGB hex digits, without `#`
- `icon`: a filename from `assets`
- `canvasWidth`, `canvasHeight`: reference canvas size, each at most 4096
- `assets`: `{file, sha256, bytes}` records; PNG/JPEG, maximum 20 MB per file,
  80 files and 80 MB per pack
- `layers`: back-to-front `{asset, center:{x,y}, width, height, opacity}` records
- `lights`: `{points:[{x,y},...], color, width, bulbRadius, bulbCount}` records;
  illumination follows the timer's fraction by distance along the path
- `events`: `{asset, trigger, duration, from:{x,y}, to:{x,y}, width, height}`;
  trigger is a timer fraction, duration is seconds; movement pauses with the timer
- `finale`: layers displayed only after completion, fading in over half a second
- `finaleDuration`: seconds before the common Time's Up/menu button appears, 0–15

Optional layer fields: `revealFrom`, `revealUntil` (bottom-up reveal between timer
fractions), `glow` (0–40), `twinkle` (boolean). Finale layers use those same fields.
The app's existing completion sound is shared by all scenes. Version 1 does not
execute downloaded scripts and does not support custom audio files.

Christmas can use a snowy background/tree layer, a winding light path, a Santa
sprite event at 0.5, and star/full-tree glow layers in the finale. This describes
capabilities, not an approved Christmas design.

## Seasonal menu ordering

The catalog optionally includes a top-level `promotions` array, alongside `scenes`.
It schedules ordering only; it never changes the selected scene or removes a scene.

```json
{
  "schemaVersion": 1,
  "scenes": [],
  "promotions": [
    {"sceneID": "builtin:hauntedHill", "annualMonth": 10, "annualDay": 31},
    {"sceneID": "download:christmas", "annualMonth": 12, "annualDay": 25},
    {"sceneID": "download:new-year", "annualMonth": 1, "annualDay": 1},
    {"sceneID": "download:spring", "dates": ["2027-04-04", "2028-04-16"]}
  ]
}
```

These are format examples, not a list of released packs. Only installed scenes
appear. The `spring` dates are illustrative explicit dates, not calculated holidays.
Use `builtin:<stored identifier>` for bundled scenes and `download:<pack id>` for
packs. Fixed holidays use month/day recurrence. Movable holidays use explicit
Gregorian `YYYY-MM-DD` dates; update future dates in this catalog without an app
update. Use either annual fields or `dates`, never both.

Promotion begins 30 local calendar days before the holiday and lasts through the
entire third local day afterward. The fourth day restores normal ordering. Among
active holidays, the closest occurrence comes first; ties retain normal order.
Then come unplayed new packs, then the normal stable scene order. A new seasonal
pack shows `New`; an already-played seasonal scene shows `Seasonal` instead.

Haunted Hill has a bundled October 31 schedule. A remote schedule for that same ID
overrides it; `{"sceneID":"builtin:hauntedHill","dates":[]}` disables its promotion.
Schedules are saved for offline use. If `promotions` is absent, existing saved
schedules remain; old catalog files continue to work. Bad or duplicate schedules
are rejected rather than replacing the last good saved schedule.

## Delivery behavior

The app checks on launch, at most every six hours per process, and parents can
check manually. It exposes only complete validated packs, keeps downloads in
Application Support for offline use, and pins artwork when starting a timer.
New badges disappear after the scene is started. Failed downloads never block
built-in timers. Removing a catalog entry stops new downloads; it does not delete
an existing user's saved pack. Keep already-published assets available.

No analytics or identifying query parameters are added. GitHub necessarily receives
ordinary network connection information, such as IP address, when serving files.
