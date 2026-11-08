# SPDX-License-Identifier: GPL-3.0-or-later

bl_info = {
    "name": "Addon Dev Reloader",
    "description": "Hot-reload an addon you're developing without restarting Blender.",
    "author": "dobesch",
    "version": (1, 1, 0),
    "blender": (4, 1, 0),
    "location": "Top Bar > right of Scene and View Layer",
    "warning": "",
    "category": "Development",
}

import bpy  # type: ignore
import sys
import addon_utils  # type: ignore


# Module name of this addon, so we can keep it out of the reload list
# (reloading the addon that is currently running mid-call is unsafe).
# Installed as an extension this is "bl_ext.<repo>.addon_dev_reloader", as a
# legacy add-on just "addon_dev_reloader"; either way it matches mod.__name__.
THIS_ADDON = __package__ or __name__

def enabled_addons():
    """(module_name, label) for every enabled addon except this one, sorted by label."""
    result = []
    for mod in addon_utils.modules():
        module_name = mod.__name__
        if module_name == THIS_ADDON:
            continue
        # Only enabled addons: reloading a disabled one would just enable it.
        is_enabled, _ = addon_utils.check(module_name)
        if not is_enabled:
            continue
        info = addon_utils.module_bl_info(mod)
        label = info.get("name", module_name) if info else module_name
        result.append((module_name, label))
    result.sort(key=lambda item: item[1].lower())
    return result


def addon_label(module_name):
    """Display name of an addon, or '' when it is not enabled any more."""
    for name, label in enabled_addons():
        if name == module_name:
            return label
    return ""


def purge_modules(module_name):
    """
    Remove the addon's package and all of its submodules from sys.modules so
    that re-enabling forces a fresh import from disk instead of reusing the
    cached (stale) bytecode.
    """
    prefix = module_name + "."
    stale = [name for name in sys.modules if name == module_name or name.startswith(prefix)]
    for name in stale:
        del sys.modules[name]
    return len(stale)


class DEV_OT_ReloadAddon(bpy.types.Operator):
    """Disable, purge the Python module cache for, and re-enable the chosen addon"""
    bl_idname = "dev.reload_addon"
    bl_label = "Reload Add-on"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        module_name = context.scene.dev_reload_module
        if not module_name:
            cls.poll_message_set("Pick an add-on to reload first")
            return False
        if not addon_label(module_name):
            cls.poll_message_set(f"'{module_name}' is not enabled")
            return False
        return True

    @classmethod
    def description(cls, context, properties):
        label = addon_label(context.scene.dev_reload_module)
        if label:
            return f"Reload {label} from disk"
        return "Reload the chosen add-on from disk"

    def execute(self, context):
        module_name = context.scene.dev_reload_module
        label = addon_label(module_name) or module_name

        try:
            # Disable runs the addon's unregister() before we purge so classes
            # are properly unregistered; then re-enable imports it fresh.
            addon_utils.disable(module_name, default_set=False)
            purged = purge_modules(module_name)
            addon_utils.enable(module_name, default_set=False)
        except Exception as exc:  # noqa: BLE001 - surface any reload failure to the user
            self.report({'ERROR'}, f"Failed to reload '{label}': {exc}")
            return {'CANCELLED'}

        # Redraw all areas so reloaded panels/operators appear immediately.
        for window in context.window_manager.windows:
            for area in window.screen.areas:
                area.tag_redraw()

        self.report({'INFO'}, f"Reloaded '{label}' ({purged} module(s) purged)")
        return {'FINISHED'}


# --- The picker ---------------------------------------------------------------
# A string property with a search callback: Blender draws it as a dark field with
# the same border as the Scene / View Layer selectors, and clicking it starts
# typing at once with a live-filtered list, best match highlighted, Enter picks.
# (Dark menu-type buttons always open their own popup first, and a search popup
# opened on top of that leaves it stuck open, eating the next click.)


def _picker_search(self, context, edit_text):
    current = context.scene.dev_reload_module
    return [
        (label, "Current" if module_name == current else module_name)
        for module_name, label in enabled_addons()
    ]


def _picker_get(self):
    return ""  # stays empty so the narrow field only shows its arrow


def _picker_set(self, value):
    for module_name, label in enabled_addons():
        if label == value:
            bpy.context.scene.dev_reload_module = module_name
            for window in bpy.context.window_manager.windows:
                for area in window.screen.areas:
                    area.tag_redraw()
            return


def draw_header_button(self, context):
    """Add-on picker + reload button at the right end of the top bar."""
    # The top bar draws the same header class twice: the left region (menus,
    # workspace tabs) and the right one (Scene, View Layer). Only use the right.
    if context.region.alignment != 'RIGHT':
        return
    layout = self.layout
    layout.separator()
    row = layout.row(align=True)
    picker = row.row(align=True)
    picker.ui_units_x = 1.2  # just the arrow, as wide as an icon button
    picker.prop(context.window_manager, "dev_reload_picker", text="", icon='DOWNARROW_HLT')
    row.operator(DEV_OT_ReloadAddon.bl_idname, text="", icon='FILE_REFRESH')


classes = (
    DEV_OT_ReloadAddon,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    # A string, not a dynamic enum: a dynamic enum is saved as an index, so
    # enabling another addon would silently shift the target to a neighbour.
    bpy.types.Scene.dev_reload_module = bpy.props.StringProperty(
        name="Reload Target",
        description="Module name of the add-on to hot-reload",
        default="",
    )
    bpy.types.WindowManager.dev_reload_picker = bpy.props.StringProperty(
        name="Add-on to Reload",
        description="Choose the add-on that Reload acts on. Click and type to search",
        search=_picker_search,
        get=_picker_get,
        set=_picker_set,
    )

    # TOPBAR_HT_upper_bar is the bar with the menus, workspace tabs and Scene/View Layer.
    bpy.types.TOPBAR_HT_upper_bar.append(draw_header_button)


def unregister():
    bpy.types.TOPBAR_HT_upper_bar.remove(draw_header_button)
    del bpy.types.WindowManager.dev_reload_picker
    del bpy.types.Scene.dev_reload_module
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
