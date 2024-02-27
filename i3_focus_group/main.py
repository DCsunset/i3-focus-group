"""
i3-focus-group
Copyright (C) <year>  <name of author>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import os
import asyncio
import argparse
import sys
import socket
from functools import partial
from collections import deque
from i3ipc.aio import Connection
from i3ipc import Event

defaultSocketDir = os.environ.get("XDG_RUNTIME_DIR", f"/run/user/{os.getuid()}")

parser = argparse.ArgumentParser(
  description="i3 script to switch between windows in history",
  formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
parser.add_argument("--size", type=int, default=100, help="Max size of group")
parser.add_argument(
  "--socket",
  default=f"{defaultSocketDir}/i3-focus-group.sock",
  help="Socket path to listen at"
)
args = parser.parse_args()

group = deque(maxlen=args.size)
lock = asyncio.Lock()


async def handle_client_connection(i3, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
  # prevent mlutiple clients from modifying states concurrently
  async with lock:
    [root, req] = await asyncio.gather(
      i3.get_tree(),
      reader.read()
    )

    cur_container = root.find_focused()
    con_id = cur_container.id

    match req.decode("utf-8"):
      case "add":
        # add current container to group
        if not con_id in group:
          group.appendleft(con_id)

      case "remove":
        # remove current container from group
        group.remove(con_id)

      case "toggle":
        # toggle current container in group
        if con_id in group:
          group.remove(con_id)
        else:
          group.appendleft(con_id)

      case "switch":
        # focus next window in group and promote this window if in group
        if len(group) == 0:
          return

        # promote this container to head if not at head
        idx = group.index(con_id)
        if idx is not None:
          # promote this container to head
          group.remove(con_id)
          group.appendleft(con_id)
          idx = 0

          # switch focus to next container and swap
          next_idx = (idx+1) % len(group)
          group[idx], group[next_idx] = group[next_idx], group[idx]

        await i3.command(f"[con_id={group[0]}] focus")

      case "peekNext":
        # focus next window in group but without changing order
        if len(group) == 0:
          return

        # promote this container to head if not at head
        idx = group.index(con_id)
        if idx is not None:
          # switch focus to next container
          next_idx = (idx+1) % len(group)
        else:
          next_idx = 0

        await i3.command(f"[con_id={group[next_idx]}] focus")

      case "peekPrev":
        # focus prev window in group but without changing order
        if len(group) == 0:
          return

        # promote this container to head if not at head
        idx = group.index(con_id)
        if idx is not None:
          # switch focus to next container
          next_idx = (idx-1) % len(group)
        else:
          next_idx = 0

        await i3.command(f"[con_id={group[next_idx]}] focus")


async def main():
  i3 = await Connection(auto_reconnect=True).connect()

  server = await asyncio.start_unix_server(partial(handle_client_connection, i3), args.socket)
  async with server:
    await asyncio.gather(
      server.serve_forever(),
      i3.main()
    )

asyncio.run(main())
