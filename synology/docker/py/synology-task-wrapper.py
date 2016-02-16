#!/usr/bin/env python
#
# Task wrapper to run inside a custom docker container on a Synology NAS running DSM.
#
# Acts on a number of environment variables which derive what to do:
#
# DSM_PRIVATE_KEY         Private (SSH) key used to pull from repos (usually just secrets) - OPTIONAL
# DSM_WORKSPACE           Directory designed as a workspace e.g. where git repos will be pulled into
# DSM_GIT_SECRETREPO      URL of git repository containing secrets e.g. keys - OPTIONAL
# DSM_GIT_CODEREPO        URL of git repository containing tasks that can be run - OPTIONAL
# DSM_TASK_EXECUTE        Task to execute (pulled in via git) - MANDATORY
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

  print("Cleaning up")
  try:
    shutil.rmtree(DSM_WORKSPACE)
  except:
    pass

  try:
      KEYFILE.close()
  except:
    pass

  print("Exit with code " + str(code))
  sys.exit(code)

# Make a directory
#
def ensure_dir(MKDIR):
  DIR = os.path.dirname(MKDIR)
  if not os.path.exists(DIR):
    os.makedirs(DIR)

# Get and set variables
#
DSM_PRIVATE_KEY = str(os.environ.get('DSM_PRIVATE_KEY'))
DSM_GIT_SECRETREPO = str(os.environ.get('DSM_GIT_SECRETREPO'))
DSM_GIT_CODEREPO = str(os.environ.get('DSM_GIT_CODEREPO'))
DSM_WORKSPACE = str(os.environ.get('DSM_WORKSPACE'))
DSM_TASK_EXECUTE = str(os.environ.get('DSM_TASK_EXECUTE'))

# Exit codes
#
EXIT_ALL_OK = 0
EXIT_SECRETS_CLONE_FAIL=100
EXIT_CODE_CLONE_FAIL=110
EXIT_TASK_FAIL=120
EXIT_KEY_FILE=130
EXIT_NO_TASK=140

# Get involved!
#
if DSM_WORKSPACE != 'None' and DSM_WORKSPACE.strip():
  pass
else:
  DSM_WORKSPACE = '/tmp/synology-task-wrapper/'
print("Temporary workspace will be: " + DSM_WORKSPACE)

SECRETS = DSM_WORKSPACE + 'secrets/'
CODE = DSM_WORKSPACE + 'code/'
IDENTITY = '/root/.ssh/private_key'

if DSM_PRIVATE_KEY != 'None' and DSM_PRIVATE_KEY.strip():
  print("Private key will be: REDACTED")
  print("Private key will be written into: " + IDENTITY)
else:
  print("No Private key specified")

if DSM_GIT_SECRETREPO != 'None' and DSM_GIT_SECRETREPO.strip():
  print("Secrets will be pulled from: " + DSM_GIT_SECRETREPO)
  print("Secrets will be pulled into: " + SECRETS)
else:
  print("No Secrets repository specified")

if DSM_GIT_CODEREPO != 'None' and DSM_GIT_CODEREPO.strip():
  print("Code will be pulled from: " + DSM_GIT_CODEREPO)
  print("Code will be pulled into: " + CODE)
else:
  print("No Code repository specified")

if DSM_TASK_EXECUTE != 'None' and DSM_TASK_EXECUTE.strip():
  print("Task executed will be: " + DSM_TASK_EXECUTE)
else:
  print("No task specified in DSM_TASK_EXECUTE")
  die(EXIT_NO_TASK)

# Clean down temp area
#
print("Cleaning up")
try:
  shutil.rmtree(DSM_WORKSPACE)
except:
  pass

# Write out our private key
#
if DSM_PRIVATE_KEY != 'None' and DSM_PRIVATE_KEY.strip():
  REALKEY = eval(DSM_PRIVATE_KEY)
  print("Creating private key")
  try:
    with open(IDENTITY, 'w') as KEYFILE:
      KEYFILE.write(REALKEY)
      os.chmod(IDENTITY, 0600)
  except:
    die(EXIT_KEY_FILE)

  KEYFILE.close()

# Make temp area
#
ensure_dir(DSM_WORKSPACE)

# Pull in secrets repo
#
if DSM_GIT_SECRETREPO != 'None' and DSM_GIT_SECRETREPO.strip():
  print("Pulling secrets")
  try:
    git.Repo.clone_from(str(DSM_GIT_SECRETREPO), str(SECRETS))
  except:
    die(EXIT_SECRETS_CLONE_FAIL)

# Pull in code repo
#
if DSM_GIT_CODEREPO != 'None' and DSM_GIT_CODEREPO.strip():
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
