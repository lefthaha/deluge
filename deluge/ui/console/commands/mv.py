#
# mv.py
#
# Deluge is free software.
#
# You may redistribute it and/or modify it under the terms of the
# GNU General Public License, as published by the Free Software
# Foundation; either version 3 of the License, or (at your option)
# any later version.
#
# deluge is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with deluge.    If not, write to:
# 	The Free Software Foundation, Inc.,
# 	51 Franklin Street, Fifth Floor
# 	Boston, MA  02110-1301, USA.
#
#    In addition, as a special exception, the copyright holders give
#    permission to link the code of portions of this program with the OpenSSL
#    library.
#    You must obey the GNU General Public License in all respects for all of
#    the code used other than OpenSSL. If you modify file(s) with this
#    exception, you may extend this exception to your version of the file(s),
#    but you are not obligated to do so. If you do not wish to do so, delete
#    this exception statement from your version. If you delete this exception
#    statement from all source files in the program, then also delete it here.
#
#
from deluge.ui.console.main import BaseCommand
import deluge.ui.console.colors as colors
from deluge.ui.client import client
import deluge.component as component

import os.path
import glob

class Command(BaseCommand):
    """Move a torrent"""
    usage = "Usage: mv <torrent-id> dest"

    def handle(self, *args, **options):
        self.console = component.get("ConsoleUI")
        # dest path not provided
        if len(args) < 2 :
            self.console.write(self.usage)
            return

        # last arg should be dest
        dest = args[-1]
        args = args[:-1]

        torrent_ids = []
        for arg in args:
            torrent_ids.extend(self.console.match_torrent(arg))

        client.core.move_storage(torrent_ids, dest)

    def complete(self, line):
        # Try to complete dest path
        if os.path.isdir(os.path.dirname(line)):
            possible_paths = glob.glob(line + '*')
            # complete only dir path
            return filter(lambda p: os.path.isdir(p), possible_paths)
        # Complete torrent id with the ConsoleUI torrent tab complete method
        else:
            return component.get("ConsoleUI").tab_complete_torrent(line)
