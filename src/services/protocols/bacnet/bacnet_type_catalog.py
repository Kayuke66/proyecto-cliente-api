from typing import Literal, TypedDict


class BacnetObjectDefinition(TypedDict, total=False):
    name: str
    category: Literal["point", "device", "system", "event", "unknown"]
    class_: Literal["analog", "binary", "multistate", "other"]
    role: Literal["input", "output", "value", "other"]


BACNET_OBJECT_TYPES: dict[int, dict] = {
    0: {"name": "analog_input", "category": "point", "class": "analog", "role": "input"},
    1: {"name": "analog_output", "category": "point", "class": "analog", "role": "output"},
    2: {"name": "analog_value", "category": "point", "class": "analog", "role": "value"},
    3: {"name": "binary_input", "category": "point", "class": "binary", "role": "input"},
    4: {"name": "binary_output", "category": "point", "class": "binary", "role": "output"},
    5: {"name": "binary_value", "category": "point", "class": "binary", "role": "value"},
    13: {"name": "multistate_input", "category": "point", "class": "multistate", "role": "input"},
    14: {"name": "multistate_output", "category": "point", "class": "multistate", "role": "output"},
    19: {"name": "multistate_value", "category": "point", "class": "multistate", "role": "value"},
    8: {"name": "device", "category": "device"},
    9: {"name": "event_enrollment", "category": "event"},
    15: {"name": "notification_class", "category": "event"},
    25: {"name": "event_log", "category": "event"},
    52: {"name": "alert_enrollment", "category": "event"},
    6: {"name": "calendar", "category": "system"},
    7: {"name": "command", "category": "system"},
    10: {"name": "file", "category": "system"},
    11: {"name": "group", "category": "system"},
    12: {"name": "loop", "category": "system"},
    16: {"name": "program", "category": "system"},
    17: {"name": "schedule", "category": "system"},
    20: {"name": "trendlog", "category": "system"},
    27: {"name": "trend_log_multiple", "category": "system"},
    29: {"name": "structured_view", "category": "system"},
    39: {"name": "bitstring_value", "category": "point", "class": "other", "role": "value"},
    40: {"name": "characterstring_value", "category": "point", "class": "other", "role": "value"},
    42: {"name": "date_value", "category": "point", "class": "other", "role": "value"},
    44: {"name": "datetime_value", "category": "point", "class": "other", "role": "value"},
    45: {"name": "integer_value", "category": "point", "class": "other", "role": "value"},
    46: {"name": "large_analog_value", "category": "point", "class": "analog", "role": "value"},
    47: {"name": "octetstring_value", "category": "point", "class": "other", "role": "value"},
    48: {"name": "positive_integer_value", "category": "point", "class": "other", "role": "value"},
    50: {"name": "time_value", "category": "point", "class": "other", "role": "value"},
    54: {"name": "lighting_output", "category": "point", "class": "analog", "role": "output"},
    55: {"name": "binary_lighting_output", "category": "point", "class": "binary", "role": "output"},
}