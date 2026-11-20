# Remote update notices — build 14 and later

The approved optional/required screens are in `design/app-updates/approved-design.png`.
Current live policy is **off**. No update is required or announced by shipping this feature.
Build 13 and older cannot display these notices: they do not contain this feature.

The app reads this public asset on foreground/menu entry, at most every five minutes
per process, using the same bounded, anonymous GitHub transport as scene downloads:

`https://github.com/andregiannini/timer-4-kids-scenes/releases/download/catalog/updates.json`

Choose importance per release. Version numbers identify who needs that release;
they do not automatically classify a release as important. Prices, purchases, paid
scene locks, and entitlements are separate features and are not implemented here.

## One active notice

```json
{
  "schemaVersion": 1,
  "mode": "optional",
  "campaignID": "layout-refresh",
  "targetVersion": "1.2",
  "title": "A fresh update is here",
  "message": "We’ve made Timer 4 Kids even better.",
  "detail": "Update whenever it suits you.",
  "expiresAt": "2026-12-20T12:00:00Z"
}
```

- `mode`: `optional`, `required`, or `off`. Change it deliberately per release.
- `campaignID`: stable identifier for that announcement. Keep it when changing importance.
- `targetVersion`: users below this public app version are affected. Optional
  `targetBuild` also targets lower builds of that same version (mostly useful in testing).
- `title`, `message`, `detail`: optional custom copy; the approved copy is the default.
- `expiresAt`: required UTC ISO8601 expiration for active notices. Use an appropriate
  future date and renew only while the notice is still needed. Expiration prevents
  a stale cached requirement from blocking an offline app indefinitely.

Only enable a notice after its target update is approved and available to all affected
users in their App Store regions and supported iOS versions. The link is fixed to this
app's App Store page and cannot be changed by downloaded JSON. A TestFlight-only build
is not an App Store update; do not activate a requirement pointing users to it.

## Several releases with different importance

Keep an older critical fix alongside a newer optional layout change:

```json
{
  "schemaVersion": 1,
  "campaigns": [
    {"schemaVersion":1,"mode":"required","campaignID":"critical-fix","targetVersion":"1.2","expiresAt":"2026-12-20T12:00:00Z"},
    {"schemaVersion":1,"mode":"optional","campaignID":"layout-refresh","targetVersion":"1.3","expiresAt":"2026-12-20T12:00:00Z"}
  ]
}
```

Affected users see a required notice first. Users already past that fix see the
newest applicable optional notice. Older optional notices do not resurface after
snoozing the newest one. Up to 20 distinct campaigns are accepted.

## User behavior

- Notices are shown only on the menu; a running or paused timer is never interrupted.
- Optional **Later** snoozes that campaign/target for seven days across app restarts.
  Successfully opening the App Store also snoozes an optional notice.
- Required has no dismiss/skip action. Returning from the parent gate returns to
  the update screen, never the timer menu. Snoozes cannot suppress required notices.
- The existing parent gate is required before the app opens the App Store.
- Invalid/offline responses cannot create a requirement. The last valid cached
  notice remains until updated or expired. A successful `off` response withdraws it.
- Fresh installs and users who have installed the target version see no notice.
- No new analytics, account, cookies, or device identifiers are added.

## Publishing

Edit and review `SceneContent/updates.json`. Copy it to the public content checkout
as `updates.json`, commit/push it there, then replace the catalog release asset:

```
gh release upload catalog /path/to/public-content/updates.json --clobber --repo andregiannini/timer-4-kids-scenes
```

Fetch the public URL without authentication afterward and verify the exact policy.
Emergency withdrawal: publish `{"schemaVersion":1,"mode":"off"}`. Connected apps
pick that up on their next eligible foreground/menu check; offline cached notices
cannot be recalled until a connection succeeds or their expiration is reached.
