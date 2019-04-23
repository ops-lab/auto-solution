#!/usr/bin/env python
# -*- coding: utf-8 -*-

# =============================================================================
# Get error info from build log and give solution by email automatic.
# =============================================================================
import argparse
import jenkins
import os
import pandas
import random
import re
import smtplib
import sys
from email.header import Header
from email.mime.text import MIMEText
from email.utils import formataddr, parseaddr

from DBAdapter import MySQLAgile, SQLAgile

if sys.version_info.major == 2:
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
elif sys.version_info.major == 3:
    import importlib
    importlib.reload(sys)

MYSQL_DB_HOST = "127.0.0.1"
MYSQL_DB_USER = 'root'
MYSQL_DB_PASSWORD = 'root'
MYSQL_DB_NAME = 'autosolution'

SQL_DB_HOST = "127.0.0.1"
SQL_DB_USER = 'root'
SQL_DB_PASSWORD = 'root'
SQL_DB_NAME = 'userinfo'

jenkins_url = "JENKINS_URL"
jenkins_username = "jenkins"
jenkins_password = "jenkins_password"

def parse_parameters():
    usage = "Usage: %prog [option] args"
    parser = argparse.ArgumentParser(description=usage)
    parser.add_argument("--build_url", dest="build_url", default=None,
                        help="BUILD_URL default value is None.")

    args = parser.parse_args()
    # parser.print_help()
    print("python {0} --build_url {1}".format(os.path.basename(__file__),
                                              args.build_url))
    return args

def get_case_keys(mysql_agile):
    """Get all case_key in case_lib database.
    And return a list.
    """
    case_keys = []

    data = mysql_agile.execute("select case_key from case_lib;")
    for case_key in data:
        case_keys.append("".join(case_key))

    return case_keys


def update_content(content, mysql_agile, case_key, err_info):
    # 根据case_key获取案例库内容
    sql_cmd = "SELECT case_key, case_info, case_type, case_description, "\
              "case_solution, case_remark FROM case_lib WHERE "\
              "case_key='{0}';".format(case_key.replace("'", "\\'"))
    case_key = case_key.replace("\*", "*").replace("\[", "[")
    data = mysql_agile.execute(sql_cmd)
    if len(data) == 0:
        remark = "WARNING: No solution to the problem was found. " \
                 "Please contact the technical support staff. " \
                 "Contact jiuchou@email.com. "
        content[0].append(case_key)
        content[1].append(err_info)
        content[2].append(" ---- ")
        content[3].append(" ---- ")
        content[4].append(" ---- ")
        content[5].append(remark)
    else:
        for i in range(len(data)):
            content[0].append(case_key)
            content[1].append(err_info)
            content[2].append(data[i][2])
            content[3].append(data[i][3])
            # content[4].append(data[i][4].replace("\n", "<br/>"))
            content[4].append(data[i][4])
            content[5].append(data[i][5])

    return content

def convert_to_html(title, content):
    d = {}
    index = 0
    for t in title:
        d[t] = content[index]
        index += 1
    pandas.set_option("expand_frame_repr", True)
    pandas.set_option('max_colwidth', -1)
    df = pandas.DataFrame(d)
    df = df[title]
    html = df.to_html(index=False).replace("\\n", "<br/>")
    return html

