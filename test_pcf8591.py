import unittest

from parameterized import parameterized, parameterized_class

from pcf8591 import Pcf8591
from random import randrange

ADRESS_GOOD = 0x09 #address of device, pins append to address later

VREF = 5.15
VAGND = 0.0

@parameterized_class(('A0', 'A1', 'A2'), [
    # This will run the test class once for each address
    (0, 0, 0),
    #(1, 0, 0),
    #(0, 1, 0),
    #(1, 1, 0),
    #(0, 0, 1)
])
class TestPcf8591Driver(unittest.TestCase):

    #This runs once before test methods in this class are run
    @classmethod
    def setUpClass(cls):
        cls.driverGood = Pcf8591(cls.A0, cls.A1, cls.A2, VREF, VAGND)  #use in all funtions
        cls.driverBad = Pcf8591(-1, -1, -1, VREF, VAGND)

    #This runs before every test method
    #def setUp(self):
        #empty

    """ --------------------------- Init tests ----------------------- """
    def test_class_init_good_address(self):
        self.assertIsNotNone(self.driverGood.i2c_bus, "Address is good, so i2c bus must be Not None")

    def test_class_init_good_params(self):
        self.assertIsNotNone(self.driverGood.i2c_bus, "Vref - Vagnd is greater than 0, so i2c bus must be Not None")

    def test_class_init_bad_params(self):
        driverGood = Pcf8591(self.A0, self.A1, self.A2, 2, 2.5)
        self.assertIsNone(driverGood.i2c_bus, "Vref - Vagnd is less than 0, so i2c bus must be None")

    """ --------------------------- Control byte settings tests ----------------------- """
    def test_control_byte_dac(self):
        self.assertEqual(self.driverGood.set_control_byte(0, False, 0, True), 0x40, "Wrong value set in set_control_byte")

    def test_control_byte_analog_read_AIN0_raw(self):
        self.assertEqual(self.driverGood.set_control_byte(0, False, 0, True), 0x40, "Wrong value set in set_control_byte")

    def test_control_byte_analog_read_AIN1_raw(self):
        self.assertEqual(self.driverGood.set_control_byte(1, False, 0, True), 0x41, "Wrong value set in set_control_byte")

    def test_control_byte_analog_read_AIN2_raw(self):
        self.assertEqual(self.driverGood.set_control_byte(2, False, 0, True), 0x42, "Wrong value set in set_control_byte")

    def test_control_byte_analog_read_AIN3_raw(self):
        self.assertEqual(self.driverGood.set_control_byte(3, False, 0, True), 0x43, "Wrong value set in set_control_byte")

    def test_control_byte_analog_read_all_raw(self):
        self.assertEqual(self.driverGood.set_control_byte(0, True, 0, True), 0x44, "Wrong value set in set_control_byte")

    def test_control_byte_voltage_read_AIN0(self):
        self.assertEqual(self.driverGood.set_control_byte(0, False, 0, True), 0x40, "Wrong value set in set_control_byte")

    def test_control_byte_voltage_read_AIN1(self):
        self.assertEqual(self.driverGood.set_control_byte(1, False, 0, True), 0x41, "Wrong value set in set_control_byte")

    def test_control_byte_voltage_read_AIN2(self):
        self.assertEqual(self.driverGood.set_control_byte(2, False, 0, True), 0x42, "Wrong value set in set_control_byte")

    def test_control_byte_voltage_read_AIN3(self):
        self.assertEqual(self.driverGood.set_control_byte(3, False, 0, True), 0x43, "Wrong value set in set_control_byte")

    def test_control_byte_voltage_read_all(self):
        self.assertEqual(self.driverGood.set_control_byte(0, True, 0, True), 0x44, "Wrong value set in set_control_byte")
       
    """ --------------------------- Dac tests with good address ----------------------- """
    def test_dac_lower_bound(self):
        self.assertEqual(self.driverGood.analog_write(0), True, "Digital input is 0, return value should be True")

    def test_dac_upper_bound(self):
        self.assertEqual(self.driverGood.analog_write(255), True, "Digital input is 255, return value should be True")

    def test_dac_outside_lower_bound(self):
        self.assertEqual(self.driverGood.analog_write(-1), False, "Digital input is -1, return value should be False")

    def test_dac_outside_upper_bound(self):
        self.assertEqual(self.driverGood.analog_write(256), False, "Digital input is -1, return value should be False")

    def test_dac_inside_random(self):
        rand = randrange(255)
        self.assertEqual(self.driverGood.analog_write(rand), True, "Digital input is {}, return value should be True".format(rand))

    """ --------------------------- Dac tests with bad address ----------------------- """
    def test_wrong_address_dac_lower_bound(self):
        self.assertEqual(self.driverBad.analog_write(0), False, "Address is wrong, return value should be False")

    def test_wrong_address_dac_upper_bound(self):
        self.assertEqual(self.driverBad.analog_write(255), False, "Address is wrong, return value should be False")

    def test_wrong_address_dac_outside_lower_bound(self):
        self.assertEqual(self.driverBad.analog_write(-1), False, "Address is wrong, return value should be False")

    def test_wrong_address_dac_outside_upper_bound(self):
        self.assertEqual(self.driverBad.analog_write(256), False, "Address is wrong, return value should be False")

    def test_wrong_address_dac_inside_random(self):
        rand = randrange(255)
        self.assertEqual(self.driverBad.analog_write(rand), False, "Address is wrong, return value should be False")

    """ --------------------------- Adc tests with good address ----------------------- """
    def test_analog_read_AIN0_raw(self):
        self.assertEqual(type(self.driverGood.analog_read_AIN0_raw()), int, "Address is correct, return value should be integer")

    def test_analog_read_AIN1_raw(self):
        self.assertEqual(type(self.driverGood.analog_read_AIN1_raw()), int, "Address is correct, return value should be integer")

    def test_analog_read_AIN2_raw(self):
        self.assertEqual(type(self.driverGood.analog_read_AIN2_raw()), int, "Address is correct, return value should be integer")

    def test_analog_read_AIN3_raw(self):
        self.assertEqual(type(self.driverGood.analog_read_AIN3_raw()), int, "Address is correct, return value should be integer")

    def test_analog_read_all_raw(self):
        self.assertEqual(type(self.driverGood.analog_read_all_raw()), list, "Address is correct, return value should be list")

    def test_voltage_read_AIN0(self):
        self.assertEqual(type(self.driverGood.voltage_read_AIN0()), float, "Address is correct, return value should be float")

    def test_voltage_read_AIN1(self):
        self.assertEqual(type(self.driverGood.voltage_read_AIN0()), float, "Address is correct, return value should be float")

    def test_voltage_read_AIN2(self):
        self.assertEqual(type(self.driverGood.voltage_read_AIN0()), float, "Address is correct, return value should be float")

    def test_voltage_read_AIN3(self):
        self.assertEqual(type(self.driverGood.voltage_read_AIN0()), float, "Address is correct, return value should be float")

    def test_voltage_read_all(self):
        self.assertEqual(type(self.driverGood.voltage_read_all()), list, "Address is correct, return value should be list")

    """ --------------------------- Adc tests with bad address ----------------------- """
    def test_analog_read_AIN0_raw(self):
        self.assertEqual(self.driverBad.analog_read_AIN0_raw(), False, "Address is wrong, return value should be False")

    def test_analog_read_AIN1_raw(self):
        self.assertEqual(self.driverBad.analog_read_AIN1_raw(), False, "Address is wrong, return value should be False")

    def test_analog_read_AIN2_raw(self):
        self.assertEqual(self.driverBad.analog_read_AIN2_raw(), False, "Address is wrong, return value should be False")

    def test_analog_read_AIN3_raw(self):
        self.assertEqual(self.driverBad.analog_read_AIN3_raw(), False, "Address is cowrongrect, return value should be False")

    def test_analog_read_all_raw(self):
        self.assertEqual(self.driverBad.analog_read_all_raw(), False, "Address is wrong, return value should be False")

    def test_voltage_read_AIN0(self):
        self.assertEqual(self.driverBad.voltage_read_AIN0(), False, "Address is wrong, return value should be False")

    def test_voltage_read_AIN1(self):
        self.assertEqual(self.driverBad.voltage_read_AIN0(), False, "Address is wrong, return value should be False")

    def test_voltage_read_AIN2(self):
        self.assertEqual(self.driverBad.voltage_read_AIN0(), False, "Address is wrong, return value should be False")

    def test_voltage_read_AIN3(self):
        self.assertEqual(self.driverBad.voltage_read_AIN0(), False, "Address is wrong, return value should be False")

    def test_voltage_read_all(self):
        self.assertEqual(self.driverBad.voltage_read_all(), False, "Address is wrong, return value should be False")

if __name__ == '__main__':
    unittest.main()
