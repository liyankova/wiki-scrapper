---
source_url: "https://wiki.hypr.land/Nix/Options-Overrides/"
title: "Options & Overrides – Hyprland Wiki"
crawl_date: "2025-11-16T07:59:46.005259Z"
selector: ".content"
---

# Options & Overrides – Hyprland Wiki

# Options & Overrides

You can override the package through the `.override` or `.overrideAttrs`
mechanisms.  
This is easily achievable on [NixOS](../Hyprland-on-NixOS) or
[Home Manager](../Hyprland-on-Home-Manager).

## Package options

These are the default options that the Hyprland package is built with.  
These can be changed by setting the appropriate option to `true` or `false`.

### Package

```
(pkgs.hyprland.override { # or inputs.hyprland.packages.${pkgs.stdenv.hostPlatform.system}.hyprland
  enableXWayland = true;  # whether to enable XWayland
  withSystemd = true;     # whether to build with systemd support
})
```

### NixOS & HM modules

```
{
  programs.hyprland = { # or wayland.windowManager.hyprland
    enable = true;
    xwayland.enable = true;
  };
}
```

## Options descriptions

### XWayland

XWayland is enabled by default in the Nix package.  
You can disable it either in the package itself, or through the module options.

## Using Nix repl

If you’re using Nix (and not NixOS or Home Manager) and you want to override,
you can do it like this:

```
$ nix repl
nix-repl> :lf github:hyprwm/Hyprland
nix-repl> :bl outputs.packages.x86_64-linux.hyprland.override { /* flag here */ }
```

Then you can run Hyprland from the built path.  
You can also use `overrideAttrs` to override `mkDerivation`’s arguments, such as
`mesonBuildType`:

```
$ nix repl
nix-repl> :lf github:hyprwm/Hyprland
nix-repl> :bl outputs.packages.x86_64-linux.hyprland.overrideAttrs (self: super: { mesonBuildType = "debug" })
```