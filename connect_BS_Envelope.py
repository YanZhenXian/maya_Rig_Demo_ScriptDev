import maya.cmds as cmds

def list_blendshapes_on_selection(ctrl,objs):
    sel = objs
    if not sel:
        cmds.warning("请先选择一个或多个模型")
        return []

    blendshapes = []
    for obj in sel:
        history = cmds.listHistory(obj, pdo=True) or []
        bs_nodes = cmds.ls(history, type="blendShape")
        if bs_nodes:
            blendshapes.extend(bs_nodes)
    
    # 去重
    blendshapes = list(set(blendshapes))
    #print("找到的 BlendShape 节点:", blendshapes)
    for bs in blendshapes:
        cmds.connectAttr("{}.FeatherBS_Envelope".format(ctrl),"{}.envelope".format(bs))
        print("bs:{}".format(bs))
        print("ctrl:{}".format(ctrl))


ads=cmds.listRelatives("eagle_R_outerwing",ad=1,typ="transform")
print(ads)
ctrl="WingAttr_R"

list_blendshapes_on_selection(ctrl,ads)
    

