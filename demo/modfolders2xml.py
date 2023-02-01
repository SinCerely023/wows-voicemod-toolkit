import os

from src.VoiceoverModKernel import VoiceoverModKernel

if __name__ == '__main__':

    path_in = input('mod xml directory:\n')
    path_in = os.path.abspath(path_in)

    if not os.path.exists(path_in):
        print("directory '" + path_in + "' not existed, please check\n")
        os.system('pause')
        exit()

    try:
        wvm = VoiceoverModKernel(path_in)
    except:
        print("read directory '" + path_in + "' error, please check\n")
        os.system('pause')
        exit()
    else:
        print('read directory successful\n')
        print("the name of mod is '" + wvm.mod_class.name + "'\n")

        try:
            wvm.rename_source(wvm.mod_class.name)
            wvm.adapt_air_support()
            wvm.write_xml(path_in)
        except:
            print('create xml error, please check')
            os.system('pause')
            exit()
        else:
            print('create xml successful, press any key to exit')
            os.system('pause')
            exit()
