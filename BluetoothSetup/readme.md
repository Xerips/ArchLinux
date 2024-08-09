# Dual Boot Bluetooth Setup:

First Install the following:
bluez
bluez-utils
fuse
ntfs-3g
chntpw

Start and Enable your bluetooth service on startup:
`sudo systemctl enable bluetooth && sudo systemctl start bluetooth`

1. Pair your headphones on your Linux drive first.

- Start your bluetooth cli tool with `bluetoothctl`
- Turn on from the bluetoothcli tool: `power on`
- Scan for your bluetooth device: `scan on`
  - Copy the MAC address of the device you want to connect.
- `pair <MAC address>` to pair with the device.
- `connect <MAC address>` if your headphones don't say "connected to blah blah blah."
- Lastly, test to make sure you have audio.

2. Reboot into your Windows drive and pair the device on the Windows installation.

- If you got ahead and paired on windows first, just remove the device from both systems and start again.

3. Reboot into Linux
4. Mount your windows drive using ntfs-3g

- cd into /mnt and create a new directory and mount your windows drive:
  - `cd /mnt`
  - sudo mkdir /windows
  - `sudo mount -t ntfs-3g /dev/nvme01p3 /mnt/windows`

5. Navigate to `/mnt/windows/Windows/System32/config` and run `chntpw -e SYSTEM`
6. Navigate to your bluetooth keys: `cd ControlSet001\Services\BTHPORT\Parameters\Keys`

- If this doesn't work, enter `ls` to see a list of Key Names. Should Be something like `<ControlSet001>, <ControlSet002>, <CurrentControlSet>` etc.
- Once you successfully cd into the right control set, you will get your bluetooth adapter's MAC Address (not your headphones, keyboard, mouse, whatever)

7. cd into your bluetooth adapters directory using `cd <adapters MAC address>`.

- `ls` to see the list of bluetooth devices connected to your windows system. You should see the MAC address of the bluetooth device you want to connect to here.

8. Read the REG_BINARY key of the device you want to connect with: `hex <value name>`

- The `value name` will resemble the mac address of the device you're looking to connect.

9. Open a root terminal (using `su root` or `sudo su`). **Watch out danger cats, you can really break stuff by operating as root.**
10. cd into your bluetooth adapters directory `cd /var/lib/bluetooth/`
11. cd into your bluetooth devices directory `cd <MAC ADDRESS>`

- It's easiest to use tab complete after entering the first 2 digits of the MAC address.

12. Open the `info` file with a text editor
13. Replace the `Key=<Value>` with the Hex key value we got from the windows system. Remove all spaces, make sure it is all CAPS.

- Don't copy and paste the below example, your hex key value will be different.

14. Add 147 under the line `Type=4`

```
[LinkKey]
Key=32FAB50DFC3790314F68F350455C9B02
Type=4
147
PINLength=0
```

15. restart your bluetooth service with `sudo systemctl restart bluetooth`

- I changed my linux machines hostname to the same as my windows machine. Not sure if this helps, but I thought it might.

Resources that will help:

- [weywot guide](https://github.com/spxak1/weywot/blob/main/guides/bt_dualboot.md) - This is the main one, but it doesn't go over mounting your windows drive.
- [mount-ntfs-linux guide](https://phoenixnap.com/kb/mount-ntfs-linux) - To understand mounting NTFS in Linux.
- [Arch Wiki - Bluetooth](https://wiki.archlinux.org/title/bluetooth).
