import unittest

from pcf8591 import Pcf8591

ADRESS_GOOD = 0x09 #address of device on A0=0, A1=0, A2=0

VREF = 5.15
VAGND = 0.0

#chip receiving analog outputs
A00 = 0
A10 = 0
A20 = 0

#chip producing analog inputs, wired to AIN0
A01 = 1
A10 = 0
A20 = 0

#chip producing analog inputs, wired to AIN1
A00 = 0
A11 = 1
A20 = 0

#chip producing analog inputs, wired to AIN2
A01 = 1
A11 = 1
A20 = 0

#chip producing analog inputs, wired to AIN3
A00 = 0
A10 = 0
A21 = 1

class TestPcf8591System(unittest.TestCase):

    # This runs once before test methods in this class are run
    @classmethod
    def setUpClass(cls):
        cls.driverReceiver = Pcf8591(A00, A10, A20, VREF, VAGND)  # use in all funtions
        cls.driverAIN0 = Pcf8591(A01, A10, A20, VREF, VAGND)
        cls.driverAIN1 = Pcf8591(A00, A11, A20, VREF, VAGND)
        cls.driverAIN2 = Pcf8591(A01, A11, A20, VREF, VAGND)
        cls.driverAIN3 = Pcf8591(A00, A10, A21, VREF, VAGND)

    def test_system_analog_all(self):

        steps = 255
        for value in range(steps):
            
            voltage_in = []
            #generate voltage values for inputs
            voltage_in.append(self.driverAIN0.DAC(value))
            voltage_in.append(self.driverAIN1.DAC(value))
            voltage_in.append(self.driverAIN2.DAC(value))
            voltage_in.append(self.driverAIN3.DAC(value))

            analogs_raw = self.driverReceiver.analog_read_all_raw()

            for i, raw_value in enumerate(analogs_raw):
                with self.subTest(raw_value=raw_value):
                    self.assesrtAlmostEqual(raw_value, voltage_in[i], delta=1)

if __name__ == '__main__':
    unittest.main()
