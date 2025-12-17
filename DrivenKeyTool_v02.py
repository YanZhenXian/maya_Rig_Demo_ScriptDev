import maya.cmds as cmds

class DrivenKeyTool:
    def __init__(self):
        self.window = "DrivenKeyToolUI"
        self.driver = ""
        self.driven = ""
        self.build_ui()

    def build_ui(self):
        if cmds.window(self.window, exists=True):
            cmds.deleteUI(self.window)

        cmds.window(self.window, title="Driven Key Tool", sizeable=True)
        cmds.columnLayout(adjustableColumn=True, rowSpacing=10, columnAlign="center")

        cmds.text(label="--- Driven Key Tool ---", height=20)

        cmds.rowLayout(nc=3, adjustableColumn=2)
        cmds.text(label="Driver: ")
        self.driverField = cmds.textField()
        cmds.button(label="Pick", c=self.pick_driver)
        cmds.setParent("..")

        cmds.rowLayout(nc=3, adjustableColumn=2)
        cmds.text(label="Driven: ")
        self.drivenField = cmds.textField()
        cmds.button(label="Pick", c=self.pick_driven)
        cmds.setParent("..")

        cmds.text(label="Driver Attribute:")
        self.driverAttrField = cmds.textField()

        cmds.text(label="Driven Attribute:")
        self.drivenAttrField = cmds.textField()

        cmds.text(label="Driver Values (comma-separated, e.g. 0,45,90):")
        self.driverValsField = cmds.textField()

        cmds.text(label="Driven Values (comma-separated, e.g. 0,10,30):")
        self.drivenValsField = cmds.textField()

        cmds.button(label="Create Driven Keys", c=self.create_driven_keys, bgc=(0.6, 0.8, 0.6))
        cmds.setParent("..")
        cmds.showWindow(self.window)

    def pick_driver(self, *args):
        sel = cmds.ls(selection=True)
        if sel:
            self.driver = sel[0]
            cmds.textField(self.driverField, edit=True, text=self.driver)
    
            attr = self.get_selected_channelbox_attr()
            if attr:
                cmds.textField(self.driverAttrField, edit=True, text=attr)
    
                # 查询最大值
                if cmds.attributeQuery(attr, node=self.driver, maxExists=True):
                    max_val = cmds.attributeQuery(attr, node=self.driver, max=True)[0]
                    cmds.textField(self.driverValsField, edit=True, text=str(max_val))
    
    def pick_driven(self, *args):
        sel = cmds.ls(selection=True)
        if sel:
            self.driven = sel[0]
            cmds.textField(self.drivenField, edit=True, text=self.driven)
    
            attr = self.get_selected_channelbox_attr()
            if attr:
                cmds.textField(self.drivenAttrField, edit=True, text=attr)
    
                # 查询最大值
                if cmds.attributeQuery(attr, node=self.driven, maxExists=True):
                    max_val = cmds.attributeQuery(attr, node=self.driven, max=True)[0]
                    cmds.textField(self.drivenValsField, edit=True, text=str(max_val))

    def get_selected_channelbox_attr(self):
        attrs = cmds.channelBox('mainChannelBox', q=True, selectedMainAttributes=True)
        if attrs:
            return attrs[0]  # 只取第一个
        return ""

    def create_driven_keys(self, *args):
        driver = cmds.textField(self.driverField, q=True, text=True)
        driven = cmds.textField(self.drivenField, q=True, text=True)
        driver_attr = cmds.textField(self.driverAttrField, q=True, text=True)
        driven_attr = cmds.textField(self.drivenAttrField, q=True, text=True)
        driver_vals = cmds.textField(self.driverValsField, q=True, text=True).split(',')
        driven_vals = cmds.textField(self.drivenValsField, q=True, text=True).split(',')

        if len(driver_vals) != len(driven_vals):
            cmds.warning("Driver and Driven value count must match.")
            return

        for drv_val, drn_val in zip(driver_vals, driven_vals):
            try:
                drv_val_f = float(drv_val)
                drn_val_f = float(drn_val)
            except:
                cmds.warning("Invalid float value in input.")
                return

            try:
                cmds.setAttr(f"{driver}.{driver_attr}", drv_val_f)
                cmds.setAttr(f"{driven}.{driven_attr}", drn_val_f)
                cmds.setDrivenKeyframe(f"{driven}.{driven_attr}",
                                       cd=f"{driver}.{driver_attr}",
                                       dv=drv_val_f,
                                       v=drn_val_f)
            except Exception as e:
                cmds.warning("Driven key creation failed: " + str(e))
                return

        cmds.inViewMessage(amg="✅ <hl>Driven Keys Created</hl>", pos='topCenter', fade=True)

# 启动工具
DrivenKeyTool()
