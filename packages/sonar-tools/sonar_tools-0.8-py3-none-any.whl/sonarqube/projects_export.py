#!/usr/local/bin/python3
#
# sonar-tools
# Copyright (C) 2019-2020 Olivier Korach
# mailto:olivier.korach AT gmail DOT com
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
'''

    Exports all projects of a SonarQube platform

'''
import sys
import os
import sonarqube.projects as projects
import sonarqube.utilities as util
import sonarqube.env as env


def main():
    parser = util.set_common_args('Exports all projects of a SonarQube platform')
    parser.add_argument('--exportTimeout', required=False, type=int, default=180, help='Maximum wait time for export')

    args = parser.parse_args()
    util.check_environment(vars(args))

    project_list = projects.search(endpoint=env.Environment(url=args.url, token=args.token))
    nb_projects = len(project_list)
    util.logger.info("%d projects to export", nb_projects)
    i = 0
    statuses = {}
    for key, p in project_list.items():
        dump = p.export(timeout=args.exportTimeout)
        status = dump['status']
        if status in statuses:
            statuses[status] += 1
        else:
            statuses[status] = 1
        if status == 'SUCCESS':
            print("{0},SUCCESS,{1}".format(key, os.path.basename(dump['file'])))
        else:
            print("{0},FAIL,{1}".format(key, status))
        i += 1
        util.logger.info("%d/%d exports (%d%%) - Latest: %s - %s", i, nb_projects,
                         int(i * 100 / nb_projects), key, status)
        summary = ''
        for s in statuses:
            summary += "{0}:{1}, ".format(s, statuses[s])
        util.logger.info("%s", summary)
    sys.exit(0)


if __name__ == "__main__":
    main()
