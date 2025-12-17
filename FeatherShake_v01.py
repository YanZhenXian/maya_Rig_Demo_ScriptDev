import maya.cmds as cmds
#con_List=cmds.ls(sl=True)
#ad=cmds.listConnections("nurbsPlane1719_BLND_bendHandle",d=True)
#nodes=[i for i in ad if cmds.nodeType(i)=="nonLinear"]
#node=list(set(node))
print(node)
ctrl="WingAttr_R"
if not cmds.objExists("{}.FeatherShake".format(ctrl)):
    cmds.addAttr(ctrl,ln="FeatherShake",at=long,min=0,max=1,dv=0)
if not cmds.objExists("{}.FeatherShakeAmplitude".format(ctrl)):
    cmds.addAttr(ctrl,ln="FeatherShakeAmplitude" ,nn="Feather Shake Amplitude",at=double,dv=1)

objList=cmds.ls(sl=True)    
for obj in objList:   
    noiseNode=cmds.createNode("noise")
    print(noiseNode)
    cmds.connectAttr("time1.outTime","{}.time".format(noiseNode))
    
    MD_NodeA=cmds.createNode('multDoubleLinear', n="{}_MDNodeA".format(obj))
    cmds.setAttr("{}.input2".format(MD_NodeA),2)
    MD_NodeB=cmds.createNode('multDoubleLinear', n="{}_MDNodeB".format(obj))    
    ConditionNodeD=cmds.createNode('condition', n="{}_ConditionNodeD".format(obj))
    cmds.setAttr("{}.secondTerm".format(ConditionNodeD),1)
    
    PM_NodeD=cmds.createNode('plusMinusAverage', n="{}_PMNodeD".format(obj))
    
    cmds.connectAttr("{}.outColor.outColorR".format(noiseNode), "{}.input1".format(MD_NodeA), f=True)
    cmds.connectAttr("{}.output".format(MD_NodeA), "{}.input1".format(MD_NodeB), f=True)
    
    cmds.connectAttr("{}.FeatherShakeAmplitude".format(ctrl), "{}.input2".format(MD_NodeB), f=True)
    
    cmds.connectAttr("{}.FeatherShake".format(ctrl), "{}.firstTerm".format(ConditionNodeD), f=True)
    cmds.connectAttr("{}.output".format(MD_NodeB), "{}.colorIfTrueR".format(ConditionNodeD), f=True)
    cmds.connectAttr("{}.outColorR".format(ConditionNodeD), "{}.input1D[0]".format(PM_NodeD), f=True)
    cmds.connectAttr("{}_MDNodeF.outputX".format(obj), "{}.input1D[1]".format(PM_NodeD), f=True)
    cmds.connectAttr("{}.output1D".format(PM_NodeD), "{}_BLND_bend.curvature".format(obj), f=True)
