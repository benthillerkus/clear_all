# Thanks, Sybren
# https://www.youtube.com/watch?v=xscQ9tcN4GI&list=PLa1F2ddGya_8acrgoQr1fTeIuQtkSd6BW&index=3

import bpy


bl_info = {
    "name": "Clear All Transforms",
    "author": "Bent Hillerkus <29630575+benthillerkus@users.noreply.github.com>",
    "version": (0, 9),
    "blender": (2, 83, 0),
    "category": "Object",
    "location": "View3D > Object > Clear > Transforms",
    "description": "Clear the location, rotation, the scale and the object origin. The default hotkey is Alt+T.",
    "warning": "",
    "doc_url": "https://github.com/benthillerkus/clear_all",
    "tracker_url": "https://github.com/benthillerkus/clear_all/issues/new",
}

addon_keymaps = [] # This will keep track of our shortcuts so we can unregister them.

def register_shortcuts():
    # Keymap code by Darkfall
    # https://www.youtube.com/watch?v=0xBhh47Tblc
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name= '3D View', space_type= 'VIEW_3D')
        kmi = km.keymap_items.new("object.transforms_clear", type= 'T', value= 'PRESS', alt= True)
        addon_keymaps.append((km, kmi))

def unregister_shortcuts():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

def set_shortcuts(self, context):
    if context.preferences.addons[__name__].preferences.shortcut:
        register_shortcuts()
    else:
        unregister_shortcuts()

class Preferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    shortcut: bpy.props.BoolProperty(
        name ="Use default shortcut (Alt + T)",
        default = True,
        update = set_shortcuts
    )

    def draw(self, context):
        self.layout.label(text= "If you already have a shortcut that uses Alt + T, you can disable the default shortcut.")
        self.layout.label(text= "To set a custom shortcut, in the keymap editor for the 3D View, add an entry for the operator object.transforms.clear")
        self.layout.prop(self, "shortcut")


class OBJECT_OT_clear_all_transforms(bpy.types.Operator):
    """Clear All Transforms"""
    bl_idname = "object.transforms_clear"
    bl_label = "Transforms"
    bl_options = {'REGISTER', 'UNDO'}

    location: bpy.props.BoolProperty(
        name = "Location",
        description = "Clear the location",
        default = True
    )

    rotation: bpy.props.BoolProperty(
        name = "Rotation",
        description = "Clear the rotation",
        default = True
    )

    scale: bpy.props.BoolProperty(
        name = "Scale",
        description = "Clear the scale",
        default = True
    )

    delta: bpy.props.BoolProperty(
        name = "Delta",
        description = "Also clear the delta transforms",
        default = False
    )

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D' and context.mode == 'OBJECT'

    def execute(self, context):
        if self.location:
            bpy.ops.object.location_clear(clear_delta= self.delta)
        
        if self.rotation:
            bpy.ops.object.rotation_clear(clear_delta= self.delta)

        if self.scale:
            bpy.ops.object.scale_clear(clear_delta= self.delta)

        return {'FINISHED'}

    def menu_draw(self, context):
        self.layout.operator("object.transforms_clear")


    bpy.types.VIEW3D_MT_object_clear.prepend(menu_draw)


def register():
    bpy.utils.register_class(Preferences)
    bpy.utils.register_class(OBJECT_OT_clear_all_transforms)

    set_shortcuts(bpy.context)


def unregister():
    unregister_shortcuts()

    bpy.utils.unregister_class(OBJECT_OT_clear_all_transforms)
    bpy.utils.unregister_class(Preferences)
