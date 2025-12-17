import maya.cmds as cmds

selection = cmds.ls(sl=True)
for i in selection:
    cmds.setAttr("{}.preInfinity".format(i),4)
    cmds.setAttr("{}.postInfinity".format(i),4)