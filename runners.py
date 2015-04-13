# The MIT License (MIT)
#
# Copyright (c) 2015 Richard Tuin
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import click
import subprocess

class TargetRunner:
    def __init__(self, plafile):
        self.plafile = plafile

    def run(self, target, error=False):
        for command in self.plafile[target]:
            if command[:1] == '=':
                error = self.run(command[1:], error)
                continue

            if error:
                click.secho('    . ' + command, fg='white', dim=True)
                continue

            try:
                subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)

                click.secho('    ' + u'\u2714'.encode('utf8') + ' ' + command, fg='green')
            except subprocess.CalledProcessError as caught:
                click.secho('    '+ u'\u2718'.encode('utf8') + ' ' + command + ':', fg='red')

                output = caught.output.splitlines()
                if output == []:
                    output = ['[no output]']

                click.secho('        ' + ('\n        '.join(output)), fg='red', dim=True)
                error = True
        return error
