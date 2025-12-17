import pymel.core as pm
import maya.cmds as cmds
import maya. mel as mel

import math


if pm.window( "RigTool_rivetTool_Window", exists=True ):
    pm.deleteUI( "RigTool_rivetTool_Window", window=True )
    
        
window = pm.window( "RigTool_rivetTool_Window", title="RigTool_rivetTool_v1", widthHeight=(650, 600) )

pm.columnLayout( adjustableColumn=True, columnOffset=("both", 4) ) 

pm.rowColumnLayout( numberOfColumns=2, columnWidth=[(1,500),(2,150)], columnSpacing=[(1,0), (2,6)] ) 
pm.setParent("..")                
pm.textFieldButtonGrp( "driver", text="driver_vtx",buttonLabel="Load",cl2=["left","right"],cw=(500,150),adj=1,bc="load_driver()")


pm.textFieldButtonGrp( "driven", text="driven",buttonLabel="Load",cl2=["left","right"],cw=(500,150),adj=1,bc="load_driven()")


pm.separator(h=3)
pm.button(l="Build_Driver",c="Build_Driver()")

pm.setParent("..")
pm.showWindow("RigTool_rivetTool_Window")

def Build_Driver():
	
  
	driver=pm.textFieldButtonGrp("driver",q=1,tx=1)

	meshNames =pm.PyNode(driver)

	driven=pm.textFieldButtonGrp("driven",q=1,tx=1)
	meshHis=meshNames.history(type="skinCluster")[0]
	infJnts=meshHis.getWeightedInfluence()
	
	for infJnt in infJnts:
	
		wi=pm.skinPercent( meshHis,meshNames,transform=infJnt, query=True)
		if wi>0.01:
			pm.parentConstraint(infJnt,driven,weight=wi,mo=1)


def load_driver():
    selJntsList=cmds.ls(sl=1)
    newMashs = [str(i) for i in selJntsList]
    selJntsListStr=str(newMashs)
    selJntsListStr01=selJntsListStr.replace("['","")
    selJntsListStr02=selJntsListStr01.replace("']","")

 
    cmds.textFieldButtonGrp("driver",e=1,tx=selJntsListStr02)
    
def load_driven():
    selJntsList=cmds.ls(sl=1)
    newMashs = [str(i) for i in selJntsList]
    selJntsListStr=str(newMashs)
    selJntsListStr01=selJntsListStr.replace("[","")
    selJntsListStr02=selJntsListStr01.replace("]","")

    selJntsListStr04=selJntsListStr02.replace("'","")
    selJntsListStr05=selJntsListStr04.replace(" ","")
    
    
    cmds.textFieldButtonGrp("driven",e=1,tx=selJntsListStr05)



    
    