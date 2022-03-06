##############################################################################
# Supplement to a Blender Sequencer:
#     1. tool = Typewriter effect
#     2. tool = Text flashing
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


bl_info = {
    "name": "Text Strip Animation",
    "author": "Jindřich Čech: jindrich.cech@quick.cz",
    "version": (3, 1, 1),
    "blender": (3, 0, 0),
    "location": "Sequencer > Tools > TypeWriter effect + Text blinking",
    "warning": "",
    "wiki_url": "",
    "category": "Sequencer",
    "description": "Present text as typewriter.\
                    Flash text with chosen period."
}

    
import bpy

from . import text_type_writer
from . import text_blinking
from . import type_writer_tool
from . import blinking_tool


# Register
_modules = [
    text_type_writer,
    text_blinking,
    type_writer_tool,
    blinking_tool
]


def register():
    ok = True
    for m in _modules:
        if hasattr(m, "register"):
            ok = ok * m.register()    # impossible AND - (short evaluate)
    if ok:
        print("Add-on text_writer+blinking registered.\n")
    else:
        print("Unsuccessful registration of add-on text_writer+blinking!\n")


def unregister():
    ok = True
    for m in reversed(_modules):
        if hasattr(m, "unregister"):
            ok = ok * m.unregister()    # impossible AND - (short evaluate)
    if ok:
        print("Add-on text_writer+blinking Un-registered.\n")
    else:
        print("Add-on text_writer+blinking was not un-registered!\n")


if __name__ == "__main__":
    # unregister()
    register()
