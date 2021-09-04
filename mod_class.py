# define the voice mod class (VMC)

import os
import xml.dom.minidom as xml

import mod_sub_class as VMSC


class wowsVoiceMod:

    name: str
    filepath: str
    mod: VMSC.AudioModification

    def __init__(self, filepath: str, filetype: str = None):
        self.filepath = os.path.abspath(filepath)
        _, filename_full = os.path.split(self.filepath)
        self.name, file_point_ext = os.path.splitext(filename_full)
        if (filetype is None and file_point_ext.find('json') != -1) \
                or (filetype is not None and filetype.find('json') != -1):
            pass

        elif (filetype is None and file_point_ext.find('xml') != -1) \
                or (filetype is not None and filetype.find('xml') != -1):
            self.read_xml()

        else:
            print('file type wrong')
            exit()

    def rename(self, name: str):
        self.name = name

    def read_xml(self) -> bool:
        tree = xml.parse(self.filepath)
        root = tree.documentElement

        self.mod = VMSC.AudioModification(root.getElementsByTagName('Name')[0].firstChild.data)
        events = root.getElementsByTagName('ExternalEvent')

        for event in events:
            name = event.getElementsByTagName('Name')[0].firstChild.data
            container = event.getElementsByTagName('Container')[0]
            cname = container.getElementsByTagName('Name')[0].firstChild.data
            eid = container.getElementsByTagName('ExternalId')[0].firstChild.data
            event_class = VMSC.ExternalEvent(name, cname, eid)

            paths = container.getElementsByTagName('Path')

            for path in paths:
                path_class = VMSC.Path()

                states = path.getElementsByTagName('State')

                for state in states:
                    try:
                        name = state.getElementsByTagName('Name')[0].firstChild.data
                        value = state.getElementsByTagName('Value')[0].firstChild.data
                    except:
                        pass
                    state_class = VMSC.State(name, value)
                    path_class.append_state(state_class)

                files = path.getElementsByTagName('File')

                for file in files:
                    file_class = VMSC.File(file.getElementsByTagName('Name')[0].firstChild.data)
                    path_class.append_file(file_class)

                event_class.append_path(path_class)

            self.mod.append_external_event(event_class)

        return True

    def write_xml(self, path):
        write_path = os.path.abspath(path + self.name + '.xml')

        tree = xml.Document()

        root = tree.createElement('AudioModification.xml')
        tree.appendChild(root)
        mod = tree.createElement('AudioModification')
        root.appendChild(mod)

        mod_name = tree.createElement('Name')
        mod_name.appendChild(tree.createTextNode(self.mod.name))
        mod.appendChild(mod_name)

        for event_class in self.mod.external_event:
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

