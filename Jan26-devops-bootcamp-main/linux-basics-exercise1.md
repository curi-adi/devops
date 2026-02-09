# Linux System Performance & Process Management - Complete Guide

## Lab Overview
**Platform:** Amazon Linux 2023  
**Duration:** 2-3 hours  
**Goal:** Master process management, CPU, memory, and I/O monitoring

---

## Prerequisites

### Launch Amazon Linux Instance

```bash
# Launch EC2 instance (t3.medium recommended for demos)
# Or use existing Amazon Linux system

# Connect via SSH
ssh -i your-key.pem ec2-user@your-instance-ip

# Update system
sudo yum update -y

# Install required tools
sudo yum install -y htop iotop sysstat stress-ng
```

---

## Part 1: Understanding Processes (30 minutes)

### What is a Process?

A process is a running program. When you start an application, the OS creates a process for it.

**Every process has:**
- PID (Process ID) - Unique identifier
- Parent PID (PPID) - Who started this process
- User - Who owns the process
- State - Running, Sleeping, Stopped, Zombie
- Priority - How important it is
- Resources - CPU, Memory it's using

---

### View All Processes

```bash
# See all processes (snapshot)
ps aux

# Explanation of output:
# USER    = Who owns the process
# PID     = Process ID
# %CPU    = CPU usage percentage
# %MEM    = Memory usage percentage
# VSZ     = Virtual memory size (KB)
# RSS     = Physical memory used (KB)
# TTY     = Terminal (? means no terminal)
# STAT    = Process state
# START   = When it started
# TIME    = Total CPU time used
# COMMAND = What's running
```

**Example output breakdown:**
```
USER  PID  %CPU %MEM    VSZ   RSS TTY   STAT START   TIME COMMAND
root    1   0.0  0.1  19692  1604 ?     Ss   10:30   0:01 /sbin/init
```

---

### Process States

```bash
# View process with states
ps aux | head -20

# State codes:
# R = Running (actively using CPU)
# S = Sleeping (waiting for event)
# D = Uninterruptible sleep (usually I/O)
# T = Stopped (paused)
# Z = Zombie (finished but not cleaned up)
# I = Idle kernel thread
# < = High priority
# N = Low priority
# s = Session leader
# + = Foreground process
```

**Common combinations:**
- `Ss` = Sleeping, session leader (typical for daemons)
- `R+` = Running in foreground
- `S<` = Sleeping with high priority

---

### Finding Specific Processes

```bash
# Find processes by name
ps aux | grep nginx

# Better way - use pgrep
pgrep nginx

# Get detailed info about specific PID
ps -p 1234 -f

# See process tree (parent-child relationships)
pstree

# Process tree with PIDs
pstree -p

# Full details of process tree
ps -ejH

# Or using top format
ps axjf
```

**Practice:**
```bash
# Start a background process
sleep 300 &

# Note the PID it shows
# Now find it
ps aux | grep sleep

# See its parent
ps -o pid,ppid,cmd -p <PID>
```

---

### Process Hierarchy

```bash
# Every process has a parent
# PID 1 is the init system (systemd on Amazon Linux)

# See who's the parent of bash
ps -o pid,ppid,cmd -p $$
# $$ is your current shell's PID

# View full hierarchy
systemctl status

# Or
ps -ef --forest
```

**Key concept:** Kill a parent, all children die too.

---

## Part 2: CPU Monitoring (45 minutes)

### Understanding CPU Usage

**What is CPU usage?**
- Percentage of time CPU spends doing work
- 100% = CPU is completely busy
- 0% = CPU is idle

**CPU time is divided into:**
- `us` (user) - Normal applications
- `sy` (system) - Kernel operations
- `ni` (nice) - Low-priority processes
- `id` (idle) - Doing nothing
- `wa` (wait) - Waiting for I/O
- `hi` (hardware interrupts) - Hardware events
- `si` (software interrupts) - Software events
- `st` (steal) - Virtual CPU stolen by hypervisor

---

### Real-Time CPU Monitoring with top

