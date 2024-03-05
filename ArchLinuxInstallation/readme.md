# Setting Up ArchLinux with:

## Grsync, Tmux, Alacritty, Neovim(LazyVim), Zsh(ohmyzsh + powerlevel10k), Qtile, and Qemu.

#### Notes:

- Soooo, I broke my system... And I was really mad... Because I wasn't set up properly to recover said system. I didn't have a current install script to get all of the packages I had installed, only part of my work was backed up to github in private and public repos, I hadn't pushed my config files in a while, aaaand I had no physical backups. To be fair, I was mad at me, not at my system. After all, your system is what you make it.
- With that embarassing admission out of the way, it's time to make it much better than it was before and put some lessons learned into practice!
- Once we have everything here set up, we should never have to go through all of this again - unless we want to play around with a fresh install. We backup the /home directory and all of the configuration files existing in ~/.config and our work is saved in /home as well. The only thing you will have to add is all of the requirements after restoring a backup from either github or your backup drive. I have saved my post config packages as base_packages.pacman, which is created with: `sudo pacman -Qqe > base_packages.pacman`.
- I haven't included any pen-testing, forensic, or other cyber security tools but they would be easily added by running ` sudo pacman -Qqe > all_packages.pacman` after you've install everything you need.
- To install packages from one of these files enter the following from your terminal: `sudo pacman -S < base_packages.pacman`
- I've also included a script named new_packages.py. I use this to determine what new packages I've installed while working on a specific project. If you have a "current_packages.pacman" list that was generated before you start your new project, you can run this script when you finish your project to determine what the requirements are for the new project, specifically.

---

### Setting up Grsync and a Backup Drive:

To list the available devices and find your backup drive:  
`sudo fdisk -l`

Start fdisk on the drive you want to partition/format:  
`sudo fdisk <device name>`  
ex: `sudo fdisk /dev/sda`

From the 'Command (m for help):' prompt:  
`n` for new partition  
`<enter/return>` for partition 1.  
`<enter/return>` for first sector.  
`<eneter/return>` for last sector.  
This will turn the drive into one large linux partition. If your drive currently has a partition(s) fdisk will try to format only the available space. Delete old partitions first, or change the sectors.  
Write this partition to disk with the `w` command.  
Exit out of fdisk with `q`.

Creat your linux file system (ext4):  
`sudo mkfs.ext4 /dev/sda1`  
'/dev/sda1' is the name of the partition you've just created. **Be very careful** while partitioning and writing file systems. If you pick the wrong drive or partition, you could lose whatever was on the drive.

---

You'll need to setup USB mounting. Your initial arch install is basic and doesn't have anything installed to do mounting/automounting of usbs.

For USB mounting:  
`sudo pacman -S udisks2`  
For USB auto Mounting:  
`sudo pacman -S udiskie`  
For both:  
`sudo pacman -S udiskie udisks2`

Although fdisk can find the drive you've connected, grsync won't be able to access the drive if it's not mounted.  
You do not have to use automounting with udiskie if you prefer to manually mount and unmount your drive with udisks2. Check the man pages for more info.

Your drive will be mounted at /run/media/<user name>/<drive here>, by default

Add udiskie to xinitrc or qtile's autostart.sh

---

You'll need a polkit agent to use grsync and a number of other tools.

TLDR:  
` sudo pacman -S polkit-gnome`  
add ` polkit-gnome-authentication-agent-1 &` to either xinitrc or qtile's autostart.sh.

