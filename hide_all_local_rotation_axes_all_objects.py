import maya.cmds as cmds

def hide_all_local_rotation_axes_all_objects():
    all_transforms = cmds.ls(type="transform")
    for obj in all_transforms:
        if cmds.attributeQuery("displayLocalAxis", node=obj, exists=True):
            try:
                cmds.setAttr(obj + ".displayLocalAxis", 0)
            except:
                pass  # 忽略无法设置的节点

hide_all_local_rotation_axes_all_objects()
