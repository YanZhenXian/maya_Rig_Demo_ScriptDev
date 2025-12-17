import maya.cmds as cmds

def check_geometry_side(obj):
    if not cmds.objExists(obj):
        return "{} 不存在".format(obj)

    # 获取世界空间下的 bounding box [minX, minY, minZ, maxX, maxY, maxZ]
    bbox = cmds.exactWorldBoundingBox(obj)
    center_x = (bbox[0] + bbox[3]) / 2.0

    if center_x > 0.001:
        return "{} 在右边 (BBox Center X: {:.3f})".format(obj, center_x)
    elif center_x < -0.001:
        return "{} 在左边 (BBox Center X: {:.3f})".format(obj, center_x)
    else:
        return "{} 在中线附近 (BBox Center X: {:.3f})".format(obj, center_x)

# 判断当前选中的物体
selection = cmds.ls(selection=True)
if selection:
    for obj in selection:
        print(check_geometry_side(obj))
else:
    print("请先选择一个或多个模型")
