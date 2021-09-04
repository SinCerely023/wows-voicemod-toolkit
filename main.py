# from xml.dom.minidom import parse
#
# tree = parse('mod.xml')
# root = tree.documentElement
#
# aa = root.getElementsByTagName('StateList')
#
# for bb in aa:
#     if bb.childNodes.__len__() > 1:
#         print('11')

# with open('mmod.xml', 'w') as f:
#     # tree.writexml(f, indent='', addindent='\t', newl='\n', encoding='utf-8')
#     tree.writexml(f, encoding='utf-8')
#
# a = tree.toprettyxml()

from mod_class import wowsVoiceMod

wvm = wowsVoiceMod('mod.xml')

wvm.rename('test')
wvm.write_xml('./')

pass
