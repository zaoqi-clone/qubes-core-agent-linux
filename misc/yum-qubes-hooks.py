#!/usr/bin/python2
#
# The Qubes OS Project, http://www.qubes-os.org
#
# Copyright (C) 2012  Marek Marczykowski <marmarek@invisiblethingslab.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
#


from yum.plugins import TYPE_CORE
import subprocess

requires_api_version = '2.4'
plugin_type = (TYPE_CORE,)


def posttrans_hook(conduit):
    if conduit.confBool('main', 'notify-updates', default=True):
        # Get all updates available _before_ this transaction
        pkg_list = conduit._base.doPackageLists(pkgnarrow='updates')
        # Get packages installed in this transaction...
        ts = conduit.getTsInfo()
        all_transactions = ts.getMembers()
        # ...and filter them out of available updates
        filtered_updates = list(
            filter(lambda x: x not in all_transactions, pkg_list.updates))
        # Notify dom0 about left updates count
        subprocess.call(
            ['/usr/lib/qubes/qrexec-client-vm', 'dom0', 'qubes.NotifyUpdates',
             '/bin/echo', str(len(filtered_updates))])
    conduit.info(1, "Notifying dom0 about installed/removed applications")
    # Notify and add app to app-menus
    subprocess.call(['/etc/qubes-rpc/qubes.PostInstall'])
