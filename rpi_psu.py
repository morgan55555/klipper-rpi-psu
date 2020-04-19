# -*- coding: utf-8 -*-
# Rpi PSU control support
#
# Copyright (C) 2020  Alex Morgan <alxmrg55@gmail.com>
#
# This file may be distributed under the terms of the GNU GPLv3 license.
#
# Install:
#
# sudo systemctl stop klipper
# cd ~
# mv klipper klipper_backup 
# PYTHONDIR="${HOME}/klippy-env"
# virtualenv ${PYTHONDIR}
# ${PYTHONDIR}/bin/pip install gpiozero
#
import gpiozero

class Rpi_PSU:
    def __init__(self, config):
        self.printer = config.get_printer()
        global _psu_pin # Workaround for RESTART and FIRMWARE_RESTART, pin must save his state
        if not ( '_psu_pin' in globals() ):
            pin = config.get('psu_pin', 1)
            active_high = config.getboolean('active_high', False)
            _psu_pin = gpiozero.DigitalOutputDevice( pin=pin, active_high=active_high, initial_value=False )
        self.psu_pin = _psu_pin
        self.startup_gcode = config.get('startup_gcode', '')
        self.shutdown_gcode = config.get('shutdown_gcode', '')
        self.gcode = self.printer.lookup_object('gcode')
        self.gcode.register_command(
            'M80', self.cmd_M80, when_not_ready=True, desc=self.cmd_M80_desc)
        self.gcode.register_command(
            'M81', self.cmd_M81, when_not_ready=True, desc=self.cmd_M81_desc)
    cmd_M80_desc = 'Turn on PSU'
    def cmd_M80(self, params):
        self.psu_pin.on()
        self.gcode.respond_info("PSU is enabled.")
        self.gcode.run_script_from_command(self.startup_gcode)
    cmd_M81_desc = 'Turn off PSU'
    def cmd_M81(self, params):
        self.gcode.run_script_from_command(self.shutdown_gcode)
        self.psu_pin.off()
        self.gcode.respond_info("PSU is disabled.")


def load_config(config):
    return Rpi_PSU(config)
    