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
from .type_writer_tool import SEQUENCER_WT_TypeWriterTool


class SEQUENCER_WT_BlinkingTextTool(bpy.types.WorkSpaceTool):
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_context_mode = 'SEQUENCER'

    # The prefix of the idname should be your add-on name.
    bl_idname = "sequencer.tool_textblinking"
    bl_label = "Blinking text"
    bl_description = (
        "Click LMB on Text strip.\n\n"
        "According to a given period changes  a text visibility.\n"
    )
    bl_icon = "brush.paint_texture.masklort"
    bl_widget = None
    bl_keymap = (("sequencer.text_blinking", {"type": 'LEFTMOUSE',
                                              "value": 'CLICK'}, {}),)

    def draw_settings(context, layout, tool):
        props = tool.operator_properties("sequencer.text_blinking")
        layout.prop(props, "period")
        

def register():
    try:
        bpy.utils.register_tool(SEQUENCER_WT_BlinkingTextTool,
                                after={SEQUENCER_WT_TypeWriterTool.bl_idname})
#        print("Registration: SEQUENCER_WT_BlinkingTextTool")
        return True
    except Exception:
        print("Registration error: SEQUENCER_WT_BlinkingTextTool")
        return False        


def unregister():
    try:
        bpy.utils.unregister_tool(SEQUENCER_WT_BlinkingTextTool)
#        print("UnRegistration: SEQUENCER_WT_BlinkingTextTool")
        return True
    except Exception:
        print("Un-registration error: SEQUENCER_WT_BlinkingTextTool")
        return False