```bash
# Start top
top

# Key metrics in header:
# %Cpu(s): 2.3 us, 1.0 sy, 0.0 ni, 96.5 id, 0.2 wa, 0.0 hi, 0.0 si, 0.0 st
#         user  system nice  idle  wait  hw-int sw-int steal

# Process columns:
# PID    = Process ID
# USER   = Owner
# PR     = Priority
# NI     = Nice value (-20 to 19, lower = higher priority)
# VIRT   = Virtual memory
# RES    = Physical memory (resident)
# SHR    = Shared memory
# S      = State (R, S, D, Z, T)
# %CPU   = CPU usage
# %MEM   = Memory usage
# TIME+  = Total CPU time
# COMMAND = Process name
```

**Useful top commands (while running):**
```bash
# Press these keys inside top:
P    # Sort by CPU usage (default)
M    # Sort by memory usage
T    # Sort by running time
k    # Kill a process (enter PID)
r    # Change priority (renice)
1    # Show individual CPU cores
c    # Show full command path
q    # Quit

# Highlight running processes
z    # Color mode
x    # Highlight sort column
```

---

### Better Alternative: htop

```bash
# Start htop
htop

# Features:
# - Color coded
# - Mouse support
# - Easier to read
# - Shows CPU cores visually
# - Tree view of processes

# Useful keys in htop:
F2   # Setup (customize view)
F3   # Search for process
F4   # Filter
F5   # Tree view
F6   # Sort by column
F9   # Kill process
F10  # Quit

# Tree view
htop -t

# Show only user processes
htop -u ec2-user
```

---

### Finding CPU Hogs

```bash
# Top 10 CPU consumers (snapshot)
ps aux --sort=-%cpu | head -11

# Continuously monitor top CPU user
watch -n 1 'ps aux --sort=-%cpu | head -6'

# Or with specific columns
ps -eo pid,ppid,cmd,%cpu,%mem --sort=-%cpu | head

# Find what's using CPU right now
top -b -n 1 | grep -A 10 "PID USER"
```

---

### Load Average Explained

```bash
# Check load average
uptime
# Output: 10:30:45 up 2 days, 3:15, 1 user, load average: 0.52, 0.58, 0.59
#                                                         1min  5min  15min

# Also shown in:
top     # First line
w       # First line
cat /proc/loadavg
```

**What does load average mean?**
- 1.0 on single-core CPU = 100% utilized
- 1.0 on dual-core CPU = 50% utilized
- 2.0 on dual-core CPU = 100% utilized

**Rule of thumb:**
- Load < CPU cores = Good
- Load = CPU cores = Fully utilized
- Load > CPU cores = Overloaded (tasks waiting)

**Check CPU cores:**
```bash
# Number of CPU cores
nproc

# Detailed CPU info
lscpu

# Quick check
cat /proc/cpuinfo | grep processor | wc -l
```

---

### Generating CPU Load for Testing

```bash
# Install stress-ng (already done in prerequisites)
sudo yum install -y stress-ng

# Stress 1 CPU core for 30 seconds
stress-ng --cpu 1 --timeout 30s

# While this runs, in another terminal:
top    # Watch CPU spike
htop   # Better visualization

# Stress all CPU cores
stress-ng --cpu $(nproc) --timeout 60s

# Stress with specific load
stress-ng --cpu 2 --cpu-load 50 --timeout 30s
```

**Exercise:**
```bash
# Terminal 1:
stress-ng --cpu 2 --timeout 120s

# Terminal 2:
# Monitor and answer:
# 1. What's the load average?
uptime

# 2. Which process is using CPU?
top

# 3. What's the total CPU usage?
top    # Look at %Cpu(s) line
```

---

## Part 3: Memory Monitoring (45 minutes)

### Understanding Memory

**Linux memory types:**
- **Physical RAM** - Actual memory chips
- **Virtual Memory** - RAM + Swap combined
- **Swap** - Disk space used as overflow RAM
- **Buffers** - Temporary storage for I/O
- **Cache** - Cached file data for speed

**Memory states:**
- **Free** - Completely unused
- **Used** - In use by applications
- **Available** - Can be freed if needed
- **Shared** - Used by multiple processes
- **Buffers/Cache** - Used but reclaimable

---

### Check Memory Usage

```bash
# Simple memory check
free

# Human-readable format (MB/GB)
free -h

# Output explanation:
#               total        used        free      shared  buff/cache   available
# Mem:           7.6Gi       1.2Gi       5.8Gi        18Mi       658Mi       6.2Gi
# Swap:          0B          0B          0B

# total     = Total physical RAM
# used      = Used by applications
# free      = Completely unused
# shared    = Used by tmpfs/shared memory
# buff/cache = Used for file caching
# available = Memory available for new applications
```

