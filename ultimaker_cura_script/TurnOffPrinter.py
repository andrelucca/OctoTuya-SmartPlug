# Copyright (c) 2017 Ghostkeeper
# The PostProcessingPlugin is released under the terms of the AGPLv3 or higher.

import re #To perform the search and replace.

from ..Script import Script


class TurnOffPrinter(Script):
    """Insert the Turn Off Action from Octotuya-SmartPlug Octoprint plugin 
    in the end of the gcode
    """

    def getSettingDataString(self):
        return """{
            "name": "Turn Off Printer",
            "key": "TurnOffPrinter",
            "metadata": {},
            "version": 2,
            "settings":
            {
                 "enabled":
                {
                    "label": "Enabled",
                    "description": "When enabled, the M81 command + the Label will be placed in the last line of the GCODE",
                    "type": "bool",
                    "default_value": false
                },
                "label":
                {
                    "label": "Label",
                    "description": "The configured label in the Octotuya-SmartPlug Octoprint plugin",
                    "type": "str",
                    "default_value": ""
                },
                "command": {
                    "label": "Command",
                    "description": "GCODE command to turn off the printer",
                    "type": "enum",
                    "options": {
                        "M81": "M81",
                        "G4 P2": "G4 P2"
                    },
                    "default_value": "M81"
                }
            }
        }"""

    def execute(self, data):
        label_string = self.getSettingValueByKey("label")
        command = self.getSettingValueByKey("command")
        if self.getSettingValueByKey("enabled"):
            
            seach_string_escape = re.escape(";End of Gcode")
            seach_string_compile = re.compile(seach_string_escape)
            turn_off_string = command+' '+label_string+' ;Turn off printer using OctoTuya\n;End of Gcode'

            for layer_number, layer in enumerate(data):
                data[layer_number] = re.sub(seach_string_compile, turn_off_string, layer)
            return data
        else:
            return data