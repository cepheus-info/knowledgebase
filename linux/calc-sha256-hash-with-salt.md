# Calc sha256 hash with salt

Below is a bash script to calc sha256 hash with salt. The salt is the command line argument.

```bash
#!/bin/bash
# parameter 1: salt
salt=$1
# calc sha256 hash
echo $(echo -n "password" | sha256sum | awk '{print $1}')$salt | sha256sum | awk '{print $1}'
```
