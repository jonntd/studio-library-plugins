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
import sys

try:
    from PySide import QtGui
    from PySide import QtCore
except:
    from PyQt4 import QtGui
    from PyQt4 import QtCore


import studiolibrary


PACKAGEPATH = (os.getenv("USERPROFILE") + "/Dropbox").replace('\\', '/')
DIRNAME = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')



class Plugin(studiolibrary.Plugin):

    def __init__(self, parent):
        studiolibrary.Plugin.__init__(self, parent)

        self.setName("Environment")
        self.setExtension("env")
        self.setIcon(self.dirname() + "/images/pose.png")

        self.setRecord(Environment)
        #~ self.setCreateWidget(PoseCreateWidget)
        #~ self.setPreviewWidget(PosePreviewWidget)



class Environment(studiolibrary.Record):

    def __init__(self, *args, **kwargs):
        studiolibrary.Record.__init__(self, *args, **kwargs)
        self.setdefault("icon", "thumbnail.png")

    def doubleClicked(self):
        self.run()



if __name__ == "__main__":
    import studiolibrary
    studiolibrary.main(plugins=["appPlugin.appPlugin"], name="AppLibrary")

