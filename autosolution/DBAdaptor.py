#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ==============================================================================
# Database adapter.
# 
# Copyright (c) 2019 jiuchou
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of jiuchou nor the
#    names of its contributors may be used to endorse or promote
#    products derived from this software without specific prior 
#    written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# 'AS IS' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Authors:
# jiuchou <315675275@qq.com>
# ==============================================================================
import MySQLdb
import pymssql
import sys

class MySQLEngine(object):
    def __init__(self, host, user, passwd, db, port):
        self.conn = MySQLdb.connect(host, user, passwd, db, port, charset='utf8')
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def execute(self, sql_cmd, params=None):
        try:
            self.cursor.execute(sql_cmd, params)
        except Exception as e:
            raise Exception(str(e) + sql_cmd)
        if sql_cmd.lower().startswith('select'):
            try :
                data = self.cursor.fetchall()
            except Exception as e:
                data = ()
                print(e)
        elif sql_cmd.lower().startswith('insert'):
            self.conn.commit()
            data = None
        else:
            data = ()
        return data

class MySQLAgile(MySQLEngine):
    def __init__(self, host, user, passwd, db, port=3306):
        MySQLEngine.__init__(self, host, user, passwd, db, port)

class SQLEngine(object):
    """SQL Server Engine Class

    Tools of DevOps business that it can operate SQL Server 2012.

    Attributes:
        conn: a object that it connect SQL Server 2012.
        cursor: a object that it is a cursor, usually sql command execute in cursor.
    """
    def __init__(self, host="127.0.0.1", user="root",
                 password="root", database="autosolution"):
        """Initialize SQL Engine.

        Initialize SQL Engine to get object, 

        Args:
            host:
            user:
            database:
            charset:

        Returns:
            A object of SQLEngine. Each function of SQLEngine can be used. For
            example:
            >>> sql_engine = DBAdapter.SQLEngine(host, username, password, database)
            >>> sql_engine.execute("SELECT * FROM table_name")

        Raises:
            pymssql.OperationalError: An error occurred accessing the SQLEngine object.
        """
        try:
            self.conn = pymssql.connect(host, user, password, database,
                                        charset="utf8")
            self.cursor = self.conn.cursor()
        except pymssql.OperationalError as e:
            msg = "Error: Could not Connection SQL Server!"
            msg += "Please check your database configuration!\n"
            msg += "Detail information:\n{0}".format(e)
            print(msg)
            sys.exit()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def execute(self, sql_cmd, params=None):
        self.cursor.execute(sql_cmd, params)
        if sql_cmd.startswith(("select", "SELECT")):
            try:
                data = self.cursor.fetchall()
            except pymssql.OperationalError as msg:
                data = ()
                print(msg)
        else:
            data = ()
        return data

class SQLAgile(SQLEngine):
    """docstring
    """
    def get_email(self, employee_number):
        table_name="employee"
        sql_cmd = "select [Email] from {0} where [employee_number] = '{1}'"\
                  .format(table_name, employee_number)
        data = self.execute(sql_cmd)
        return data