def get_solution_html(server, mysql_agile, build_url, filename):
    title = [
        '关键字',
        '报错信息',
        '错误类型（参考）',
        '报错描述（参考）',
        '解决方案（参考，若无帮助可暂忽略或上报作案例共享）',
        '备注'
    ]
    content = [[], [], [], [], [], []]

    # 获取案例库所有案例键
    case_keys = get_case_keys(mysql_agile)
    case_keys = list(set(case_keys))

    # console output information
    project_name = build_url.split("/")[4]
    build_number = build_url.split("/")[5]
    # 获取构建日志
    #   方法1：使用jenkins api接口
    #       存在bug: 构建步骤期间无法检索完整的控制台输出
    #       参考: Jenkins - retrieve full console output during build step
    #       http://www.it1352.com/547426.html
    # output = server.get_build_console_output(project_name, int(build_number))
    #   方法2：使用服务器中的日志文件
    #       问题：依赖于Jenkins Master
    #       JENKINS_HOME: /var/jenkins_home
    output_file = "/var/jenkins_home/jobs/{0}/builds/{1}/log".format(
        project_name, build_number)
    with open(output_file, "r") as fr:
        output = fr.read()

    print(" WARNING: The name of error info file is {0}".format(filename))
    try:
        f = open(filename, "w")
        for case_key in case_keys:
            case_key = case_key.replace("*", "\*").replace("[", "\[")
            if bool(re.search(case_key, output, re.IGNORECASE)):
                err_info = re.findall(".*{0}.*".format(case_key), output)
                err_info = "\n".join(set(err_info))
                update_content(content, mysql_agile, case_key, err_info)
                # 将错误的构建信息内容存储到构建信息表内，留待后续使用
                sql_cmd = "INSERT INTO build_info (job_name, build_number, "\
                          "build_url, err_info, err_key) "\
                          "VALUES('{0}', '{1}', '{2}', '{3}', '{4}');"\
                          .format(project_name,
                                  build_number,
                                  build_url,
                                  err_info,
                                  case_key)
                mysql_agile.execute(sql_cmd)
                # 将错误的构建信息内容存储到构建信息表内
                sql_cmd = "INSERT INTO build_info (job_name, build_number, "\
                          "build_url, err_info, err_key) "\
                          "VALUES('{0}', '{1}', '{2}', '{3}', '{4}');"\
                          .format(project_name,
                                  build_number,
                                  build_url,
                                  err_info.replace("'", "\\'"),
                                  case_key.replace("'", "\\'"))
                mysql_agile.execute(sql_cmd)
                # 清除重复数据
                from datetime import datetime, timedelta
                time_s = datetime.utcnow() - timedelta(days=1)
                time_e= datetime.utcnow() + timedelta(days=1)
                timestamper_s = "{0}-{1}-{2}".format(
                    time_s.year, time_s.month, time_s.day)
                timestamper_e = "{0}-{1}-{2}".format(
                    time_e.year, time_e.month, time_e.day)
                sql_cmd1 = \
                    "DELETE FROM build_info WHERE "\
                    "create_time>='{0}' AND create_time<='{1}' "\
                    "AND id NOT IN (SELECT id FROM "\
                    "(SELECT MAX(id) AS id FROM build_info WHERE "\
                    "create_time>='{0}' AND create_time<='{1}' "\
                    "GROUP BY build_info.build_url, build_info.err_info "\
                    "HAVING count(*)>=1) m);"\
                    .format(timestamper_s, timestamper_e)
                mysql_agile.execute(sql_cmd1)
                # 保存case_key内容，展示到邮件的 [报错信息] 中
                f.write("".join(err_info) + "\n")
    except Exception as e:
        print(" ERROR: Write file Error! {0}".format(e))
    finally:
        f.close()

    html = convert_to_html(title, content)
    return html

def get_err_info_html(filename):
    err_info_html = ""
    with open(filename, "r") as f:
        for line in f.readlines():
            line = "<li>{0}</li>\n".format(line)
            err_info_html = err_info_html + line
    return err_info_html
