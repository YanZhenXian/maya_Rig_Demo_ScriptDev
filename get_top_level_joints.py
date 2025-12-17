import maya.cmds as cmds

def get_top_level_joints(joint_list):
    top_joints = []
    all_set = set(joint_list)
    for joint in joint_list:
        parent = cmds.listRelatives(joint, parent=True, fullPath=False)
        if not parent or parent[0] not in all_set:
            top_joints.append(joint)
    return top_joints
selected_joints = cmds.ls(selection=True, type="joint")
print selected_joints
top_joints = get_top_level_joints(selected_joints)

print("Top-level joints:")
for jnt in top_joints:
    print(jnt)
