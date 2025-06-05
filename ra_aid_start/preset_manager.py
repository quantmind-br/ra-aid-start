import os
import json

CONFIG_PATH = os.path.expanduser("~/.ra_aid_start_presets.json")

def load_presets():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    return {}

def save_presets(presets):
    with open(CONFIG_PATH, 'w') as f:
        json.dump(presets, f, indent=2)

def add_preset(name, command):
    presets = load_presets()
    presets[name] = command
    save_presets(presets)

def delete_preset(name):
    presets = load_presets()
    if name in presets:
        del presets[name]
        save_presets(presets)
