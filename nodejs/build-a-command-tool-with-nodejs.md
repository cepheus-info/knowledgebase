# Build a command tool with nodejs

## 1. Overview

It's common to use nodejs to handle some basic tasks with commond tool.

## 2. Steps

### 2.1. Initialize a typescript project

#### 2.1.1. Create a project

```bash
mkdir bcrypt-encoder
cd bcrypt-encoder
npm init -y
npm install typescript --save-dev
npx tsc --init
```

#### 2.1.2. Configure project

> You can change your package.json with build command.

```json
{
  "name": "bcrypt-encoder",
  "main": "index.ts",
  "bin": {
    "@cepheusinfo/bcrypt-encoder": "dist/index.js",
    "bcrypt-encoder": "dist/index.js"
  },
  "publishConfig": {
    "access": "public"
  },
  "scripts": {
    "build": "tsc",
    "test": "echo \"Error: no test specified\" && exit 1"
  }
}
```

> You can also change your tsconfig.json with output directory.

```json
"outDir": "./dist",
```

#### 2.1.3. Configure launch.json for debugging

> As in vscode, you can debug your code with launch settings. The preLaunchTask is used to build your code before debugging and the args is used to pass parameters to your code.

Use command like this: Ctrl + Shift + P -> Debug: Add Configuration -> Node.js

Then you can find the launch.json in .vscode folder. Modify it like this:

```json
"configurations": [
  {
    "type": "node",
    "request": "launch",
    "name": "Launch Program",
    "program": "${workspaceFolder}/dist/index.js",
    "preLaunchTask": "tsc: build - tsconfig.json",
    "args": [
      "-p",
      "123456"
    ],
    "outFiles": [
      "${workspaceFolder}/dist/**/*.js"
    ]
  }
]
```

> Enable configurations in tsconfig.json

```json
"sourceMap": true,
"outDir": "./dist",
"resolveJsonModule": true,
```

### 2.2. Install dependencies

```bash
npm install commander figlet bcryptjs --save
npm install @types/commander @types/figlet @types/bcryptjs @types/node --save-dev
```

### 2.3. Code implementation

```typescript
#!/usr/bin/env node

import { Command } from "commander";
import { version } from "./package.json";
import figlet from "figlet";
import bcrypt from "bcryptjs";

console.log(figlet.textSync("Bcrypt CLI"));

const program = new Command();

program
  .version(version)
  .description("A CLI for hashing strings with bcrypt")
  .option("-s, --string <string>", "String to hash")
  .parse(process.argv);

const options = program.opts();

if (options.string) {
  const password = typeof options.string === "string" ? options.password : "";
  const salt = bcrypt.genSaltSync(10);
  const hash = bcrypt.hashSync(password, salt);
  console.log(hash);
}
```

### 2.4. Build

```bash
npm run build
```

### 2.5. Install

```bash
npm link
```

### 2.6. Usage

```bash
bcrypt-encoder -s 123456
```

## 3. Reference

- [Commander.js](https://github.com/tj/commander.js)

- [Figlet](https://github.com/patorjk/figlet.js)

- [Bcrypt](https://github.com/kelektiv/node.bcrypt.js)
