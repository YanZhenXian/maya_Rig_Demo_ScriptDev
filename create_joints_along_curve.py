import maya.cmds as cmds

def create_joints_along_curve(curve, num_joints):
    if not cmds.objExists(curve):
        cmds.warning("Curve does not exist: {}".format(curve))
        return

    shape = cmds.listRelatives(curve, shapes=True, fullPath=True)[0]
    if cmds.nodeType(shape) != "nurbsCurve":
        cmds.warning("Please select a NURBS curve.")
        return

    joint_list = []
    for i in range(num_joints):
        param = float(i) / (num_joints - 1) if num_joints > 1 else 0.5
        point = cmds.pointOnCurve(curve, pr=param, p=True, top=True)
        cmds.select(clear=True)  # Prevent auto-parenting
        joint_name = "joint_{:02d}".format(i + 1)
        jnt = cmds.joint(name=joint_name, position=point)
        joint_list.append(jnt)

    # Parent joints in a chain
    for i in range(len(joint_list) - 1):
        cmds.parent(joint_list[i + 1], joint_list[i])

    # Orient joints to point X toward children
    cmds.select(joint_list[0])
    cmds.joint(edit=True, orientJoint="xyz", secondaryAxisOrient="yup", children=True, zeroScaleOrient=True)

    # Match the last joint's orientation to its parent
    if len(joint_list) >= 2:
        last_joint = joint_list[-1]
        parent_joint = joint_list[-2]
        orient = [cmds.getAttr("{}.jointOrient{}".format(parent_joint, axis)) for axis in "XYZ"]
        for i, axis in enumerate("XYZ"):
            cmds.setAttr("{}.jointOrient{}".format(last_joint, axis), orient[i])


    cmds.select(clear=True)
    return joint_list

def open_joint_tool_ui():
    if cmds.window("curveJointUI", exists=True):
        cmds.deleteUI("curveJointUI")

    window = cmds.window("curveJointUI", title="Joints Along Curve", widthHeight=(300, 100))
    cmds.columnLayout(adjustableColumn=True, rowSpacing=8, columnAlign="center")

    cmds.intSliderGrp("jointCountSlider", field=True, label="Number of Joints", 
                      minValue=2, maxValue=50, fieldMinValue=1, fieldMaxValue=200, value=5)

    cmds.button(label="Create Joints", command=lambda x: on_create_joints())
    cmds.setParent("..")
    cmds.showWindow(window)

def on_create_joints():
    sel = cmds.ls(sl=True)
    if not sel:
        cmds.warning("Please select a NURBS curve first.")
        return

    curve = sel[0]
    num_joints = cmds.intSliderGrp("jointCountSlider", query=True, value=True)
    create_joints_along_curve(curve, num_joints)

# Run the tool
open_joint_tool_ui()
