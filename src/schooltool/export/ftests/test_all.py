#
# SchoolTool - common information systems platform for school administration
# Copyright (c) 2009 Shuttleworth Foundation
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""
Functional tests for schooltool.export
"""
import unittest

from schooltool.testing.functional import collect_ftests
from schooltool.export.ftesting import export_functional_layer


def test_suite():
    """
    use "--at-level 2" or "make testall" to reach these tests
    """
    return collect_ftests(layer=export_functional_layer, level=2)


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
