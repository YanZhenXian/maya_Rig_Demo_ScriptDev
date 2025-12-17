import maya.cmds as cmds
import rigUtils.Rig_utils as ru
def create_bend_for_Feather(obj):
    if not cmds.objExists("feather_blnd_Grp"):
        cmds.createNode("transform",name="feather_blnd_Grp")
    loc = cmds.spaceLocator(name="{}_Loc".format(obj))[0]
    cmds.matchTransform(loc, obj, pos=1, rot=1)
    attach_geo=obj
    fol_loc=ru.create_follicle(grp_parent=None, geo=attach_geo, ctrl=loc)
    
    fol=cmds.listRelatives(fol_loc,p=True)[0]
    
    cmds.setAttr("{}.parameterU".format(fol),0.4)
    cmds.setAttr("{}.parameterV".format(fol),0.5)
    fol_Aim_loc=cmds.duplicate(fol_loc,name="{}_Aim_Loc".format(obj))[0]
    
    print(fol_Aim_loc)
    
    cmds.setAttr("{}.tx".format(fol_Aim_loc),5)
    cmds.parent(fol_Aim_loc,"Follicle_Grp")
    
    bend, handle = cmds.nonLinear(obj, type='bend', name=obj + '_bend')
    cmds.setAttr(bend + '.highBound', 1)
    cmds.setAttr(bend + '.lowBound', 0)
    cmds.setAttr(bend + '.curvature', 90) 
    cmds.matchTransform(handle,fol_loc,pos=True)
    cmds.aimConstraint(fol_Aim_loc,handle,offset=(0 ,0 ,0), weight=1,aimVector=[0 ,1, 0],upVector=(1 ,0 ,0) ,worldUpType="vector" ,worldUpVector=[0 ,1, 0])
    feather_blnd=cmds.duplicate(obj,name="{}_BLND".format(obj))[0]
    cmds.parent(feather_blnd,"feather_blnd_Grp")
    
obj_List = cmds.ls(sl=True)
for obj in obj_List:
    create_bend_for_Feather(obj)
    