**Key insight:** Don't panic if "free" is low. Linux uses free memory for cache. Look at "available" instead.

---

### Continuous Memory Monitoring

```bash
# Update every 2 seconds
watch -n 2 free -h

# With top
top
# Look at: KiB Mem line

# With htop
htop
# Visual bars at top show memory usage
```

---

### Detailed Memory Information

```bash
# Detailed memory stats
cat /proc/meminfo

# Key fields:
# MemTotal     = Total RAM
# MemFree      = Unused RAM
# MemAvailable = Available for allocation
# Buffers      = Temporary storage for raw disk blocks
# Cached       = Page cache
# SwapTotal    = Total swap space
# SwapFree     = Unused swap

# System memory summary
vmstat

# Output:
# procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----
#  r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
#  0  0      0 6123456  65432 673456    0    0     5    12   45   89  1  0 99  0  0

# r  = Processes waiting for CPU
# b  = Processes in uninterruptible sleep
# swpd = Virtual memory used
# free = Free memory
# buff = Buffer cache
# cache = Page cache
# si = Memory swapped in from disk
# so = Memory swapped out to disk
```

---

### Finding Memory Hogs

```bash
# Top 10 memory consumers
ps aux --sort=-%mem | head -11

# Or with specific columns
ps -eo pid,ppid,cmd,%mem,rss --sort=-%mem | head

# RSS = Resident Set Size (actual physical memory used)

# Continuous monitoring
top
# Press M to sort by memory
# or
htop
# Press F6, select %MEM
```

---

### Memory Per Process

```bash
# Detailed memory for specific process
cat /proc/<PID>/status | grep -i mem

# Or
pmap <PID>

# Summary
pmap -x <PID>

# Human readable
pmap -x <PID> | tail -1
```

---

### Swap Usage

```bash
# Check if swap is enabled
swapon --show

# If empty, no swap configured

# Enable swap (Amazon Linux often has no swap)
# Create 2GB swap file
sudo dd if=/dev/zero of=/swapfile bs=1M count=2048
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Verify
free -h
swapon --show

# Check swap usage
cat /proc/swaps

# Disable swap (for cleanup)
sudo swapoff /swapfile
sudo rm /swapfile
```

**When to worry about swap:**
- `si` and `so` in vmstat are high = System swapping heavily = Bad performance
- Swap usage > 50% = System needs more RAM

---

### Generating Memory Pressure

```bash
# Stress memory - allocate 1GB
stress-ng --vm 1 --vm-bytes 1G --timeout 60s

# While running, monitor:
# Terminal 1:
stress-ng --vm 2 --vm-bytes 512M --timeout 120s

# Terminal 2:
watch -n 1 free -h

# Terminal 3:
top
# Press M to sort by memory
```

**Exercise:**
```bash
# Find out:
# 1. How much memory is available?
free -h | grep Mem | awk '{print $7}'

# 2. What process uses most memory?
ps aux --sort=-%mem | head -2

# 3. How much memory does stress-ng use?
pgrep stress-ng | head -1 | xargs ps -o pid,cmd,%mem -p
```

---

## Part 4: I/O Monitoring (30 minutes)

### Understanding I/O

**I/O = Input/Output**
- Reading from disk (input)
- Writing to disk (output)
- Network I/O (not covered here, disk focus)

**Why I/O matters:**
- Disk is 1000x slower than RAM
- High I/O wait = CPU waiting for disk = Slow system

---

### Check I/O Statistics

```bash
# Install sysstat (if not already)
sudo yum install -y sysstat

# Basic I/O stats
iostat

# Output:
# avg-cpu:  %user   %nice %system %iowait  %steal   %idle
#            1.23    0.00    0.45    0.12    0.00   98.20
#
# Device             tps    kB_read/s    kB_wrtn/s    kB_read    kB_wrtn
# nvme0n1           1.23        12.34        56.78     123456     567890

# %iowait = CPU time waiting for I/O (high = problem)
# tps     = Transactions per second
# kB_read/s = Kilobytes read per second
# kB_wrtn/s = Kilobytes written per second
```

