from ..constant.paths import KEYFILE_PATH


class LoginConfig(object):
    def __init__(self):
        self.load_keyfile()

    def load_keyfile(self):
        with open(KEYFILE_PATH, "r") as r:
            self.jwt_key = r.readline()

    def get_jwt_key(self):
        return self.jwt_key