def get_html_msg(df_html, build_url, err_info_file):
    project_name = build_url.split("/")[4]
    build_number = build_url.split("/")[5]

    if os.path.exists(err_info_file):
        err_info_html = get_err_info_html(err_info_file)
    else:
        err_info_html = ""

    head = """
        <head>
            <meta charset="utf-8">
            <STYLE TYPE="text/css" MEDIA=screen>

                table.dataframe {
                    border-collapse: collapse;
                    border: 2px solid #a19da2;
                    /*居中显示整个表格*/
                    margin: auto;
                }

                table.dataframe thead {
                    border: 2px solid #91c6e1;
                    background: #f1f1f1;
                    padding: 10px 10px 10px 10px;
                    color: #333333;
                }

                table.dataframe tbody {
                    border: 2px solid #91c6e1;
                    padding: 10px 10px 10px 10px;
                }

                table.dataframe tr {

                }

                table.dataframe th {
                    vertical-align: top;
                    font-size: 14px;
                    padding: 10px 10px 10px 10px;
                    color: #105de3;
                    font-family: arial;
                    text-align: center;
                }

                table.dataframe td {
                    font-size: 11px;
                    text-align: left;
                    padding: 10px 10px 10px 10px;
                }

                body {
                    font-family: 微软雅黑;
                }

                h1 {
                    color: #5db446
                }

                div.header h2 {
                    color: #0000FF;
                    font-family: 黑体;
                }

                div.content h2 {
                    text-align: center;
                    font-size: 28px;
                    text-shadow: 2px 2px 1px #de4040;
                    color: #fff;
                    font-weight: bold;
                    background-color: #008eb7;
                    line-height: 1.5;
                    margin: 20px 0;
                    box-shadow: 10px 10px 5px #888888;
                    border-radius: 5px;
                }

                h3 {
                    font-size: 22px;
                    background-color: rgba(0, 2, 227, 0.71);
                    text-shadow: 2px 2px 1px #de4040;
                    color: rgba(239, 241, 234, 0.99);
                    line-height: 1.5;
                }

                h4 {
                    color: #e10092;
                    font-family: 楷体;
                    font-size: 20px;
                    text-align: center;
                }

                td img {
                    /*width: 60px;*/
                    max-width: 300px;
                    max-height: 300px;
                }

            </STYLE>
        </head>
        """


    body = """
        <body>
            <div align="center" class="header">
                <!--标题部分的信息-->
                <h2 align="left">项目级自助解决方案</h2>
                <p style="font-size: 10pt;" align="left">本邮件是自助解决方案工具自动下发的，请勿回复！</p>
            </div>

            <table width="95%" cellpadding="0" cellspacing="0"
            style="font-size: 11pt; font-family: Tahoma, Arial, Helvetica, sans-serif">
                <tr>
                    <td>
                        <br />
                        <b><font color="#0B610B">工具说明</font></b>
                        <hr size="2" width="100%" align="center" />
                    </td>
                </tr>
                <tr>
                    <p style="color: #ee1313; font-size: 11pt;" align="left">
                        &nbsp;&nbsp;&nbsp;&nbsp;目的：根据错误码快速支撑开发工程师问题定位/解决
                    </p>
                </tr>
                <!--构建信息-->
                <tr>
                    <td>
                        <br />
                        <b><font color="#0B610B">构建信息</font></b>
                        <hr size="2" width="100%" align="center" />
                    </td>
                </tr>
                <tr>
                    <td>
                        <ul>
                            <li>工程名称: {project_name}</li>
                            <li>构建编号: 第{build_number}次构建</li>
                            <li>构建日志: <a href="{build_url}console">{build_url}console</a></li>
                            <li>构建地址: <a href="{build_url}">{build_url}</a></li>
                        </ul>
                    </td>
                </tr>

                <tr>
                    <td>
                        <br />
                        <b><font color="#0B610B">报错信息</font></b>
                        <hr size="2" width="100%" align="center" />
                    </td>
                </tr>
                <tr>
                    <p style="font-size: 11pt;" align="left">
                        WARNING: If error information is not exist, please 
                        contact the technical support staff.<br/>
                        Contact jiuchou@email.com.<br/><br/>
                    </p>
                </tr>
                <tr>
                    <td><ul>{err_info_html}</ul></td>
                </tr>

                <tr>
                    <td>
                        <br />
                        <b><font color="#0B610B">解决方案</font></b>
                        <hr size="2" width="100%" align="center" />
                    </td>
                </tr>
            </table>

            <div class="content">
                <!--解决方案-->
                <div>{df_html}</div>
            </div>
        </body>
        """.format(project_name=project_name,
                   build_number=build_number,
                   build_url=build_url,
                   err_info_html=err_info_html,
                   df_html=df_html)

    html_msg = "<html>" + head + body + "</html>"
    html_msg = html_msg.replace("\n", "").encode("utf-8")
    return html_msg

