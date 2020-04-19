# klipper-rpi-psu

Klipper can't control PSU with RPI pins, only by printer's mainboard pins.

This plugin adds to Klipper this functionality.

Just use gcode M80, M81 now.

## Setup

```
 sudo systemctl stop klipper
 cd ~
 mv klipper klipper_backup 
 PYTHONDIR="${HOME}/klippy-env"
 virtualenv ${PYTHONDIR}
 ${PYTHONDIR}/bin/pip install gpiozero
 
 git clone https://github.com/morgan55555/klipper-rpi-psu.git
 ln -s ~/klipper-rpi-psu/rpi_psu.py ~/klipper/klippy/extras/rpi_psu.py
```

## Klipper configuration

Just copy that code and change parameters to any that you need.

```ini
[rpi_psu]
# pin
psu_pin: 17
# Invert enable logic, useful for inverted relays
active_high: False
# Run gcode after startup
startup_gcode: RESTART
# Run gcode before shutdown
# shutdown_gcode: 
```

Available pin formats: [link](https://gpiozero.readthedocs.io/en/stable/recipes.html#pin-numbering)
