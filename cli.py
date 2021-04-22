#!/usr/bin/python3




# Imports
import os
import sys
import argparse
import logging




# Local imports
# (Can't use relative imports because this is a top-level script)
import stateless_gpg




# Shortcuts
gpg = stateless_gpg.code.stateless_gpg.gpg




# Notes:
# - Using keyword function arguments, each of which is on its own line,
# makes Python code easier to maintain. Arguments can be changed and
# rearranged much more easily.




# Set up logger for this module. By default, it logs at ERROR level.
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
logger.setLevel(logging.ERROR)
log = logger.info
deb = logger.debug




def setup(
    log_level = 'error',
    debug = False,
    log_timestamp = False,
    log_filepath = None,
    ):
  logger_name = 'cli'
  # Configure logger for this module.
  stateless_gpg.util.module_logger.configure_module_logger(
    logger = logger,
    logger_name = logger_name,
    log_level = log_level,
    debug = debug,
    log_timestamp = log_timestamp,
    log_filepath = log_filepath,
  )
  log('Setup complete.')
  deb('Logger is logging at debug level.')
  # Configure logging levels for stateless_gpg package.
  # By default, without setup, it produces no log output.
  # Optionally, the package could be configured here to use a different log level, by e.g. passing in 'error' instead of log_level.
  stateless_gpg.setup(
    log_level = log_level,
    debug = debug,
    log_timestamp = log_timestamp,
    log_filepath = log_filepath,
  )




def main():

  parser = argparse.ArgumentParser(
    description='Command-Line Interface (CLI) for using the stateless_gpg package.'
  )

  parser.add_argument(
    '-t', '--task',
    help="Task to perform (default: '%(default)s').",
    default='hello',
  )

  parser.add_argument(
    '-l', '--logLevel', type=str,
    choices=['debug', 'info', 'warning', 'error'],
    help="Choose logging level (default: '%(default)s').",
    default='info',
  )

  parser.add_argument(
    '-d', '--debug',
    action='store_true',
    help="Sets logLevel to 'debug'. This overrides --logLevel.",
  )

  parser.add_argument(
    '-s', '--logTimestamp',
    action='store_true',
    help="Choose whether to prepend a timestamp to each log line.",
  )

  parser.add_argument(
    '-o', '--logToFile',
    action='store_true',
    help="Choose whether to save log output to a file.",
  )

  parser.add_argument(
    '-p', '--logFilepath',
    help="The path to the file that log output will be written to.",
    default='log_edgecase_client.txt',
  )

  a = parser.parse_args()

  log_filepath = a.logFilepath if a.logToFile else None

  # Setup
  setup(
    log_level = a.logLevel,
    debug = a.debug,
    log_timestamp = a.logTimestamp,
    log_filepath = log_filepath,
  )

  # Run top-level function (i.e. the appropriate task).
  tasks = 'hello fail'.split()
  if a.task not in tasks:
    print("Unrecognised task: {}".format(a.task))
    stop()
  globals()[a.task](a)  # run task.




def hello(a):
  data = "hello world\n"
  log("data = " + data.strip())
  private_key_file = 'stateless_gpg/data/test_key_1_private_key.txt'
  private_key = open(private_key_file).read()
  signature = gpg.make_signature(private_key, data)
  public_key_file = 'stateless_gpg/data/test_key_1_public_key.txt'
  public_key = open(public_key_file).read()
  result = gpg.verify_signature(public_key, data, signature)
  log("result = " + str(result))
  if not result:
    raise Exception("Failed to create and verify signature")
  print("Signature created and verified.")




def fail(a):
  data = "hello world\n"
  log("data = " + data.strip())
  private_key_file = 'stateless_gpg/data/test_key_1_private_key.txt'
  private_key = open(private_key_file).read()
  signature = gpg.make_signature(private_key, data)
  public_key = "invalid key data"
  result = gpg.verify_signature(public_key, data, signature)
  log("result = " + str(result))
  if not result:
    raise Exception("Failed to create and verify signature")
  print("Signature created and verified.")




if __name__ == '__main__':
  main()