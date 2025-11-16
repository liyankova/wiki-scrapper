---
source_url: "https://wiki.hypr.land/Hypr-Ecosystem/hyprlauncher"
title: "hyprlauncher – Hyprland Wiki"
crawl_date: "2025-11-16T08:00:19.964619Z"
selector: ".content"
---

# hyprlauncher – Hyprland Wiki

# hyprlauncher

Hyprlauncher is a multipurpose and versatile launcher / picker for hyprland. It’s fast, simple, and provides
various modules.

## Usage

Hyprlauncher is *always* a daemon. Launching it spawns a daemon that will listen to
requests. If launched with `hyprlauncher -d`, it will not open a window for the first launch.

To open hyprlauncher, just bind `hyprlauncher` to a key.

## Configuration

### Theming

Theme follows your [hyprtoolkit](../hyprtoolkit) theme.

### Config

`~/.config/hypr/hyprlauncher.conf`

Config categories and their values:

#### General

| option | description | type | default |
| --- | --- | --- | --- |
| grab\_focus | whether to force a full keyboard focus grab | bool | true |

#### Cache

| option | description | type | default |
| --- | --- | --- | --- |
| enabled | controls whether modules keep a cache of often used entries. That history is stored on your disk, in plain text, in `~/.local/share/hyprlauncher`. | bool | true |

#### Finders

Available finders: `math`, `desktop`, `unicode`.

Prefixes can only be one character.

| option | description | type | default |
| --- | --- | --- | --- |
| default\_finder | controls the default finder used | string | desktop |
| desktop\_prefix | prefix for the desktop finder to be used | string | empty |
| unicode\_prefix | prefix for the unicode finder to be used | string | . |
| math\_prefix | prefix for the math finder to be used | string | = |
| desktop\_launch\_prefix | launch prefix for each desktop app, e.g. `uwsm app --` | string | empty |
| desktop\_icons | whether to enable desktop icons in the results | bool | true |