---
source_url: "https://wiki.hypr.land/Configuring/Monitors/"
title: "Monitors – Hyprland Wiki"
crawl_date: "2025-11-16T07:57:14.043898Z"
selector: ".content"
---

# Monitors – Hyprland Wiki

# Monitors

## General

The general config of a monitor looks like this:

```
monitor = name, resolution, position, scale
```

A common example:

```
monitor = DP-1, 1920x1080@144, 0x0, 1
```

This will make the monitor on `DP-1` a `1920x1080` display, at
144Hz, `0x0` off from the top left corner, with a scale of 1 (unscaled).

To list all available monitors (active and inactive):

```
hyprctl monitors all
```

Monitors are positioned on a virtual “layout”. The `position` is the position,
in pixels, of said display in the layout. (calculated from the top-left corner)

For example:

```
monitor = DP-1, 1920x1080, 0x0, 1
monitor = DP-2, 1920x1080, 1920x0, 1
```

will tell Hyprland to put DP-1 on the *left* of DP-2, while

```
monitor = DP-1, 1920x1080, 1920x0, 1
monitor = DP-2, 1920x1080, 0x0, 1
```

will tell Hyprland to put DP-1 on the *right*.

The `position` may contain *negative* values, so the above example could also be
written as

```
monitor = DP-1, 1920x1080, 0x0, 1
monitor = DP-2, 1920x1080, -1920x0, 1
```

Hyprland uses an inverse Y cartesian system. Thus, a negative y coordinate
places a monitor higher, and a positive y coordinate will place it lower.

For example:

```
monitor = DP-1, 1920x1080, 0x0, 1
monitor = DP-2, 1920x1080, 0x-1080, 1
```

will tell Hyprland to put DP-2 *above* DP-1, while

```
monitor = DP-1, 1920x1080, 0x0, 1
monitor = DP-2, 1920x1080, 0x1080, 1
```

will tell Hyprland to put DP-2 *below*.

Note

The position is calculated with the scaled (and transformed) resolution, meaning
if you want your 4K monitor with scale 2 to the left of your 1080p one, you’d
use the position `1920x0` for the second screen (3840 / 2). If the monitor is
also rotated 90 degrees (vertical), you’d use `1080x0`.

Warning

No monitors can overlap. This means that if your set positions make any monitors
overlap, you will get a warning.

Leaving the name empty will define a fallback rule to use when no other rules
match.

There are a few special values for the resolutions:

* `preferred` - use the display’s preferred size and refresh rate.
* `highres` - use the highest supported resolution.
* `highrr` - use the highest supported refresh rate.
* `maxwidth` - use the widest supported resolution.

Position also has a few special values:

* `auto` - let Hyprland decide on a position. By default, it places each new monitor to the right of existing ones,
  using the monitor’s top left corner as the root point.
* `auto-right/left/up/down` - place the monitor to the right/left, above or below other monitors,
  also based on each monitor’s top left corner as the root.
* `auto-center-right/left/up/down` - place the monitor to the right/left, above or below other monitors,
  but calculate placement from each monitor’s center rather than its top left corner.

***Please Note:*** While specifying a monitor direction for your first monitor is allowed, this does nothing and it will
be positioned at (0,0). Also, the direction is always from the center out, so you can specify `auto-up` then `auto-left`,
but the left monitors will just be left of the origin and above the origin. You can also specify duplicate directions and
monitors will continue to go in that direction.

You can also use `auto` as a scale to let Hyprland decide on a scale for you.
These depend on the PPI of the monitor.

Recommended rule for quickly plugging in random monitors:

```
monitor = , preferred, auto, 1
```

This will make any monitor that was not specified with an explicit rule
automatically placed on the right of the other(s), with its preferred
resolution.

For more specific rules, you can also use the output’s description (see
`hyprctl monitors` for more details). If the output of `hyprctl monitors` looks
like the following:

```
Monitor eDP-1 (ID 0):
        1920x1080@60.00100 at 0x0
        description: Chimei Innolux Corporation 0x150C (eDP-1)
        make: Chimei Innolux Corporation
        model: 0x150C
        [...]
```

then the `description` value up to, but not including the portname `(eDP-1)` can
be used to specify the monitor:

```
monitor = desc:Chimei Innolux Corporation 0x150C, preferred, auto, 1.5
```

Remember to remove the `(portname)`!

### Custom modelines

You can set up a custom modeline by changing the resolution field to a modeline,
for example:

```
monitor = DP-1, modeline 1071.101 3840 3848 3880 3920 2160 2263 2271 2277 +hsync -vsync, 0x0, 1
```

### Disabling a monitor

To disable a monitor, use

```
monitor = name, disable
```

Warning

Disabling a monitor will literally remove it from the layout, moving all windows
and workspaces to any remaining ones. If you want to disable your monitor in a
screensaver style (just turn off the monitor) use the `dpms`
[dispatcher](../Dispatchers).

## Custom reserved area

A reserved area is an area that remains unoccupied by tiled windows.
If your workflow requires a custom reserved area, you can add it with:

