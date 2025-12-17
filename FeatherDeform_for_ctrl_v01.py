import pymel.core as pm
import maya.cmds as cmds
import rigUtils.Rig_utils as utils
def list_all_parents(obj):
    parents = []
    current = obj

    while True:
        parent = cmds.listRelatives(current, parent=True)
        if parent:
            current = parent[0]
            parents.append(current)
        else:
            break

    return parents

def find_controllers_for_joint(jnt):
    if not cmds.objExists(jnt):
        cmds.error("指定的骨骼不存在: {}".format(jnt))
        return []

    # 获取所有进入 joint transform 属性的连接
    connections = cmds.listConnections(jnt, s=True, d=False, plugs=True) or []
    
    controllers = set()
    for conn in connections:
        src_node = conn.split('.')[0]
        if cmds.objectType(src_node) in ['constraint', 'parentConstraint', 'orientConstraint', 'pointConstraint', 'scaleConstraint']:
            # 获取 constraint 的驱动对象（控制器）
            sources = cmds.listConnections(src_node + ".target", s=True, d=False) or []
            for s in sources:
                if cmds.objectType(s) == 'transform':
                    controllers.add(s)
        else:
            # 如果是直接连接，例如 FK 控制器直接连接了 joint 的 rotateX 等
            if cmds.objectType(src_node) == 'transform':
                controllers.add(src_node)

    return list(controllers)

weightedJnts=[]
def list_all_points():
    sel = cmds.ls(selection=True, long=True)
    if not sel:
        cmds.error("请先选择模型或曲面对象")
        return

    all_points = []

    for obj in sel:
        shapes = cmds.listRelatives(obj, shapes=True, fullPath=True)
        if not shapes:
            continue
        shape = shapes[0]
        shape_type = cmds.nodeType(shape)

        # Polygon 网格
        if shape_type == "mesh":
            vtx_count = cmds.polyEvaluate(shape, vertex=True)
            for i in range(vtx_count):
                all_points.append("{}.vtx[{}]".format(obj, i))

        # Nurbs 曲面
        elif shape_type == "nurbsSurface":
            spans_u = cmds.getAttr("{}.spansU".format(shape))
            spans_v = cmds.getAttr("{}.spansV".format(shape))
            deg_u = cmds.getAttr("{}.degreeU".format(shape))
            deg_v = cmds.getAttr("{}.degreeV".format(shape))
            cv_count_u = spans_u + deg_u
            cv_count_v = spans_v + deg_v

            for u in range(cv_count_u):
                for v in range(cv_count_v):
                    all_points.append("{}.cv[{}][{}]".format(obj, u, v))

        else:
            print("不支持的类型: {}".format(shape_type))

    return all_points

def getWeightedJnt(vtx):
    #driver=pm.ls(sl=1,fl=1)[0]
    print(driver)
    
    meshNames =pm.PyNode(vtx)
    print(meshNames)
    
    mesh_SkinCluster=meshNames.history(type="skinCluster")[0]
    infJnts=mesh_SkinCluster.getWeightedInfluence()
    
    for infJnt in infJnts:
    
    	wi=pm.skinPercent(mesh_SkinCluster,vtx,transform=infJnt, query=True)
    	if wi>0.01:
    	    print(wi)
    	    weightedJnts.append(infJnt)
    #print("weightedJnts:{}".format(weightedJnts))
    		#pm.parentConstraint(infJnt,driven,weight=wi,mo=1)
all_pts = list_all_points()
for p in all_pts:
    cv=p.split("|")[-1]
    #print(cv)
    getWeightedJnt(cv)
weightedJnts=list(dict.fromkeys(weightedJnts))
weightedJnts.pop(0)
weightedJnts.pop()

for jnt in weightedJnts:    
    controllers = find_controllers_for_joint(jnt.name())
    #print("控制 {} 的控制器有:".format(jnt))
    for ctrl in controllers:
        print(" -", ctrl)
        name = ctrl
        if name.startswith("FK"):
            name = name[2:]
        print(name)
        FKOffset="FKOffset{}".format(name)
        FKPS2="FKPS2{}".format(name)
        cmds.orientConstraint(FKPS2,FKOffset,mo=True)
        #Loc=utils.create_follicle(grp_parent=None, geo=planeMesh, ctrl=obj)

#print("weightedJnts:{}".format(weightedJnts))

