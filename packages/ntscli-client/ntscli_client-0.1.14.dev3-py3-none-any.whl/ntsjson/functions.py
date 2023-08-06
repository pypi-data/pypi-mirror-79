import atexit
from io import BytesIO
import json
import logging
import os
import platform
import sys
import threading

from kaiju_mqtt_py import MqttPacket
from ntscli_cloud_lib.automator import DeviceIdentifier

# Implementation libs
from ntsjson import MISSING_TARGET_ERROR
from ntsjson.log import logger

if platform.system() != "Windows":
    import fcntl


def make_basic_options_dict(esn, ip, rae, serial, configuration="cloud"):
    """Make the boilerplate "form my options dict" go away."""

    target: DeviceIdentifier = get_target_from_env(ip, esn, serial)

    if not target.esn and not target.ip and not target.serial:
        logger.critical(MISSING_TARGET_ERROR)
        sys.exit(1)

    options = {"configuration": configuration}
    if rae:
        options["rae"] = rae
    if target.esn:
        options["esn"] = target.esn
    if target.ip:
        options["ip"] = target.ip
    if serial:
        options["serial"] = target.serial
    return options


def set_log_levels_of_libs():
    """Consolidate all interesting loggers to the same level as the local logger."""
    logging.basicConfig(stream=sys.stderr, level=logger.level)
    from ntscli_cloud_lib.log import logger as cloud_logger

    logging.getLogger("urllib3.connectionpool").setLevel(logging.CRITICAL)

    cloud_logger.setLevel(logger.level)
    from kaiju_mqtt_py import KaijuMqtt

    KaijuMqtt.logger.setLevel(logger.level)


def analyze_mqtt_status_packet(packet: MqttPacket):
    print(json.dumps(packet.payload, indent=4))


write_lock = threading.Lock()


def nonblock_target_write(target_: BytesIO, s_: str):
    """
    Write and flush a string as utf-8

    Writing large segments of data to a stdout type stream can crash your app if you do it wrong.
    """

    def write_last(target: BytesIO, s: str):
        with write_lock:
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
                    written = written + os.write(target.fileno(), to_write[written:])
                except BlockingIOError:
                    # logger.debug("HEY DAVE! HERE!")
                    continue
                except OSError as e:
                    logger.debug(e)

            try:
                written + os.write(target.fileno(), "\n".encode("utf-8"))
            except BlockingIOError:
                logger.debug("HEY DAVE! HERE! ANOTHER ONE!")
            except OSError as e:
                logger.debug(e)

            target.flush()

    atexit.register(write_last, target=target_, s=s_)


def get_target_from_env(ip, esn, serial) -> DeviceIdentifier:
    """
    Form a DeviceIdentifier with defaults from the env.

    :return:
    """
    if not ip and not esn and not serial:
        di = DeviceIdentifier(esn=os.getenv("ESN"), ip=os.getenv("DUT_IP"), serial=os.getenv("DUT_SERIAL"))
    else:
        return DeviceIdentifier(esn=esn, ip=ip, serial=serial)
    return di
