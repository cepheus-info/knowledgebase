# Install openSUSE Microos via OVA

## Overview

OVA stands for Open Virtual Appliance. As openSUSE Microos is a readonly os, it's likely we need to configure some bootstrapping process before installation.

## Prerequisite

- We are using vmware workstation for this demonstration.

- vmdk & vmx file to launch os.
  As we're not able to use ignition with DVD installation.

- configured ignition iso See [config ignition for microos](./config-ignition-for-microos.md)

## Installation

### Download vmdk & vmx

Download vmdk.xz & vmx file from [https://en.opensuse.org/Portal:MicroOS/Downloads](https://en.opensuse.org/Portal:MicroOS/Downloads)

Extract and rename openSUSE-MicroOS.x86_64-ContainerHost-VMware.vmdk to openSUSE-MicroOS.x86_64-16.0.0.vmdk as the vmx file asked for.

### OVA or VMX

#### use OVA to bootstrap os

##### Convert vmx to ova

Vmware workstation contains a builtin ovftool in below location:

```ps1
C:\Program Files (x86)\VMware\VMware Workstation\OVFTool
```

```ps1
ovftool.exe .\openSUSE-MicroOS.x86_64-ContainerHost-VMware.vmx opensuse-microos.ova
# Opening VMX source: .\openSUSE-MicroOS.x86_64-ContainerHost-VMware.vmx
# Opening OVA target: openSUSE.ova
# Writing OVA package: openSUSE.ova
# Transfer Completed
# Completed successfully
```

##### Boot ova via ovftool

If you choose gzip for guestinfo.ignition.config.data.encoding. You can execute gzip & base64 command in wsl.

```bash
# encode config.ign with base64
# -w 0 will disable wrap text
gzip < config.ign | base64 -w 0
```

Execute below powershell script:

```ps1
$content = (Get-Content .\config.ign -Raw).ToString()
$by = [System.Text.Encoding]::UTF8.GetBytes($content)
$output =[Convert]::ToBase64String($by)
# Can also use previously provided string directly
$CONFIG_ENCODED= $output
$CONFIG_ENCODING='base64'
# use gzip+base64 if copied from previous command
# $CONFIG_ENCODING='gzip+base64'
$VM_NAME='worker3-opensuse-microos'
$OVA_FILE='./opensuse-microos.ova'
$VIRTUAL_MACHINE_PATH='D:\VirtualMachines'
ovftool --powerOffTarget --name="${VM_NAME}" --allowExtraConfig --extraConfig:guestinfo.ignition.config.data.encoding="${CONFIG_ENCODING}"   --extraConfig:guestinfo.ignition.config.data="${CONFIG_ENCODED}" "${OVA_FILE}" ${VIRTUAL_MACHINE_PATH}
```

#### Edit vmx directly?

Or you can edit vmx file directly to append 2 lines of configuration there.

```bash
# open & edit .\openSUSE-MicroOS.x86_64-ContainerHost-VMware.vmx
# append below content
guestinfo.ignition.config.data = "base64 encoded config.ignition string"
guestinfo.ignition.config.data.encoding = "base64"
```

```bash
# Todo: don't know if direct editing is working
```

### Open Vmware to boot

We can now use vmware to open or scan vmx file to boot the os.

## Conclusion

We explore two ways to configure ignition with openSUSE Microos. And vmware is not the only option to do that.
