##############################################################################
# Part of Blender add-on package "sequencer_text_plus"
# version: 3.1.1
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


class SEQUENCER_OT_Text_Typewriter(bpy.types.Operator):
    """ Adds item "Typewriter effect" into Toolbar.
        Default rate is 5 char/sec - optional - "Rate" (1-25).
        To the beginning "Text-strip" adds as many "Text-strips" as the
        original "Text-strip" has characters.
    """

    bl_idname = "sequencer.text_typewriter"
    bl_label = "Typewriter effect"
    bl_description = "Adds characters step by step."
    bl_options = {'REGISTER'}
    
    writing_speed: bpy.props.IntProperty(name="Number chars/sec:",
                                         min=1, max=25,
                                         default=5)

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
            # print("Invoke True")
            strip.select = True
            return self.execute(context)
        else:
            # print("Invoke False")
            self.report({'ERROR'}, "Click to an Un-muted TEXT strip!")
            return {'CANCELLED'}
    
    def execute(self, context):
        """
         Sets length of Text-strips in accordance to chosen rate (def=5 zn/sec.)
         (Each character = one Text-strip.)
         Adds Text-strips according to the characters of Text.
        """
        vse = bpy.context.scene.sequence_editor
        strip = context.selected_sequences[0]
        new_length = round(bpy.context.scene.render.fps/self.writing_speed)
        if new_length == 0:
            new_length = 1
        start_ramec = strip.frame_final_start
        dilek = None
        obsah = ''   
        for character in strip.text:
            dilek = vse.sequences.new_effect(name='Text_dilek', type='TEXT',
                                             frame_start=start_ramec,
                                             frame_end=start_ramec+new_length,
                                             channel=strip.channel + 1)
            obsah = obsah + character
            dilek.text = obsah
            dilek.blend_type = strip.blend_type
            dilek.font = strip.font
            dilek.font_size = strip.font_size
            dilek.color = strip.color
            dilek.use_shadow = strip.use_shadow
            dilek.shadow_color = strip.shadow_color
            dilek.use_box = strip.use_box
            dilek.box_color = strip.box_color 
#            print(strip.box_margin)
            dilek.box_margin = strip.box_margin               
            dilek.location[0] = strip.location[0]
            dilek.location[1] = strip.location[1]
            dilek.align_x = strip.align_x
            dilek.align_y = strip.align_y
            dilek.blend_alpha = 1
            dilek.wrap_width = strip.wrap_width            
            start_ramec = start_ramec + new_length

        # last dilek align to original:
        if dilek.frame_final_end < strip.frame_final_end:
            dilek.frame_final_end = strip.frame_final_end
        strip.mute = True                 
                  
        return {'FINISHED'}


def register():
    try:
        bpy.utils.register_class(SEQUENCER_OT_Text_Typewriter)
#        print("Registration: SEQUENCER_OT_Text_Typewriter")
        return True
    except Exception:
        print("Registration error: SEQUENCER_OT_Text_Typewriter")
        return False        


def unregister():
    try:
        bpy.utils.unregister_class(SEQUENCER_OT_Text_Typewriter)
#        print("UnRegistration: SEQUENCER_OT_Text_Typewriter")
        return True
    except Exception:
        print("Un-registration error: SEQUENCER_OT_Text_Typewriter")
        return False
