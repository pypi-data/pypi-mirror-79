"""
deployOracle
"""
#  MIT License
#
#  Copyright (c) 2020 Jac. Beekers
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


import logging
import sys
import argparse
import glob
from cicd.database.utilities import OracleUtils
# from os import listdir
from supporting import log
from supporting import generalSettings
from supporting import errorcodes as err
from supporting import exitscript
from supporting import configurelogger
import cicd.database.dbSettings as dbSettings

#logger = logging.getLogger(__name__)


class DeployOracle:
    """Deploys a previously built Oracle package"""

    def __init__(self, schema):
        self.logger = logging.getLogger(__name__)
        self.database_schema = schema
        dbSettings.getdbenvvars()
        self.database_tns_name \
            , self.database_schema \
            , self.database_user \
            , self.database_user_password \
            = dbSettings.getschemaenvvars(schema)
        self.sqldir = dbSettings.targetsqldir
        self.on_error = dbSettings.on_error
        dbSettings.outdbenvvars()
        dbSettings.outschemaenvvars()

    def deploy_artifact(self):
        """

        :return: result
        """
        thisproc = "deploy_artifact"
        overall_result = err.OK
        log(self.logger, logging.INFO, thisproc, "deploy_artifact started.")
        log(self.logger, logging.DEBUG, thisproc, "sqldir is >" + self.sqldir + "<")
        log(self.logger, logging.DEBUG, thisproc
            , "database_schema is >" + self.database_schema + "<.")
        schema_directory = self.sqldir + '/' + self.database_schema
        log(self.logger, logging.DEBUG, thisproc, "schema_directory is >" + schema_directory + "<.")
        sql_files = [f for f in glob.glob(schema_directory + "**/*.sql")]
        log(self.logger, logging.DEBUG, thisproc, "sql_files found >" + str(len(sql_files)) + "<.")
        sql_files.sort()
        for sqlfile in sql_files:
            if sqlfile[-4:] != ".sql":
                log(self.logger, logging.INFO, thisproc, "Ignored non-sql file >" + sqlfile + "<.")
                continue
            log(self.logger, logging.INFO, thisproc, "Processing sql file >" + sqlfile + "<.")
            oracle_util = OracleUtils.OracleUtilities(self.database_user
                                                      , self.database_user_password
                                                      , self.database_tns_name
                                                      , self.on_error
                                                      , self.database_schema + '_sqloutput.log')
            sqlplus_result = oracle_util.run_sqlplus(sqlfile)
            if sqlplus_result.rc != err.OK:
                log(self.logger, logging.WARNING, thisproc, "sqlplus returned >"
                    + sqlplus_result.code + "<.")
                overall_result = sqlplus_result

        log(self.logger, logging.INFO, thisproc, "deploy_artifact completed with >"
            + overall_result.code + "<.")
        return overall_result


def parse_the_arguments(argv):
    """Parses the provided arguments and exits on an error.
    Use the option -h on the command line to get an overview of the required and optional arguments.
     """
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--schema", required=True, action="store", dest="schema_name",
                        help="Deploy mentioned schema.")
    args = parser.parse_args(argv)

    return args


def main(argv):
    """Deploy the Oracle artifact to the target environment.
    Usage: deployOracle.py [-h] -s SCHEMA_NAME
    The module uses environment variables to steer the deployment,
    like target Oracle database, connections and such.
    For more information check the deployOracle docs.
    """
    thisproc = "MAIN"
    main_proc = 'deployOracle'

    resultlogger = configurelogger(main_proc)
    logger = logging.getLogger(main_proc)

    args = parse_the_arguments(argv)

    generalSettings.getenvvars()

    log(logger, logging.DEBUG, thisproc, 'Started')
    log(logger, logging.DEBUG, thisproc, 'logDir is >' + generalSettings.logDir + "<.")

    schema = args.schema_name
    log(logger, logging.INFO, thisproc, "Schema to be deployed is >" + schema + "<.")
    depl = DeployOracle(schema)
    result = depl.deploy_artifact()
    exitscript(resultlogger, result)


if __name__ == '__main__':
    main(sys.argv[1:])
