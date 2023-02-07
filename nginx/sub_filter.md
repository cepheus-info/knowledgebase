---
title: Use sub_filter to modify response content
description: subfilter
published: true
date: 2022-10-31T04:59:21.587Z
tags: 
editor: markdown
dateCreated: 2022-10-31T04:59:21.587Z
---

# Use subfilter to modify response content

## Overview
Sometimes, we need to modify the response content of a website. We can use the `sub_filter` directive to modify the response content. We can use the following command to modify the response content.

```bash
sub_filter 'old string' 'new string';
```

## Configure nginx to use subfilter to modify response content

A complete example is like below:

```bash
server {
    listen      80;
    server_name www.example.com;
    #...

    location / {
        sub_filter 'old string' 'new string';
        sub_filter_types text/html;
        sub_filter_once off;
        proxy_pass https://www.example.com;
    }
}
```

Then, we need to restart the nginx service. We can use the following command to restart the nginx service.

```bash
sudo systemctl restart nginx
```

## Tips
Avoid using the `sub_filter` directive to modify the response content of a website if there is any other way. The `sub_filter` directive is not efficient.