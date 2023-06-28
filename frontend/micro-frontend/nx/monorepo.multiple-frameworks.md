# Using Nx to create mixed frameworks micro-frontend application

## 1. Walkthrough

### 1.1. Create a new workspace

```bash
npx create-nx-workspace@latest mixed-frameworks --preset=ts
```

### 1.2. Install framework dependencies

```bash
npm install --save-dev @nx/angular @nx/react
```

### 1.3. create packages in packages folder

```bash
npx nx g @nx/react:host hostapp
```

```bash
npx nx g @nx/angular:remote remoteapp
```
