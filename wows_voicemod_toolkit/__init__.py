
import os
import json
import xml.dom.minidom as xml

import wows_voicemod_toolkit.elements


class wowsVoiceMod:

    name: str
    src_file_path: str
    file_data_flag: bool
    mod_class: elements.AudioModification

    def __init__(self, filepath: str, filetype: str = None):
        self.src_file_path = os.path.abspath(filepath)
        _, filename_full = os.path.split(self.src_file_path)
        self.name, file_point_ext = os.path.splitext(filename_full)

        if (filetype is None and file_point_ext.find('json') != -1) \
                or (filetype is not None and filetype.find('json') != -1):
            self.file_data_flag = False
            self._read_json()

        elif (filetype is None and file_point_ext.find('xml') != -1) \
                or (filetype is not None and filetype.find('xml') != -1):
            self.file_data_flag = True
            self._read_xml()

        else:
            print('file type wrong')
            exit()

    def rename(self, name: str):
        self.name = name

    def _read_xml(self) -> bool:
        tree = xml.parse(self.src_file_path)
        root = tree.documentElement

        self.mod_class = elements.AudioModification(root.getElementsByTagName('Name')[0].firstChild.data)
        events = root.getElementsByTagName('ExternalEvent')

        for event in events:
            name = event.getElementsByTagName('Name')[0].firstChild.data
            container = event.getElementsByTagName('Container')[0]
            cname = container.getElementsByTagName('Name')[0].firstChild.data
            eid = container.getElementsByTagName('ExternalId')[0].firstChild.data
            event_class = elements.ExternalEvent(name, cname, eid)

            paths = container.getElementsByTagName('Path')

            for path in paths:
                path_class = elements.Path()

                states = path.getElementsByTagName('State')

                for state in states:
                    name = state.getElementsByTagName('Name')[0].firstChild.data
                    value = state.getElementsByTagName('Value')[0].firstChild.data
                    state_class = elements.State(name, value)
                    path_class.append_state(state_class)

                files = path.getElementsByTagName('File')

                for file in files:
                    file_class = elements.File(file.getElementsByTagName('Name')[0].firstChild.data)
                    path_class.append_file(file_class)

                event_class.append_path(path_class)

            self.mod_class.append_external_event(event_class)

        return True

    def write_xml(self, path) -> bool:
        write_path = os.path.abspath(path + self.name + '.xml')

        tree = xml.Document()

        root = tree.createElement('AudioModification.xml')
        tree.appendChild(root)
        mod = tree.createElement('AudioModification')
        root.appendChild(mod)

        mod_name = tree.createElement('Name')
        mod_name.appendChild(tree.createTextNode(self.mod_class.name))
        mod.appendChild(mod_name)

        for event_class in self.mod_class.external_event:
            event = tree.createElement('ExternalEvent')

            event_name = tree.createElement('Name')
            event_name.appendChild(tree.createTextNode(event_class.name))
            event.appendChild(event_name)

            container = tree.createElement('Container')

            container_name = tree.createElement('Name')
            container_name.appendChild(tree.createTextNode(event_class.cname))
            container.appendChild(container_name)

            eid = tree.createElement('ExternalId')
            eid.appendChild(tree.createTextNode(event_class.external_id))
            container.appendChild(eid)

            for path_class in event_class.path:
                path = tree.createElement('Path')

                state_list = tree.createElement('StateList')

                for state_class in path_class.state:
                    state = tree.createElement('State')

                    state_name = tree.createElement('Name')
                    state_name.appendChild(tree.createTextNode(state_class.name))
                    state.appendChild(state_name)

                    value_name = tree.createElement('Value')
                    value_name.appendChild(tree.createTextNode(state_class.value))
                    state.appendChild(value_name)

                    state_list.appendChild(state)

                path.appendChild(state_list)

                file_list = tree.createElement('FilesList')

                for file_class in path_class.file:
                    file = tree.createElement('File')

                    file_name = tree.createElement('Name')
                    file_name.appendChild(tree.createTextNode(file_class.name))
                    file.appendChild(file_name)

                    file_list.appendChild(file)

                path.appendChild(file_list)

                container.appendChild(path)

            event.appendChild(container)

            mod.appendChild(event)

        with open(write_path, 'w') as f:
            tree.writexml(f, indent='', addindent='\t', newl='\n', encoding='utf-8')

        return True

    def _read_json(self) -> bool:
        with open(self.src_file_path, 'r', encoding='utf8') as f:
            json_str = f.read()
        mod_json = json.loads(json_str)

        self.mod_class = elements.AudioModification(mod_json['Name'])
        events = mod_json['ExternalEvent']

        for event in events:
            name = event['Name']
            cname = event['ContainerName']
            eid = event['ExternalId']
            event_class = elements.ExternalEvent(name, cname, eid)

            paths = event['Path']

            for path in paths:
                path_class = elements.Path()

                states = path['State']

                for state in states:
                    name = state['Name']
                    value = state['Value']
                    state_class = elements.State(name, value)
                    path_class.append_state(state_class)

                files = path['File']

                for file in files:
                    file_class = elements.File(file)
                    path_class.append_file(file_class)

                event_class.append_path(path_class)

            self.mod_class.append_external_event(event_class)

        return True

    def write_json(self, path) -> bool:
        write_path = os.path.abspath(path + self.name + '.json')

        mod_json = {'Name': self.mod_class.name,
                    'ExternalEvent': []}

        events_json = []

        for event_class in self.mod_class.external_event:
            event_json = {'Name': event_class.name,
                          'ContainerName': event_class.cname,
                          'ExternalId': event_class.external_id,
                          'Path': []}

            paths_json = []

            for path_class in event_class.path:
                path_json = {'State': [],
                             'File': []}

                states_json = []

                for state_class in path_class.state:
                    state_json = {'Name': state_class.name,
                                  'Value': state_class.value}

                    states_json.append(state_json)

                path_json['State'] = states_json

                files_json = []

                for file_class in path_class.file:
                    files_json.append(file_class.name)

                path_json['File'] = files_json

                paths_json.append(path_json)

            event_json['Path'] = paths_json

            events_json.append(event_json)

        mod_json['ExternalEvent'] = events_json

        with open(write_path, 'w') as f:
            json.dump(mod_json, f, indent='\t', ensure_ascii=False)

        return True

    def _read_folder(self) -> bool:
        pass

    def write_folder(self, path) -> bool:
        flags = {'Voice': False, 'SFX': False, 'Loop': False}

        if not os.path.exists(path):
            print("path '" + path + "' not exist")
            return False

        mod_path = os.path.join(os.path.abspath(path), self.name)

        if os.path.exists(mod_path):
            print("path '" + mod_path + "' existed")
            return False

        os.mkdir(mod_path)

        for event_class in self.mod_class.external_event:
            if not flags[event_class.cname]:
                flags[event_class.cname] = True
                os.mkdir(os.path.join(mod_path, event_class.cname))

            event_path = os.path.join(mod_path, event_class.cname, event_class.name.replace('Play_', '', 1))
            os.mkdir(event_path)

            for path_class in event_class.path:
                state_classes = path_class.state
                state_path = event_path

                if not state_classes == 0:
                    state_pair_list = []
                    for state_class in state_classes:
                        state_pair_list.append(state_class.name + '__' + state_class.value)

                    state_pair_list.sort()
                    for state_pair in state_pair_list:
                        state_path = os.path.join(state_path, state_pair)
                        if not os.path.exists(state_path):
                            os.mkdir(state_path)
        return True

