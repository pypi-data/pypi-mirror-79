import json
import logging
import sys

from kaiju_mqtt_py import MqttPacket

# Implementation libs
from ntsjson.log import logger


def make_basic_options_dict(esn, ip, rae, serial, configuration="cloud"):
    """Make the boilerplate "form my options dict" go away."""

    options = {"configuration": configuration}
    if rae is not None:
        options["rae"] = rae
    if esn is not None:
        options["esn"] = esn
    if ip is not None:
        options["ip"] = ip
    if serial is not None:
        options["serial"] = serial
    return options


def set_log_levels_of_libs():
    """Consolidate all interesting loggers to the same level as the local logger."""
    logging.basicConfig(stream=sys.stderr, level=logger.level)
    from ntscli_cloud_lib.log import logger as cloud_logger

    cloud_logger.setLevel(logger.level)
    from kaiju_mqtt_py import KaijuMqtt

    KaijuMqtt.logger.setLevel(logger.level)


def analyze_mqtt_status_packet(packet: MqttPacket):
    print(json.dumps(packet.payload, indent=4))
