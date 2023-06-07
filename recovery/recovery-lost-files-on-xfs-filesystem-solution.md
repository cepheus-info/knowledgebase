# Recover lost files on xfs filesystem solution

## 1. Install xfsprogs

```bash
sudo apt-get install xfsprogs
```

## 2. Check the filesystem

```bash
sudo xfs_repair /dev/sda1
```

## 3. Mount the filesystem

```bash
sudo mount /dev/sda1 /mnt
```

## 4. Recover the files

```bash
sudo xfsdump -J - /dev/sda1 | xfsrestore -J - /mnt
```
