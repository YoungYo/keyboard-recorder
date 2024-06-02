import datetime

from pynput.keyboard import Listener
from log import logger
from model import KeyboardRecord
import dao
from config import PLATFORM, MACOS


KEY_NAME_MAP = {
    'cmd': '左⌘',
    'ctrl': '左⌃' if PLATFORM == MACOS else '左Ctrl',
    'alt': '左⌥' if PLATFORM == MACOS else '左Alt',
    'cmd_r': '右⌘',
    'ctrl_r': '右⌃' if PLATFORM == MACOS else '右Ctrl',
    'alt_r': '右⌥' if PLATFORM == MACOS else '右Alt',
    'shift_r': '右⇧' if PLATFORM == MACOS else '右Shift',
    'shift': '左⇧' if PLATFORM == MACOS else '左Shift',
    'enter': '回车',
    'space': '空格',
    'esc': 'Esc',
    'delete': 'Delete',
    'backspace': 'Backspace',
    'tab': '⇥' if PLATFORM == MACOS else 'Tab',
    'caps_lock': 'Caps Lock',
    'right': '→',
    'left': '←',
    'up': '↑',
    'down': '↓',
    'f1': 'F1',
    'f2': 'F2',
    'f3': 'F3',
    'f4': 'F4',
    'f5': 'F5',
    'f6': 'F6',
    'f7': 'F7',
    'f8': 'F8',
    'f9': 'F9',
    'f10': 'F10',
    'f11': 'F11',
    'f12': 'F12'
}


def format_key(key):
    if hasattr(key, 'name'):
        return key.name
    elif hasattr(key, 'vk'):
        if 65 <= key.vk <= 127:
            return chr(key.vk)
        elif key.vk == 179:
            return 'Fn'
        else:
            return str(key.char)


def on_press(key):
    key_id = format_key(key)
    if key_id in KEY_NAME_MAP:
        key_show_name = KEY_NAME_MAP[key_id]
    else:
        key_show_name = key_id
    key_name = key.name if hasattr(key, 'name') else None
    key_vk = key.vk if hasattr(key, 'vk') else None
    logger.info(f"{PLATFORM}\t{key_show_name}\t{key_name}\t{key_vk}")
    record = KeyboardRecord(key_show_name, key_name, key_vk, datetime.datetime.now(), PLATFORM)
    dao.save_record(record)


def on_release(key):
    pass


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
