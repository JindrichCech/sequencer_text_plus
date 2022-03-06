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


class SEQUENCER_WT_TypeWriterTool(bpy.types.WorkSpaceTool):
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_context_mode = 'SEQUENCER'

    # The prefix of the idname should be your add-on name.
    bl_idname = "sequencer.tool_typewriter"
    bl_label = "Typewriter effect"
    bl_description = (
        "Click LMB on Text strip.\n\n"
        "This Text will be presented by chosen velocity.\n"
    )
    bl_icon = "brush.sculpt.displacement_smear"
    bl_widget = None
    bl_keymap = (("sequencer.text_typewriter", {"type": 'LEFTMOUSE',
                                                "value": 'PRESS'}, {}),)

    def draw_settings(context, layout, tool):
        props = tool.operator_properties("sequencer.text_typewriter")
        layout.prop(props, "writing_speed")
        

def register():
    try:
        bpy.utils.register_tool(SEQUENCER_WT_TypeWriterTool,
                                after={"builtin.blade"},
                                separator=True, group=True)
#        print("Registration: SEQUENCER_WT_TypeWriterTool")
        return True
    except Exception:
        print("Registration error: SEQUENCER_WT_TypeWriterTool")
        return False


def unregister():
    try:    
        bpy.utils.unregister_tool(SEQUENCER_WT_TypeWriterTool)
#        print("UnRegistration: SEQUENCER_WT_TypeWriterTool")  
        return True  
    except Exception:
        print("Un-registration error: SEQUENCER_WT_TypeWriterTool")
        return False
