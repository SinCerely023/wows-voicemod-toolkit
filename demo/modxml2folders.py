import os

from wows_voicemod_toolkit import wowsVoiceMod

if __name__ == '__main__':

    path_in = input('mod xml file directory/path:\n')
    path_in = os.path.abspath(path_in)

    if not os.path.exists(path_in):
        print("file '" + path_in + "' not existed, please check\n")
        os.system('pause')
        exit()

    if not os.path.isfile(path_in):
        path_in = os.path.join(path_in, 'mod.xml')
    else:
        directory, filename_full = os.path.split(path_in)
        filename, file_point_ext = os.path.splitext(filename_full)

    if not os.path.exists(path_in):
        print("file '" + path_in + "' not existed, please check\n")
        os.system('pause')
        exit()

    try:
        wvm = wowsVoiceMod(path_in)
    except:
        print("read file '" + path_in + "' error, please check\n")
        os.system('pause')
        exit()
    else:
        print('read file successful\n')
        print("the name of mod is '" + wvm.mod_class.name + "'\n")

        path_in = input('mod folders output directory:\n')
        path_in = os.path.abspath(path_in)

        try:
            wvm.rename(wvm.mod_class.name)
            if not wvm.write_folder(path_in):
                os.system('pause')
                exit()
        except:
            print('create folders error, please check')
            os.system('pause')
            exit()
        else:
            print('create folders successful, press any key to exit')
            os.system('pause')
            exit()
