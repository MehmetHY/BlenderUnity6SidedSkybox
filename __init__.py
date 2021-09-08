import bpy
import math

bl_info = {
    "name": "Unity 6 Sided Skybox",
    "author": "MehmetHY",
    "version": (1, 0),
    "blender": (2, 93, 0),
    "location": "3D View -> N Panel -> Skybox -> Unity 6 Sided Skybox",
    "description": "Render and export 6 sided skybox for Unity3D with a single click.",
    "warning": "",
    "doc_url": "",
    "tracker_url": "https://github.com/MehmetHY/BlenderUnity6SidedSkybox",
    "category": "Render"
}

class SkyboxProperties(bpy.types.PropertyGroup):
    file_path: bpy.props.StringProperty(name='File Path', description='Output Directory', subtype='DIR_PATH')
    file_name: bpy.props.StringProperty(name='File Name', description='Output Directory', subtype='FILE_NAME')
    file_format: bpy.props.EnumProperty(items=[('PNG', 'PNG', ''), ('OPEN_EXR', 'EXR', ''), (
        'HDR', 'HDR', ''), ('JPEG', 'JPEG', ''), ('JPEG2000', 'JPEG2000', ''), ('TIFF', 'TIFF', ''), ('BMP', 'BMP', ''), ('TARGA', 'TARGA', ''), ('TARGA_RAW', 'TARGA_RAW', '')], name='File Format', description='File Format', default='PNG')
    dimensions: bpy.props.IntProperty(name='Dimensions', description='Image Dimensions', default=1024, min=1)
    front_postfix: bpy.props.StringProperty(name='Front Postfix', description='Image output postfix of the front side', default='_front')
    right_postfix: bpy.props.StringProperty(name='Right Postfix', description='Image output postfix of the right side', default='_right')
    left_postfix: bpy.props.StringProperty(name='Left Postfix', description='Image output postfix of the Left side', default='_left')
    back_postfix: bpy.props.StringProperty(name='Back Postfix', description='Image output postfix of the back side', default='_back')
    up_postfix: bpy.props.StringProperty(name='Up Postfix', description='Image output postfix of the up side', default='_up')
    down_postfix: bpy.props.StringProperty(name='Down Postfix', description='Image output postfix of the down side', default='_down')

class skybox_panel(bpy.types.Panel):
    bl_idname = "RENDER_SKYBOX_PT_six_sided"
    bl_label = "Unity 6 Sided Skybox"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Skybox"

    @classmethod
    def poll(cls, context):
        return (context.scene is not None)

    def draw(self, context):
        prop_group = bpy.context.scene.skybox_props
        layout = self.layout

        row = layout.row()
        row.label(text="Render")
        box = layout.box()
        box.operator('render.unity_render_skybox_6_sided', text='Render')
    
        row = layout.row()
        row.label(text="Output")
        box = layout.box()
        box.prop(prop_group, 'file_name', text="File Name")
        box.prop(prop_group, 'file_path', text="Output Folder")
        box.prop(prop_group, 'file_format', text="File Format")
        box.prop(prop_group, 'dimensions', text="Dimensions")
        box.prop(prop_group, 'front_postfix', text="Front Postfix")
        box.prop(prop_group, 'right_postfix', text="Right Postfix")
        box.prop(prop_group, 'left_postfix', text="Left Postfix")
        box.prop(prop_group, 'back_postfix', text="Back Postfix")
        box.prop(prop_group, 'up_postfix', text="Up Postfix")
        box.prop(prop_group, 'down_postfix', text="Down Postfix")



