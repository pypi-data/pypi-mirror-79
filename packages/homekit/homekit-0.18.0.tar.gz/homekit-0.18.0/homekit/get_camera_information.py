# !/usr/bin/env python3

#
# Copyright 2018-2020 Joachim Lusiardi
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import argparse
import sys
import logging
from base64 import b64decode

import tlv8

from homekit.controller import Controller
from homekit.log_support import setup_logging, add_log_arguments
from homekit.model.characteristics import CharacteristicsTypes

STREAMING_STATUS_CHAR = CharacteristicsTypes.get_uuid(CharacteristicsTypes.STREAMING_STATUS)
SUPPORTED_RTP_CONFIGURATION_CHAR = CharacteristicsTypes.get_uuid(CharacteristicsTypes.SUPPORTED_RTP_CONFIGURATION)
SUPPORTED_VIDEO_STREAM_CONFIGURATION_CHAR = CharacteristicsTypes.get_uuid(CharacteristicsTypes.SUPPORTED_VIDEO_STREAM_CONFIGURATION)

def setup_args_parser():
    parser = argparse.ArgumentParser(description='HomeKit get_resource - retrieve value of snapshot '
                                                 'resource  from paired HomeKit accessories.')
    parser.add_argument('-f', action='store', required=True, dest='file', help='File with the pairing data')
    parser.add_argument('-a', action='store', required=True, dest='alias', help='alias for the pairing')
    parser.add_argument('-A', action='store', dest='accessory_id', help='Accessory id for the camera (optional)')
    add_log_arguments(parser)
    return parser.parse_args()


def analyse_streaming_status(value):
    result = tlv8.decode(value, {1: tlv8.DataType.INTEGER})
    print('streaming status', tlv8.format_string(result))


def analyse_supported_rtp_configuration(value):
    result = tlv8.decode(value, {2: tlv8.DataType.INTEGER})
    print('supported_rtp_configuration', tlv8.format_string(result))


def analyse_supported_video_stream_configuration(value):
    result = tlv8.decode(value, {
        1: {
            1: tlv8.DataType.INTEGER,
            2: {
                1: tlv8.DataType.INTEGER,
                2: tlv8.DataType.INTEGER,
                3: tlv8.DataType.INTEGER,
                4: tlv8.DataType.INTEGER
            },
            3: {
                1: tlv8.DataType.INTEGER,
                2: tlv8.DataType.INTEGER,
                3: tlv8.DataType.INTEGER,
            }
        }
    })
    print('supported_video_stream_configuration', tlv8.format_string(result))

if __name__ == '__main__':
    args = setup_args_parser()

    setup_logging(args.loglevel)

    controller = Controller()
    controller.load_data(args.file)
    if args.alias not in controller.get_pairings():
        print('"{a}" is no known alias'.format(a=args.alias))
        sys.exit(-1)

    pairing = controller.get_pairings()[args.alias]

    for accessory in pairing.list_accessories_and_characteristics():
        for service in accessory['services']:
            for characteristic in service['characteristics']:
                char_type = characteristic['type']
                if char_type == STREAMING_STATUS_CHAR:
                    char_value = b64decode(characteristic['value'])
#                    analyse_streaming_status(char_value)
                if char_type == SUPPORTED_RTP_CONFIGURATION_CHAR:
                    char_value = b64decode(characteristic['value'])
                    analyse_supported_rtp_configuration(char_value)
                if char_type == SUPPORTED_VIDEO_STREAM_CONFIGURATION_CHAR:
                    char_value = b64decode(characteristic['value'])
 #                   analyse_supported_video_stream_configuration(char_value)
