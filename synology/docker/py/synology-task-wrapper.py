#!/usr/bin/env python
#
# Task wrapper to run inside a custom docker container on a Synology NAS running DSM.
#
# Acts on a number of environment variables which derive what to do:
#
# DSM_GIT_SECRETREPO      URL of git repository containing secrets e.g. keys
# DSM_GIT_CODEREPO        URL of git repository containing tasks that can be run
# DSM_TASK_EXECUTE        Task to execute (pulled in via git)
#
# Other variables may be defined and passed to docker run (using an environments file) which can then be passed on
# to the task being executed by this wrapper.
#
# Tested with:
#
# Synology DS415+
# DSM 5.2-5644 Update 3
# Docker 1.6.2-0036 (on DSM)
# Gitlab 8.2.3-0015 (on DSM)
#
# It is recommened that the repository containing secrets is kept private for obvious reasons. For example, hosted
# by Gitlab running on the same NAS.
#

# Imports
#
import os
import shutil
import sys

# Functions
#

# Clean up and exit
def die(code):

  #shutil.rmtree(TMPDIR)

  print("Exit with code " + str(code))
  sys.exit(code)

# Make a directory
#
def ensure_dir(TMPDIR):
  DIR = os.path.dirname(TMPDIR)
  if not os.path.exists(DIR):
    os.makedirs(DIR)

# Get and set variables
#
DSM_GIT_SECRETREPO = str(os.environ.get('DSM_GIT_SECRETREPO'))
DSM_GIT_CODEREPO = str(os.environ.get('DSM_GIT_CODEREPO'))
DSM_TASK_EXECUTE = str(os.environ.get('DSM_TASK_EXECUTE'))
TMPDIR = '/tmp/synology-task-wrapper/'

# Get involved!
#
print("Secrets will be pulled from:" + DSM_GIT_SECRETREPO)
print("Code will be pulled from: " + DSM_GIT_CODEREPO)
print("Task executed will be: " + DSM_TASK_EXECUTE)
print("Temporary area will be: " + TMPDIR)

# Make temp area
#
ensure_dir(TMPDIR)

die(0)
