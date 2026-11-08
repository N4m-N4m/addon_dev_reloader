# Addon Dev Reloader

Hot-reload the Blender add-on you're developing, without restarting Blender.

Pick an add-on from the picker in the top bar (right of Scene / View Layer), edit its code, click **Reload**. The add-on is disabled, every one of its modules is dropped from Python's module cache, and it's enabled again, so the next import reads your changes from disk.

## Features

- **One click from anywhere.** The picker and reload button sit at the right end of the top bar, so they're there in every workspace.
- **Search as you type.** Click the picker and start typing; the list of enabled add-ons filters live and Enter picks the best match.
- **Full reload, not just the top module.** All submodules of the add-on are purged from `sys.modules`, so changes in `utils.py` or `ui/panels.py` are picked up too.
- **Clean unregister.** The add-on's own `unregister()` runs before the reload, so panels, operators and properties don't pile up.
- **Stable target.** The chosen add-on is stored by module name, so enabling or disabling other add-ons never shifts it to a neighbour.
- Works with both extensions (`bl_ext.*`) and legacy add-ons.

## Install

Requires Blender 4.2 or newer.

1. Download `addon_dev_reloader-<version>.zip` from the [Releases](https://github.com/N4m-N4m/addon_dev_reloader/releases) page.
2. In Blender, open **Edit > Preferences > Get Extensions**, click the **⌄** menu in the top right and choose **Install from Disk...**, then pick the zip.
   (Or drag the zip into the Blender window.)

## Usage

1. Click the **⌄** button at the right end of the top bar and choose the add-on you're working on.
2. Edit its code and save.
3. Click the **⟳** button next to it. The status bar reports the reload and how many modules were purged.

Hovering the reload button shows which add-on it will reload. If the add-on fails to import, the error is shown in the status bar and the add-on stays disabled until you fix it and reload again.

### Limitations

- Only enabled add-ons are listed; reloading a disabled one would just enable it.
- Anything an add-on stores outside its own modules (handlers it forgot to remove in `unregister()`, data on `bpy.types` it never deletes) survives the reload. That's a bug in the reloaded add-on worth fixing anyway.

## Building from source

```sh
blender --command extension build --source-dir . --output-dir dist
```

## License

[GPL-3.0-or-later](LICENSE)
