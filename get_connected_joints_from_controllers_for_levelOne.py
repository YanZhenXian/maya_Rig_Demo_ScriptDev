import maya.cmds as cmds

def get_connected_joints_from_controllers():
    """
    返回当前选择的控制器及其**第一层子物体**所连接或约束的 joint。
    包括：
    - 属性连接 (connectAttr)
    - 约束驱动 (parent/orient/point/scaleConstraint)
    """
    selection = cmds.ls(sl=True, long=True)
    if not selection:
        cmds.warning("请先选择控制器或控制组")
        return []

    joints = set()

    def is_joint(node):
        return cmds.nodeType(node) == 'joint'

    def find_connected_joints(node):
        conn_pairs = cmds.listConnections(node, s=False, d=True, plugs=True, connections=True) or []
        for i in range(0, len(conn_pairs), 2):
            src_attr = conn_pairs[i]
            dest_attr = conn_pairs[i + 1]

            dest_node = dest_attr.split('.')[0]
            if not cmds.objExists(dest_node):
                continue

            dest_type = cmds.nodeType(dest_node)

            if is_joint(dest_node):
                joints.add(dest_node)
                print("连接到 joint 属性: {} → {}".format(src_attr, dest_attr))

            elif dest_type in ['parentConstraint', 'orientConstraint', 'pointConstraint', 'scaleConstraint']:
                targets = cmds.listConnections(dest_node + '.constraintParentInverseMatrix', s=True, d=False) or []
                for t in targets:
                    if is_joint(t):
                        joints.add(t)
                        print("约束驱动 joint: {}".format(t))
            else:
                find_connected_joints(dest_node)

    for ctrl in selection:
        children = cmds.listRelatives(ctrl, c=True, type="transform", fullPath=True) or []
        all_nodes = [ctrl] + children
        for node in all_nodes:
            find_connected_joints(node)

    if not joints:
        print("没有找到任何连接的 joint")
    return list(joints)
joints = get_connected_joints_from_controllers()
print("控制器连接的骨骼：", joints)

