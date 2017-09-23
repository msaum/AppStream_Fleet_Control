#!/usr/bin/env python
"""
Name: fleet_control.py
Purpose: Manage starting and stopping an Appstream Fleet
Version: 1.0
Date: September 23, 2017
Author: Mark Saum
Email: mark@saum.net
GitHub: https://github.com/msaum

-------------------------------------------------------------------------------

Revisions:
1.0 - Initial build

-------------------------------------------------------------------------------

References:

-------------------------------------------------------------------------------
"""

__author__ = 'msaum'

import argparse
import boto3
import logging
import os
import json
from ConfigParser import SafeConfigParser

# -------------------------------------------------------------------------------
# setup simple logging for INFO
# -------------------------------------------------------------------------------
logger = logging.getLogger()
logger.setLevel('CRITICAL') # Default

# -------------------------------------------------------------------------------
# Process Arguments
# -------------------------------------------------------------------------------
parser = argparse.ArgumentParser(description='Snapshot an arbitrary volume via Lambda..')
parser.add_argument("--debug", "-d", help="turn on debugging output", action="store_true")
parser.add_argument("--verbose", "-v", help="turn on program status information output", action="store_true")
parser.add_argument("--start", help="start a fleet", action="store_true")
parser.add_argument("--stop", help="stop a fleet", action="store_true")
parser.add_argument("--profile", "-p", type=str, help="use an AWS profile context for local debugging")
args = parser.parse_args()
if args.verbose:
    logger.setLevel('INFO')
if args.debug:
    logger.setLevel('DEBUG')

# -------------------------------------------------------------------------------
# Read program configuration information
# -------------------------------------------------------------------------------
logging.info('* ' + os.path.basename(__file__) + ' parsing configuration file')
parser = SafeConfigParser()
try:
    parser.read('fleet.ini')
    fleet_name = parser.get('global', 'fleet_name')
except:
    logging.error('Failed to parse fleet.ini configuration file.', exc_info=True)
    raise


# -------------------------------------------------------------------------------
# start_fleet Lambda Entry Point
# -------------------------------------------------------------------------------
def start_fleet(event, context):
    if event != '':                 # If running in a Lambda function, turn on INFO debugging
        logger.setLevel('INFO')

    logging.info('** ' + os.path.basename(__file__) + ' start_fleet begin')

    try:
        if args.profile:
            session = boto3.Session(profile_name=args.profile)
            client = session.client('appstream')
        else:
            client = boto3.client('appstream')
    except:
        logging.error('Failed to create connection to AWS appstream via boto3.' , exc_info=True)
        raise

    # http://boto3.readthedocs.io/en/latest/reference/services/appstream.html#AppStream.Client.start_fleet
    try:
        logging.info(client.start_fleet(Name=fleet_name))
    except:
        logging.error('Failed to start_fleet: ' + fleet_name , exc_info=True)
        raise

    # Lambda Status Info
    if context != '':
        logging.info("*** Log stream name: %s", context.log_stream_name)
        logging.info("*** Log group name: %s", context.log_group_name)
        logging.info("*** Request ID: %s", context.aws_request_id)
        logging.info("*** Mem. limits(MB): %s", context.memory_limit_in_mb)
        logging.info("*** Time remaining (MS): %s", context.get_remaining_time_in_millis())
    logging.info('** ' + os.path.basename(__file__) + ' start_fleet end')


# -------------------------------------------------------------------------------
# stop_fleet Lambda Entry Point
# -------------------------------------------------------------------------------
def stop_fleet(event, context):
    if event != '':                 # If running in a Lambda function, turn on INFO debugging
        logger.setLevel('INFO')
    logging.info('** ' + os.path.basename(__file__) + ' stop_fleet begin')

    try:
        if args.profile:
            session = boto3.Session(profile_name=args.profile)
            client = session.client('appstream')
        else:
            client = boto3.client('appstream')
    except:
        logging.error('Failed to create connection to AWS appstream via boto3.' , exc_info=True)
        raise

    # http://boto3.readthedocs.io/en/latest/reference/services/appstream.html#AppStream.Client.start_fleet
    try:
        logging.info(client.stop_fleet(Name=fleet_name))
    except:
        logging.error('Failed to start_fleet: ' + fleet_name , exc_info=True)
        raise

    # Lambda Status Info
    if context != '':
        logging.info("*** Log stream name: %s", context.log_stream_name)
        logging.info("*** Log group name: %s", context.log_group_name)
        logging.info("*** Request ID: %s", context.aws_request_id)
        logging.info("*** Mem. limits(MB): %s", context.memory_limit_in_mb)
        logging.info("*** Time remaining (MS): %s", context.get_remaining_time_in_millis())
    logging.info('** ' + os.path.basename(__file__) + ' stop_fleet end')


# -------------------------------------------------------------------------------
# Console Entry Point
# -------------------------------------------------------------------------------
if __name__ == "__main__":
    logging.info('** ' + os.path.basename(__file__) + ' __main__ start')

    if (not args.start) & (not args.stop):
        logging.error('** ' + os.path.basename(__file__) + ' must choose start or stop option when executing locally')
        exit(1)

    if args.start & args.stop:
        logging.error('** ' + os.path.basename(__file__) +
                      ' must choose only one of start or stop option when executing locally')
        exit(1)

    if args.start:
        start_fleet('', '')

    if args.stop:
        stop_fleet('', '')

    logging.info('** ' + os.path.basename(__file__) + ' __main__ end')
