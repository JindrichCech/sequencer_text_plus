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


class SEQUENCER_OT_Text_Scrolling(bpy.types.Operator):
    """ Adds item "Scrolling text" into a Toolbar.
        Default Direction is LEFT to RIGHT.
    """

    bl_idname = "sequencer.text_scrolling"
    bl_label = "Scrolling text"
    bl_description = "Text is scrolling in accordance to chosen direction."
    bl_options = {'REGISTER'}

    direction: bpy.props.EnumProperty(items=[("LtR", "from LEFT to RIGHT",
                                              "Text moves from left border.",
                                              "BACK", 1),
                                      ("RtL", "RIGHT to LEFT",
                                       "Text moves from right screen border.",
                                       "FORWARD", 2),
                                      ("BtU", "BOTTOM to UP",
                                       "Text moves from bottom screen border.",
                                       "SORT_DESC", 3),
                                      ("TtB", "TOP to BOTTOM",
                                       "Text moves from top screen border.",
                                       "SORT_ASC", 4)],
                                      name="Direction:",
                                      description="",
                                      default=1)

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
        """ Set Keyframes for text moving. """

        screen_width = context.scene.render.resolution_x
        screen_height = context.scene.render.resolution_y
        strip = context.selected_sequences[0]
        strip.align_x = 'CENTER'
        strip.align_y = 'CENTER'
        strip.transform.offset_x = 0
        strip.transform.offset_y = 0
        height_correction = 0
        if strip.use_bold:
            koef = 0.85
        else:
            koef = 0.6
        width_of_text = len(strip.text) * koef * strip.font_size  # pixels(appr)
        words = strip.text.split(" ")
        number_of_words = len(words)
        longest_word = 0
        for word in words:
            if len(word) > longest_word:
                longest_word = len(word)

        if strip.wrap_width == 0:
            number_of_lines = 1
        else:
            number_of_lines = width_of_text // (strip.wrap_width * screen_width)
            if width_of_text % (strip.wrap_width * screen_width) > 0:
                number_of_lines += 1
            if number_of_lines > 1:
                if number_of_lines > number_of_words:
                    number_of_lines = number_of_words
                    width_of_text = longest_word * koef * strip.font_size
                else:
                    width_of_text = strip.wrap_width * screen_width  # pixels

                # For wrap_width>0 Blender does not vertically center
                # more lines correctly:
                height_correction = 0.6 * strip.font_size / screen_height

        height_of_text = number_of_lines * 1.2 * strip.font_size
        print(width_of_text, height_of_text, number_of_lines)
        if strip.use_box:
            box_margin = strip.box_margin
        else:
            box_margin = 0
        # part of screen:
        half_of_text_width = box_margin + (width_of_text / (2 * screen_width))
        half_of_text_height = box_margin + (height_of_text / (2 * screen_height))
        print(half_of_text_width, half_of_text_height)
        if self.direction == 'LtR':
            data_index = 0
            anim_from = 1 - (strip.crop.max_x / screen_width) + \
                half_of_text_width
            anim_to = (strip.crop.min_x / screen_width) - half_of_text_width
        elif self.direction == 'RtL':
            data_index = 0
            anim_from = (strip.crop.min_x / screen_width) - half_of_text_width
            anim_to = 1 - (strip.crop.max_x / screen_width) + \
                half_of_text_width
        elif self.direction == 'BtU':
            data_index = 1
            anim_from = (strip.crop.min_y / screen_height) - \
                half_of_text_height - height_correction
            anim_to = 1 - (strip.crop.max_y / screen_height) + \
                half_of_text_height + height_correction
        else:    # self.direction == 'TtB':
            data_index = 1
            anim_from = 1 - (strip.crop.max_y / screen_height) + \
                half_of_text_height + height_correction
            anim_to = (strip.crop.min_y / screen_height) - \
                half_of_text_height - height_correction

        strip.location[data_index] = anim_from
        strip.keyframe_insert(data_path='location', index=data_index,
                              frame=strip.frame_final_start)
        strip.location[data_index] = anim_to
        strip.keyframe_insert(data_path='location', index=data_index,
                              frame=strip.frame_final_end)
        # linear interpolation on the last added animation curve:
        context.scene.animation_data.action.fcurves[-1].keyframe_points[
            0].interpolation = 'LINEAR'

        return {'FINISHED'}


def register():
    try:
        bpy.utils.register_class(SEQUENCER_OT_Text_Scrolling)
        #        print("Registration: SEQUENCER_OT_Text_Blinking")
        return True
    except Exception as ex:
        print("Registration error: SEQUENCER_OT_Text_Scrolling\n",
              str(ex))
        return False


def unregister():
    try:
        bpy.utils.unregister_class(SEQUENCER_OT_Text_Scrolling)
        #        print("UnRegistration: SEQUENCER_OT_Text_Blinking")
        return True
    except Exception as ex:
        print("Un-registration error: SEQUENCER_OT_Text_Scrolling\n",
              str(ex))
        return False
