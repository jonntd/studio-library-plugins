#!/usr/bin/python
"""
# Released subject to the BSD License
# Please visit http://www.voidspace.org.uk/python/license.shtml
#
# Copyright (c) 2011, Kurt Rathjen
# All rights reserved.
# Comments, suggestions and bug reports are welcome.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
   # * Redistributions of source code must retain the above copyright
   #   notice, this list of conditions and the following disclaimer.
   # * Redistributions in binary form must reproduce the above copyright
   # notice, this list of conditions and the following disclaimer in the
   # documentation and/or other materials provided with the distribution.
   # * Neither the name of Kurt Rathjen nor the
   # names of its contributors may be used to endorse or promote products
   # derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY Kurt Rathjen ''AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL Kurt Rathjen BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
"""
import os

try:
    from PySide import QtGui
    from PySide import QtCore
except ImportError:
    from PyQt4 import QtGui
    from PyQt4 import QtCore

import studiolibrary
PACKAGEPATH = (os.getenv("USERPROFILE") + "/Dropbox/packages").replace('\\', '/')
DIRNAME = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')


class Plugin(studiolibrary.Plugin):

    def __init__(self, parent):
        studiolibrary.Plugin.__init__(self, parent)

        self.setName("Launcher")
        self.setExtension("app")
        self.setIcon(self.dirname() + "/images/pose.png")
        self.setRecord(App)


class App(studiolibrary.Record):

    def __init__(self, *args, **kwargs):
        studiolibrary.Record.__init__(self, *args, **kwargs)
        self.setdefault("icon", "thumbnail.png")

    def command(self,):
        path = (self.dirname() + "/run.app")
        f = open(path, "rb")
        command = f.read()
        f.close()
        command = command.strip().replace("DIRNAME", self.dirname())
        command = command.strip().replace("PACKAGEPATH", PACKAGEPATH)
        print command
        return command

    def environment(self):
        path = (self.dirname() + "/environment.dict")
        #self.window().records()

        if os.path.exists(path):
            f = open(path, "rb")
            env = f.read()
            f.close()

            env = env.strip().replace("DIRNAME", self.dirname())
            env = env.strip().replace("PACKAGEPATH", PACKAGEPATH)
            return eval(env.strip())

    def contextMenu(self, menu, records):
        if records:
            icon = studiolibrary.icon(self.plugin().dirname() + "/images/arrow.png")
            action = studiolibrary.Action(icon, "Console", menu)
            action.setCallback(self.openConsole)
            menu.addAction(action)
        studiolibrary.Record.contextMenu(self, menu, records)

    def openConsole(self,):
        self.setEnvironment()

        if studiolibrary.isWindows():
            path = os.environ['windir']
            os.startfile(r"%s/system32/cmd.exe" % path)
        else:
            print "Error: Not supported on this OS!"

    def environments(self, dirname):

        root = self.window().root()

        if not root.endswith("/"):
            root += "/"

        folders = dirname.replace(root, "").split("/")
        results = {}

        for folder in folders:
            root += "/" + folder
            for s in [s for s in os.listdir(root) if ".env" in s]:
                key = folder + ": " + s.replace(".env", "")
                value = root + "/" + s
                results[key] = value

        return results

    def doubleClicked(self):
        self.run()

    def setEnvironment(self, env=None):
        if not env:
            env = self.environment()

        if env:
            for var in env:
                os.environ.setdefault(var, "")
                if studiolibrary.isWindows():
                    os.environ[var] = ";".join(env[var])
                else:
                    os.environ[var] = ":".join(env[var])

    def run(self, cmd=None, env=None):
        try:
            from subprocess import Popen, PIPE, STDOUT

            self.setEnvironment(env)

            if not cmd:
                cmd = self.command()
            print cmd
            p = Popen(cmd, shell=False, stdin=PIPE, stdout=PIPE)
        except:
            import traceback
            print traceback.format_exc()


if __name__ == "__main__":
    import studiolibrary
    studiolibrary.main(plugins=["launcherplugin.launcher"], name="Launcher")

