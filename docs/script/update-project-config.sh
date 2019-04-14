#!/bin/bash

department_name=$1

ROOT_PATH=$(cd $(dirname $0); pwd -P)

JENKINS_CLI_PATH="/home/jenkins/.jenkins/war/WEB-INF/jenkins-cli.jar"
JENKINS_URL="http://127.0.0.1:8080"

JENKINS_USERNAME="jenkins"
JENKINS_PASSWORD="xxxxxxxx"

JENKINS_CMD_PREFIX="java -jar ${JENKINS_CLI_PATH} -s ${JENKINS_URL}"

${JENKINS_CMD_PREFIX} login --username ${JENKINS_USERNAME} --password ${JENKINS_PASSWORD}

if [[ "${department_name}" == "" ]]; then
    jobs=$(${JENKINS_CMD_PREFIX} list-jobs)
else
    jobs=$(${JENKINS_CMD_PREFIX} list-jobs | grep "${department_name}")
fi
for job in ${jobs[@]}; do
    ${JENKINS_CMD_PREFIX} get-job ${job} > config.xml

    sed -i "/<org.jenkinsci.plugins.postbuildscript.PostBuildScript/,/<\/org.jenkinsci.plugins.postbuildscript.PostBuildScript>/d" config.xml
    sed -i "/org.jenkinsci.plugins.postbuildscript.PostBuildScript/d" config.xml

    line=$(grep -rn "</publishers>" config.xml | awk -F ':' '{print $1}')
    line=$(expr ${line} - 1)
    sed -i "${line}r PostBuildScriptConfig" config.xml

    ${JENKINS_CMD_PREFIX} update-job ${job} < config.xml
done

rm -f config.xml
