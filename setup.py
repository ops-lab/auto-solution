# -*- coding: utf-8 -*-
"""
setup.py for auto-solution
"""
import os
import re
from setuptools import find_packages, setup

# Document:
# [1] https://setuptools.readthedocs.io/en/latest/setuptools.html
# [2] https://www.cnblogs.com/numbbbbb/p/3615155.html
# [3] http://blog.konghy.cn/2018/04/29/setup-dot-py/

def get_name(package):
    """
    Return package version as listed in `__title__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__title__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


name = get_name('autosolution')
version = get_version('autosolution')

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# 第三方依赖包及版本
requires = [
    'python-jenkins==1.4.0',
    'pandas==0.22.0',
    'mysqlclient>=1.3.14',
    'pymssql==2.1.4',
]
# setuptools [1]
setup(
    name=name,
    version=version,
    packages=find_packages(),
    # package_dir = {'': 'auto-solution'}
    # scripts 参数是一个 list，安装包时在该参数中列出的文件会被安装到系统 PATH 路径下
    # scripts=['auto-solution/manage.py'],

    # entry_points 参数用来支持自动生成脚本，其值应该为是一个字典，从 entry_point 组名映射到一个表
    # 示 entry_point 的字符串或字符串列表 [3]
    # entry_points = {'console_scripts': [
    #     'auto-solution-manage = auto-solution.manage:main',
    # ]},

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=requires,

    # use MANIFEST.in [2]
    # 该参数被设置为 True 时自动添加包中受版本控制的数据文件，可替代 package_data，同时，
    # exclude_package_data 可以排除某些文件。注意当需要加入没有被版本控制的文件时，还是仍然需要使用
    # package_data 参数才行
    include_package_data=True,
    # exclude_package_data={
    #     '': ['.gitignore']
    # },
    # package_data = {
    #     # If any package contains *.txt or *.rst files, include them:
    #     '': ['*.txt', '*.rst'],
    #     # include any *.msg files found in the 'hello' package, too:
    #     'hello': ['*.msg'],
    # },
    # data_files=[
    #     ('bitmaps', ['bm/b1.gif', 'bm/b2.gif']),
    #     ('config', ['cfg/data.cfg']),
    #     ('/etc/init.d', ['init-script'])
    # ],

    license='MIT License',
    keywords="auto-solution",
    description='A simple Django app to manage svn server.',
    long_description=README,
    url='https://github.com/jiuchou/auto-solution',
    author='jiuchou',
    author_email='315675275@qq.com',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    project_urls={
        "Bug Tracker": "https://github.com/jiuchou/auto-solution/issues",
        "Documentation": "https://github.com/jiuchou/auto-solution/wikis",
        "Source Code": "https://github.com/jiuchou/auto-solution/wiki",
    }
)