class render_unity_skybox_6_sided(bpy.types.Operator):
    bl_idname = 'render.unity_render_skybox_6_sided'
    bl_label = 'Render Unity Skybox 6 Sided'
    bl_description = 'Renders 6 sided skybox for Unity3D'


    def execute(self, context):
        self.init()
        return {'FINISHED'}
    
    def init(self):
        # Deselect All
        bpy.ops.object.select_all(action='DESELECT')

        # Disable Bloom
        self.pre_bloom_state = bpy.context.scene.eevee.use_bloom
        bpy.context.scene.eevee.use_bloom = False

        # Create Camera
        self.cam_data = bpy.data.cameras.new('Unity Skybox 6 Sided Camera')
        self.cam = bpy.data.objects.new('Unity Skybox 6 Sided Camera', self.cam_data)
        bpy.context.collection.objects.link(self.cam)
        bpy.context.scene.camera = self.cam
        self.cam.data.lens_unit = 'FOV'
        self.cam.data.angle = math.radians(90)
        self.cam.select_set(state=True)

        # Set Output Settings
        bpy.context.scene.render.image_settings.file_format = bpy.context.scene.skybox_props.file_format
        bpy.context.scene.render.resolution_x = bpy.context.scene.skybox_props.dimensions
        bpy.context.scene.render.resolution_y = bpy.context.scene.skybox_props.dimensions

        # Render
        self.render_ft()
        self.render_rt()
        self.render_lf()
        self.render_bk()
        self.render_up()
        self.render_dn()

        # Clear
        self.finalize()
    
    def finalize(self):
        bpy.ops.object.delete(confirm=False)
        bpy.context.scene.eevee.use_bloom = self.pre_bloom_state

    def render_ft(self):
        bpy.ops.transform.rotate(value=math.radians(-90), orient_axis='X', orient_type='GLOBAL')

        bpy.context.scene.render.filepath = f"{bpy.context.scene.skybox_props.file_path}{bpy.context.scene.skybox_props.file_name}{bpy.context.scene.skybox_props.front_postfix}"
        bpy.ops.render.render(write_still=True)
        
    def render_rt(self):
        bpy.ops.transform.rotate(value=math.radians(-90), orient_axis='Z', orient_type='GLOBAL')

        bpy.context.scene.render.filepath = f"{bpy.context.scene.skybox_props.file_path}{bpy.context.scene.skybox_props.file_name}{bpy.context.scene.skybox_props.right_postfix}"
        bpy.ops.render.render(write_still=True)

    def render_lf(self):
        bpy.ops.transform.rotate(value=math.radians(180), orient_axis='Z', orient_type='GLOBAL')

        bpy.context.scene.render.filepath = f"{bpy.context.scene.skybox_props.file_path}{bpy.context.scene.skybox_props.file_name}{bpy.context.scene.skybox_props.left_postfix}"
        bpy.ops.render.render(write_still=True)

    def render_bk(self):
        bpy.ops.transform.rotate(value=math.radians(90), orient_axis='Z', orient_type='GLOBAL')

        bpy.context.scene.render.filepath = f"{bpy.context.scene.skybox_props.file_path}{bpy.context.scene.skybox_props.file_name}{bpy.context.scene.skybox_props.back_postfix}"
        bpy.ops.render.render(write_still=True)

    def render_up(self):
        bpy.ops.transform.rotate(value=math.radians(180), orient_axis='Z', orient_type='GLOBAL')
        bpy.ops.transform.rotate(value=math.radians(-90), orient_axis='X', orient_type='GLOBAL')

        bpy.context.scene.render.filepath = f"{bpy.context.scene.skybox_props.file_path}{bpy.context.scene.skybox_props.file_name}{bpy.context.scene.skybox_props.up_postfix}"
        bpy.ops.render.render(write_still=True)

    def render_dn(self):
        bpy.ops.transform.rotate(value=math.radians(180), orient_axis='X', orient_type='GLOBAL')

        bpy.context.scene.render.filepath = f"{bpy.context.scene.skybox_props.file_path}{bpy.context.scene.skybox_props.file_name}{bpy.context.scene.skybox_props.down_postfix}"
        bpy.ops.render.render(write_still=True)


classes_to_register = (SkyboxProperties, skybox_panel, render_unity_skybox_6_sided)

def register():
    for cls in classes_to_register:
        bpy.utils.register_class(cls)
    bpy.types.Scene.skybox_props = bpy.props.PointerProperty(type=SkyboxProperties)
def unregister():
    for cls in classes_to_register:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.skybox_props
    

if __name__ == "__main__":
    register()
