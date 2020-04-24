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
# git clone https://github.com/morgan55555/klipper-rpi-psu.git
# ln -s ~/klipper-rpi-psu/rpi_psu.py ~/klipper/klippy/extras/rpi_psu.py
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
        self.before_startup_gcode = config.get('before_startup_gcode', '')
        self.after_startup_gcode = config.get('after_startup_gcode', '')
        self.before_shutdown_gcode = config.get('before_shutdown_gcode', '')
        self.after_shutdown_gcode = config.get('after_shutdown_gcode', '')
        self.gcode = self.printer.lookup_object('gcode')
        self.gcode.register_command(
            'M80', self.cmd_M80, when_not_ready=True, desc=self.cmd_M80_desc)
        self.gcode.register_command(
            'M81', self.cmd_M81, when_not_ready=True, desc=self.cmd_M81_desc)
    cmd_M80_desc = 'Turn on PSU'
    def cmd_M80(self, params):
        self.gcode.run_script_from_command(self.before_startup_gcode)
        self.psu_pin.on()
        self.gcode.run_script_from_command(self.after_startup_gcode)
        self.gcode.respond_info("PSU is enabled.")
    cmd_M81_desc = 'Turn off PSU'
    def cmd_M81(self, params):
        self.gcode.run_script_from_command(self.before_shutdown_gcode)
        self.psu_pin.off()
        self.gcode.run_script_from_command(self.after_shutdown_gcode)
        self.gcode.respond_info("PSU is disabled.")
    def get_status(self):
        return self.psu_pin.value


def load_config(config):
    return Rpi_PSU(config)
    
