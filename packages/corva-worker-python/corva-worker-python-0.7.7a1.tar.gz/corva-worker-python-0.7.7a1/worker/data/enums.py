from enum import Enum


class LambdaStates(Enum):
    TIMED_OUT = "Lambda timed out."
    SUCCEEDED = "Lambda process succeeded."
    FAILED = "Lambda process failed."


class EventTypes(Enum):
    STREAM = "stream_event"
    TASK = "task_event"
    SCHEDULER = "scheduler_event"
    GENERIC = "generic_event"


class SPMStatus(Enum):
    ON = "spm_on"
    OFF = "spm_off"
    MISSING = "missing"


class MudFlowInStatus(Enum):
    ON = "mud_flow_in_on"
    OFF = "mud_flow_in_off"
    MISSING = "missing"


class DataStatus(Enum):
    VALID = "valid"
    MISSING = "missing"
    OVERRIDDEN = "overridden"


class Environment(Enum):
    QA = "qa"
    STAGING = "staging"
    PRODUCTION = "production"
    LOCAL = "local"
