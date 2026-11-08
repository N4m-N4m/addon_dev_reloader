bl_info = {
    "name": "Quick Scatter",
    "author": "Studio Tools",
    "version": (0, 3, 0),
    "blender": (4, 2, 0),
    "category": "Object",
}

import bpy


class OBJECT_OT_quick_scatter(bpy.types.Operator):
    """Scatter copies of the active object around it"""
    bl_idname = "object.quick_scatter"
    bl_label = "Scatter Copies"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        settings = context.scene.quick_scatter
        self.report({'INFO'}, f"Scattered {settings.count} copies")
        return {'FINISHED'}


class QuickScatterSettings(bpy.types.PropertyGroup):
    count: bpy.props.IntProperty(name="Count", default=24, min=1)
    radius: bpy.props.FloatProperty(name="Radius", default=4.0, unit='LENGTH')
    seed: bpy.props.IntProperty(name="Seed", default=7)


class OBJECT_PT_quick_scatter(bpy.types.Panel):
    bl_label = "Quick Scatter"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False
        settings = context.scene.quick_scatter

        layout.prop(settings, "count")
        layout.prop(settings, "radius")
        layout.prop(settings, "seed")
        layout.operator("object.quick_scatter")


classes = (QuickScatterSettings, OBJECT_OT_quick_scatter, OBJECT_PT_quick_scatter)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.quick_scatter = bpy.props.PointerProperty(type=QuickScatterSettings)


def unregister():
    del bpy.types.Scene.quick_scatter
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
