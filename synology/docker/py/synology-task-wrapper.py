#!/usr/bin/env python
#
# Task wrapper to run inside a custom docker container on a Synology NAS running DSM.
#
# Acts on a number of environment variables which derive what to do:
#
# DSM_PRIVATE_KEY         Private (SSH) key used to pull from repos (usually just secrets)
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
import git
import os
import shutil
import subprocess
import sys

# Functions
#

# Clean up and exit
#
def die(code):

  try:
    shutil.rmtree(TMPDIR)
  except:
    print("Cleaning up")

  KEYFILE.close()

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
DSM_PRIVATE_KEY = str(os.environ.get('DSM_PRIVATE_KEY'))
DSM_GIT_SECRETREPO = str(os.environ.get('DSM_GIT_SECRETREPO'))
DSM_GIT_CODEREPO = str(os.environ.get('DSM_GIT_CODEREPO'))
DSM_TASK_EXECUTE = str(os.environ.get('DSM_TASK_EXECUTE'))
TMPDIR = '/tmp/synology-task-wrapper/'
SECRETS = TMPDIR + 'secrets/'
CODE = TMPDIR + 'code/'

# Exit codes
#
EXIT_ALL_OK = 0
EXIT_SECRETS_CLONE_FAIL=100
EXIT_CODE_CLONE_FAIL=110
EXIT_TASK_FAIL=120
EXIT_KEY_FILE=130

# Clean down temp area
#
#shutil.rmtree(TMPDIR)

# Get involved!
#
print("Private key will be: REDACTED")
print("Secrets will be pulled from: " + DSM_GIT_SECRETREPO)
print("Secrets will be pulled into: " + SECRETS)
print("Code will be pulled from: " + DSM_GIT_CODEREPO)
print("Code will be pulled into: " + CODE)
print("Task executed will be: " + DSM_TASK_EXECUTE)
print("Temporary area will be: " + TMPDIR)

# Write out our private key
#
REALKEY = eval(DSM_PRIVATE_KEY)
IDENTITY = '/root/.ssh/private_key'
try:
  with open(IDENTITY, 'w') as KEYFILE:
    KEYFILE.write(REALKEY)
    os.chmod(IDENTITY, 0600)
except:
  die(EXIT_KEY_FILE)

KEYFILE.close()

# Make temp area
#
ensure_dir(TMPDIR)

# Pull in secrets repo
#
print("Pulling secrets")
try:
  git.Repo.clone_from(str(DSM_GIT_SECRETREPO), str(SECRETS))
except:
  die(EXIT_SECRETS_CLONE_FAIL)

# Pull in code repo
#
print("Pulling code")
try:
  git.Repo.clone_from(str(DSM_GIT_CODEREPO), str(CODE))
except:
  die(EXIT_CODE_CLONE_FAIL)

# Call task
#
print("Calling " + DSM_TASK_EXECUTE)
TASK_ARRAY = DSM_TASK_EXECUTE.split()
try:
  PROCESS = subprocess.Popen(TASK_ARRAY, stdout=subprocess.PIPE)
  PROCESS.wait()
except:
  die(EXIT_TASK_FAIL)

# Show me
#
for LINE in PROCESS.stdout:
  print(LINE)

# Fin!
#
die(EXIT_ALL_OK)
