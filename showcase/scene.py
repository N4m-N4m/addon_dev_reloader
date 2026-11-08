import sys, os, bpy, addon_utils
sys.path.insert(0, os.environ["ADR_HARNESS_DIR"])  # folder holding bl_ui_harness.py
import bl_ui_harness as H
W = os.environ["ADR_WORK"]  # work folder: res/, demo/, out/
SCALE = float(os.environ.get("ADR_SCALE", "1.0"))
PHASE = os.environ.get("ADR_PHASE", "probe")

def setup(h):
    bpy.context.preferences.view.ui_scale = SCALE
    for m in ["node_wrangler", "rigify", "copy_global_transform", "io_curve_svg", "io_mesh_uv_layout",
              "pose_library", "io_scene_x3d", "hydra_storm", "ui_translate", "quick_scatter", "addon_dev_reloader"]:
        try: addon_utils.enable(m, default_set=True)
        except Exception as e: print("NOENABLE", m, e)
    h.window.workspace = bpy.data.workspaces["Scripting"]
    yield 1.0
    scr = h.window.screen
    for a in scr.areas:
        if a.type == 'PROPERTIES':
            a.spaces.active.context = 'OBJECT'
        if a.type == 'TEXT_EDITOR':
            t = bpy.data.texts.load(os.path.join(W, "res", "scripts", "addons", "quick_scatter", "__init__.py"))
            sp = a.spaces.active
            sp.text = t; sp.show_line_numbers = True; sp.show_syntax_highlight = True
            sp.top = 30; sp.font_size = 12; sp.show_region_footer = False
    bpy.context.view_layer.objects.active = bpy.data.objects["Cube"]
    bpy.data.objects["Cube"].select_set(True)
    bpy.context.scene.dev_reload_module = "quick_scatter"
    for a in scr.areas: a.tag_redraw()
    yield 1.0


def win(h, x, y):
    """window coords from a top-left pixel of the window screenshot"""
    return int(x), int(h.window.height - y)

def move(h, x, y):
    wx, wy = win(h, x, y)
    h.window.event_simulate(type='MOUSEMOVE', value='NOTHING', x=wx, y=wy)
    h.pointer = (wx, wy)

def click(h, x, y):
    move(h, x, y); yield 0.3
    wx, wy = h.pointer
    h.window.event_simulate(type='LEFTMOUSE', value='PRESS', x=wx, y=wy)
    h.window.event_simulate(type='LEFTMOUSE', value='RELEASE', x=wx, y=wy)
    yield 0.2

def props_to_bottom(h):
    a = h.area('PROPERTIES')
    with h.override(a):
        for _ in range(40):
            bpy.ops.view2d.scroll_down(deltay=60)

def park(h):
    move(h, 900, 700)  # empty part of the text editor

def scenario(h):
    yield from setup(h)
    props_to_bottom(h)
    park(h)
    yield 1.0
    if PHASE == "story":
        h.shot("a_before.png"); yield 0.3
        # the developer edits and saves the add-on
        src = os.path.join(W, "demo", "v2.py")
        dst = os.path.join(W, "res", "scripts", "addons", "quick_scatter", "__init__.py")
        open(dst, "w").write(open(src).read())
        ta = h.area('TEXT_EDITOR')
        with h.override(ta):
            bpy.ops.text.reload()
        ta.spaces.active.top = 30
        yield 0.8
        rx = h.window.width - 15
        move(h, rx, 12); yield 0.3
        move(h, rx, 13); yield 1.6
        h.shot("b_hover.png")
        yield from click(h, rx, 13)
        yield 0.6
        props_to_bottom(h)
        yield 0.4
        h.shot("c_after.png")
        yield 0.3
    else:
        px = h.window.width - 15 - 21 * SCALE
        yield from click(h, px, 12 * SCALE)
        yield 1.0
        hx, hy = map(int, os.environ.get("ADR_HOVER1", "0,0").split(","))
        if hx: move(h, hx, hy); yield 0.6
        h.shot("d_picker.png")
        for ch in "sc":
            wx, wy = h.pointer
            h.window.event_simulate(type='TEXTINPUT', value='PRESS', x=wx, y=wy, unicode=ch)
        yield 1.0
        print("WINSIZE", h.window.width, h.window.height)
        h.shot("e_search.png")
        # rest the pointer on the first result so it reads as the pick
        move(h, *map(int, os.environ.get("ADR_HOVER2", "1700,67").split(","))); yield 0.6
        h.shot("f_search_hover.png")
        yield 0.2

H.run(scenario)