**Good values:**
- %iowait < 10% = Good
- %iowait 10-30% = Moderate
- %iowait > 30% = Disk bottleneck

---

### Extended I/O Statistics

```bash
# Detailed I/O stats
iostat -x 1

# Output columns:
# r/s    = Reads per second
# w/s    = Writes per second
# rkB/s  = KB read per second
# wkB/s  = KB written per second
# await  = Average time for I/O requests (ms)
# %util  = Device utilization (100% = saturated)

# Watch continuously (update every 2 seconds)
iostat -x 2

# Show only specific device
iostat -x nvme0n1 2
```

**Key metrics to watch:**
- `await` > 10ms = Slow
- `await` > 50ms = Very slow
- `%util` > 80% = Disk saturated

---

### Per-Process I/O

```bash
# Install iotop (if not installed)
sudo yum install -y iotop

# Real-time I/O by process
sudo iotop

# Key columns:
# TID   = Thread ID
# PRIO  = Priority
# USER  = Owner
# DISK READ  = Read speed
# DISK WRITE = Write speed
# SWAPIN = Swap in percentage
# IO>   = I/O percentage
# COMMAND = Process name

# Show only processes doing I/O
sudo iotop -o

# Batch mode (no interaction)
sudo iotop -b -n 1

# Show accumulated I/O
sudo iotop -a
```

---

### Check Disk Usage

```bash
# Disk space usage
df -h

# Inode usage (files count limit)
df -i

# Disk usage by directory
du -sh /*

# Find large directories
du -h / 2>/dev/null | sort -hr | head -20

# Find large files
find / -type f -size +100M 2>/dev/null | xargs ls -lh
```

---

### Monitoring I/O Wait

```bash
# Check iowait in top
top
# Look at: %Cpu(s): ... 0.2 wa ...
# wa = iowait

# Better view with htop
htop
# Red bar in CPU graph = iowait

# Historical iowait stats
sar -u 1 10
# Shows CPU stats for 10 seconds

# Just iowait
sar -u | awk '{print $6}' | grep -v iowait | grep -v ^$
```

---

### Generating I/O Load

```bash
# Generate read I/O
dd if=/dev/zero of=/tmp/testfile bs=1M count=1024

# Generate write I/O
dd if=/dev/zero of=/tmp/testfile bs=1M count=2048 oflag=direct

# While running, monitor:
# Terminal 1:
dd if=/dev/zero of=/tmp/testfile bs=1M count=5120

# Terminal 2:
iostat -x 1

# Terminal 3:
sudo iotop -o

# Stress I/O with stress-ng
stress-ng --io 4 --timeout 60s

# Cleanup
rm /tmp/testfile
```

**Exercise:**
```bash
# Run I/O stress and find:
# Terminal 1:
stress-ng --io 2 --timeout 120s

# Terminal 2 - Answer these:
# 1. What's the iowait?
iostat 1 2 | grep -A1 avg-cpu

# 2. Which process is doing I/O?
sudo iotop -o -n 1

# 3. What's disk utilization?
iostat -x 1 2 | grep nvme
```

---

## Part 5: Process Management (30 minutes)

### Starting Processes

```bash
# Run in foreground (blocks terminal)
sleep 100

# Run in background (doesn't block)
sleep 100 &

# The number shown is PID
# [1] 12345
#  ^   ^
#  |   PID
#  Job number

# Start multiple
sleep 200 &
sleep 300 &
sleep 400 &

# View background jobs
jobs

# Output:
# [1]   Running    sleep 200 &
# [2]-  Running    sleep 300 &
# [3]+  Running    sleep 400 &
```

---

### Foreground/Background Control

```bash
# Start a process
sleep 500

# Pause it: Press Ctrl+Z
# Output: [1]+ Stopped    sleep 500

# Resume in background
bg

# Or resume in foreground
fg

# If multiple jobs, specify which:
bg %2    # Resume job 2 in background
fg %1    # Bring job 1 to foreground

# Send specific job to background
sleep 1000
# Press Ctrl+Z
bg %1
```

---

### Killing Processes

