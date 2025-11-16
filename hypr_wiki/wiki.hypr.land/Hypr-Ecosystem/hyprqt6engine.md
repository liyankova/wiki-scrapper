---
source_url: "https://wiki.hypr.land/Hypr-Ecosystem/hyprqt6engine"
title: "hyprqt6engine – Hyprland Wiki"
crawl_date: "2025-11-16T08:00:40.731069Z"
selector: ".content"
---

# hyprqt6engine – Hyprland Wiki

# hyprqt6engine

hyprqt6engine provides a theme for QT6 apps. It’s a replacement for qt6ct, compatible with KDE Apps / KColorScheme.

## Usage

Install, then set `QT_QPA_PLATFORMTHEME=hyprqt6engine`. You can set this as `env=` in Hyprland, or in `/etc/environment` for setting it system-wide.

## Configuration

The config file is located in `~/.config/hypr/hyprqt6engine.conf`.

### Theme

category `theme:`

| variable | description | type | default |
| --- | --- | --- | --- |
| color\_scheme | the full path to a color scheme. Can be a qt6ct theme, or a KColorScheme. Empty for defaults. | string | empty |
| icon\_theme | name of an icon theme to use | string | empty |
| style | widget style to use, e.g. Fusion or kvantum-dark. | string | Fusion |
| font\_fixed | font family for the fixed width font | string | monospace |
| font\_fixed\_size | font size for the fixed width font | int | 11 |
| font | font family for the regular font | string | Sans Serif |
| font\_size | font size for the regular font | int | 11 |

### Misc

category `misc:`

| variable | description | type | default |
| --- | --- | --- | --- |
| single\_click\_activate | whether single-clicks should activate, or open | bool | true |
| menus\_have\_icons | whether context menus should include icons | bool | true |
| shortcuts\_for\_context\_menus | whether context menu options should show their keyboard shortcuts | bool | true |