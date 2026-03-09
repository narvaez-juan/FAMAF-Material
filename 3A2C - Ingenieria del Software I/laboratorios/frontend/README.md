# Frontend setup and running

## Clone the repository
```bash
git clone https://github.com/IngSoft1-pseudoIngenieros/frontend.git
# Change directory to the cloned repo folder
cd frontend
```
This will create a local copy of the frontend project and move into the frontend folder.

## Steps to run the frontend on Linux Ubuntu (Bash)

These instructions assume you are on Linux Ubuntu and using Bash.

1) Install dependencies

```bash
npm install
```

2) Run the development server

```bash
npm run dev
```
3) Paste on a browser navegator the link on `Local: `

```bash
# It may be different
http://localhost:3000/
```

4) Run tests

Run all tests

```bash
npm run test
```

If you want to run seeing the coverage
```
npm install --save-dev @vitest/coverage-v8
npm run test:coverage
```
