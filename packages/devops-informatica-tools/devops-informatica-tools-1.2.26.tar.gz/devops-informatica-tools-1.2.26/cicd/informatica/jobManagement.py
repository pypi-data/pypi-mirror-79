#  MIT License
#
#  Copyright (c) 2019 Jac. Beekers
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
#

from supporting import log
import logging
from cicd.informatica import buildCommand
from cicd.informatica import executeInfacmd
from cicd.informatica import infaConstants
from supporting import errorcodes

class JobExecution:

    def __init__(self, pre_command=None, **keyword_arguments):
        self.logger = logging.getLogger(__name__)
        self.keyword_arguments = keyword_arguments
        self.pre_command = pre_command

    def manage(self):
        RunCommand = buildCommand.build(**self.keyword_arguments)

        if self.pre_command is None:
            log(self.logger, logging.INFO, __name__, "no pre_command provided.")
        else:
            log(self.logger, logging.INFO, __name__, "preCommand is >" + self.pre_command + "<.")
        log(self.logger, logging.INFO, __name__, "RunCommand is >" + RunCommand + "<.")
        result = executeInfacmd.execute(command=RunCommand, pre_command=self.pre_command)

        if result.rc != errorcodes.OK.rc:
            oldResult = result.message
            result = self.keyword_arguments["OnError"]
            result.message = oldResult

        return (result)

    def translateOptimizationLevel(self, value):
        return infaConstants.optimization_level[value]
