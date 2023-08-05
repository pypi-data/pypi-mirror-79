import sys
import logging
import os
from vconnector.vertica_connector import VerticaConnector

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.captureWarnings(True)


def get_ddl_path_default(schema):
    try_path = [os.getcwd().replace("/src", "/") + "db/vertica/{}".format(schema),  "src/db/vertica/{}".format(schema), "db/vertica/{}".format(schema)]
    for path in try_path:
        if not os.path.exists(path):
            logging.info("Path {} not found, you have to create directory src/db/schema to upload file".format(path))
        else:
            return path


class TableLoader(VerticaConnector):
    def __init__(
        self,
        user,
        password,
        database,
        vertica_configs,
        table_name,
        schema,
        staging_schema=None,
        dll_path=None,
        debug=True,
        sec_to_recconect=5,
        count_retries=1,
    ):

        """
        Class to uploding sql to table using temporary table in staging schema
        :param user: see VerticaConnector
        :param password:   see VerticaConnector
        :param database:   see VerticaConnector
        :param vertica_configs:   see VerticaConnector
        :param sec_to_recconect: see VerticaConnector  params
        :param count_retries:    see VerticaConnector
        :param table_name: table to upload
        :param schema: schema to upload
        :param staging_schema:
        :param ddl_path: where is searching for ddl
        :param debug:
        """
        VerticaConnector.__init__(
            self,
            user=user,
            password=password,
            database=database,
            vertica_configs=vertica_configs,
            debug=debug,
            sec_to_recconect=sec_to_recconect,
            count_retries=count_retries,
        )
        self.table_name = table_name
        self.ddl_path = dll_path or get_ddl_path_default(schema)
        self.schema = schema
        self.staging_schema = staging_schema or "netology_staging"
        self.main_ddl = None
        self.foreign_keys_dll = []

    def __str__(self):
        return "TableLoader to {}".format(self.connection_info["database"])

    def __exec_sql(self, sql):
        with self.__enter__() as cnx:
            cur = cnx.cursor()
            if self.debug:
                logging.info(sql)
            cur.execute(sql)
            cnx.commit()

    def __get_ddl_from_file(self):
        """
        read ddl from self.ddl_path directory
        Returns: create table_ddl

        """
        if self.table_name + ".sql" not in os.listdir(self.ddl_path):
            raise Exception(
                "File {table_name}.sql doesn't exists in {dir} directory. You have to create it manually or using "
                "new_tables_creator.py ".format(
                    table_name=self.table_name, dir=self.ddl_path
                )
            )

        f = open(self.ddl_path + "/" + self.table_name + ".sql", "r")
        ddl_txt = f.read()
        ddl = [x + ";" for x in ddl_txt.replace("\n", "").split(";") if x != ""]
        self.foreign_keys_dll = ddl[1:]
        self.main_ddl = ddl[0:1]

    def __create_staging_table(self):
        self.__get_ddl_from_file()
        ddls = [
            dd.replace(
                self.schema + "." + self.table_name,
                self.staging_schema + "." + self.table_name,
            )
            for dd in self.main_ddl
        ]
        sqls = ["drop table if exists {staging_schema}.{table_name} cascade;"] + ddls
        for sql in sqls:
            if sql == "":
                continue
            self.__exec_sql(
                sql.format(
                    schema=self.schema,
                    table_name=self.table_name,
                    staging_schema=self.staging_schema,
                )
            )

    def __reload_table(self):
        sqls = [
            "drop table {schema}.{table_name} cascade;",
            "alter table {staging_schema}.{table_name} set schema {schema};",
            "drop table if exists {staging_schema}.{table_name} cascade;",
        ] + self.foreign_keys_dll
        for sql in sqls:
            self.__exec_sql(
                sql.format(
                    schema=self.schema,
                    table_name=self.table_name,
                    staging_schema=self.staging_schema,
                )
            )

    def script_to_table(self, script):
        self.__create_staging_table()
        script_insert = "insert into {schema}.{table_name} {script}".format(
            schema=self.staging_schema, table_name=self.table_name, script=script
        )
        self.__exec_sql(script_insert)
        self.__reload_table()
