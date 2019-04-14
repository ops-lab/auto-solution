=============
auto-solution
=============

Configuration
-------------

1.Config post build script
>>>>>>>>>>>>>>>>>>>>>>>>>>

Use system groovy script of postbuildscript plugin in post-build action of jenkins project. 
And config postbuildscript.groovy for jenkins project.

Configuration content from postbuildscript.groovy_

.. _postbuildscript.groovy: usage/postbuildscript.groovy

Automatic Tools
    Execute automation script(update-project-config.sh_) to update all projects configuration.
    ::

        # refresh all departments
        bash update-project-config.sh
        # refresh designated department
        bash update-project-config.sh ${department_name}

    Notice: If jenkins server version is Jenkins2.x
        1. modify JENKINS_CLI_PATH and JENKINS_URL in update-project-config.sh file to correct value

        2. modify the PostBuildScriptConfig field in update-project-config.sh file to PostBuildScriptConfigV2 field

.. _update-project-config.sh: ../script/update-project-config.sh

2.Config server environment
>>>>>>>>>>>>>>>>>>>>>>>>>>>

- Create script(postbuildscript.sh_) to trigger auto-solution tools

.. _postbuildscript.sh: usage/postbuildscript.sh

- Create and into python virtualenv environment::

    virtual --no-site-package venv
    source venv/bin/activate

- Install auto-solution tools(How to get auto-solution tools refer to README.rst_)::

    pip install auto-solution-1.0.tar.gz

.. _README.rst: ../README.rst

3.Add cases to case library
>>>>>>>>>>>>>>>>>>>>>>>>>>

    Notice:
        The principle of matching is that keywords in case base can be matched in error information, otherwise they can't be matched.

Add cases into database.sql_ according to format.

.. _database.sql: docs/script/database.sql

::

    INSERT INTO case_lib(case_key, case_info, case_type, case_description, case_solution, case_remark) VALUES(
        '',
        '',
        '',
        '',
        '',
        ''
    );

Then execute database.sql that case writed to case library.

::

    mysql -h127.0.0.1 -P3306 -uroot -proot < database.sql
