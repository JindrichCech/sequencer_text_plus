##############################################################################
# Part of Blender add-on packages "sequencer"
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
from math import floor


def mouse_frame_channel(context, event):
    """
    Convert mouse coordinates to frame, channel.
    Returns a tuple: (frame, channel) as integers.
    """
    frame, channel = context.region.view2d.region_to_view(event.mouse_region_x,
                                                          event.mouse_region_y)
    # print(frame, channel, round(frame), floor(channel))
    return round(frame), floor(channel)


def strip_under_mouse(context, frame, channel):
    """
    Look for strip in 'channel' which includes 'frame'.
    Args:
        - frame: on which was cursor
        - channel: in which was cursor
    If click is not on strip, returns 'Nothing'.
    """
    strip = None
    for s in context.sequences:
        if s.frame_final_start <= frame <= s.frame_final_end and \
                s.channel == channel:
            strip = s
    return strip


def last_frame():
    """
    Return the frame number after the last strip.
    """
    ramec = 1
    for strip in bpy.context.scene.sequence_editor.sequences:
        t = strip.frame_final_end
        if t > ramec:
            ramec = t
    return ramec
