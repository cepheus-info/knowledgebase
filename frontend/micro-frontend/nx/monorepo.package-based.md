# Guide to use Nx to build a package based micro-frontend application

## 1. Walkthrough

### 1.1. Create a new workspace

```bash
npx create-nx-workspace@latest package-based --preset=npm
```

### 1.2. Add a package in packages folder

the file tree is like this:

```bash
├── README.md
├── nx.json
├── packages
│   ├── is-even
│   │   ├── index.ts
│   │   ├── package.json
│   ├── is-odd
│   │   ├── index.ts
│   │   ├── package.json
├── package.json
└── package-lock.json
```

### 1.3. Update dependencies in your package's package.json

```json
{
  "name": "is-odd",
  "version": "1.0.0",
  "devDependencies": {
    "typescript": "^5.1.5"
  },
  "dependencies": {
    "is-even": "*"
  },
  "main": "dist/index.js",
  "scripts": {
    "build": "tsc index.ts --outDir dist"
  }
}
```

### 1.4. Task dependencies in nx.json

```json
{
  // ...
  "targetDefaults": {
    "build": {
      "dependsOn": ["^build"]
    }
  }
}
```

### 1.5. Build your package

> Build your package in the root folder of your workspace

```bash
npx nx build is-odd
```

> Build multiple packages

```bash
npx nx run-many --target=build --projects=is-odd,is-even
```

## 2. References

- [Nx](https://nx.dev/)
- [https://github.com/nrwl/nx-recipes/tree/main/package-based](https://github.com/nrwl/nx-recipes/tree/main/package-based)
