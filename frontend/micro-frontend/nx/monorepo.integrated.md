# Guide to use Nx to build a integrated micro-frontend application

## 1. Walkthrough

### 1.1. Create a new workspace

```bash
npx create-nx-workspace@latest integrated --preset=ts
```

### 1.2. create packages in packages folder

```bash
npx nx g @nx/js:library is-even --publishable --importPath @integrated/is-even --simpleModuleName
```

```bash
npx nx g @nx/js:library is-odd --publishable --importPath @integrated/is-odd --simpleModuleName
```

The tsconfig.base.json contains the following:

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@integrated/is-even": ["packages/is-even/src/index.ts"],
      "@integrated/is-odd": ["packages/is-odd/src/index.ts"]
    }
  }
}
```

### 1.3. build packages

```bash
npx nx run-many --target=build
```

## References

- [Nx](https://nx.dev/)
- [https://github.com/nrwl/nx-recipes/tree/main/integrated](https://github.com/nrwl/nx-recipes/tree/main/integrated)
