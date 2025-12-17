import maya.cmds as cmds

def fix_blendshape_order():
    sel = cmds.ls(sl=True, long=True)
    if not sel:
        cmds.warning("请先选择一个或多个模型")
        return

    for obj in sel:
        # 获取 shape 节点
        shapes = cmds.listRelatives(obj, s=True, ni=True, fullPath=True) or []
        if not shapes:
            cmds.warning("找不到 shape: {}".format(obj))
            continue
        shape = shapes[0]

        # 获取 deformers（仅 deformers 类型节点）
        history = cmds.listHistory(shape, pdo=True) or []
        deformers = [h for h in history if cmds.nodeType(h) in ['blendShape', 'skinCluster']]

        blend_nodes = [n for n in deformers if cmds.nodeType(n) == 'blendShape']
        skin_nodes = [n for n in deformers if cmds.nodeType(n) == 'skinCluster']

        if not blend_nodes or not skin_nodes:
            continue  # 如果没有 blend 或 skin，就跳过

        skin = skin_nodes[0]  # 通常只有一个 skinCluster

        for blend in blend_nodes:
            deform_order = cmds.listHistory(shape, il=1, pdo=True) or []
            if blend in deform_order and skin in deform_order:
                bs_index = deform_order.index(blend)
                sk_index = deform_order.index(skin)

                if bs_index > sk_index:
                    # 顺序错误，blend 在 skin 后，修复
                    cmds.reorderDeformers(blend, skin, shape)
                    print("已修复顺序: {} 在 {} 前".format(blend, skin))
                else:
                    print("顺序正确: {} 已在 {} 前".format(blend, skin))
            else:
                print("未在 deform 顺序中找到 {} 或 {}".format(blend, skin))

fix_blendshape_order()
