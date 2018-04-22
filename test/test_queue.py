import queue.qscript_utility
import sys

queue.qscript_utility.submit_job_into_queue("single", sys.argv[1], "%s %s %s" % ("fenv", sys.argv[1], "0"))
