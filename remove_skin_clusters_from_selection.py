import maya.cmds as cmds

def remove_skin_clusters_from_selection():
    sel = cmds.ls(selection=True, long=True)
    if not sel:
        cmds.warning("请选择一个或多个对象")
        return

    # 获取所有包含的 transform 节点
    all_objs = cmds.listRelatives(sel, allDescendents=True, type='transform', fullPath=True) or []
    all_objs += sel
    all_objs = list(set(all_objs))  # 去重

    removed = []

    for obj in all_objs:
        shapes = cmds.listRelatives(obj, shapes=True, fullPath=True) or []
        for shape in shapes:
            history = cmds.listHistory(shape, pruneDagObjects=True) or []
            skin_clusters = [node for node in history if cmds.nodeType(node) == 'skinCluster']
            for sc in skin_clusters:
                try:
                    cmds.skinCluster(sc, edit=True, unbind=True)
                    removed.append((obj, sc))
                except Exception as e:
                    print("❌ 无法移除: {} 的 skinCluster: {}，错误: {}".format(obj, sc, e))

    print("✅ 完成，共解绑 {} 个 skinCluster:".format(len(removed)))
    for obj, sc in removed:
        print(" - {} (skinCluster: {})".format(obj, sc))

# 执行
remove_skin_clusters_from_selection()
