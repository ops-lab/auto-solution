import hudson.model.*
import hudson.AbortException
import hudson.console.HyperlinkNote
import java.util.concurrent.CancellationException

println " ------------------------------------------------------------------------------ "
println " -                               auto-solution                                - "
println " ------------------------------------------------------------------------------ "
// get current thread / Executor
def thr = Thread.currentThread()
// get current build
def build = thr?.executable

def JENKINS_HOME = build.getEnvironment()['JENKINS_HOME']
def BUILD_URL = build.getEnvironment()['BUILD_URL']

def command = "bash ${JENKINS_HOME}/postbuildscript/postbuildscript.sh ${BUILD_URL}"
def proc = command.execute()
proc.waitFor()
println " [auto-solution] return code: ${proc.exitValue()}"
println " [auto-solution] stdout: ${proc.in.text}"
println " [auto-solution] stderr: ${proc.err.text}"

println " [auto-solution] Success!"
println " ------------------------------------------------------------------------------ \n"
