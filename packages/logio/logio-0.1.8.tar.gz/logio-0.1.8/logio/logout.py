# -*- coding: utf-8 -*-
from __future__ import print_function
from io import open
import re
import copy
import logging
import MySQLdb as mysql

logger = logging.getLogger(__name__)

LOG_OUTPUT_TYPES = {}

def register_output_type(name, klass):
    LOG_OUTPUT_TYPES[name] = klass

def unregister_output_type(name):
    del LOG_OUTPUT_TYPES[name]

def get_output_class(name):
    return LOG_OUTPUT_TYPES.get(name, None)

class LogOutput(object):

    def __init__(self, settings):
        self.settings = settings or {}

    def update(self, info):
        """True means saved, False means cached, raise exception means something error.
        """
        raise NotImplementedError()

    def flush(self):
        """Force to save the data.
        """
        raise NotImplementedError()

    @classmethod
    def init(cls, settings):
        output_type = settings.get("type", "mysql")
        output_class = get_output_class(output_type)
        if not output_class:
            return None
        return output_class(settings)

class BufferedLogOutput(LogOutput):

    def __init__(self, settings):
        super(BufferedLogOutput, self).__init__(settings)
        self.buffer_size = self.settings.get("buffer-size", 1) or 1
        self.count = 0
        self.buffer = []

    def update(self, info):
        self.buffer.append(info)
        self.count += 1
        if self.count % self.buffer_size == 0:
            self.buffer_handler()
            return True
        else:
            return False

    def flush(self):
        self.buffer_handler()
        return True

    def buffer_handler(self):
        for info in self.buffer:
            self.line_handler(info)
        self.buffer = []
        return True

    def line_handler(self, info):
        raise NotImplementedError()

class LogToStdout(BufferedLogOutput):

    def line_handler(self, info):
        print(info)

class LogToMysql(BufferedLogOutput):

    DEFAULT_MYSQL_SETTINGS = {
        "autocommit": True,
        "charset": "utf8",
    }

    def __init__(self, settings):
        super(LogToMysql, self).__init__(settings)
        # mysql properties
        self.mysql_settings = copy.copy(self.DEFAULT_MYSQL_SETTINGS)
        self.mysql_settings.update(self.settings.get("mysql", {}) or {})
        self.mysql_connect = None
        # properties
        self.ignore_not_matched_lines = self.settings.get("ignore-not-matched-lines", True)
        self.keep_failed_lines = self.settings.get("keep-failed-lines", "") or ""
        self.inserts = self.settings["inserts"] # settings.inserts required
        self.inserts["DEFAULT"] # settings.inserts.DEFAULT required

    def do_keep_failed_lines(self, infos):
        with open(self.keep_failed_lines, "a", encoding="utf-8") as fobj:
            for info in infos:
                fobj.write(u"{0}\n".format(info["_line"]))

    def get_cursor(self):
        if not self.mysql_connect:
            self.mysql_connect = mysql.connect(**self.mysql_settings)
        else:
            self.mysql_connect.ping()
        return self.mysql_connect.cursor()

    def get_categoryed_buffer(self):
        data = {"DEFAULT": []}
        for info in self.buffer:
            if not info["_matched"] and self.ignore_not_matched_lines:
                continue
            matched_name = info["_matched_name"]
            if matched_name in self.inserts:
                if matched_name in data:
                    data[matched_name].append(info)
                else:
                    data[matched_name] = [info]
            else:
                data["DEFAULT"].append(info)
        return data

    def buffer_handler(self):
        if self.buffer:
            try:
                cursor = self.get_cursor()
            except Exception as err:
                logger.error(u"Error: Connect to mysql failed, message={0}。".format(str(err)))
                cursor = None
                self.do_keep_failed_lines(self.buffer)
            if cursor:
                for insert_name, rows in self.get_categoryed_buffer().items():
                    sql_template = self.inserts[insert_name]
                    self.fix_missing_field(sql_template, rows)
                    try:
                        cursor.executemany(sql_template, rows)
                        logger.info(u"Info: insert data into mysql success, {0} records inserted.".format(len(rows)))
                    except Exception as err:
                        logger.error(u"Error: insert data into mysql failed, message={0}, sql_template={1}。".format(str(err), sql_template))
                        self.do_keep_failed_lines(rows)
        self.buffer = []
        return True

    def fix_missing_field(self, sql_template, rows):
        fields = re.findall("\\%\\(([a-zA-Z0-9_]+)\\)s", sql_template)
        for row in rows:
            for field in fields:
                if not field in row:
                    row[field] = None

class PrintNotMatchedLine(BufferedLogOutput):

    def line_handler(self, info):
        matched = info.get("_matched", False)
        if not matched:
            print(info["_line"])

register_output_type("mysql", LogToMysql)
register_output_type("stdout", LogToStdout)
register_output_type("print-not-matched-line", PrintNotMatchedLine)
