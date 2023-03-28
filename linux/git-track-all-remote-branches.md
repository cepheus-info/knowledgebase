# Use bash to create all remote branches locally

## Process

Use below command to create all branches locally:

```bash
for i in `git branch -a | grep remote | grep -v HEAD | grep -v master`; do git branch --track ${i#remotes/origin/} $i; done
```
