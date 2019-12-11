import zipfile
import json
import bpy
import os

bl_info = {
    "name" : "Sketch Blender",
    "blender" : (2, 80, 0),
    "category" : "Import-Export"
}

class SketchSettings(bpy.types.PropertyGroup):
    sketch_filepath : bpy.props.StringProperty(
        name = "Sketch file:",
        description="Choose a Sketch file to import artboards",
        default="",
        maxlen=1024,
        subtype='FILE_PATH')

# Paths
class Paths:
    sketchtool_path = '/Applications/Sketch.app/Contents/MacOS/sketchtool'

# Panel
class Sketch2BlenderPanel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Sketch"
    bl_label = "Sketch"
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(text="Sketch2Blender")

    def draw(self, context):
        layout = self.layout

        box = layout.box()
        box.label(text="Import Sketch File")
        
        # Import / Update
        row = box.row()
        row.prop(context.scene.sketch_settings, "sketch_filepath")
        
        row = box.row()
        row.operator("sketch.import_artboards")
        row.operator("sketch.update_artboards")

# Operator
class ImportArtboards(bpy.types.Operator):
    """Runs Import for the Specified File"""
    bl_idname = "sketch.import_artboards"
    bl_label = "Import Artboards"
    bl_options = {'REGISTER','UNDO'}
    
    paths = Paths()

    @classmethod
    def export_artboards(cls, sketch_file):
        abs_path = bpy.path.abspath(sketch_file)
        os.chdir(os.path.dirname(abs_path))
        os.system(cls.paths.sketchtool_path + ' export artboards ' + abs_path + ' --output=exports/')

    @classmethod
    def import_artboard(cls, artboard_path):
        bpy.ops.import_image.to_plane(shader='SHADELESS', files=[{'name':artboard_path}])
    
    @classmethod
    def import_artboards(cls, sketch_file):
        cls.export_artboards(sketch_file)
        exports_path = os.path.dirname(bpy.path.abspath(sketch_file)) + '/exports/'
        # For objects that don't exist in the hierarchy, import as planes
        for filename in os.listdir(exports_path):
            artboard_name = os.path.splitext(filename)[0]
            if bpy.data.objects.get(artboard_name) is None:
                cls.import_artboard(exports_path + filename)    

    def execute(self, context):
        self.import_artboards(context.scene.sketch_settings.sketch_filepath)
        return {'FINISHED'}

# Operator
class UpdateArtboards(bpy.types.Operator):
    """Runs Update for the Specified File"""
    bl_idname = "sketch.update_artboards"
    bl_label = "Update Artboards"
    bl_options = {'REGISTER','UNDO'}

    paths = Paths()

    # Functions
    @classmethod
    def update_artboards(cls, sketch_file):
        cls.export_artboards(sketch_file)
        # Reload all images
        for image in bpy.data.images:
            image.reload()

    @classmethod
    def export_artboards(cls, sketch_file):
        print("Exporting artboards...")
        abs_path = bpy.path.abspath(sketch_file)
        os.chdir(os.path.dirname(abs_path))
        os.system(cls.paths.sketchtool_path + ' export artboards ' + abs_path + ' --output=exports/')

    def execute(self, context):
        self.update_artboards(context.scene.sketch_settings.sketch_filepath)
        return {'FINISHED'}
    
def register():
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("SKETCHBLENDER REGISTER CALLED")
        bpy.utils.register_class(SketchSettings) 
        bpy.utils.register_class(ImportArtboards)                   
        bpy.utils.register_class(UpdateArtboards)    
        bpy.utils.register_class(Sketch2BlenderPanel)
        bpy.types.Scene.sketch_settings = bpy.props.PointerProperty(type=SketchSettings)
        
def unregister():
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("SKETCHBLENDER UNREGISTER CALLED")
        bpy.utils.unregister_class(SketchSettings)        
        bpy.utils.unregister_class(ImportArtboards)
        bpy.utils.unregister_class(UpdateArtboards)
        bpy.utils.unregister_class(Sketch2BlenderPanel)
        del bpy.types.Scene.sketch_settings
        
# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()