def get_staffs(sql_agile, build_url):
    staffs = ""
    job_name = build_url.split("/")[4]
    if len(job_name.split("_")) > 1:
        project_number = job_name.split("_")[1]
        staff = sql_agile.get_staff(project_number)
        staffs = ",".join([j for i in staff for j in i])
    return staffs

def get_recipients(server, build_url):
    recipients = ""

    job_name = build_url.split("/")[4]
    config_info = server.get_job_config(job_name)
    lines = config_info.split("\n")
    for line in lines:
        if "<recipientList>" in line:
            recipients = line.split(">")[1].split("<")[0].replace(" ", "")
            break
    return recipients

def covert_to_receiver(sql_agile, recipient):
    email = sql_agile.get_email(recipient)
    receiver = "".join([j for i in email for j in i])
    return receiver

def get_receivers(sql_agile, recipients):
    i = 0
    for recipient in recipients.split(","):
        if recipient.isdigit():
            receiver = covert_to_receiver(sql_agile, recipient)
        else:
            receiver = recipient

        if i == 0:
            receivers = receiver
        else:
            receivers = "{0},{1}".format(receiver, receivers)
        i += 1
    return receivers

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((
        Header(name, "utf-8").encode(),
        addr.encode("utf-8") if isinstance(addr, unicode) else addr
    ))

def send_mail(html_msg, project_name, receivers):
    smtp_host = "mail.email.com"
    smtp_port = 25
    username = "jenkins@email.com"
    password = "jenkins_password"

    sender = "jenkins@email.com"
    cc = "jiuchou@email.com"

    mail_msg = MIMEText(html_msg, "html", "utf-8")
    mail_msg['From'] = _format_addr(sender)
    mail_msg['To'] = receivers
    mail_msg['Cc'] = cc
    print(" Email sender: {0}".format(sender))
    print(" Email receivers: {0}".format(receivers))

    project_name = build_url.split("/")[4]
    build_number = build_url.split("/")[5]
    subject = "[auto-solution]Coverity: {0} Build # {1}".format(project_name,
                                                                build_number)
    mail_msg['Subject'] = Header(subject, "utf-8")

    try:
        smtp_server = smtplib.SMTP(smtp_host, smtp_port)
        smtp_server.set_debuglevel(0)
        smtp_server.login(username, password)
        smtp_server.sendmail(sender,
                             receivers.split(",") + cc.split(","),
                             mail_msg.as_string())
    except smtplib.SMTPException:
        print("ERROR: Send email failed!")
    finally:
        smtp_server.quit()

if __name__ == "__main__":
    args = parse_parameters()
    build_url = args.build_url

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    ARCHIVE_DIR = os.path.join(BASE_DIR, "archive")
    if not os.path.exists(ARCHIVE_DIR):
        os.mkdir(ARCHIVE_DIR)
    random_string = "".join(random.sample("abcdefghijklmnopqrstuvwxyz", 10))
    err_info_file = "{0}/ErrorInfo_{1}".format(ARCHIVE_DIR, random_string)

    server = jenkins.Jenkins(jenkins_url, jenkins_username, jenkins_password)
    sql_agile = SQLAgile(SQL_DB_HOST, SQL_DB_USER, SQL_DB_PASSWORD, SQL_DB_NAME)
    mysql_agile = MySQLAgile(MYSQL_DB_HOST, MYSQL_DB_USER,
                             MYSQL_DB_PASSWORD, MYSQL_DB_NAME)
    try:
        df_html = get_solution_html(
            server, mysql_agile, build_url, err_info_file)
        html_msg = get_html_msg(df_html, build_url, err_info_file)

        staffs = get_staffs(sql_agile, build_url)
        recipients = get_recipients(server, build_url)
        recipients = "{0},{1}".format(staffs, recipients)
        # delete repeat data
        recipients = ",".join(set(recipients.replace(' ', '').split(',')))
        receivers = get_receivers(sql_agile, recipients)
    except Exception as e:
        print("ERROR: {0}".format(e))
    finally:
        sql_agile.close()
        mysql_agile.close()

    send_mail(html_msg, build_url, receivers)


