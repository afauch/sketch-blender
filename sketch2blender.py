import zipfile
import json
import bpy
import os

bl_info = {
    "name" : "Sketch Blender",
    "blender" : (2, 80, 0),
    "category" : "IMPORT-EXPORT"
}

class UpdateArtboards(bpy.types.Operator):
    """Runs Import for the Specified File"""
    bl_idname = "sketch.update_artboards"
    bl_label = "Update Sketch Artboards"
    bl_options = {'REGISTER','UNDO'}

    # Class variables
    sketchtool_path = '/Applications/Sketch.app/Contents/MacOS/sketchtool'
    
    # TODO: Later this will be managed through a panel
    base_path = '/Users/afaucher/Documents/Coding/Blender/SketchBlender/'
    file_name = 'test'
    sketch_file = base_path + file_name + '.sketch'
    sketch_file_json = base_path + file_name + '/document.json'
    exports_path = base_path + 'exports/'

    # Functions
    @classmethod
    def unzip_sketch_file(cls, sketch_file):
        with zipfile.ZipFile(sketch_file, 'r') as zip_ref:
            zip_ref.extractall(cls.base_path + cls.file_name + '/')

    @classmethod
    def import_json_file(cls, json_file):
        json_data = open(json_file)
        parsed_json = (json.loads(json_data.read()))
        print(json.dumps(parsed_json, indent=4, sort_keys=True))

    @classmethod
    def export_artboards(cls, sketch_file):
        os.chdir(cls.base_path)
        # TODO: sketchtool may not be in user's path. That should be registered with plugin.
        os.system(cls.sketchtool_path + ' export artboards ' + sketch_file + ' --output=exports/')

    @classmethod
    def import_artboard(cls, artboard_path):
        bpy.ops.import_image.to_plane(shader='PRINCIPLED', files=[{'name':artboard_path}])

    @classmethod
    def update_artboards(cls):
        cls.export_artboards(cls.sketch_file)
        # Reload all images
        for image in bpy.data.images:
            image.reload()
        # For objects that don't exist in the hierarchy, import as planes
        for filename in os.listdir(cls.exports_path):
            artboard_name = os.path.splitext(filename)[0]
            if bpy.data.objects.get(artboard_name) is None:
                cls.import_artboard(cls.exports_path + filename)

    def execute(self, context):
        self.unzip_sketch_file(self.sketch_file)
        self.import_json_file(self.sketch_file_json)
        self.export_artboards(self.sketch_file)
        self.update_artboards()
            
        return {'FINISHED'}
    
def register():
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("SKETCHBLENDER REGISTER CALLED")
        bpy.utils.register_class(UpdateArtboards)
        
def unregister():
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("SKETCHBLENDER UNREGISTER CALLED")
        bpy.utils.unregister_class(UpdateArtboards)
        
# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()