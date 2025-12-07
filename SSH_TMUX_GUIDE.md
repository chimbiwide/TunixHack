# SSH and tmux Setup Guide

A comprehensive guide for setting up SSH and tmux to remotely monitor long-running processes on Linux Mint.

## Table of Contents
- [SSH Setup](#ssh-setup)
- [tmux Basics](#tmux-basics)
- [Using SSH + tmux Together](#using-ssh--tmux-together)
- [Common Commands Reference](#common-commands-reference)
- [Troubleshooting](#troubleshooting)

---

## SSH Setup

### On the Server (Machine Running the Generation)

**1. Install SSH Server**
```bash
sudo apt update
sudo apt install openssh-server
```

**2. Start and Enable SSH Service**
```bash
# Start SSH service
sudo systemctl start ssh

# Enable SSH to start on boot
sudo systemctl enable ssh
```

**3. Verify SSH is Running**
```bash
sudo systemctl status ssh
```
You should see `active (running)` in green text.

**4. Find Your IP Address**
```bash
# Method 1: Simple
hostname -I

# Method 2: Detailed
ip addr show
```
Look for your local IP address (usually starts with `192.168.x.x` or `10.x.x.x`)

**5. Configure Firewall (if enabled)**
```bash
# Allow SSH through firewall
sudo ufw allow ssh

# Enable firewall
sudo ufw enable

# Check status
sudo ufw status
```

---

### On the Client (Your Other Laptop)

**1. Install SSH Client (usually pre-installed)**
```bash
sudo apt install openssh-client
```

**2. Connect to the Server**
```bash
ssh username@192.168.x.x
```
Replace:
- `username` with your username on the server machine
- `192.168.x.x` with the server's IP address

**3. First Connection**
On first connection, you'll see:
```
The authenticity of host '192.168.x.x' can't be established.
ED25519 key fingerprint is SHA256:...
Are you sure you want to continue connecting (yes/no)?
```
Type `yes` and press Enter.

**4. Enter Password**
Enter your password for the server machine.

---

### Optional: SSH Key Authentication (No Password Required)

**On the Client Machine:**

**1. Generate SSH Key Pair**
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```
Press Enter to accept default location, optionally set a passphrase.

**2. Copy Public Key to Server**
```bash
ssh-copy-id username@192.168.x.x
```
Enter your password one last time.

**3. Test Password-less Login**
```bash
ssh username@192.168.x.x
```
You should connect without entering a password!

---

### Optional: SSH Config Shortcut

Create/edit `~/.ssh/config`:
```bash
nano ~/.ssh/config
```

Add this configuration:
```
Host generation-pc
    HostName 192.168.x.x
    User username
    Port 22
```

Now you can connect with just:
```bash
ssh generation-pc
```

---

## tmux Basics

### What is tmux?

tmux (terminal multiplexer) allows you to:
- Run programs that continue even after you disconnect
- Create multiple terminal sessions in one window
- Detach and reattach to sessions from anywhere

### Installation

```bash
sudo apt install tmux
```

### Basic tmux Commands

**Starting a New Session**
```bash
# Start new session
tmux

# Start with a name
tmux new -s session_name

# Example
tmux new -s generation
```

**Detaching from a Session**
- Press `Ctrl+B`, then press `D`
- Your session keeps running in the background

**List All Sessions**
```bash
tmux ls
```

**Attach to a Session**
```bash
# Attach to the most recent session
tmux attach

# Attach to a specific session
tmux attach -t session_name

# Example
tmux attach -t generation
```

**Kill a Session**
```bash
# Kill specific session
tmux kill-session -t session_name

# Kill all sessions
tmux kill-server
```

### Essential tmux Key Bindings

All tmux commands start with the prefix: `Ctrl+B`

| Keys | Action |
|------|--------|
| `Ctrl+B` then `D` | Detach from session |
| `Ctrl+B` then `C` | Create new window |
| `Ctrl+B` then `N` | Next window |
| `Ctrl+B` then `P` | Previous window |
| `Ctrl+B` then `%` | Split pane vertically |
| `Ctrl+B` then `"` | Split pane horizontally |
| `Ctrl+B` then `Arrow` | Navigate between panes |
| `Ctrl+B` then `[` | Scroll mode (use arrow keys, `Q` to exit) |

---

## Using SSH + tmux Together

### Workflow for Long-Running Processes

**On the Server:**

**1. SSH into the server**
```bash
ssh username@192.168.x.x
```

**2. Start a tmux session**
```bash
tmux new -s generation
```

**3. Start your long-running process**
```bash
cd /home/david/PycharmProjects/TunixHack
python generate_databricks.py
```

**4. Detach from tmux**
Press `Ctrl+B`, then press `D`

**5. Disconnect from SSH**
```bash
exit
```

Your process continues running!

---

**From Your Other Laptop (Check Progress):**

**1. SSH into the server**
```bash
ssh username@192.168.x.x
```

**2. List tmux sessions**
```bash
tmux ls
```

**3. Attach to your session**
```bash
tmux attach -t generation
```

You'll see the live output of your running process!

**4. Detach again when done checking**
Press `Ctrl+B`, then press `D`

**5. Exit SSH**
```bash
exit
```

---

## Common Commands Reference

### SSH Commands

```bash
# Connect to server
ssh username@hostname

# Connect with specific port
ssh -p 2222 username@hostname

# Copy file to server
scp file.txt username@hostname:/path/to/destination

# Copy file from server
scp username@hostname:/path/to/file.txt ./

# Copy directory recursively
scp -r folder/ username@hostname:/path/to/destination
```

### tmux Commands

```bash
# Session management
tmux new -s name              # Create new session
tmux ls                       # List sessions
tmux attach -t name           # Attach to session
tmux kill-session -t name     # Kill session
tmux rename-session -t old new # Rename session

# Inside tmux (after Ctrl+B)
d                             # Detach
c                             # New window
,                             # Rename current window
w                             # List windows
&                             # Kill current window
[                             # Enter scroll mode
?                             # Show all keybindings
```

---

## Troubleshooting

### SSH Issues

**Connection Refused**
```bash
# Check if SSH is running on server
sudo systemctl status ssh

# Restart SSH service
sudo systemctl restart ssh
```

**Can't Find Server**
```bash
# Ping the server
ping 192.168.x.x

# Check if both machines are on same network
ip addr show
```

**Permission Denied**
- Verify username is correct
- Verify password is correct
- Check SSH key permissions: `chmod 600 ~/.ssh/id_ed25519`

**Firewall Blocking**
```bash
# On server, allow SSH
sudo ufw allow ssh
sudo ufw status
```

### tmux Issues

**Session Not Found**
```bash
# List all sessions
tmux ls

# If no sessions, the process may have finished or crashed
```

**Can't Detach**
- Make sure you're pressing `Ctrl+B` first, release, then press `D`
- Not `Ctrl+B+D` all at once

**Scrolling Not Working**
- Enter copy mode: `Ctrl+B` then `[`
- Use arrow keys or Page Up/Down
- Press `Q` to exit copy mode

**Multiple Clients Attached**
```bash
# Attach in read-only mode
tmux attach -t name -r

# Force detach other clients
tmux attach -t name -d
```

---

## Tips and Best Practices

1. **Always use descriptive session names**
   ```bash
   tmux new -s databricks-generation
   ```

2. **Use tmux for any long-running process**
   - Machine learning training
   - Large file processing
   - Data downloads

3. **Keep SSH keys secure**
   ```bash
   chmod 600 ~/.ssh/id_ed25519
   chmod 644 ~/.ssh/id_ed25519.pub
   ```

4. **Create SSH aliases for frequently accessed servers**
   Add to `~/.ssh/config`

5. **Use tmux logging to save output**
   Inside tmux: `Ctrl+B` then `:` then type:
   ```
   pipe-pane -o 'cat >> ~/output.log'
   ```

6. **Check tmux sessions before creating new ones**
   ```bash
   tmux ls
   ```

---

## Quick Start Checklist

### First Time Setup
- [ ] Install SSH server on generation machine
- [ ] Start and enable SSH service
- [ ] Get IP address of generation machine
- [ ] Test SSH connection from other laptop
- [ ] Set up SSH key authentication (optional)
- [ ] Install tmux on generation machine

### Every Time You Start a Process
- [ ] SSH into server
- [ ] Start tmux session with descriptive name
- [ ] Navigate to project directory
- [ ] Start your process
- [ ] Verify it's running correctly
- [ ] Detach from tmux (`Ctrl+B` then `D`)
- [ ] Exit SSH

### Checking Progress
- [ ] SSH into server
- [ ] List tmux sessions (`tmux ls`)
- [ ] Attach to session (`tmux attach -t name`)
- [ ] Check progress
- [ ] Detach when done (`Ctrl+B` then `D`)
- [ ] Exit SSH