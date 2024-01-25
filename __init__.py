# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "Multi-UV Helper",
    "author" : "A guy called 'brockmann' on Stack Exchange",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}
import bpy

class OBJECT_OT_set_active_uv(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.set_active_uv_selection"
    bl_label = "Set UV Layer on all Objects in Selection"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.type == 'MESH' and obj.data.uv_layers.active

    def execute(self, context):        
        target_uv = context.active_object.data.uv_layers.active
        for obj in context.selected_objects:
            if obj.type == 'MESH' and obj != context.active_object:
                if target_uv.name in obj.data.uv_layers.keys():
                    # Active UV Layer = Target Layer
                    obj.data.uv_layers.active = obj.data.uv_layers[target_uv.name]
                    #obj.data.uv_layers[target_uv.name].active_render = True
                else:
                    obj.data.uv_layers.new(name=target_uv.name)
                    obj.data.uv_layers.active = obj.data.uv_layers[target_uv.name]
                    #obj.data.uv_layers[target_uv.name].active_render = True

        return {'FINISHED'}

class OBJECT_OT_remove_non_active(bpy.types.Operator):
    bl_idname = "object.remove_non_active_selection"
    bl_label = "Remove non-active UV layout"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.type == 'MESH' and obj.data.uv_layers.active

    def execute(self, context):
        active_obj = context.active_object
        active_uv = obj.data.uv_layers.active

        objects = bpy.context.selected_objects

        for obj in [objects for x in objects if x.type == 'MESH']:
            for layer in obj.data.uv_layers.keys():
                layer = obj.data.uv_layers[layer]
                if layer != active_uv:
                    obj.data.uv_layers.remove(layer)





def draw_set_active_uv(self, context):
    layout = self.layout
    layout.operator(OBJECT_OT_set_active_uv.bl_idname)
    layout.operator(OBJECT_OT_remove_non_active.bl_idname)


classes = (
    OBJECT_OT_remove_non_active,
    OBJECT_OT_set_active_uv
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.DATA_PT_uv_texture.append(draw_set_active_uv)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    bpy.types.DATA_PT_uv_texture.remove(draw_set_active_uv)


if __name__ == "__main__":
    register()