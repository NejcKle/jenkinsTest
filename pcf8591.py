import smbus2
import logging
import time
'''
The address consists of a fixed part and a programmable part. The programmable
part must be set according to the address pins A0, A1 and A2. 
'''

DEVICE_ADDRESS = 0x09

class Pcf8591(object):
    #A0, A1, A2 should be either 0 or 1, vref is reference voltage for analog pins, vagnd is analog ground
    def __init__(self, A0, A1, A2, vref, vagnd):
        """Init smbus channel and Pcf8591 driver on specified address."""
        try:
            self.i2c_bus = smbus2.SMBus(1)
            self.i2c_address = DEVICE_ADDRESS << 3 | A2 << 2 | A1 << 1 | A0
            self.ref_voltage = vref
            self.agnd_voltage = vagnd

            if (vref - vagnd < 0):
                self.i2c_bus = None
            
        except:
            logging.error("Bus on channel {} is not available.".format(1))
            logging.info("Available busses are listed as /dev/i2c*")
            self.i2c_bus = None
    
    def DAC(self, digital_value):
        """Converts discrete value and sets voltage on pin AOUT."""
        control_byte = self.set_control_byte(0, False, 0, True)
        #writing 2 bytes of data
        self.i2c_bus.write_byte_data(self.i2c_address, control_byte, digital_value)
    
    def analog_read_raw(self, pin):
        """Returns raw value read on specified pin -- only to be used internally."""
        control_byte = self.set_control_byte(pin, False, 0, False)
        #writing one byte of data
        self.i2c_bus.write_byte(self.i2c_address, control_byte)

        self.i2c_bus.read_byte(self.i2c_address) #empty read, always returns 80h
        return self.i2c_bus.read_byte(self.i2c_address)

    def analog_read_AIN0_raw(self):
        """Returns raw value read on pin A0."""
        return self.analog_read_raw(0)

    def analog_read_AIN1_raw(self):
        """Returns raw value read on pin A1."""
        return self.analog_read_raw(1)

    def analog_read_AIN2_raw(self):
        """Returns raw value read on pin A2."""
        return self.analog_read_raw(2)

    def analog_read_AIN3_raw(self):
        """Returns raw value read on pin A3."""
        return self.analog_read_raw(3)

    def analog_read_all_raw(self):
        """Returns list of raw readouts on pins A0 to A4."""
        reads = [] #list of reads from all channels (4)

        control_byte = self.set_control_byte(0, True, 0, False) #auto ad_channel
       # print(control_byte)
        self.i2c_bus.write_byte(self.i2c_address, control_byte)
        self.i2c_bus.read_byte(self.i2c_address) #empty read, always returns 80h

        reads.append(self.i2c_bus.read_byte(self.i2c_address))
        reads.append(self.i2c_bus.read_byte(self.i2c_address))
        reads.append(self.i2c_bus.read_byte(self.i2c_address))
        reads.append(self.i2c_bus.read_byte(self.i2c_address))

        return reads

    def voltage_read(self, pin):
        """Returns read voltage on specified pin -- only to be used internally."""
        control_byte = self.set_control_byte(pin, False, 0, False)

        self.i2c_bus.write_byte(self.i2c_address, control_byte)
        self.i2c_bus.read_byte(self.i2c_address) #empty read, always returns 80h
        return (self.ref_voltage - self.agnd_voltage) / 256.0 * self.i2c_bus.read_byte(self.i2c_address)

    def voltage_read_AIN0(self):
        """Returns read voltage on pin A0."""
        return self.voltage_read(0)

    def voltage_read_AIN1(self):
        """Returns read voltage on pin A1."""
        return self.voltage_read(1)

    def voltage_read_AIN2(self):
        """Returns read voltage on pin A2."""
        return self.voltage_read(2)

    def voltage_read_AIN3(self):
        """Returns read voltage on pin A3."""
        return self.voltage_read(3)

    def voltage_read_all(self):
        """Returns list of voltage readouts on pins A0 to A4."""
        reads = []

        control_byte = self.set_control_byte(0, True, 0, False) #auto increment ad_channel

        self.i2c_bus.write_byte(self.i2c_address, control_byte)
        self.i2c_bus.read_byte(self.i2c_address) #empty read, always returns 80h

        reads.append((self.ref_voltage - self.agnd_voltage) / 256.0 * self.i2c_bus.read_byte(self.i2c_address))
        reads.append((self.ref_voltage - self.agnd_voltage) / 256.0 * self.i2c_bus.read_byte(self.i2c_address))
        reads.append((self.ref_voltage - self.agnd_voltage) / 256.0 * self.i2c_bus.read_byte(self.i2c_address))
        reads.append((self.ref_voltage - self.agnd_voltage) / 256.0 * self.i2c_bus.read_byte(self.i2c_address))

        return reads

    def set_control_byte(self, ad_channel, auto_increment, analog_mode, analog_output):
        """Sets value of control byte (second byte in transmission) -- only to be used internally."""
        control_byte = 0x00
        
        #analog output enable flag - set bit 6 - Analog output enable flag - enables DAC
        if (analog_output == True):
            control_byte |= 1 << 6
        
        #set bits 4 and 5 - Analog Input Programming
        if (analog_mode == 0):
            control_byte |= 0 << 4

        if (analog_mode == 1):
            control_byte |= 1 << 4

        if (analog_mode == 2):
            control_byte |= 2 << 4

        if (analog_mode == 3):
            control_byte |= 3 << 4
        
        #set bit 3 - Auto Increment
        if (auto_increment == True):
            control_byte |= 1 << 2

        #set bits 1 and 2 - A/D Channel Number
        control_byte |= ad_channel
        return control_byte

#test
'''
pin = 0
i2c_address = DEVICE_ADDRESS << 3
address = i2c_address | pin
print(address)
i2c_bus.write_quick(address)
print(i2c_bus.read_byte(address)) #empty read, always returns 80h
print(i2c_bus.read_byte(address))

'''
#pcf = Pcf8591(0, 0, 0, 5.15, 0.0)
'''
pcf.DAC(0)
time.sleep(1)
pcf.DAC(127)
time.sleep(1)
pcf.DAC(255)
time.sleep(1)

A0 = pcf.analog_read_A0_raw()
A1 = pcf.analog_read_A1_raw()
A2 = pcf.analog_read_A2_raw()
A3 = pcf.analog_read_A3_raw()
print(A0)
print(A1)
print(A2)
print(A3)

V0 = pcf.voltage_read_A0()
V1 = pcf.voltage_read_A1()
V2 = pcf.voltage_read_A2()
V3 = pcf.voltage_read_A3()
print(V0)
print(V1)
print(V2)
print(V3)
'''


'''
reads = pcf.analog_read_all_raw()
for i in range(len(reads)):
    print(reads[i])

reads = pcf.voltage_read_all()
for i in range(len(reads)):
    print(reads[i])
    '''