import maya.cmds as cmds
mainCtrl="FKTail2_M"

def batch_connectAttr(sel,mainCtrl):
    sel = sel
    attr=['visibility', 'translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ', 'scaleX', 'scaleY', 'scaleZ']
    selAttr=cmds.listAttr(sel,k=1)
    customAttr=[i for i in selAttr if i not in attr]
    stiffnessList=[i for i in customAttr if "stiffness" in i]
    dampingList=[i for i in customAttr if "damping" in i]
    print(dampingList)
    for s,d in zip(stiffnessList,dampingList):
        try:
            cmds.connectAttr("{}.spring_stiffness".format(mainCtrl),"{}.{}".format(sel,s))
            cmds.connectAttr("{}.spring_damping".format(mainCtrl),"{}.{}".format(sel,d))
        except:
            pass 
        
sels=cmds.ls(sl=1)
for sel in sels:
    batch_connectAttr(sel,mainCtrl)
    
    

    