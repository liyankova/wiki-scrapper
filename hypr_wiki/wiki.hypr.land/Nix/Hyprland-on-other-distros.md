---
source_url: "https://wiki.hypr.land/Nix/Hyprland-on-other-distros/"
title: "Hyprland on Other Distros – Hyprland Wiki"
crawl_date: "2025-11-16T07:59:43.885509Z"
selector: ".content"
---

# Hyprland on Other Distros – Hyprland Wiki

# Hyprland on Other Distros

If you use Nix on distros other than NixOS, you can still use Hyprland.  
The best option would be through [Home Manager](../Hyprland-on-Home-Manager).

However, if Home Manager is not for you, Hyprland can be installed as a normal
package.  
First, [enable flakes](https://nixos.wiki/wiki/Flakes#Enable_flakes), then, once you
have flakes working, install Hyprland through `nix profile`:

From NixpkgsFrom the Flake

The easiest method is to get Hyprland directly from Nixpkgs:

```
nix profile install nixpkgs#hyprland
```

Note

Make sure to enable [Cachix](../Cachix) first.

```
nix profile install github:hyprwm/Hyprland
```

Since you’re using Hyprland outside of NixOS, it won’t be able to find graphics
drivers.  
To get around that, you can use
[nixGL](https://github.com/guibou/nixGL).

First, install it:

```
nix profile install github:guibou/nixGL --impure
```

`--impure` is needed due to `nixGL`’s reliance on hardware information.

From now on, you can run Hyprland by invoking it with nixGL.

```
nixGL Hyprland
```

Or by creating a wrapper script that runs the above command inside.

## Upgrading

In order to upgrade all your packages, you can run:

```
nix profile upgrade '.*'
```

Check the
[nix profile](https://nixos.org/manual/nix/stable/command-ref/new-cli/nix3-profile.html)
command documentation for other upgrade options.