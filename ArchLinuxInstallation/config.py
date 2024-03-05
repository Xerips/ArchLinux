"""
________   __  .__.__           _________                _____.__        
\_____  \_/  |_|__|  |   ____   \_   ___ \  ____   _____/ ____\__| ____  
 /  / \  \   __\  |  | _/ __ \  /    \  \/ /  _ \ /    \   __\|  |/ ___\ 
/   \_/.  \  | |  |  |_\  ___/  \     \___(  <_> )   |  \  |  |  / /_/  >
\_____\ \_/__| |__|____/\___  >  \______  /\____/|___|  /__|  |__\___  / 
       \__>                 \/          \/            \/        /_____/  
~/.config/qtile/config.py
Default Config: /usr/share/doc/qtile/default_config.py
"""

import os
import subprocess

from libqtile import bar, extension, layout, qtile, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from qtile_extras import widget
from qtile_extras.widget.decorations import BorderDecoration

######## Variables ########

mod = "mod4"
terminal = "alacritty"
browser = "firefox"

######## AutoStart ########


@hook.subscribe.startup
def autostart():
    home = os.path.expanduser("~/.config/qtile/autostart.sh")
    subprocess.Popen([home])


######## Keybindings ########

keys = [
    #### Switch between windows ####
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Cycle windows"),
    #### Swap Windows ####
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    #### Adjust window sizes ####
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    #### Toggle between split and unsplit sides of stack. ####
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(), desc="Toggle split"),
    #### Launch Alacritty ####
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    #### Toggle between different layouts as defined below ####
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    #### Kill focused window ####
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    #### Toggle Fullscreen ####
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Toggle Fullscreen"),
    #### Toggle Floating Mode on focus ####
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on window"),
    #### Reload Config ####
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    #### Shutdown Qtile ####
    # Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    #### App Launcher rofi ####
    Key([mod], "r", lazy.spawn("rofi -show drun"), desc="Open rofi app launcher"),
    #### Open Browser ####
    Key([mod], "b", lazy.spawn(browser), desc="Open browser"),
    # Switch focus of monitors
    Key([mod], "o", lazy.next_screen(), desc="Move focus to next monitor"),
    Key([mod], "p", lazy.prev_screen(), desc="Move focus to prev monitor"),
]

######## Desktop Groups ########

groups = []
group_names = ["1", "2", "3", "4"]

# group_labels = ["1", "2", "3", "4"]
# group_labels = ["WORK", "WWW", "SYS", "VM"]
group_labels = ["󰇴", "󰯊", "󱨑", ""]

group_layouts = ["Columns", "Columns", "Columns", "Columns"]

for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i],
            label=group_labels[i],
        )
    )

for i in groups:
    keys.extend(
        [
            # mod4 + group number = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod4 + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
        ]
    )

######## catppuccin ########

catppuccin = {
    "flamingo": "#F3CDCD",
    "mauve": "#DDB6F2",
    "pink": "f5c2e7",
    "maroon": "#e8a2af",
    "red": "#f28fad",
    "peach": "#f8bd96",
    "yellow": "#fae3b0",
    "green": "#abe9b3",
    "teal": "#b4e8e0",
    "blue": "#96cdfb",
    "sky": "#89dceb",
    "white": "#d9e0ee",
    "gray": "#6e6c7e",
    "black": "#1a1826",
    "mantle": "#181825",
    "arch": "#1793D1",
}

######## Layouts ######## You can find more Layouts in Qtile documentation ####

layout_theme = {
    "border_width": 2,
    "margin": 5,
    "border_focus": "AD69AF",
    "border_normal": "1D2330",
}

