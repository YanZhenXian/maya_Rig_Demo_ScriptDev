import maya.cmds as cmds

sel = cmds.ls(sl=True)[0]
FKOffset = "FKOffset{}".format(sel[2:])

c1 = cmds.listRelatives(FKOffset, c=True) or []
print("子节点:", c1)

c2 = [i for i in c1 if cmds.nodeType(i) == 'transform']
print("Transform 类型子节点:", c2)

# 创建 FK Global 控制器
FKGlobal = cmds.duplicate(sel, parentOnly=True, name="FKGlobal{}".format(sel[2:]))[0]
FKGlobalStatic = cmds.duplicate(sel, parentOnly=True, name="FKGlobalStatic{}".format(sel[2:]))[0]
cmds.parent(FKGlobal, FKGlobalStatic)
cmds.parent(FKGlobalStatic, FKOffset)
cmds.parent(c2, FKGlobal)

# 创建 Global 控制器
Global = cmds.duplicate(sel, parentOnly=True, name="Global{}".format(sel[2:]))[0]
GlobalOffset = cmds.duplicate(sel, parentOnly=True, name="GlobalOffset{}".format(sel[2:]))[0]
cmds.parent(Global, GlobalOffset)
cmds.parent(GlobalOffset, "GlobalFollowMain")

# 添加约束
cmds.orientConstraint(Global, FKGlobal, mo=True)
cnst = cmds.orientConstraint(FKGlobalStatic, FKGlobal, mo=True)

# 添加属性
if not cmds.objExists("{}.Global".format(sel)):
    cmds.addAttr(sel, ln="Global", at="double", min=0, max=10, dv=0, keyable=True)

# 创建 reverse 节点
ReverseNode = cmds.createNode("reverse", name="globalReverse{}".format(sel[2:]))

# 连接属性
multNode=cmds.createNode("multDoubleLinear")
cmds.setAttr("{}.input2".format(multNode),0.1)
cmds.connectAttr("{}.Global".format(sel), "{}.input1".format(multNode))
cmds.connectAttr("{}.output".format(multNode), "{}.inputX".format(ReverseNode))

# 获取权重目标列表
targets = cmds.orientConstraint(cnst, q=True, targetList=True)

# 确保权重连接正确
cmds.connectAttr("{}.outputX".format(ReverseNode), "{}.{}W1".format(cnst[0], targets[1]))
cmds.connectAttr("{}.Global".format(sel), "{}.{}W0".format(cnst[0], targets[0]))
