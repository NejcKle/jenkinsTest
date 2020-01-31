import smbus2
import logging
import time
'''
The address consists of a fixed part and a programmable part. The programmable
part must be set according to the address pins A0, A1 and A2. 

!!! IMPORTANT !!!
When using internal oscillator EXT pin must be wired to Vss
'''

DEVICE_ADDRESS = 0x09
USING_INTERNAL_OSCILLATOR = True #when using internal oscillator analog output enable flag should be set to True

class Pcf8591(object):
    #A0, A1, A2 should be either 0 or 1, vref is reference voltage for analog pins, vagnd is analog ground
    def __init__(self, A0, A1, A2, vref, vagnd):
        """Init smbus channel and Pcf8591 driver on specified address."""
        try:
            self.i2c_bus = smbus2.SMBus(1)
            self.i2c_address = DEVICE_ADDRESS << 3 | A2 << 2 | A1 << 1 | A0
            self.ref_voltage = vref #reference voltage and analog ground voltage are necessary for converting digital readings to 
            self.agnd_voltage = vagnd

            if (vref - vagnd < 0):
                self.i2c_bus = None
            
        except:
            logging.error("Bus on channel {} is not available.".format(1))
            logging.info("Available busses are listed as /dev/i2c*")
            self.i2c_bus = None
    
    """ ------------------------------- DAC ------------------------------- """
    def analog_write(self, digital_value):
        """Converts discrete value and sets voltage on pin AOUT."""
        if (digital_value < 0 or digital_value > 255): return False

        try:
            control_byte = self.set_control_byte(0, False, 0, USING_INTERNAL_OSCILLATOR)
            #writing 2 bytes of data
            self.i2c_bus.write_byte_data(self.i2c_address, control_byte, digital_value)
        except IOError:
            return False

        return True
    
    """ ------------------------------- ADC ------------------------------- """
    def trigger_ADC_on_pin(self, pin):
        """Triggers ADC on selected pin"""
        control_byte = self.set_control_byte(pin, False, 0, USING_INTERNAL_OSCILLATOR)
        #writing one byte of data
        self.i2c_bus.write_byte(self.i2c_address, control_byte)

    def disable_ADC_on_pin(self, pin):
        """Disables ADC on selected pin -- not used"""
        control_byte = self.set_control_byte(0, False, 0, False)
        #writing one byte of data
        self.i2c_bus.write_byte(self.i2c_address, control_byte)

    def analog_read_raw(self, pin):
        """Returns raw discrete value read on specified pin -- only to be used internally."""
        try:
            self.trigger_ADC_on_pin(pin)
            self.i2c_bus.read_byte(self.i2c_address) #empty read, always returns 80h
        except IOError:
            return False

        value = self.i2c_bus.read_byte(self.i2c_address)
        #self.disable_ADC_on_pin(pin)
        return value

    def analog_read_AIN0_raw(self):
        """Returns raw discrete value read on pin A0."""
        return self.analog_read_raw(0)

    def analog_read_AIN1_raw(self):
        """Returns raw discrete value read on pin A1."""
        return self.analog_read_raw(1)

    def analog_read_AIN2_raw(self):
        """Returns raw discrete value read on pin A2."""
        return self.analog_read_raw(2)

    def analog_read_AIN3_raw(self):
        """Returns raw discrete value read on pin A3."""
        return self.analog_read_raw(3)

    def analog_read_all_raw(self):
        """Returns list of raw discrete readouts on pins A0 to A4."""
        try:
            reads = [] #list of reads from all channels (4)

            control_byte = self.set_control_byte(0, True, 0, USING_INTERNAL_OSCILLATOR) #auto increment ad_channel, Analog output enable - must be set to True if using internal oscillator

            self.i2c_bus.write_byte(self.i2c_address, control_byte)
            self.i2c_bus.read_byte(self.i2c_address) #empty read, always returns 80h

            reads.append(self.i2c_bus.read_byte(self.i2c_address))
            reads.append(self.i2c_bus.read_byte(self.i2c_address))
            reads.append(self.i2c_bus.read_byte(self.i2c_address))
            reads.append(self.i2c_bus.read_byte(self.i2c_address))
        except IOError:
            return False

        return reads

    def voltage_read(self, pin):
        """Returns read voltage on specified pin -- only to be used internally."""
        try:
            self.trigger_ADC_on_pin(pin)
            self.i2c_bus.read_byte(self.i2c_address) #empty read, always returns 80h
        except IOError:
            return False

        return (self.ref_voltage - self.agnd_voltage) / 255.0 * self.i2c_bus.read_byte(self.i2c_address)

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
        try:
            reads = []

            control_byte = self.set_control_byte(0, True, 0, USING_INTERNAL_OSCILLATOR) #auto increment ad_channel, Analog output enable - must be set to True if using internal oscillator

            self.i2c_bus.write_byte(self.i2c_address, control_byte)
            self.i2c_bus.read_byte(self.i2c_address) #empty read, always returns 80h
            
            reads.append((self.ref_voltage - self.agnd_voltage) / 255.0 * self.i2c_bus.read_byte(self.i2c_address))
            reads.append((self.ref_voltage - self.agnd_voltage) / 255.0 * self.i2c_bus.read_byte(self.i2c_address))
            reads.append((self.ref_voltage - self.agnd_voltage) / 255.0 * self.i2c_bus.read_byte(self.i2c_address))
            reads.append((self.ref_voltage - self.agnd_voltage) / 255.0 * self.i2c_bus.read_byte(self.i2c_address))
        except IOError:
            return False

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

"""TEST CODE"""
#pcf = Pcf8591(0, 0, 0, 3.3, 0)
'''
time.sleep(1)
print(pcf.analog_write(0))

time.sleep(1)
pcf.analog_write(62)
time.sleep(1)
pcf.analog_write(127)
time.sleep(1)
pcf.analog_write(190)
time.sleep(1)
pcf.analog_write(250)
time.sleep(1)
'''
'''
for i in range(5000):
    AIN0 = pcf.analog_read_AIN0_raw()
    print("AIN0: {}".format(AIN0))
    AIN1 = pcf.analog_read_AIN1_raw()
    print("AIN1: {}".format(AIN1))
    AIN2 = pcf.analog_read_AIN2_raw()
    print("AIN2: {}".format(AIN2))
    AIN3 = pcf.analog_read_AIN3_raw()
    print("AIN3: {}".format(AIN3))
    print("")
'''
'''
    reads = pcf.analog_read_all_raw()
    for i in range(len(reads)):
        print("A{}: {}".format(i, reads[i]))

    print("")
    reads = pcf.voltage_read_all()
    for i in range(len(reads)):
        print("V{}: {}v".format(i, reads[i]))
    print("")
'''