
from typing import List


class State:
    name: str
    value: str

    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value


class File:
    name: str

    def __init__(self, name: str):
        self.name = name


class Path:

    state: List[State]
    file: List[File]

    def __init__(self):
        self.state = []
        self.file = []

    def __len__(self):
        return self.state.__len__(), self.file.__len__()

    def append_state(self, obj: State) -> None:
        self.state.append(obj)
        return

    def append_file(self, obj: File) -> None:
        self.file.append(obj)
        return


class ExternalEvent:

    name: str
    cname: str
    external_id: str
    path: List[Path]

    # def __init__(self, name: str, eid: str = None):
    #     self.name = name
    #     self.external_id: str
    #     if eid is None:
    #         self.external_id = 'V' + name[5:]
    #     else:
    #         self.external_id = eid
    #     self.path = []

    def __init__(self, name: str, cname: str, eid: str):
        self.name = name
        self.cname = cname
        self.external_id = eid
        self.path = []

    def __len__(self):
        return self.path.__len__()

    def append_path(self, obj: Path) -> None:
        self.path.append(obj)
        return


class AudioModification:

    name: str
    external_event: List[ExternalEvent]

    def __init__(self, name: str):
        self.name = name
        self.external_event = []

    def __len__(self):
        return self.external_event.__len__()

    def append_external_event(self, obj: ExternalEvent) -> None:
        self.external_event.append(obj)
        return
