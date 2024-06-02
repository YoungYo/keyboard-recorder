class DataSource(object):
    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database


class KeyboardRecord(object):
    def __init__(self, key_show_name, key_name, key_vk, press_time, platform):
        self.key_show_name = key_show_name
        self.key_name = key_name
        self.key_vk = key_vk
        self.press_time = press_time
        self.platform = platform