```bash
# Gentle kill (SIGTERM - allows cleanup)
kill <PID>

# Force kill (SIGKILL - immediate)
kill -9 <PID>

# Kill by name
killall sleep

# Kill all processes matching pattern
pkill sleep

# Example:
sleep 1000 &
# Note the PID
kill <PID>

# Force kill if needed
kill -9 <PID>

# Verify it's dead
ps aux | grep sleep
```

**Common signals:**
```bash
# List all signals
kill -l

# Common ones:
kill -1 <PID>   # SIGHUP (reload config)
kill -2 <PID>   # SIGINT (Ctrl+C)
kill -9 <PID>   # SIGKILL (force kill)
kill -15 <PID>  # SIGTERM (gentle kill, default)
kill -18 <PID>  # SIGCONT (continue if stopped)
kill -19 <PID>  # SIGSTOP (pause process)
```

---

### Process Priority (Nice Values)

```bash
# Nice values: -20 (highest) to 19 (lowest)
# Default nice = 0

# Start with low priority (nice = 10)
nice -n 10 sleep 1000 &

# Start with high priority (needs sudo)
sudo nice -n -10 sleep 1000 &

# Check nice values
ps -eo pid,ni,cmd | grep sleep

# Change priority of running process
# Renice to 5
renice 5 <PID>

# Renice to -10 (needs sudo)
sudo renice -10 <PID>

# Example:
sleep 2000 &
PID=$!
ps -o pid,ni,cmd -p $PID
renice 10 $PID
ps -o pid,ni,cmd -p $PID
```

**When to use:**
- Background batch jobs: nice 10-19
- Real-time critical: nice -5 to -10
- Normal: nice 0 (default)

---

### Process Limits

```bash
# Check current limits
ulimit -a

# Output shows:
# core file size          (blocks, -c) 0
# data seg size           (kbytes, -d) unlimited
# scheduling priority             (-e) 0
# file size               (blocks, -f) unlimited
# max locked memory       (kbytes, -l) 65536
# max memory size         (kbytes, -m) unlimited
# open files                      (-n) 1024
# pipe size            (512 bytes, -p) 8
# POSIX message queues     (bytes, -q) 819200
# real-time priority              (-r) 0
# stack size              (kbytes, -s) 8192
# cpu time               (seconds, -t) unlimited
# max user processes              (-u) 15259

# Set limit for open files
ulimit -n 2048

# Check specific limit
ulimit -n
```

---

## Part 6: System-Wide Monitoring (20 minutes)

### All-in-One Monitoring

```bash
# Monitor everything at once
# CPU, Memory, I/O, Network
dstat

# Or if not installed
sudo yum install -y dstat
dstat -tcmdln 1

# Columns:
# time  | cpu | memory | disk | load | net
```

---

### Historical Statistics with sar

```bash
# Enable sysstat if not running
sudo systemctl start sysstat
sudo systemctl enable sysstat

# CPU usage history (today)
sar -u

# Memory usage history
sar -r

# I/O history
sar -b

# Load average history
sar -q

# All stats for specific time
sar -u -s 10:00:00 -e 12:00:00

# Yesterday's stats
sar -u -f /var/log/sa/sa$(date -d yesterday +%d)
```

---

### Creating a Custom Monitor Script

Create `system-monitor.sh`:

```bash
#!/bin/bash

echo "=== System Performance Monitor ==="
echo "Time: $(date)"
echo ""

echo "=== CPU Usage ==="
top -b -n 1 | grep "Cpu(s)" | awk '{print "User: " $2 ", System: " $4 ", Idle: " $8 ", IOWait: " $10}'
echo ""

echo "=== Load Average ==="
uptime | awk -F'load average:' '{print $2}'
echo ""

echo "=== Memory Usage ==="
free -h | grep Mem | awk '{print "Total: " $2 ", Used: " $3 ", Free: " $4 ", Available: " $7}'
echo ""

echo "=== Top 5 CPU Processes ==="
ps aux --sort=-%cpu | head -6 | tail -5 | awk '{print $11, "-", $3 "%"}'
echo ""

echo "=== Top 5 Memory Processes ==="
ps aux --sort=-%mem | head -6 | tail -5 | awk '{print $11, "-", $4 "%"}'
echo ""

echo "=== Disk Usage ==="
df -h | grep -v tmpfs | grep -v devtmpfs
echo ""

echo "=== I/O Wait ==="
iostat | grep -A1 avg-cpu | tail -1 | awk '{print "IOWait: " $4 "%"}'
```