layouts = [
    layout.Columns(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.Floating(**layout_theme),
    layout.Stack(**layout_theme),
]

######## Widgets and Bar Layout ########

widget_defaults = dict(
    font="Ubuntu Bold",
    fontsize=16,
    padding=0,
    background=catppuccin["black"],
)

extension_defaults = widget_defaults.copy()


def init_widgets_list():
    widgets_list = [
        widget.Image(
            filename="~/.config/qtile/icons/arch.png",
            scale="False",
            mouse_callbacks={
                "Button1": lambda: qtile.cmd_spawn("shutdown -h now")
            },  # -h for a more graceful/safe shutdown.
        ),
        widget.Prompt(font="Ubuntu Mono", fontsize=14, foreground=catppuccin["gray"]),
        widget.GroupBox(
            fontsize=20,
            margin_y=5,
            margin_x=5,
            padding_y=1,
            padding_x=3,
            borderwidth=3,
            active=catppuccin["sky"],
            inactive=catppuccin["gray"],
            rounded=False,
            highlight_color=catppuccin["black"],
            highlight_method="line",
            this_current_screen_border=catppuccin["mauve"],
            this_screen_border=catppuccin["green"],
            other_current_screen_border=catppuccin["mauve"],
            other_screen_border=catppuccin["green"],
        ),
        widget.TextBox(
            text="|",
            font="Ubuntu Mono",
            foreground=catppuccin["gray"],
            padding=2,
            fontsize=14,
        ),
        widget.CurrentLayoutIcon(
            # custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
            foreground=catppuccin["gray"],
            padding=4,
            scale=0.6,
        ),
        widget.CurrentLayout(foreground=catppuccin["gray"], padding=5),
        widget.TextBox(
            text="|",
            font="Ubuntu Mono",
            foreground=catppuccin["gray"],
            padding=2,
            fontsize=14,
        ),
        widget.WindowName(foreground=catppuccin["blue"], max_chars=40),
        widget.GenPollText(
            update_interval=60,
            func=lambda: subprocess.check_output(
                "printf $(uname -r | awk -F '-' '{print $1}')", shell=True, text=True
            ),
            foreground=catppuccin["arch"],
            fmt="󰣇  {}",
            decorations=[
                BorderDecoration(
                    colour=catppuccin["arch"],
                    border_width=[0, 0, 2, 0],
                )
            ],
        ),
        widget.Spacer(length=8),
        widget.CheckUpdates(
            distro="Arch",  # Change to "Arch_paru" or "Arch_yay" to update through AUR helper.
            display_format="  : {updates}",
            no_update_string="  : 0",
            update_interval=60,
            foreground=catppuccin["red"],
            decorations=[
                BorderDecoration(
                    colour=catppuccin["red"],
                    border_width=[0, 0, 2, 0],
                )
            ],
        ),
        widget.Spacer(length=8),
        widget.CPU(
            format="  Cpu: {load_percent}%",
            foreground=catppuccin["green"],
            decorations=[
                BorderDecoration(
                    colour=catppuccin["green"],
                    border_width=[0, 0, 2, 0],
                )
            ],
        ),
        widget.Spacer(length=8),
        widget.Memory(
            foreground=catppuccin["sky"],
            mouse_callbacks={"Button1": lambda: qtile.cmd_spawn(terminal + " -e htop")},
            format="{MemUsed: .0f}{mm}",
            fmt="󰧑  Mem: {}",
            decorations=[
                BorderDecoration(
                    colour=catppuccin["sky"],
                    border_width=[0, 0, 2, 0],
                )
            ],
        ),
        widget.Spacer(length=8),
        widget.DF(
            update_interval=60,
            foreground=catppuccin["peach"],
            mouse_callbacks={"Button1": lambda: qtile.cmd_spawn(myTerm + " -e df")},
            partition="/",
            # format = '[{p}] {uf}{m} ({r:.0f}%)',
            format="{uf}{m} free",
            fmt="  Disk: {}",
            visible_on_warn=False,
            decorations=[
                BorderDecoration(
                    colour=catppuccin["peach"],
                    border_width=[0, 0, 2, 0],
                )
            ],
        ),
        widget.Spacer(length=8),
        widget.Volume(
            foreground=catppuccin["mauve"],
            fmt="  Vol: {}",
            decorations=[
                BorderDecoration(
                    colour=catppuccin["mauve"],
                    border_width=[0, 0, 2, 0],
                )
            ],
        ),
        widget.Spacer(length=8),
        widget.KeyboardLayout(
            foreground=catppuccin["green"],
            fmt=" : {}",
            decorations=[
                BorderDecoration(
                    colour=catppuccin["green"],
                    border_width=[0, 0, 2, 0],
                )
            ],
        ),
        widget.Spacer(length=8),
        widget.Clock(
            foreground=catppuccin["sky"],
            format="󰃰  %a, %b %d - %I:%M",
            decorations=[
                BorderDecoration(
                    colour=catppuccin["sky"],
                    border_width=[0, 0, 2, 0],
                )
            ],
        ),
        widget.Spacer(length=8),
        widget.Systray(padding=3),
        widget.Spacer(length=8),
    ]
    return widgets_list


######## Screens ########


def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1


def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    del widgets_screen2[24:25]
    return widgets_screen2


def init_screens():
    return [
        Screen(top=bar.Bar(widgets=init_widgets_screen1(), size=26)),
        Screen(top=bar.Bar(widgets=init_widgets_screen2(), size=26)),
    ]


if __name__ in ["config", "__main__"]:
    screens = init_screens()
    widgets_list = init_widgets_list()
    widgets_screen1 = init_widgets_screen1()
    widgets_screen2 = init_widgets_screen2()

#### Screen Functions ####


def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)


def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)


def window_to_previous_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group)


def window_to_next_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group)


def switch_screens(qtile):
    i = qtile.screens.index(qtile.current_screen)
    group = qtile.screens[i - 1].group
    qtile.current_screen.set_group(group)


######## Drag floating layouts. ########

mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

######## Tweaking The "Feel" ########
dgroups_key_binder = None
dgroups_app_rules = [
    # Rule(Match(wm_class=['firefox']), group="2"),
    # Rule(Match(wm_class=['virt-manager']), group="4"),
]
follow_mouse_focus = False
bring_front_click = False
floats_kept_above = True
cursor_warp = False

#### Rules for what applications start in floating ####
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
# wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
