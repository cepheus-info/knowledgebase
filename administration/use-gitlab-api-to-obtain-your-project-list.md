# Use Gitlab API to obtain your project list

## Walkthrough

### 1) Get your private token

1. Login to your Gitlab account.

2. Click your avatar on the top right corner and select `Settings`.

3. Select `Access Tokens` on the left menu.

### 2) Get your project list

Use below command to get your project list:

```bash
TOKEN="your-private-token"; PREFIX="http_url_to_repo"; curl --header "PRIVATE-TOKEN: $TOKEN" https://your-gitlab-host/api/v4/projects?per_page=100 | grep -o "\"$PREFIX\":[^ ,]\+" | sed "s/\"$PREFIX\"://g" | sed "s/\"//g" > repos.dump
```