```bash
chmod +x system-monitor.sh
./system-monitor.sh
```

---

### Continuous Monitoring

```bash
# Run monitor every 5 seconds
watch -n 5 ./system-monitor.sh

# Or log to file
while true; do
    ./system-monitor.sh >> system-monitor.log
    sleep 60
done &
```

---

## Part 7: Real-World Scenarios (30 minutes)

### Scenario 1: High CPU Usage

**Problem:** System is slow, CPU at 100%

**Investigation:**
```bash
# Step 1: Check overall CPU
top
# Press 1 to see per-core usage

# Step 2: Find the culprit
ps aux --sort=-%cpu | head -10

# Step 3: Check process details
ps -p <PID> -o pid,ppid,cmd,%cpu,%mem,stat,start

# Step 4: Decide action
# If legitimate: Let it run or lower priority
renice 10 <PID>

# If unwanted: Kill it
kill <PID>

# If it respawns: Find what's starting it
ps -o ppid= -p <PID>
```

---

### Scenario 2: Memory Leak

**Problem:** Memory usage keeps growing

**Investigation:**
```bash
# Step 1: Monitor memory over time
watch -n 5 'free -h; echo ""; ps aux --sort=-%mem | head -6'

# Step 2: Identify growing process
# Run this a few times
ps aux --sort=-%mem | head -3

# Step 3: Get detailed memory info
pmap <PID> | tail -1

# Step 4: Monitor specific process
watch -n 2 "ps -o pid,cmd,%mem,rss -p <PID>"

# Step 5: If confirmed leak
# Restart the service
sudo systemctl restart <service>
```

---

### Scenario 3: High I/O Wait

**Problem:** System slow, high iowait

**Investigation:**
```bash
# Step 1: Confirm iowait
iostat -x 1 5
# Look at %iowait and %util

# Step 2: Find which process
sudo iotop -o -n 5

# Step 3: Check what files it's accessing
sudo lsof -p <PID> | grep -E "REG|DIR"

# Step 4: Check disk health
sudo smartctl -a /dev/nvme0n1

# Step 5: Optimize or kill
# Lower priority
sudo renice 15 <PID>

# Or kill if not needed
kill <PID>
```

---

### Scenario 4: System Unresponsive

**Problem:** Can't SSH, system not responding

**Prevention - Set up logging:**
```bash
# Log system stats every minute
* * * * * /usr/bin/iostat -x 1 1 >> /var/log/iostat.log 2>&1
* * * * * /usr/bin/free -h >> /var/log/memory.log 2>&1
* * * * * /usr/bin/ps aux --sort=-%cpu | head -10 >> /var/log/top-cpu.log 2>&1

# Add to crontab
crontab -e
```

**After recovery, investigate:**
```bash
# Check system logs
sudo journalctl -xe

# Check kernel messages
sudo dmesg | tail -50

# Review your logs
tail -100 /var/log/iostat.log
tail -100 /var/log/memory.log
```

---

### Scenario 5: Finding Resource Hogs

Create `find-hogs.sh`:

```bash
#!/bin/bash

echo "=== Resource Hogs Report ==="
echo "Generated: $(date)"
echo ""

echo "=== Top 5 CPU Hogs ==="
ps aux --sort=-%cpu | head -6 | tail -5
echo ""

echo "=== Top 5 Memory Hogs ==="
ps aux --sort=-%mem | head -6 | tail -5
echo ""

echo "=== Processes in D state (I/O wait) ==="
ps aux | awk '$8 ~ /D/ {print $0}'
echo ""

echo "=== Zombie Processes ==="
ps aux | awk '$8 ~ /Z/ {print $0}'
echo ""

echo "=== High Nice Value Processes ==="
ps -eo pid,ni,cmd | awk '$2 > 10 {print $0}'
```

```bash
chmod +x find-hogs.sh
./find-hogs.sh
```

---

## Practice Exercises

### Exercise 1: CPU Hunt

```bash
# Generate CPU load
stress-ng --cpu 2 --timeout 300s &

# Your tasks:
# 1. Find the PID of stress-ng
pgrep stress-ng

# 2. What's its CPU usage?
ps -p <PID> -o %cpu

# 3. Lower its priority
renice 10 <PID>

# 4. Monitor for 30 seconds
top -p <PID> -d 1 -n 30

# 5. Kill it
kill <PID>
```

