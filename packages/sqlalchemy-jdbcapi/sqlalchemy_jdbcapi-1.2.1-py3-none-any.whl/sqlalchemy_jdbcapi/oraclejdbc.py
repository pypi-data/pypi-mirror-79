from __future__ import absolute_import
from __future__ import unicode_literals

import os
import re
from sqlalchemy.dialects.oracle.base import OracleDialect
from sqlalchemy.sql import sqltypes
from sqlalchemy import util, exc
from .base import MixedBinary, BaseDialect

colspecs = util.update_copy(
    OracleDialect.colspecs, {sqltypes.LargeBinary: MixedBinary,},
)


class OracleJDBCDialect(BaseDialect, OracleDialect):
    jdbc_db_name = "oracle"
    jdbc_driver_name = "oracle.jdbc.OracleDriver"
    colspecs = colspecs

    def initialize(self, connection):
        super(OracleJDBCDialect, self).initialize(connection)

    def _driver_kwargs(self):
        return {}

    def create_connect_args(self, url):
        if url is not None:
            params = super(OracleJDBCDialect, self).create_connect_args(url)[1]

            kwargs = {
                "jclassname": self.jdbc_driver_name,
                "url": self._create_jdbc_url(url),
                "driver_args": [params["username"], params["password"]]
            }
            return ((), kwargs)

    def _create_jdbc_url(self, url):
        return "jdbc:oracle:thin:@{}:{}/{}".format(
            url.host, url.port or 1521, url.database,
        )

    def _get_server_version_info(self, connection):

        try:
            banner = connection.execute(
                "SELECT BANNER FROM v$version"
            ).scalar()
        except exc.DBAPIError:
            banner = None
        version = re.search(r"Release ([\d\.]+)", banner).group(1)
        return tuple(int(x) for x in version.split("."))


dialect = OracleJDBCDialect
