class FirefoxNotFoundError(Exception):
    pass


class GeckodriverVersionNotFoundError(Exception):
    pass


class PATHNotFoundError(Exception):
    pass


class BinaryNotFoundError(Exception):
    pass


class PlatformError(RuntimeError):
    pass
