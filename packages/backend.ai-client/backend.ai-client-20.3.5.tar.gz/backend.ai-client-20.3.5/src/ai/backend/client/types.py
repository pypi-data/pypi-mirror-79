import enum


class Sentinel(enum.Enum):
    """
    A special type to represent a special value to indicate closing/shutdown of queues.
    """
    token = 0


class Undefined(enum.Enum):
    """
    A special type to represent an undefined value.
    """
    token = 0


sentinel = Sentinel.token
undefined = Undefined.token
