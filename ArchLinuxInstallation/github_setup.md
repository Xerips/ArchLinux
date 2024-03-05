# How to connect to an existing github account:

## Create you new SSH key:

https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent

1. Create SSH key on host: `ssh-keygen -t ed25519 -C "your_email@example.com"`
2. Follow prompts.
3. Start the ssh-agent in the background: `eval "$(ssh-agent -s)"`
4. Add your private key to the ssh-agent: `ssh-add ~/.ssh/id_ed25519`
5. Go to your github page, go to settings, add the new ssh-key to your github account.

## Reconnect to the repo:

1. Clone the repo: `git clone git@github.com:<github username>/<repo>.git`
2. cd `<repo>`
3. `git pull`
4. Setup config for all repos with --global:
5. `git config --global user.name "<your name /alias"`
6. `git config --global user.email "Example@pexamplemail.com"`
7. `git config --global user.username "<github username>"`
8. Check config: `git config --list`

## Setup a new Repo:

1. Initialize the directory: `git init`
2. Add (stage) the files: `git add .`
3. Commit staged files: `git commit -m "initial commit"`
4. Connect to your repo (after setting up keys and what not): `git remote add origin git@github.com:<username>/<reponame>.git`
5. git push -u origin main