```
monitor = name, addreserved, TOP, BOTTOM, LEFT, RIGHT
```

Where `TOP` `BOTTOM` `LEFT` `RIGHT` are integers, i.e the number in pixels of
the reserved area to add. This does stack on top of the calculated reserved area
(e.g. bars), but you may only use one of these rules per monitor in the config.

## Extra args

You can combine extra arguments at the end of the monitor rule, examples:

```
monitor = eDP-1, 2880x1800@90, 0x0, 1, transform, 1, mirror, DP-2, bitdepth, 10
```

See below for more details about each argument.

### Mirrored displays

If you want to mirror a display, add a `, mirror, <NAME>` at the end of the
monitor rule, examples:

```
monitor = DP-3, 1920x1080@60, 0x0, 1, mirror, DP-2
monitor = , preferred, auto, 1, mirror, DP-1
```

Please remember that mirroring displays will not “re-render” everything for your
second monitor, so if mirroring a 1080p screen onto a 4K one, the resolution
will still be 1080p on the 4K display. This also means squishing and stretching
will occur on aspect ratios that differ (e.g 16:9 and 16:10).

### 10 bit support

If you want to enable 10 bit support for your display, add a `, bitdepth, 10` at
the end of the monitor rule, e.g:

```
monitor = eDP-1, 2880x1800@90, 0x0, 1, bitdepth, 10
```

Warning

Colors registered in Hyprland (e.g. the border color) do *not* support
10 bit.  
Some applications do *not* support screen capture with 10 bit enabled.

### Color management presets

Add a `, cm, X` to change default sRGB output preset

```
monitor = eDP-1, 2880x1800@90, 0x0, 1, bitdepth, 10, cm, wide
```

```
auto    - srgb for 8bpc, wide for 10bpc if supported (recommended)
srgb    - sRGB primaries (default)
dcip3   - DCI P3 primaries
dp3     - Apple P3 primaries
adobe   - Adobe RGB primaries
wide    - wide color gamut, BT2020 primaries
edid    - primaries from edid (known to be inaccurate)
hdr     - wide color gamut and HDR PQ transfer function (experimental)
hdredid - same as hdr with edid primaries (experimental)
```

Fullscreen HDR is possible without hdr `cm` setting if `render:cm_fs_passthrough` is enabled.

Use `sdrbrightness, B` and `sdrsaturation, S` to control SDR brightness and saturation in HDR mode. The default for both values is `1.0`. Typical brightness value should be in `1.0 ... 2.0` range.

```
monitor = eDP-1, 2880x1800@90, 0x0, 1, bitdepth, 10, cm, hdr, sdrbrightness, 1.2, sdrsaturation, 0.98
```

The default transfer function assumed to be in use on an SDR display for sRGB content is defined by `, sdr_eotf, X`. The default (`0`) is to follow `render:cm_sdr_eotf`. This can be changed to piecewise sRGB with `1`, or Gamma 2.2 with `2`.

### VRR

Per-display VRR can be done by adding `, vrr, X` where `X` is the mode from the
[variables page](../Variables).

## Rotating

If you want to rotate a monitor, add a `, transform, X` at the end of the monitor
rule, where `X` corresponds to a transform number, e.g.:

```
monitor = eDP-1, 2880x1800@90, 0x0, 1, transform, 1
```

Transform list:

```
0 -> normal (no transforms)
1 -> 90 degrees
2 -> 180 degrees
3 -> 270 degrees
4 -> flipped
5 -> flipped + 90 degrees
6 -> flipped + 180 degrees
7 -> flipped + 270 degrees
```

## Monitor v2

Alternative syntax. `monitor = DP-1,1920x1080@144,0x0,1,transform,2` is the same as

```
monitorv2 {
  output = DP-1
  mode = 1920x1080@144
  position = 0x0
  scale = 1
  transform = 2
}
```

The `disable` flag turns into `disabled = true`, but other named settings keep their names: `name, value` → `name = value` (e.g. `bitdepth,10` → `bitdepth = 10`)

EDID overrides and SDR → HDR settings:

| name | description | type |
| --- | --- | --- |
| supports\_wide\_color | Force wide color gamut support (1 - force on, 0 - does nothing) | bool |
| supports\_hdr | Force HDR support. Requires wide color gamut (1 - force on, 0 - does nothing) | bool |
| sdr\_min\_luminance | SDR minimum lumninace used for SDR → HDR mapping. Set to 0.005 for true black matching HDR black | float |
| sdr\_max\_luminance | SDR maximum luminance. Can be used to adjust overall SDR → HDR brightness. 80 - 400 is a reasonable range. The desired value is likely between 200 and 250 | int |
| min\_luminance | Monitor’s minimum luminance | float |
| max\_luminance | Monitor’s maximum possible luminance | int |
| max\_avg\_luminance | Monitor’s maximum luminance on average for a typical frame | int |

Note: those values might get passed to the monitor itself and cause increased burn-in or other damage if it’s firmware lacks some safety checks.

## Default workspace

See [Workspace Rules](../Workspace-Rules).

### Binding workspaces to a monitor

See [Workspace Rules](../Workspace-Rules).