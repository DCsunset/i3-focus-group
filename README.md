# i3-focus-group

[![PyPI](https://img.shields.io/pypi/v/i3-focus-group)](https://pypi.org/project/i3-focus-group/)
[![GitHub](https://img.shields.io/github/license/DCsunset/i3-focus-group?color=blue)](https://github.com/DCsunset/i3-focus-group)

Create a group for i3/sway containers to easily switch focus between.

## Installation

Using pip:

```
pip install i3-focus-group
```

If you are using Nix, you can install it from NUR.

## Usage

i3-focus-group will listen at a Unix domain socket for incoming requests.
Each request includes a single line of string as the name of command.

The following commands are supported:

| Command  | Description                                                          |
|----------|----------------------------------------------------------------------|
| add      | Add the current container to the group                               |
| remove   | Remove the current container from the group                          |
| toggle   | Toggle the current container (add or remove)                         |
| clear    | Clear the group (remove all containers)                              |
| switch   | Focus next container in group and promote this container if in group |
| peekNext | Focus next container in group but without changing order             |
| peekPrev | Focus previous container in group but without changing order         |

You can use any program that supports Unix domain socket to send the request.
For example:
```
echo "add" | socat - $XDG_RUNTIME_DIR/i3-focus-group.sock
echo "switch" | socat - $XDG_RUNTIME_DIR/i3-focus-group.sock
```

To use it with i3/sway, simply add keybindings to run the above commands:
```
bindsym Mod4+Tab exec echo "switch" | socat - $XDG_RUNTIME_DIR/i3-focus-group.sock
bindsym Mod4+grave exec echo "toggle" | socat - $XDG_RUNTIME_DIR/i3-focus-group.sock
bindsym Mod4+Shift+grave exec echo "clear" | socat - $XDG_RUNTIME_DIR/i3-focus-group.sock
bindsym Mod4+comma exec echo "peekPrev" | socat - $XDG_RUNTIME_DIR/i3-focus-group.sock
bindsym Mod4+period exec echo "peekNext" | socat - $XDG_RUNTIME_DIR/i3-focus-group.sock
```

For more command-line options, run `i3-focus-group -h`.


## Example

1. To start with, the group with be empty.
2. Then suppose two containers A, B, and C are added to the group and now C is focused.
   The group becomes `[C] B A`. (bracket means current focus)
3. Suppose `switch` command is issued, it will focus on the next container B and promote it to the head.
   The group becomes `[B] C A`.
4. Suppose `switch` command is issued again, the group will become `[C] B A`.
5. Suppose `peekNext` is issued. The focus will change to B but without promoting the container.
   The group becomes `C [B] A`.
6. Suppose `peekNext` is issued again. The focus will change to A.
   The group becomes `C B [A]`.
7. Suppose `switch` is issued next. A will be promoted first and focus will switch to the next container C.
   The group becomes `[C] A B`.

If the current focus not in the group, the next `switch` or `peek` command will focus on the first container in the group.


## License

```
i3-focus-group
Copyright (C) 2024  DCsusnet

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
```

