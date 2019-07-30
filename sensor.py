from homeassistant.const import TEMP_CELSIUS
from homeassistant.helpers.entity import Entity
import os
import decimal


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the sensor platform."""
    add_devices([TempSensor(config['nice_name'], config['serial_id'])])


class TempSensor(Entity):
    """Representation of a Sensor."""

    nice_name = "nice_name not defined"
    serial_id = "not defined"

    def __init__(self, nice_name, serial_id):
        """Initialize the sensor."""
        self._state = None
        self.nice_name = nice_name
        self.serial_id = serial_id

    @property
    def name(self):
        """Return the name of the sensor."""
        return self.nice_name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    def update(self):
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = self.readTemp()

    def readTemp(self):
        sensorPath = "/sys/bus/w1/devices/%s/w1_slave" % self.serial_id
        if os.path.isfile(sensorPath) == True:
            tfile = open(sensorPath) 
            tempText = tfile.read() 
            tfile.close() 
            if tempText.find("YES") == -1:
                return 0
            temperatureData = temperatureData = tempText.split("\n")[1].split(" ")[9] 
            temperature = decimal.Decimal(temperatureData[2:]) 
            temperature = temperature / 1000
            temperature = format(temperature, '.1f')
            return temperature
        else:
            return 0