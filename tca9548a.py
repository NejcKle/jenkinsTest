"""
TCA9548A I2C switch driver, Texas instruments
8 bidirectional translating switches
I2C SMBus protocol
Manual: tca9548.pdf
Copyright (C) 2019 Vid Rajtmajer <vid@irnas.eu>
"""
import logging
import smbus

from src.constants import I2C_CHANNEL


class TCA9548A(object):
    def __init__(self, address):
        """Init smbus channel and tca driver on specified address."""
        try:
            self.PORTS_COUNT = 8     # number of switches

            self.i2c_bus = smbus.SMBus(I2C_CHANNEL)
            self.i2c_address = address
            if self.get_control_register() is None:
                raise ValueError
        except ValueError:
            logging.error("No device found on specified address!")
            self.i2c_bus = None
        except:
            logging.error("Bus on channel {} is not available.".format(I2C_CHANNEL))
            logging.info("Available busses are listed as /dev/i2c*")
            self.i2c_bus = None

    def get_control_register(self):
        """Read value (length: 1 byte) from control register."""
        try:
            value = self.i2c_bus.read_byte(self.i2c_address)
            return value
        except:
            return None

    def get_channel(self, ch_num):
        """Get channel state (specified with ch_num), return 0=disabled or 1=enabled."""
        if ch_num < 0 or ch_num > self.PORTS_COUNT:
            return None
        register = self.get_control_register()
        if register is None:
            return None
        value = ((register >> ch_num) & 1)
        return value

    def set_control_register(self, value):
        """Write value (length: 1 byte) to control register."""
        try:
            if value < 0 or value > 255:
                return False
            self.i2c_bus.write_byte(self.i2c_address, value)
            return True
        except:
            return False

    def set_channel(self, ch_num, state):
        """Change state (0=disable, 1=enable) of a channel specified in ch_num."""
        if ch_num < 0 or ch_num > self.PORTS_COUNT:
            return False
        if state != 0 and state != 1:
            return False
        current_value = self.get_control_register()
        if current_value is None:
            return False
        if state:
            new_value = current_value | 1 << ch_num
        else:
            new_value = current_value & (255 - (1 << ch_num))
        return_value = self.set_control_register(new_value)
        return return_value

    def __del__(self):
        """Driver destructor."""
        self.i2c_bus = None



# ------------------------ Test code ----------------------------
tca = TCA9548A(0x70)
print(bin(tca.get_control_register()))
num = int("00001000", 2)
tca.set_control_register(num)    # enable all connected devices
print(bin(tca.get_control_register()))
'''
# tca.set_control_register(0)     # disable all channels
# tca.set_channel(6, 1)    # enable extender
# print(tca.get_channel(4))
'''