---

### Exercise 2: Memory Investigation

```bash
# Generate memory load
stress-ng --vm 1 --vm-bytes 500M --timeout 300s &

# Your tasks:
# 1. How much memory is it using?
ps aux | grep stress-ng | grep -v grep | awk '{print $4 "%"}'

# 2. Get exact RSS value
ps -p <PID> -o rss

# 3. Watch it for 1 minute
watch -n 5 "ps -p <PID> -o pid,cmd,%mem,rss"

# 4. Check if system is swapping
vmstat 1 10 | awk '{print $7, $8}'
```

---

### Exercise 3: I/O Testing

```bash
# Generate I/O
dd if=/dev/zero of=/tmp/bigfile bs=1M count=5000 &
DD_PID=$!

# Your tasks:
# 1. What's the iowait?
iostat 1 5 | grep -A1 avg-cpu

# 2. Which process is doing I/O?
sudo iotop -o -b -n 1

# 3. How much data written?
iostat -x 1 5 | grep nvme

# 4. Kill the dd process
kill $DD_PID
rm /tmp/bigfile
```

---

## Quick Reference Cheat Sheet

### Process Commands
```bash
ps aux                          # All processes
ps -ef                          # Full format
pgrep <name>                    # Find by name
pstree                          # Process tree
kill <PID>                      # Kill process
kill -9 <PID>                   # Force kill
killall <name>                  # Kill by name
nice -n 10 <cmd>               # Start with priority
renice 5 <PID>                 # Change priority
```

### CPU Monitoring
```bash
top                             # Real-time monitor
htop                            # Better top
uptime                          # Load average
lscpu                           # CPU info
ps aux --sort=-%cpu | head     # Top CPU users
```

### Memory Monitoring
```bash
free -h                         # Memory usage
vmstat 1                        # Virtual memory stats
ps aux --sort=-%mem | head     # Top memory users
pmap <PID>                     # Process memory map
cat /proc/meminfo              # Detailed memory
```

### I/O Monitoring
```bash
iostat -x 1                     # I/O stats
sudo iotop                      # I/O by process
df -h                           # Disk space
du -sh /*                       # Directory sizes
lsof -p <PID>                  # Open files
```

### Quick Diagnostics
```bash
# System health check
uptime && free -h && df -h

# Find resource hogs
ps aux --sort=-%cpu | head -5
ps aux --sort=-%mem | head -5

# Check for problems
ps aux | grep -E "D|Z"         # Stuck or zombie
iostat | grep -A1 avg-cpu      # High iowait?
```

---

## Common Issues & Solutions

### Issue 1: Can't Kill Process

```bash
# Try gentle kill first
kill <PID>

# If not working, force
kill -9 <PID>

# If still running, check if it's a kernel process
ps -p <PID> -o comm
# If in [], it's kernel (can't kill)

# Or check if process is in D state (uninterruptible)
ps -p <PID> -o stat
# D state means waiting for I/O, wait or reboot
```

---

### Issue 2: System Slow but Nothing in top

```bash
# Check iowait
iostat -x 1 5

# Check if swapping
vmstat 1 5

# Check disk health
sudo smartctl -a /dev/nvme0n1

# Check system logs
sudo journalctl -xe | tail -50
```

---

### Issue 3: Memory Full

```bash
# Check what's using memory
ps aux --sort=-%mem | head -20

# Check for cache
free -h
# If buff/cache is high, it's okay

# Clear cache (usually not needed)
sudo sync
sudo echo 3 > /proc/sys/vm/drop_caches

# Check for memory leaks
watch -n 5 'ps aux --sort=-%mem | head -6'
```

---

## Cleanup

```bash
# Kill all stress processes
killall stress-ng

# Remove swap if created
sudo swapoff /swapfile
sudo rm /swapfile

# Remove test files
rm /tmp/testfile
```

---

## Next Steps

After mastering this:
- Learn `strace` for system call tracing
- Study `perf` for performance profiling
- Explore `bpftrace` for advanced tracing
- Learn about cgroups for resource limits
- Study Docker container resource management

---

**Remember:** Always understand what you're measuring before taking action. High CPU isn't always bad. High memory usage is normal. Context matters!
