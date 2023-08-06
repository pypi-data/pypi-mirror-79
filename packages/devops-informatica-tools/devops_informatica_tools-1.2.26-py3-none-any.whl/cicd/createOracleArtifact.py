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

##
# Create Oracle Database Artifact
# @Since: 22-MAR-2019
# @Author: Jac. Beekers

import logging, datetime, supporting
import supporting.errorcodes as err
from cicd.database import databaseArtifactChecks as dbchecks
import cicd.database.artifact
import cicd.database.dbSettings as settings
import supporting.generalSettings as generalsettings
import sys, argparse

now = datetime.datetime.now()
result = err.OK
settings.databaseType = 'Oracle'


def parse_the_arguments(argv):
    """Parses the provided arguments and exits on an error.
    Use the option -h on the command line to get an overview of the required and optional arguments.
     """
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    return args


def main(argv):
    """Creates an Oracle artifact, consisting on collected sql files
    It uses a deploy list that contains schema and init.sql. Check the OracleArtifact docs and examples for more info.
    Module uses environment variables that steer the artifact creation.
    """
    thisproc = "MAIN"
    mainProc = 'CreateOracleArtifact'

    resultlogger = supporting.configurelogger(mainProc)
    logger = logging.getLogger(mainProc)

    args = parse_the_arguments(argv)

    supporting.log(logger, logging.DEBUG, thisproc, 'Started')
    supporting.log(logger, logging.DEBUG, thisproc, 'logDir is >' + generalsettings.logDir + "<.")

    # Check requirements for artifact generation
    generalsettings.getenvvars()
    settings.getdbenvvars()
    settings.outdbenvvars()

    result = dbchecks.databaseartifactchecks()
    if result.rc == err.IGNORE.rc:
        # deploylist is not mandatory since 2020-02-09
        supporting.log(logging, result.level, thisproc, 'Artifact ignored.')
        result = err.OK
    else:
        if result.rc != 0:
            supporting.log(logger, logging.ERROR, thisproc,
                           'Database Artifact Checks failed with >' + result.message + "<.")
            supporting.exitscript(resultlogger, result)
        else:
            result = cicd.database.artifact.processList(settings.dbdeploylist)

    supporting.log(logger, logging.DEBUG, thisproc, 'Completed with return code >' + str(result.rc)
                   + '< and result code >' + result.code + "<.")
    #    supporting.writeresult(resultlogger, result)
    supporting.exitscript(resultlogger, result)


if __name__ == '__main__':
    main(sys.argv)
