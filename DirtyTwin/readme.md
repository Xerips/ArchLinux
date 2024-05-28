# Dirty Twin

## Table of Contents

### Installation

Setting up your custom Arch intall as a virtual machine using Qemu, KVM, Vert-Manager.

### Tooling

Some basic tools for starting your hacking journey.

### Hacking Examples

A separate directory where I will add some guides and examples.

## Installation

If you're looking for a detailed guide on setting up your virtual machine client, check out [Setting up Qemu for virtualization](https://github.com/Xerips/ArchLinux/tree/main/ArchLinuxInstallation#setting-up-qemu-for-virtualization).

- _Why use Arch for pentesting_:

* You really want to live in Arch.
* You're not particularly concerned with anonymity.
  - If you're going for maximum anonymity, having a very unique setup can compromise that anonymity. When you reach out to things on the internet through your browser or other services, you will be fingerprinted by the destinations you touch. For maximum anonymity when it comes to fingerprinting, use the most popular tools with minimal configuration changes. Doing this makes your system seem like just another straw of hay in the haystack. Having a super riced optimally configured browser, os, etc. can help distinguish you from other users, and not in a good way.
* If you're looking for anonymity, using default kali would be a good bet. This will help you to blend in while also providing the tools you need.
* You may also be interested in installing BlackArch as a VM to have a large tool selection out of the box and customize it as you need for your pentesting/forensic/etc machine. Black arch uses awesomewm and a few other

**Qemu Setup**

- First step is to choose your archlinux .iso file that you can get from the [Arch Linux website](https://archlinux.org/download/) with your choice of download method. They also provide checksums and a guide to verify the files integrity.
  - choose the operating system you are installing, search arch linux and select that option.
- Next we need to allocate memory and CPU settings.
  - I went with 11444 MiB or 12GB memory. This is around 1/3 of my available memory and will be WAY more than enough for our Dirty Twin.
  - I went with 8 CPUs. Again this is around 1/3 of my available CPU cores, which will also be WAY more than enough.
  - The reasoning behind this is I want to be able to run this VM pretty hard. When doing pen testing it's common to have a lot of tools running at once. You may be doing Dir busting, Nmap scans, maybe brute forcing hashes you've found, running sql map, while using burpsuite to probe forms or inputs for vulnerabilities, etc. This can add up, particularly if you have a browser open with 15 tabs. That being said, this system will run on fairly minimal specs, it just won't be as beefy and you'll may have to manage your resources a bit more (you could probably get away with 4GB of ram and 2 CPUs).
- For disk space this is more personal preference, how much will you be storing on this system?
- You could definitely get away with 20GiB. I went with 80GB because you gotta love having room to grow.
- Name your machine, click customize configuration before install, select your network, and click finish.
- From the custom configuration menu, click on CPUs check the Manually set CPU topology, and change the topology to sockets: 1, Cores: 8, Threads: 1. For a more detailed explanation about this, and a starting point for learning more, you can check out [this forum post](https://forum.level1techs.com/t/virt-manager-cpu-topology/162094).
  - Fun Fact: you can look up your CPU topology and a lot of other information with the `lscpu` command in your host or VM terminal.
- Click the "Begin Installation" button on the top left of the window.

**Arch Install**

- Once you've booted into the install media, you should automatically have internet access seeing as it's a VM. If you're installing on bare metal, you may need to look up how to use iwctl to configure wifi.
- The first step (once you're connected to the internet) is to simply type archinstall into the ternimal. This is the arch installation script and really helps to streamline the installation process. It can be fun to do everything manually, but after doing that once or twice, you'll definitely appreciate using the script.
- Use the arrow keys on your keyboard to navigate through the setup option:
  - Select the mirror closest to you by country
  - Set up your Locales if needed
  - For Disk Config, you can manually configure the drive like we did with our wazuh ubuntu server, or just use best-effort default partition layout with ext4. We can use our hypervisor to take snapshots so btrfs won't give us much added value as it has slower read/write speeds. You could use btrfs for your host file system, and then ext4 for your virtual machines if you want snapshots for the host and faster read/writes for your VM.
  - Setup Disk encryption if you want to.
  - Keep Bootloader as Grub.
  - Keep swap enabled.
  - Name your host.
  - Set a root password (recommended, make sure it's a strong password and different than your user password).
  - Set up a User account (make a sudoer).
  - Profile is where we can setup our GUI.
    - Select `Type` and then Qtile, this is our tiling windows manager.
    - Under graphics selecting `All open-source` works fine.
    - Under greeter, I like lightdm-slick-greeter.
  - I like to use pipewire for an audio driver.
  - Kernel I select the basic linux kernel.
  - Under Additional packages you'll want to add all of the packages that will help you to setup your system, the remaining packages we will download using pacman and the package list we generated from our host system.
    - `firefox git neovim alacritty`
  - You can select `Use NetworkManager (...)` from Network configuration.
  - Select your timezone
  - Automatic time sync (NTP) should be set to true.
  - Finally, you can add the multilib and/or testing repositories under optional repositories. We will be using the AUR through yay, so unless you need something from these repositories or have a reason to wanting to explore them, you can leave this blank.
  - Scroll to install and let 'er rip!
  - You shouldn't need to unmount the media or anything like that when using Vert-Manager, just reboot after install.

Immediate Problems! You'll notice after logging into your VM for the first time that mod + r (the default qtile launch shortcut) will open up our hosts Rofi launcher. Don't panic! What we have to do is set different mod keys for each system.

- We will change our hosts mod key in the ~/.config/qtile/config.py to the ALT key. You can do this by changing the `mod = "mod4"` under our ######## Variables ######## header at the top of config.py to `mod = "mod1"` and then reloading qtile with mod4 + ctrl + r.
  Now our host's mod key is set to alt. This will let us use the default settings for qtile in the new VM.
- Move to your VM and use the `mod+r` to open alacritty, then download the package list we created with our host system through github, or a other service that you save your configs and setup files to.
  - Install pacman packages with `sudo pacman -S < pkglist.txt`
- Download your .config files which you should have backed up via github or similar services. It's best to save these to a private repo.
- Reload Qtile with `mod+shift+r`
- Decide which system (host or vm) uses alt (mod1) as superkey and which uses the 'windows key' (mod4) for shortcuts/keychords.

  - Change your qtile config.py's accordingly.

- If you're experiencing issues, you can drop into a tty by selecting the `Send Key` menu drop down and then selecting `Ctrl+Alt+F2` through `Ctrl+Alt+F6`. To return to the GUI select `Ctrl+Alt+F7`.
  - This will give you access to a terminal (tty) to work on the system without entering your GUI. It can be helpful if you get black screened, or if you forgot to install alacritty (or other terminal emulator) you can use the tty to install one (I forget to install a terminal emulator all the time...).

The last thing to do is to install the black arch repo. You can find instructions on how to install the black arch repo on top of arch linux at [blackarch.org/downloads.html](https://blackarch.org/downloads.html).

```
# Run https://blackarch.org/strap.sh as root and follow the instructions.
$ curl -O https://blackarch.org/strap.sh

# Verify the SHA1 sum
$ echo 26849980b35a42e6e192c6d9ed8c46f0d6d06047 strap.sh | sha1sum -c

# Set execute bit
$ chmod +x strap.sh

# Run strap.sh
$ sudo ./strap.sh

# Enable multilib following https://wiki.archlinux.org/index.php/Official_repositories#Enabling_multilib and run:
$ sudo pacman -Syu
```

From here you can use the black arch repo through pacman to install things like John (John the ripper), hashcat, burpsuite, nikto, gobuster, etc.  
Happy Hacking!
