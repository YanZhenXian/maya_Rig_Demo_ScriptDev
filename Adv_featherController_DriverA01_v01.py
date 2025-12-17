import maya.cmds as cmds
import maya.api.OpenMaya as om
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


def create_plane_perpendicular_to_joint_y():
    selection = cmds.ls(sl=True)
    if not selection:
        cmds.error("请先选择一个或多个骨骼。")
        return
    planeGrp="folGeo_Grp"
    if not cmds.objExists(planeGrp):
        cmds.createNode("transform",name=planeGrp)

    for obj in selection:
        
        # 获取位置
        pos = cmds.xform(obj, q=True, ws=True, t=True)

        # 获取世界矩阵
        m = cmds.xform(obj, q=True, ws=True, m=True)
        matrix = om.MMatrix(m)

        # 提取骨骼的Y轴向量（世界空间）
        y_axis = om.MVector(matrix[1], matrix[5], matrix[9]).normalize()

        # 选择一个与Y轴不平行的参考向量
        ref = om.MVector(0, 0, 1) if abs(y_axis * om.MVector(0, 0, 1)) < 0.99 else om.MVector(1, 0, 0)

        # 计算垂直于 Y 的法线方向（作为 Z轴）
        z_axis = (ref ^ y_axis).normalize()  # 法线方向 ⟂ Y
        x_axis = (y_axis ^ z_axis).normalize()  # 确保正交
        y_axis = (z_axis ^ x_axis).normalize()  # 重算 y_axis 保正交系

        # 构建旋转矩阵（行优先）
        mat = om.MMatrix([
            x_axis.x, x_axis.y, x_axis.z, 0,
            y_axis.x, y_axis.y, y_axis.z, 0,
            z_axis.x, z_axis.y, z_axis.z, 0,
            0,        0,        0,        1
        ])

        # 转换为欧拉角
        transform = om.MTransformationMatrix(mat)
        rot = transform.rotation()
        rot_deg = [om.MAngle(rot.x).asDegrees(), om.MAngle(rot.y).asDegrees(), om.MAngle(rot.z).asDegrees()]

        # 创建面片，默认 Z 是法线
        planeMesh = cmds.polyPlane(w=1, h=1, sx=1, sy=1, axis=(0, 1, 0),name="{}_plane".format(obj), ch=False)[0]
        cmds.scale(0.5, 0.5, 0.5, planeMesh)
        cmds.parent(planeMesh,planeGrp)
        
        cmds.xform(planeMesh, ws=True, t=pos)
        cmds.xform(planeMesh, ws=True, rotation=rot_deg)
        cmds.select(planeMesh)
        cmds.select(obj,tgl=True)
        cmds.matchTransform(rot=True)
        cmds.makeIdentity(planeMesh, apply=True, t=0, r=0, s=1, n=0)
        # 创建Driver Group
        all_parents = list_all_parents(obj)
    
        print("所有父级节点:", all_parents)
        ParentConstraintGrp=[i for i in all_parents if "ParentConstraint" in i][0]
        FKCurveGuideOffset_Grp=[i for i in all_parents if "FKCurveGuideOffset" in i][0]
        FKCurveGuideGrp=[i for i in all_parents if "FKCurveGuideRt" in i][0]
        FKExtraGrp=[i for i in all_parents if "FKExtra" in i][0]
        
        print("FKExtraGrp:", FKExtraGrp)
        print("ParentConstraintGrp:", ParentConstraintGrp)
        #FKDriver_A = cmds.duplicate(FKExtraGrp, parentOnly=True, name="{}_Driver".format(FKExtraGrp))[0]
        #cmds.setAttr(FKDriver_A + ".useOutlinerColor", 1)
        #cmds.setAttr(FKDriver_A + ".outlinerColor", 0.9, 0.6, 0.3, type="double3")
        #FKDriver_OffsetGrp = cmds.duplicate(FKDriver_A, parentOnly=True, name="{}_OffsetGrp".format(FKExtraGrp))[0]
        #FKDriven_FKCurveGuideGrp = cmds.duplicate(FKCurveGuideGrp, parentOnly=True, name="{}_driven".format(FKCurveGuideGrp))[0]
        #cmds.parent(FKDriver_A,FKDriver_OffsetGrp)
        #cmds.parent(FKDriver_OffsetGrp,FKDriven_FKCurveGuideGrp)
        
        #cmds.setAttr(FKDriven_FKCurveGuideGrp + ".useOutlinerColor", 1)
        #cmds.setAttr(FKDriven_FKCurveGuideGrp + ".outlinerColor", 0.9, 0.6, 0.3, type="double3")
        #cmds.orientConstraint(FKCurveGuideGrp,FKDriven_FKCurveGuideGrp,mo=1)
        
        Loc=utils.create_follicle(grp_parent=None, geo=planeMesh, ctrl=obj)
        print("Loc is :{}".format(Loc))
        #driver_cmpMtx_Mult=cmds.createNode("multMatrix",name="{}cmpMtx_Mult".format(obj))
        #cmds.connectAttr("{}.worldMatrix[0]".format(Loc),"{}.matrixIn[0]".format(driver_cmpMtx_Mult))
        #cmds.connectAttr("{}.parentInverseMatrix[0]".format(FKExtraGrp),"{}.matrixIn[1]".format(driver_cmpMtx_Mult))
        
        #driver_DecMtx=cmds.createNode("decomposeMatrix",name="{}DecMtx".format(obj))
        #cmds.connectAttr("{}.matrixSum".format(driver_cmpMtx_Mult),"{}.inputMatrix".format(driver_DecMtx))
        #cmds.connectAttr("{}.outputRotate".format(driver_DecMtx),"{}.rotate".format(FKExtraGrp))
        cmds.pointConstraint(Loc,FKCurveGuideGrp,mo=True)
        #print("FKDriver_A is >>{}".format(FKDriver_A))
        #for attr in ["translate","rotate"]:    
            #cmds.connectAttr("{}.{}X".format(FKDriver_A,attr),
                          # "{}.{}X".format(FKExtraGrp,attr),force=True)
            #cmds.connectAttr("{}.{}Y".format(FKDriver_A, attr),
                           #"{}.{}Y".format(FKExtraGrp, attr),force=True)
            #cmds.connectAttr("{}.{}Z".format(FKDriver_A, attr),
                           #"{}.{}Z".format(FKExtraGrp, attr),force=True)


create_plane_perpendicular_to_joint_y()
