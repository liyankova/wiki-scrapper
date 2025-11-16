---
source_url: "https://wiki.hypr.land/Hypr-Ecosystem/hyprtoolkit"
title: "hyprtoolkit – Hyprland Wiki"
crawl_date: "2025-11-16T08:00:43.137244Z"
selector: ".content"
---

# hyprtoolkit – Hyprland Wiki

# hyprtoolkit

Hyprtoolkit is a GUI toolkit for developing applications that run natively on Wayland.
It’s specifically made for Hyprland’s needs, but will generally run on any Wayland compositor
that supports modern standards.

For developer docs, see [development](./development)

## Configuration

The general toolkit config is at `~/.config/hypr/hyprtoolkit.conf`. It contains theming and some minor adjustments.

| variable | description | type | default |
| --- | --- | --- | --- |
| background | background color | color | FF181818 |
| base | base color | color | FF202020 |
| text | text color | color | FFDADADA |
| alternate\_base | alternative base color | color | FF272727 |
| bright\_text | bright text color | color | FFFFDEDE |
| accent | accent color | color | FF00FFCC |
| accent\_secondary | secondary accent color | color | FF0099F0 |
| h1\_size | font size for H1 | int | 19 |
| h2\_size | font size for H2 | int | 15 |
| h3\_size | font size for H3 | int | 13 |
| font\_size | font size for regular text elements | int | 11 |
| small\_font\_size | font size for small text elements | int | 10 |
| icon\_theme | name of the icon theme to use, empty for “the first found” | string | empty |
| font\_family | name of the font family to use | string | Sans Serif |
| font\_family\_monospace | name of the monospace font family to use | string | monospace |