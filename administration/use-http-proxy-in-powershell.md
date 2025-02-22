# Use http proxy in powershell

## Walkthrough

We could use below command to set HTTP_PROXY & HTTPS_PROXY in Powershell environment.

```ps1
$proxy='http://127.0.0.1:1080'
$ENV:HTTP_PROXY=$proxy
$ENV:HTTPS_PROXY=$proxy
# Use below command to check connectivity
curl -v https://google.com
```
