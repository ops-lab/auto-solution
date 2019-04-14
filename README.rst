=============
auto-solution
=============

auto-solution is a tool that get error info from build log and give solution by email automatic.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Get auto-solution::

    git clone https://github.com/jiuchou/auto-solution.git

2. Config and Install auto-solution as a library for Python::

    MYSQL_DB_HOST = "127.0.0.1"
    MYSQL_DB_USER = 'root'
    MYSQL_DB_PASSWORD = 'root'
    MYSQL_DB_NAME = 'autosolution'

    jenkins_url = "JENKINS_URL"
    jenkins_username = "jenkins"
    jenkins_password = "jenkins_password"

    make

3. Create Database in MySQL Database::

    CREATE DATABASE autosolution DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

4. Config jenkins global script post::

5. Config jenkins automatic project::

6. Start use or develop auto-solution.

For more detail, please see the configuration.rst_

.. _configuration.rst: docs/configuration.rst

Quick Develop
-------------

Support Version
>>>>>>>>>>>>>>>

- Jenkins
    - Verify:
        Jenkins1.609.1
    - Theoretical:
        Jenkins1.x
        Jenkins2.x

- Python
    - Verify:
        Python2.7/Python3.4
    - Theoretical:
        Python3+

- mysqlclient

- pandas

- python-jenkins

Author
------
jiuchou

Contact
-------
315675275@qq.com

