---
title: Mount hgfs for vmware linux shared folder
description: 
published: true
date: 2022-11-22T05:25:19.059Z
tags: 
editor: markdown
dateCreated: 2022-08-23T06:51:11.165Z
---

# Mount hgfs

## Use vmhgfs-fuse
vmhgfs-fuse /mnt/hgfs/share/

## Troubleshooting

In case there is an error "Error -107 cannot open connection!" occurring, which means vmtools not installed.

We can mount cdrom and install it in guest machine.

```bash
# Mount /dev/cdrom
sudo mkdir /mnt/cdrom
sudo mount /dev/cdrom /mnt/cdrom
```

```bash
# Extract VMwareTools-10.3.23-16594550.tar.gz into another location
mkdir /home/tmp/vmtools
cd /home/tmp/vmtools
tar zvxf /mnt/cdrom/VMwareTools-10.3.23-16594550.tar.gz
```

```bash
# Execute install command
cd vmware-tools-distrib
sudo ./vmware-install.pl
```

Note that you should install insserv-compat before vmware-install if you are running a SUSE distribution.
```bash
# Search insserv-compat via https://software.opensuse.org/ and then find the repository
# zypper add repository
sudo zypper ar -r https://download.opensuse.org/repositories/home:/alveus:/depository/openSUSE_Tumbleweed/home:alveus:depository.repo
# zypper install
sudo zypper install insserv-compat
```