[Polkit](https://en.wikipedia.org/wiki/Polkit) stands for Policy Kit, and it's basically "a component for controlling system-wide privileges in Unix-like operating systems. It provides an organized way for non-privileged processes to communicate with privileged ones. Polkit allows a level of control of centralized system policy."  
It's worth taking a look at the [archwiki](https://wiki.archlinux.org/title/Polkit) as well to learn more about different Polkit Agents.  
A polkit agent is one of those things you probably haven't come across if you've only ever used desktop environments like KDE, Plasma, Ubuntu, etc. This is because those DE's ship with a polkit agent already installed.

If you've gone with a more minimal arch install using only a window manager and not a full desktop environment, you will most likely have to install one yourself.  
I've decided to go with polkit-gnome, but it really doesn't matter too much.  
If you only want to run the polkit agent when you're using something that requires it, like grsync, then you can just run it when you need to. Otherwise you can put it in your Qtile autostart.sh script, or your xinitrc file.

---

Creating your first backup with grsync:

- Open grsync via the terminal by entering `grsync`
- Your session at the top of the screen will be default, you can change this by adding a new one if you like with the + icon to the right.
- The first text field is your source, or what directory you're looking to backup.
- The second text field is your destination, or where you're looking to write your backup to. For me, I can find my USB drive in /run/media/$USER/drive_name.
- When you're ready, press the lightbulb icon to do a test run. If all goes well it should finish with no errors.
- Click the play button to start your backup.
- Done!

- I will most likely get rid of Grsync eventually. If you're just looking to backup your user directories like /home or /home/Work, grsync is easy and simple. If you're looking to backup more of your filesystem, you will want to get familiar with rsync as well so you can do things like ignore your /tmp folder which will cause "vanishing files" warnings.

You will have to have udiskie running from terminal or in your startup script:  
udiskie &

You will have to have polkit-gnome running from terminal or in your startup script:  
/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &

Once you've made your first backup, it's time to get on to the next step!

---

### Setting Up tmux:

It's a lot easier for me to complete these readme's on the go if I used a terminal multiplexer like TMUX. A multiplexer will allow you to split your terminal into separate panes to complete different tasks. Neovim is a terminal text editor, so being able to have Neovim in one pane with something like NeoTree to navigate the file system gives a nice "All-in one pane" type experience for editing files. In a separate pane you can work from the command line to do things like install packages, run cli tools, run commands etc.

I'll be using TMUX with the Alacritty terminal, but you could use a different terminal emulator (TE) than alacritty like Konsole or Terminator which have built in multiplexers - if you go with a TE with a built in multiplexor, you don't need tmux unless you want more control over sessions, windows, and panes. The reason why I don't use a TE with a built in multiplexor is because Alacritty is a GPU accelerated terminal emulator which means when I use fancy prompts like Power10K, and have a lot going on in the terminal, I can use my graphics card to render the graphics which means a faster and smoother terminal.

Copy this config (if you want it) into your ~/.config/tmux/ directory:

```
set -g default-terminal "tmux-256color"

set-option -g status-position bottom

# Change the bind key from ctrl+b to ctrl+a. I used my palm to hit the ctrl key and and pinky to hit a. Change this to whatever you like!
# This prefix works like a "leader" key in nvim. Once you press ctrl+a, you can take your fingers off the keys and then press the shortcut key.
unbind C-b
set -g prefix C-a
bind C-a send-prefix

# Refresh your tmux from the source file (usually after changes) with ctrl+a r.
unbind r
bind r source-file ~/.config/tmux/tmux.conf

# Changes the split windows key from % and " to | and - to be more visually intuitive.
# ctrl+a shit+\ to do a horizontal split. ctrl+a - to do a vertical split.
unbind %
bind | split-window -h

unbind '"'
bind - split-window -v

# Lets you use the mouse to resize panes when you need to.
set -g mouse on

# Use vim key bindings to resize panes.
bind -r h resize-pane -L 5
bind -r j resize-pane -D 5
bind -r k resize-pane -U 5
bind -r l resize-pane -R 5

bind -r m resize-pane -Z # Keybinding to restore pane sizes.

# Uses vim keybindings for copy and paste and navigation. Disable with # if you're not into it.
set-window-option -g mode-keys vi

bind-key -T copy-mode-vi 'v' send -X begin-selection
bind-key -T copy-mode-vi 'y' send -X copy-selection

# tpm plugin
set -g @plugin 'tmux-plugins/tpm'

# list of tmux plugins
set -g @plugin 'christoomey/vim-tmux-navigator' # Need this plugin for nvim as well, or you get one way traffic for navigating between panes.
set -g @plugin 'jimeh/tmux-themepack'
set -g @plugin 'tmux-plugins/tmux-resurrect' # Persist tmux sessions after computer restart.
set -g @plugin 'tmux-plugins/tmux-continuum' # Automatically saves sessions for you every 15 minutes.

set -g @themepack 'powerline/default/cyan'

set -g @resurrect-capture-pane-contents 'on'
set -g @continuum-restore 'on'

# Initialize TMUX plugin manager (keep this at the very bottom of tmux.conf)
run '~/.config/tmux/plugins/tpm/tpm'
```

Once that's done, you need to install tpm in the .config/tmux/plugins directory.  
cd to ~/.config/tmux/plugins and:  
`git clone https://github.com/tmux-plugins/tpm`
If you want to upload all of your config files to github, remove the .git folder from tpm to do so.

Restart or reload tmux.  
install packages from tpm with `ctrl+a I (shift+i)`

Dependencies:  
tmux  
tpm - Handles installing plugins, no need to do it yourself.

---

### Setting Up Alacritty:

Here's an alacritty config that will give you a sexy catppuccin look. I'm addicted to the catppuccin theme, so everything is catppuccin.  
If you want to have a different catppuccin "flavour" just google alacritty catppuccin and you'll see there github.  
Copy the below text and paste it into your empty ~/.config/alacritty/alacritty.toml config file.

```
[font]
size = 12.0

[font.bold]
family = "MesloLGM Nerd Font"
style = "Bold"

[font.bold_italic]
family = "MesloLGM Nerd Font"
style = "Bold Italic"

[font.italic]
family = "MesloLGM Nerd Font"
style = "Italic"

[font.normal]
family = "MesloLGM Nerd Font"
style = "Regular"

# Catppuccin Color Scheme

[colors.primary]
background = "#24272b"
foreground = "#CDD6F4"
dim_foreground = "#CDD6F4"
bright_foreground = "#CDD6F4"

[colors.cursor]
text = "#1E1E2E"
cursor = "#F5E0DC"

[colors.vi_mode_cursor]
text = "#1E1E2E"
cursor = "#B4BEFE"

[colors.search.matches]
foreground = "#1E1E2E"
background = "#A6ADC8"

[colors.search.focused_match]
foreground = "#1E1E2E"
background = "#A6E3A1"

[colors.footer_bar]
foreground = "#1E1E2E"
background = "#A6ADC8"

[colors.hints.start]
foreground = "#1E1E2E"
background = "#F9E2AF"

[colors.hints.end]
foreground = "#1E1E2E"
background = "#A6ADC8"

[colors.selection]
text = "#1E1E2E"
background = "#F5E0DC"

[colors.normal]
black = "#45475A"
red = "#F38BA8"
green = "#A6E3A1"
yellow = "#F9E2AF"
blue = "#89B4FA"
magenta = "#F5C2E7"
cyan = "#94E2D5"
white = "#BAC2DE"

[colors.bright]
black = "#585B70"
red = "#F38BA8"
green = "#A6E3A1"
yellow = "#F9E2AF"
blue = "#89B4FA"
magenta = "#F5C2E7"
cyan = "#94E2D5"
white = "#A6ADC8"

[colors.dim]
black = "#45475A"
red = "#F38BA8"
green = "#A6E3A1"
yellow = "#F9E2AF"
blue = "#89B4FA"
magenta = "#F5C2E7"
cyan = "#94E2D5"
white = "#BAC2DE"

[[colors.indexed_colors]]
index = 16
color = "#FAB387"

[[colors.indexed_colors]]
index = 17
color = "#F5E0DC"

[env]
TERM = "xterm-256color"

[shell]
program = "tmux"
```

Requirements:  
nerd-fonts  
tmux  
Alacritty

---

### Setting Up .zsh:

- oh-my-zsh allows us to easily install plugins for zsh.
- powerlevel10k is a nice prompt theme that makes it easier for us to see what's going on while working in Alacritty. It's also pretty...

1. Download the \*Requirements in the order they appear.
2. Edit .zshrc file and set ZSH_THEME="powerlevel10k/powerlevel10k"
3. Reload zsh with:
   `source ~/.zshrc`
4. Complete the powerlevel10k configuration to your taste.

\*Requirements:

zsh - just use pacman  
ohmyzsh - to install:  
`sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"`  
powerlevel10k - to install:  
`git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k`

Plugins:  
zsh-autosuggestions - to install:  
`git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions`  
Edit ~/.zshrc and add `zsh-autosuggestions` to `plugins=(git)`

zsh-syntax-highlighting - to install:  
`git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting`
Edit ~/.zshrc and add `zsh-syntax-highlighting` to `plugins=(git zsh-autosuggestions`

Run `source ~/.zshrc` to load the new config.

You can find pre-installed oh-my-zsh plugins in ~/.oh-my-zsh/plugins/  
All you need to do to install them is add them to you .zshrc within `plugins=(git example2 example3)`

---

### Setting Up Neovim:

We're going to use the LazyVim nvim "distro", this is the first time I'm using it, but I've heard good things.

Install [lazyvim](https://www.lazyvim.org/):
`git clone https://github.com/LazyVim/starter ~/.config/nvim`  
Then start up nvim  
Okay, that was easy...

Hitting <space> will open up which-key, which will show you all of the shortcuts you can use with the leader key.  
Typing ":" will open the command box, this is actually pretty nice...  
:LazyExtras will open up a bunch of extra plugins. These are not all of the plugins, but the ones native to LazyVim.  
:Mason will open up mason for linting and formatting plugins.

Add plugins like catppuccin color scheme by adding the plugin file to **~/.config/nvim/lua/plugins/example.lua**  
Example 1 for adding catppuccin to the plugins directory:  
`nvim catppuccin.lua`  
add the following text to the file:

```
return {
  {
    "LazyVim/LazyVim",
    opts = {
      colorscheme = "catppuccin",
    }
  }
}
```

Example 2 for adding vim-tmux-navigator:

```
return {
  {
    "christoomey/vim-tmux-navigator",
    cmd = {
      "TmuxNavigateLeft",
      "TmuxNavigateDown",
      "TmuxNavigateUp",
      "TmuxNavigateRight",
      "TmuxNavigatePrevious",
    },
    keys = {
      { "<c-h>",  "<cmd><C-U>TmuxNavigateLeft<cr>" },
      { "<c-j>",  "<cmd><C-U>TmuxNavigateDown<cr>" },
      { "<c-k>",  "<cmd><C-U>TmuxNavigateUp<cr>" },
      { "<c-l>",  "<cmd><C-U>TmuxNavigateRight<cr>" },
      { "<c-\\>", "<cmd><C-U>TmuxNavigatePrevious<cr>" },
    },
  }
}
```

---

### Setting up Qtile:

This is my first time using Qtile and I have to admit, it's freaking awesome!  
I've Added the config.py as a separate file because it's quite large. I've also added a screenshot of what my config looks like in case you're interested in the old, "bibbity bobbity, your dotfiles are now my property."  
There's simply too much in the config to walk through it all here but I've made a bunch of comments in the config and it's pretty readable. Take a look through it and change what makes sense for you.

Tips Tricks:

- Qtile has absolutely incredible documentation. Check it out [here](https://docs.qtile.org/en/stable/). They say it contains "Everything you need to know," and although you may want to search for examples or tricks from other people, they ain't lying!
- You can use Xephyr to load your config in a nested window to check out how it looks and feels. This is a safe mode if you're not sure your config will work. If you do this, you'll want to change your modkey in the nested Xephyr config or else your system will run your shortcuts in the host.
- Qtile seems to load the default config (or the last working config?) if you really mess things ups, or at least it did for me when I made some mistakes that threw python errors. This is a superpower level feature.
- Make a backup of your config every time you make changes from your current working config. I just save mine as config.py.bak.
- If you're latest config doesn't seem to load, run `python3 config.py` from the /qtile directory and it will print error messages to the terminal. This is a great way to figure out where any typos or syntax errors are.
- I have some images in /qtile/icons that are used in the config. Add your own or switch them up!

- As you get familiary with your system and start optimizing your work flow, you can add different rules like 'always start firefox on group 2' which is represented by our web icon in the `GroupBox` widget. I've provided a few examples in `dgroups_app_rules` under ######## Tweaking the "Feel" ########.

---

### Setting up Qemu for virtualization:

- Why Qemu? True KVM bad assery that will dumpster VirtualBox in performance. Don't understand that last sentence? That's cool, check out this video to catch the hype: [Stop using Virtualbox, Here's how to use QEMU instead](https://www.youtube.com/watch?v=Kq849CpGd88&t=322s.)
- In reality, there are definitely reasons to use VirtualBox too. The biggest reasons to use VirtualBox are it's easy to use and a lot of content out there is optimized to work on it. Some things that don't work properly out of the box on Qemu might work better on Virtualbox or visa-versa.

Install:  
`sudo pacman -Syy qemu virt-manager virt-viewer dnsmasq vde2 bridge-utils openbsd-netcat ebtables iptables-nft`

Start KVM libvirt service:  
`sudo systemctl enable libvirtd.service`
`sudo systemctl start libvirtd.service`

Check the service is running:  
`systemctl status libvirtd.service`

That's it! You're ready to launch `virt-manager` and to start installing some test vm's or juicy boxes from [vulhub](https://www.vulnhub.com/) to pwn!

---

### GitHub

I've added a markdown file called github_setup.md that helps with setting up GitHub. Check it out if you're interested in using GitHub to help backup your work and do version control (you should!).

---

### The End! Kinda...

PHEW! We did it! We're back and better than ever!

I'd call this a base install. Now all that's left to do is add the [black arch](https://blackarch.org/downloads.html) repo, starting hording tools, build handy scripts, work on some cool projects, and hone your skills as a bad ass cyber operator!

If you've taken a look at my BHP repo, you'll have seen that I go through an entire book dedicated on how to compromise a system that you have basic access to with python scripts. The reason why this book is so handy is because when you've gotten a foothold on a system, you may not have access to the tools that will allow you to easily escalate your permissions, exfil data, and a number of other nafarious tasks hackers may be interested in. It would be pretty silly of us to install all of the tools hackers may want/need on our base system. If we do this, it's effectively like handing over the keys to the castle to anyone who can get a foothold. Soooo, let's not! Instead, let's create a "Dirty Twin" of our snazzy new Arch installation in a virtual machine which we can load up with all of the pen-testing and experimental tools we could possibly want.  
By doing this we can keep our main system clean, stabled, and safe. We avoid experimental packages that may break our system, tools that hackers could use against up, and have free reign to do whatever we want! If we toast the VM, we can just spin up another one from a snapshot.

With that, I think we're done with this section on setting up a new Arch system. I hope your system lives long and prospers! I'll catch you in the next section "Dirty Twin"!
