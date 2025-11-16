---
source_url: "https://wiki.hypr.land/Configuring/Tearing/"
title: "Tearing – Hyprland Wiki"
crawl_date: "2025-11-16T07:57:31.917805Z"
selector: ".content"
---

# Tearing – Hyprland Wiki

# Tearing

Screen tearing is used to reduce latency and/or jitter in games.

## Enabling tearing

To enable tearing:

* Set `general:allow_tearing` to `true`. This is a “master toggle”
* Add an `immediate` windowrule to your game of choice. This makes sure that
  Hyprland will tear it.

Warning

Please note that tearing will only be in effect when the game is in fullscreen
and the only thing visible on the screen.

Example snippet:

```
general {
    allow_tearing = true
}

windowrule = immediate, class:^(cs2)$
```

Warning

If you experience graphical issues, you may be out of luck. Tearing support is
experimental.  
See the likely culprits below.

## Common issues

### No tearing at all

Make sure your window rules are matching and you have the master toggle enabled.

Also make sure nothing except for your game is showing on your monitor. No
notifications, overlays, lockscreens, bars, other windows, etc. (on a different
monitor is fine)

### Apps that should tear, freeze

Almost definitely means your GPU driver does not support tearing.

Please *do not* report issues if this is the culprit.

### Graphical artifacts (random colorful pixels, etc)

Likely issue with your graphics driver.

Please *do not* report issues if this is the culprit. Unfortunately, it’s most
likely your GPU driver’s fault.