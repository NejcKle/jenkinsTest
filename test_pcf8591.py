import unittest

from pcf8591 import Pcf8591

ADRESS_GOOD = 0x09 #address of device on A0=0, A1=0, A2=0

VREF = 5.15
VAGND = 0.0

A0 = 0
A1 = 0
A2 = 0

class TestPcf8591Driver(unittest.TestCase):

    # This runs once before test methods in this class are run
    @classmethod
    def setUpClass(cls):
        cls.driver = Pcf8591(A0, A1, A2, VREF, VAGND)  # use in all funtions

    # This runs before every test method
   # def setUp(self):
        #empty

    def test_class_init_good_address(self):
        driver = Pcf8591(A0, A1, A2, VREF, VAGND)
        self.assertIsNotNone(driver.i2c_bus, "Address is good, so i2c bus must be Not None")
    
    '''
    #we can't check, no registers to read on chip
    def test_class_init_bad_address(self):
        #bad address also happens when A0, A1 or A2 are specified wrongly
        driver = Pcf8591(A0, 1, 1, VREF, VAGND)
        self.assertIsNone(driver.i2c_bus, "Address is bad, so i2c bus must be None")
    '''

    def test_class_init_good_params(self):
        driver = Pcf8591(A0, A1, A2, VREF, VAGND)
        self.assertIsNotNone(driver.i2c_bus, "Vref - Vagnd is greater than 0, so i2c bus must be Not None")

    def test_class_init_bad_params(self):
        driver = Pcf8591(A0, A1, A2, 2, 2.5)
        self.assertIsNone(driver.i2c_bus, "Vref - Vagnd is less than 0, so i2c bus must be None")

    def test_control_byte_dac(self):
        self.assertEqual(self.driver.set_control_byte(0, False, 0, True), 64, "Wrong value set in set_control_byte")

    def test_control_byte_analog_read_raw_AIN0(self):
        self.assertEqual(self.driver.set_control_byte(0, False, 0, False), 0, "Wrong value set in set_control_byte")

    def test_control_byte_analog_read_raw_AIN1(self):
        self.assertEqual(self.driver.set_control_byte(1, False, 0, False), 1, "Wrong value set in set_control_byte")

    def test_control_byte_analog_read_raw_AIN2(self):
        self.assertEqual(self.driver.set_control_byte(2, False, 0, False), 2, "Wrong value set in set_control_byte")

    def test_control_byte_analog_read_raw_AIN3(self):
        self.assertEqual(self.driver.set_control_byte(3, False, 0, False), 3, "Wrong value set in set_control_byte")

    def test_control_byte_analog_read_all_raw(self):
        self.assertEqual(self.driver.set_control_byte(0, True, 0, False), 4, "Wrong value set in set_control_byte")

    def test_control_byte_voltage_read_AIN0(self):
        self.assertEqual(self.driver.set_control_byte(0, False, 0, False), 0, "Wrong value set in set_control_byte")

    def test_control_byte_voltage_read_AIN1(self):
        self.assertEqual(self.driver.set_control_byte(1, False, 0, False), 1, "Wrong value set in set_control_byte")

    def test_control_byte_voltage_read_AIN2(self):
        self.assertEqual(self.driver.set_control_byte(2, False, 0, False), 2, "Wrong value set in set_control_byte")

    def test_control_byte_voltage_read_AIN3(self):
        self.assertEqual(self.driver.set_control_byte(3, False, 0, False), 3, "Wrong value set in set_control_byte")

    def test_control_byte_voltage_read_all(self):
        self.assertEqual(self.driver.set_control_byte(0, True, 0, False), 4, "Wrong value set in set_control_byte")

if __name__ == '__main__':
    unittest.main()
