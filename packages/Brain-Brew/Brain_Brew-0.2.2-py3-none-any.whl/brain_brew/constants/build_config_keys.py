from collections import namedtuple
from enum import Enum

# TODO: Make this a class
BuildTaskEnum = namedtuple("BuildTaskEnum", "key_name source_type task_to_execute reverse_task_to_execute")


class BuildConfigKeys(Enum):
    SUBCONFIG = "subconfig"

    NOTES = "notes"
    HEADERS = "headers"
