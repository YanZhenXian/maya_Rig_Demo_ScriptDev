import maya.cmds as cmds

def get_connected_joints_from_controllers():
    """
    返回选择的控制器及其子节点，所连接或约束的所有 joint
    """
    selection = cmds.ls(sl=True, long=True)
    if not selection:
        cmds.warning("请先选择控制器或控制组")
        return []

    joints = set()

    def is_joint(node):
        return cmds.nodeType(node) == 'joint'

    def find_connected_joints(node):
        # 用 connection=True 获取详细连接对
        conn_pairs = cmds.listConnections(node, s=False, d=True, plugs=True, connections=True) or []
        if not conn_pairs:
            return

        # 成对遍历：每次2个（srcAttr, destAttr）
        for i in range(0, len(conn_pairs), 2):
            src_attr = conn_pairs[i]
            dest_attr = conn_pairs[i + 1]

            dest_node = dest_attr.split('.')[0]
            if not cmds.objExists(dest_node):
                continue

            node_type = cmds.nodeType(dest_node)

            if is_joint(dest_node):
                joints.add(dest_node)
                print("找到 joint 属性连接: {} -> {}".format(src_attr, dest_attr))

            elif node_type in ['parentConstraint', 'orientConstraint', 'pointConstraint', 'scaleConstraint']:
                targets = cmds.listConnections(dest_node + '.constraintParentInverseMatrix', s=True, d=False) or []
                for target in targets:
                    if is_joint(target):
                        joints.add(target)
                        
            else:
                # 递归查找下游连接
                find_connected_joints(dest_node)

    for ctrl in selection:
        all_nodes = cmds.listRelatives(ctrl, ad=True, fullPath=True) or []
        all_nodes.append(ctrl)

        for node in all_nodes:
            find_connected_joints(node)

    if not joints:
        print("未找到任何 joint 连接。")
    print("找到约束目标 joint: {}".format(list(joints)))
    return set(list(joints))
    
    
get_connected_joints_from_controllers()
