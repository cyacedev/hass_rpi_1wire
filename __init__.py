DOMAIN = 'rpi_1wire'

def setup(hass, config):
    hass.states.set('hello_state.world', 'Paulus')

    # Return boolean to indicate that initialization was successful.
    return True