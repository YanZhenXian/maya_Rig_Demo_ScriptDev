import maya.cmds as cmds

def set_outliner_color(r, g, b):
    selection = cmds.ls(selection=True, type='transform')
    if not selection:
        cmds.warning("请先选择一个组对象（transform）")
        return

    for obj in selection:
        if not cmds.attributeQuery('useOutlinerColor', node=obj, exists=True):
            cmds.addAttr(obj, longName='useOutlinerColor', attributeType='bool')
        if not cmds.attributeQuery('outlinerColor', node=obj, exists=True):
            cmds.addAttr(obj, longName='outlinerColor', usedAsColor=True, attributeType='float3')
            cmds.addAttr(obj, longName='outlinerColorR', attributeType='float', parent='outlinerColor')
            cmds.addAttr(obj, longName='outlinerColorG', attributeType='float', parent='outlinerColor')
            cmds.addAttr(obj, longName='outlinerColorB', attributeType='float', parent='outlinerColor')

        cmds.setAttr(obj + ".useOutlinerColor", 1)
        cmds.setAttr(obj + ".outlinerColor", r, g, b, type="double3")

def show_ui():
    if cmds.window("outlinerColorWin", exists=True):
        cmds.deleteUI("outlinerColorWin")

    window = cmds.window("outlinerColorWin", title="设置 Outliner 颜色", widthHeight=(320, 280))
    cmds.columnLayout(adjustableColumn=True, rowSpacing=8)

    # RGB sliders
    r_slider = cmds.floatSliderGrp(label="R", field=True, min=0, max=1, value=0.5)
    g_slider = cmds.floatSliderGrp(label="G", field=True, min=0, max=1, value=0.5)
    b_slider = cmds.floatSliderGrp(label="B", field=True, min=0, max=1, value=0.5)

    # Color preview
    color_preview = cmds.canvas(rgbValue=(0.5, 0.5, 0.5), width=100, height=40)

    def update_preview(*args):
        r = cmds.floatSliderGrp(r_slider, query=True, value=True)
        g = cmds.floatSliderGrp(g_slider, query=True, value=True)
        b = cmds.floatSliderGrp(b_slider, query=True, value=True)
        cmds.canvas(color_preview, edit=True, rgbValue=(r, g, b))

    def on_set_color(*args):
        update_preview()
        r = cmds.floatSliderGrp(r_slider, query=True, value=True)
        g = cmds.floatSliderGrp(g_slider, query=True, value=True)
        b = cmds.floatSliderGrp(b_slider, query=True, value=True)
        set_outliner_color(r, g, b)

    cmds.floatSliderGrp(r_slider, edit=True, dragCommand=update_preview)
    cmds.floatSliderGrp(g_slider, edit=True, dragCommand=update_preview)
    cmds.floatSliderGrp(b_slider, edit=True, dragCommand=update_preview)

    cmds.button(label="应用颜色到选中组", command=on_set_color)

    cmds.text(label="颜色预设：")

    # 两排颜色按钮，每排 8 个
    color_presets = [
        (1, 0, 0),      # 红
        (0, 1, 0),      # 绿
        (0, 0, 1),      # 蓝
        (1, 1, 0),      # 黄
        (0, 1, 1),      # 青
        (1, 0, 1),      # 紫
        (1, 0.5, 0),    # 橙
        (0.3, 0.3, 0.3),# 深灰
        (0.6, 0.6, 0.6),# 浅灰
        (1, 1, 1),      # 白
        (0, 0, 0),      # 黑
        (0.8, 0.2, 0.2),# 桃红
        (0.2, 0.6, 0.2),# 草绿
        (0.2, 0.4, 1),  # 天蓝
        (0.5, 0.2, 0.6),# 暗紫
        (0.2, 0.2, 0.6) # 深蓝
    ]

    def apply_preset_color(rgb):
        r, g, b = rgb
        cmds.floatSliderGrp(r_slider, edit=True, value=r)
        cmds.floatSliderGrp(g_slider, edit=True, value=g)
        cmds.floatSliderGrp(b_slider, edit=True, value=b)
        update_preview()

    for i in range(0, len(color_presets), 8):
        cmds.rowLayout(numberOfColumns=8, columnAttach=[(i+1, 'both', 1) for i in range(8)], adjustableColumn=8)
        for rgb in color_presets[i:i+8]:
            def make_callback(c=rgb):
                return lambda *_: apply_preset_color(c)
            cmds.button(label="", width=30, height=20, backgroundColor=rgb, command=make_callback(rgb))
        cmds.setParent("..")

    cmds.setParent("..")
    cmds.showWindow(window)

# 运行 UI
show_ui()
