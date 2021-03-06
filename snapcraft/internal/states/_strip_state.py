# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4 -*-
#
# Copyright (C) 2016 Canonical Ltd
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import yaml

from snapcraft.internal.states._state import State


def _strip_state_constructor(loader, node):
    parameters = loader.construct_mapping(node)
    return StripState(**parameters)

yaml.add_constructor(u'!StripState', _strip_state_constructor)


class StripState(State):
    yaml_tag = u'!StripState'

    def __init__(self, files, directories, dependency_paths=None,
                 options=None):
        super().__init__(options)

        self.files = files
        self.directories = directories
        self.dependency_paths = set()

        if dependency_paths:
            self.dependency_paths = dependency_paths

    def properties_of_interest(self, options):
        """Extract the properties concerning this step from the options.

        The only property of interest to the strip step is the `snap` keyword
        used to filter out files with a white or blacklist.
        """

        return {'snap': getattr(options, 'snap', ['*']) or ['*']}
