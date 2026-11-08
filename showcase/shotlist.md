# Shot list

One sentence: a top-bar button that hot-reloads the add-on you're developing, without restarting Blender.

- **01 Pick from the top bar** (2x UI scale crop, picker open): which add-on Reload acts on.
- **02 Edit, then reload** (full window, tooltip on Reload): code changed on disk, panel still old.
- **03 Reloaded** (full window): new panel rows, the Info log and status bar report the reload.
- **featured**: name + one line, close-up of 01.
- **icon**: reload arrow around a plug-in block.

Demo add-on: `demo/v1.py` -> `demo/v2.py` ("Quick Scatter", fictional).
Re-shoot: set `ADR_WORK` (work folder) and `ADR_HARNESS_DIR` (folder with bl_ui_harness.py), run `scene.py` in Blender 5.2 with `--factory-startup --enable-event-simulate`,
`BLENDER_USER_RESOURCES=<work>/res` (with `res/scripts/addons/quick_scatter/__init__.py` = v1),
`ADR_PHASE=story` at 1600x900 and `ADR_PHASE=picker ADR_SCALE=2.0` at 1920x1080, then `compose.py <work>`.
