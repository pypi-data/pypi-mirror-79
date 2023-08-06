import argparse
import os
import json
import datetime
import platform
import socket
import uuid
import alphabetic_timestamp as ats
import time

try:
    import Tkinter as tk
except Exception as e:
    import tkinter as tk

from . import gui


class Path(object):
    @classmethod
    def package_directory(cls):
        return os.path.dirname(os.path.abspath(__file__))

    @classmethod
    def configuration_directory(cls):
        return os.path.join(cls.package_directory(), "configuration")

    @classmethod
    def starter_configuration(cls):
        return os.path.join(cls.configuration_directory(), "starter.json")


class DataFiller(object):
    def __init__(self):
        self.gui = None
        self.cfg = None

    def fill(self, gui, cfg):
        self.gui = gui
        self.cfg = cfg

        self._fill_working_directory()
        self._fill_variables()
        self._fill_tags()
        self._fill_notes()

    def _fill_working_directory(self):
        self.gui.working_directory.entry_string.set(self.cfg["working_directory"])

    def _fill_variables(self):
        for cfg, widget in zip(self.cfg["variables"], self.gui.variables):
            widget.variable_string.set(cfg["name"])
            widget.value_string.set(cfg["value"])
            self._fill_check_button(widget, cfg)

    def _fill_check_button(self, widget, cfg):
        if "checked" in cfg:
            if cfg["checked"] == "True" or cfg["checked"] == "1":
                widget.checkbox_variable.set(1)
            else:
                widget.checkbox_variable.set(0)
        else:
            widget.checkbox_variable.set(0)

    def _fill_tags(self):
        self.gui.tags.entry_string.set(", ".join(self.cfg["tags"]))

    def _fill_notes(self):
        self.gui.note.text.delete(1.0, "end")
        self.gui.note.text.insert(1.0, "\n".join(self.cfg["note"]))


class Binder(object):
    def __init__(self):
        pass

    def bind(self, gui, controller):
        gui.button.button.bind("<Button-1>", controller.button_click)


class TunnerFile(object):
    def __init__(self):
        self.gui = None

    def content(self, gui, specific_time):
        self.gui = gui
        return {
            "id": ats.base62.from_datetime(specific_time, time_unit=ats.TimeUnit.seconds),

            "time": {
                "str": str(specific_time),
                "epoch": specific_time.timestamp(),
                "zone": str(time.tzname)
            },

            "environment": {
                "platform": {
                    "machine": platform.machine(),
                    "node": platform.node(),
                    "processor": platform.processor(),
                    "release": platform.release(),
                    "system": platform.system(),
                    "version": platform.version(),
                },
                "network": {
                    "host": socket.gethostbyname(socket.gethostname()),
                    "mac": uuid.getnode()
                }
            },

            "tags": self._tags(),

            "variables": self._variables(),

            "note": self._note()

        }

    def _tags(self):
        return [tag.strip() for tag in self.gui.tags.entry.get().split(",")]

    def _variables(self):
        variables = []

        for variable in self.gui.variables:
            v = {}
            v["name"] = variable.variable_string.get().strip()
            v["value"] = variable.value_string.get().strip()
            v["checked"] = variable.checkbox_variable.get()

            variables.append(v)

        return variables

    def _note(self):
        return self.gui.note.text.get("1.0","end")


class StarterController:
    def __init__(self):
        self.cfg = None
        self.gui = None
        self.root = None
        self.data_filler = DataFiller()
        self.binder = Binder()
        self.specific_time = None
        self.directory_path = None

    def run(self, arguments):
        self.root = tk.Tk()
        self.gui = gui.starter.build(self.root)
        self.read_configuration()
        self.data_filler.fill(self.gui, self.cfg)
        self.binder.bind(self.gui, self)
        self.root.mainloop()

    def read_configuration(self):
        with open(Path.starter_configuration()) as cfg_file:
            self.cfg = json.load(cfg_file)

    def button_click(self, event):
        # self._disabled_button()
        self._get_specific_time()
        self._evaluate_directory_path()
        self._create_working_directory()
        self._write_tunner_file()
        print(self.directory_path)
        # self._enabled_button()

    def _create_working_directory(self):
        os.makedirs(self.directory_path, exist_ok=True)

    def _write_tunner_file(self):
        tf = TunnerFile()

        with open(self._tunner_file_path(), "w+") as f:
            json.dump(tf.content(self.gui, self.specific_time), f, indent=4, sort_keys=True)

    def _get_specific_time(self):
        self.specific_time = datetime.datetime.now()

    def _evaluate_directory_path(self):
        template = self.gui.working_directory.entry.get()
        path = self.specific_time.strftime(template)

        for variable in self.gui.variables:
            if variable.checkbox_variable.get():
                path = path.replace(variable.variable_string.get().strip(), variable.value_string.get().strip())

        self.directory_path = path

    def _tunner_file_path(self):
        return os.path.join(self.directory_path, ".tunner")

    def _disabled_button(self):
        self.gui.button.button.configure(text="working", bg="#737373")
        self.gui.button.button["state"] = "disabled"

    def _enabled_button(self):
        self.gui.button.button.configure(text="Start", bg="#434343")
        self.gui.button.button["state"] = "normal"


class CopierController(object):
    def __init__(self):
        pass

    def run(self, arguments):
        print("aaa")


def main():
    starter = StarterController()
    copier = CopierController()

    parser = argparse.ArgumentParser(description="TUNNER: PRE-ALPHA VERSION",
                                     formatter_class=argparse.RawTextHelpFormatter)
    subparsers = parser.add_subparsers()

    starter_parser = subparsers.add_parser('starter')
    starter_parser.set_defaults(func=starter.run)

    copier_parser = subparsers.add_parser('cp')
    copier_parser.set_defaults(func=copier.run)

    arguments = parser.parse_args()
    arguments.func(arguments)


if __name__ == "__main__":
    main()