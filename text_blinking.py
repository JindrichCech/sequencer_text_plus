##############################################################################
# Part of Blender add-on package "sequencer_text_plus"
# version: 3.2.1
##############################################################################

# ##### BEGIN GPL LICENSE BLOCK ##############################################
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK ###############################################


import bpy
from .utils_sequencer import mouse_frame_channel, strip_under_mouse


class SEQUENCER_OT_Text_Blinking(bpy.types.Operator):
    """ Adds item "Blinking text" into a Toolbar.
        Default Period is 2 flash/sec - optional [1-5].
    """

    bl_idname = "sequencer.text_blinking"
    bl_label = "Blinking text"
    bl_description = "Text is flashing in accordance to chosen period."
    bl_options = {'REGISTER'}
    
    period: bpy.props.IntProperty(name="Number flashing/sec:",
                                  min=1, max=5,
                                  default=2)

    @classmethod
    def poll(cls, context):
        # Sequence_editor
        return context.sequences

    def invoke(self, context, event):
        """ 'Select' strip under a mouse cursor."""
        for s in context.selected_sequences:
            s.select = False
        frame, channel = mouse_frame_channel(context, event)
        strip = strip_under_mouse(context, frame, channel)

        if strip is not None and strip.type == 'TEXT' and not strip.mute:
            strip.select = True
            return self.execute(context)
        else:
            self.report({'ERROR'}, "Click to an Un-muted TEXT strip!")
            return {'CANCELLED'}

    def execute(self, context):
        """ Set Keyframes for alternating values of Opacity=0, 1. """
        
        strip = context.selected_sequences[0]
        anim_length = round(bpy.context.scene.render.fps/self.period)
        if strip.frame_final_duration < anim_length:
            self.report({'ERROR'}, "Text strip is too short !")
            return {'CANCELLED'}
         
        visible = round(anim_length/2)     # number frame for Opacity=1
        invisible = visible - 2            # number frame for Opacity=0
        
        position = strip.frame_final_start
        
        while position < strip.frame_final_end:
            strip.blend_alpha = 1
            strip.keyframe_insert(data_path='blend_alpha', frame=position)
            position += visible
            strip.keyframe_insert(data_path='blend_alpha', frame=position)
            strip.blend_alpha = 0
            position += 1
            strip.keyframe_insert(data_path='blend_alpha', frame=position)
            position += invisible
            strip.keyframe_insert(data_path='blend_alpha', frame=position)
            position += 1
            
        return {'FINISHED'} 


def register():
    try:
        bpy.utils.register_class(SEQUENCER_OT_Text_Blinking)
#        print("Registration: SEQUENCER_OT_Text_Blinking")
        return True
    except Exception as ex:
        print("Registration error: SEQUENCER_OT_Text_Blinking\n",
              str(ex))
        return False        


def unregister():
    try:
        bpy.utils.unregister_class(SEQUENCER_OT_Text_Blinking)
#        print("UnRegistration: SEQUENCER_OT_Text_Blinking")
        return True  
    except Exception as ex:
        print("Un-registration error: SEQUENCER_OT_Text_Blinking\n",
              str(ex))
        return False
