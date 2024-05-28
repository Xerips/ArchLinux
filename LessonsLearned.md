# Lessons Learned

So right at the end of my BHP project, my Arch Linux installation died. I was messing around in awesomewm to access virt-manager a little easier, and everything broke. I couldn't even access the tty with Ctrl+Alt+F1 through to F6 to trouble shoot.

Luckily I had everything backed up to GitHub, so all but about 2 days were recoverable. Losing 2 days hurt, but it wasn't as devastating as losing the entire project.

## Lesson One: Back up your work!

There seems to be an infinite number of ways you can break your system, and there is nothing worse that setting yourself back days, weeks, or even months if you don't bother to back up your work.  
It's easy to do what I did where you work on a set of files, but because it's fairly straightforward or easily replicated, you just wait till you're finished to push the code/files to github. Losing a couple days has encouraged me to tighten up on my version control and backups with Github.  
If you can't write a simple comment to describe what you've done because the comment can't easily break down everything that's happened across multiple files, break down your commits. If you worked on a readme in one directory/project, edited some code in another directory/project, and added a new script, you shouldn't commit the code under one, "Worked on stuff, added some stuff, edited some stuff," comment. Do your commits in a way that allows you to follow the changes/additions you make. This also stops you from being a bonehead (like me) and waiting till there's "enough" to make a meaningful commit and push the code.

Best practice: Add commits for files/code/work as you leave it. If you're done working on it for the day, commit the changes and push the code. If you're about to do some testing or work with system configs or other important pieces of the OS, you should have all of your work backed up to github/storage drives/etc before starting.

## Lesson Two: I don't love Kali Linux anymore.

I've used Kali linux a lot for working on boxes on vulhub, hackthebox, and offensive security labs. What you get out of the box is great and it can really help you to see what's out there as far as tools are concerned, which can help you discover interesting new things to learn about and use in your penetration tests or general security learning.

I reinstalled Kali after losing my system thinking I would just jump into a new system quickly, it will be stable, it will be familiar, and I'll just get right back to work. I hated it. I hated how they had so much I wasn't going to use, I hated not having a tiling window manager, I realized I really like using pacman and yay over apt, and a lot more. I realized that if I were to make it function like I wanted, I would essentially just be turning Kali into my old arch system in the hardest way possible. Lesson: pick the distro you like, are comfortable with, and is the best fit for you, then install the tools you need.

## Lesson Three: Slow is smooth, smooth is fast!

I have a tendancy to over-prepare when making changes and editing things like configs - or at least I thought I did. When I broke my system I was just "popping into the config" to make some quick changes and to add some shortcuts. I was thinking, man I'm always researching the formats, checking out example configs, checking and double checking syntax, indentation, etc. I didn't want to do that because it was just a "quick change/addition," and even though I noticed some inconsistency with spacing, and I wasn't thinking through the whole code block to see if it made sense, I went ahead and hacked together the .config file. Aaaaand it broke.

Two things here:

1. It is almost impossible to spend too much time on making sure things are done correctly with respect to things like editing configs or other potentially system breaking tasks. If I were to have spent 2 hours making sure everything was right, which would have been an insanely long time to be "making sure" for the type of changes I was making, it would have saved me a few days of being frustrated and honestly, pissed off.

2. When all things are equal, choose tools that are configured in a language you are familiar with. This is a lot harder to accomplish because most of the time you will use the best tool for your needs, not the most understandable tool. When it comes to configuration however, the more you know about the language you're configuring in, the more you're going to be able to get out of it. I've decided to switch from AwesomeWM to Qtile for this reason. As you may have noticed I like python and I've been learning and using python for a long time now. Qtile is written in and configured with Python, so I'm hoping when I make changes to the config it's easier for me to pick up errors or mistakes, as well as help to squeeze out some extra functionality.

## Lesson Four: Take what you can get.

I wasn't creating snapshots or backups of my system. I thought, "Whatever, my work and . files are backed up, and I have tool lists spread out through different projects that I would be able to use to re-install everything. This is true, but it is still a lot of work to go through and manually install everything - without missing those one or two packages you forgot to write down and now you gotta goose chase your system looking for what it needs to function. **Doing backups and being able to restore your system from a previous snapshot is a superpower.** If you're running anything like Arch and really like to play around with it, you're going to break stuff. Even if you're not playing around, one bad update or accidentally doing a partial and bricking something is likely to happen eventually. Put yourself in a position for recovery by adding multiple layers of backups/redundancy.

## Lesson Five: Linux is awesome and Arch is worth it.

Once you get yourself a tidy little Arch setup with a tiling window manager set up just for you, an nvim (or whatever) setup that looks beautiful (catpuccine) and functions better and faster than most IDEs with linting, formatting, etc, and all the little toys like a nice .zsh build, fzf, zoxide, eza, etc., It's really hard not to get hooked.

Despite breaking my system and having to recover from a less than perfect position, using a Linux OS that really suites your needs is worth the risk. Being in my custom install feels homey, familiar, and efficient. I haven't been able to achieve that as easily(?)/fully(?) with other systems.

I should also mention that you don't need to use the latest rolling release distro with access to experimental/testing repos and all that bleeding edge stuff. You can use a very stable distro and avoid more experimental tools or setups and I would say you're just as stable as any Windows or Mac device (If you use it in the same way).

## Use configuration tools to help automate your setup once you know what you're looking for(?)

I'm unsure about this but I'm going to try it out. In my last install everything was manually configured, then reconfigured, then changed, then reconfigured. A benefit for me in doing a fresh install is not having old packages or unnecessary .config files on the system. It's clean. This time around I'm going to leverage some of the cool configuration tools like neochad or ohmyzsh to help speed up the process of configuration. Who knows, it might be great!

Check out my ArchInstall directory to follow along.
