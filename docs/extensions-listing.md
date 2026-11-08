# extensions.blender.org listing

Everything the upload form asks for, in the order it asks.

| Field | Value |
|---|---|
| File | `addon_dev_reloader-1.1.0.zip` (GitHub release v1.1.0) |
| Name, tagline, version, tags, license, Blender min | read from `blender_manifest.toml` |
| Icon (256 x 256 PNG) | `media/icon.png` |
| Featured image (1920 x 1080) | `media/featured.png` |
| Preview images (1920 x 1080), in this order | `media/01_pick_from_top_bar.png`, `media/02_edit_then_reload.png`, `media/03_reloaded.png` |
| Website | https://github.com/N4m-N4m/addon_dev_reloader |
| Report issues | https://github.com/N4m-N4m/addon_dev_reloader/issues |

## Release notes (1.1.0)

First release as a Blender extension. Requires Blender 4.2 or newer.

- One-click reload of the add-on you're developing, from the top bar next to Scene and View Layer.
- Click the picker and type to find the add-on among everything that's enabled.
- The add-on's `unregister()` runs first, then it and all of its submodules are dropped from Python's module cache, so every file is read from disk again.
- The status bar confirms each reload and says how many modules were reloaded. If the add-on fails to import, it shows the error instead.
- The chosen add-on is remembered by module name, so enabling or disabling other add-ons doesn't change it.
- Works with both extensions and legacy add-ons.

## Preview captions

1. Pick the add-on you're working on from the top bar. Click the field and type to filter.
2. Edit and save your code. Hovering Reload names the add-on it will reload.
3. One click: the add-on is reloaded from disk and the new UI is there. No restart.

## Description (paste as Markdown)

Developing an add-on usually means restarting Blender, or disabling and enabling it in Preferences, every time you change the code. And even then Python keeps the old submodules cached, so edits to `utils.py` or `ui/panels.py` don't show up.

**Addon Dev Reloader puts a one-click reload in the top bar.**

1. Pick the add-on you're working on from the picker at the right end of the top bar, next to Scene and View Layer.
2. Edit its code and save.
3. Click **Reload**. The status bar confirms it and says how many modules were reloaded.

### What it does on reload

- Runs the add-on's own `unregister()`, so panels, operators and properties don't pile up.
- Removes the add-on **and all of its submodules** from Python's module cache, so every file is read from disk again.
- Enables the add-on again and redraws every editor, so new panels appear at once.

### Details

- Works in every workspace: the controls live in the top bar.
- Click the picker and start typing to filter the list of enabled add-ons.
- The chosen add-on is remembered by its module name, so enabling or disabling other add-ons never changes the target.
- Works for both extensions and legacy add-ons.
- If the add-on fails to import, the error is shown and you can fix it and reload again.

### Limitations

- Only enabled add-ons are listed.
- Anything an add-on leaves behind outside its own modules (a handler it doesn't remove in `unregister()`, for example) survives the reload.

Source and issues: https://github.com/N4m-N4m/addon_dev_reloader
