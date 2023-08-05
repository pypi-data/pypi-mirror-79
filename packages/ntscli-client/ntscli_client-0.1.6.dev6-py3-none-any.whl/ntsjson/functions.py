from io import BytesIO
import json
import logging
import os
import platform
import sys

from kaiju_mqtt_py import MqttPacket

# Implementation libs
from ntsjson.log import logger

if platform.system() != "Windows":
    import fcntl


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


def nonblock_target_write(target: BytesIO, s: str):
    """
    Write and flush a string as utf-8

    Writing large segments of data to a stdout type stream can crash your app if you do it wrong.
    """
    if platform.system() != "Windows":
        # make stdout/file a non-blocking file
        # this is apparently not possible like this in Windows, so we're putting a band-aid on it for today
        fd = target.fileno()
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

    to_write = s.encode("utf-8")
    written = 0
    while written < len(s):
        try:
            written = written + os.write(sys.stdout.fileno(), to_write[written:])
        except OSError as e:
            logger.debug(e)
    try:
        written + os.write(sys.stdout.fileno(), "\n".encode("utf-8"))
    except OSError as e:
        logger.debug(e)

    target.flush()
