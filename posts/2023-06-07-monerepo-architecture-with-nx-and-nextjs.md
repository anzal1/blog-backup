---
title: "Monerepo Architecture with Nx and Next.js"
slug: "monerepo-architecture-with-nx-and-nextjs"
date: "2023-06-07T19:10:28+00:00"
author: "Anzal Husain Abidi"
description: "Introduction to monorepo architecture What is a monorepo ? Monorepo architecture, short for \"monolithic repository architecture,\" is a software development approach where multiple projects or components are stored within a single repository. Instead ..."
cover: "https://cdn.hashnode.com/res/hashnode/image/upload/v1686164822125/2d2a383c-9653-459c-8137-ec3b72b5ca61.png"
tags:
  - "newbie"
  - "Web Development"
  - "Next.js"
  - "Developer"
  - "webdev"
canonical_url: "https://anzal.hashnode.dev/monerepo-architecture-with-nx-and-nextjs"
source: "hashnode"
---

![Monerepo Architecture with Nx and Next.js](https://cdn.hashnode.com/res/hashnode/image/upload/v1686164822125/2d2a383c-9653-459c-8137-ec3b72b5ca61.png)

## Introduction to monorepo architecture

### What is a monorepo ?

Monorepo architecture, short for "monolithic repository architecture," is a software development approach where multiple projects or components are stored within a single repository. Instead of maintaining separate repositories for each project or component, all the code, assets, and related resources are consolidated into a single repository.

In a monorepo, you would typically find multiple directories or folders, each representing a different project or component. These projects or components might be related to each other, such as different services of a larger application or different libraries used across multiple projects. By organizing them together, it becomes easier to manage and coordinate changes, dependencies, and version control.

There are a few advantages to using a monorepo architecture:

1. **Code sharing and reuse**: With all the projects in one repository, it's easier to share and reuse code between different components. Developers can extract shared libraries, utilities, or modules that can be utilized across the entire codebase.
2. **Simplified dependency management**: In a monorepo, managing dependencies becomes more straightforward. Instead of dealing with separate dependencies for each project, you can have a centralized dependency management system. This can reduce conflicts, ensure consistent versions, and simplify the overall build process.
3. **Consistent versioning**: Since all projects are within the same repository, it's easier to ensure consistent versioning across different components. You can tag releases, manage changelogs, and track version history more efficiently.
4. **Easier code refactoring and collaboration**: Having a monorepo can facilitate collaboration among developers. It's easier to refactor code across different projects, perform cross-project refactorings, and make sweeping changes if required. Developers can also work on multiple projects simultaneously, making it simpler to coordinate changes and releases.

However, there are also some challenges and considerations with monorepo architecture:

1. **Increased repository size**: Since all projects are stored in a single repository, the overall size of the repository can grow significantly. This can impact clone times, disk space requirements, and the performance of certain operations.
2. **Build and test complexity**: As the number of projects or components increases, the build and test processes can become more complex. Building and testing the entire monorepo can be time-consuming and resource-intensive. It requires a robust build system and efficient test suites to manage these complexities effectively.
3. **Organization and access control**: With multiple projects in a monorepo, it's important to have a clear organization and access control mechanisms in place. Developers need to understand the repository structure and have proper permissions to work on specific projects or components.

Overall, monorepo architecture can be a powerful approach for managing large-scale software projects or interconnected components. It provides advantages such as code sharing, simplified dependency management, and easier collaboration. However, it also requires careful planning, tooling, and consideration of potential challenges to ensure successful implementation.

## How to set a monorepo with Nx and Next.js

### Project Setup

We'll begin by creating a default Next.js application with a Typescript template.

```powershell
npx create-next-app --ts nextjs-fullstack-app-template

cd nextjs-fullstack-app-template
```

First we will test to make sure the app is working. We're going to be using `yarn` for this example, but you could just as easily use NPM if you choose.

```powershell
yarn install

yarn dev
```

Also recommended to run

```powershell
yarn build
```

To ensure you can successfully do a production build of the project. It's recommended (but not required) to close your dev server when running a Next.js build. Most of the time there is no issue but occasionally the build can put your dev server in a weird state that requires a restart.

You should get a nice little report on the command line of all the pages built with green coloured text implying they are small and efficient. We'll try to keep them that way as we develop the project.

### Engine Locking

We would like for all developers working on this project to use the same Node engine and package manager we are using. To do that we create two new files:

- `.nvmrc` - Will tell other uses of the project which version of Node is used
- `.npmrc` - Will tell other users of the project which package manager is used

We are using `Node v14 Fermium` and `yarn` for this project so we set those values like so:

`.nvmrc`

```powershell
lts/fermium
```

`.npmrc`

```json
engine-strict=true
```

You can check your version of Node with `node --version` and make sure you are setting the correct one. A list of Node version codenames can be found [here](https://github.com/nodejs/Release/blob/main/CODENAMES.md)

Note that the use of `engine-strict` didn't specifically say anything about `yarn`, we do that in `package.json`:

`package.json`

```json
  "name": "nextjs-fullstack-app-template",
  "author": "YOUR_NAME",
  "description": "A tutorial and template for creating a production-ready fullstack Next.js application",
  "version": "0.1.0",
  "private": true,
  "license" : "MIT"
  "homepage": "YOUR_GIT_REPO_URL"
  "engines": {
    "node": ">=14.0.0",
    "yarn": ">=1.22.0",
    "npm": "please-use-yarn"
  },
  ...
```

The `engines` field is where you specify the specific versions of the tools you are using. You can also fill in your personal details if you choose.

### Git Setup

This would be a good time to make our first commit to our remote repo, to make sure our changes are backed up, and to follow best practices for keeping related changes grouped within a single commit before moving to something new.

By default your Next.js project will already have a repo initialized. You can check what branch you are on with `git status`. It should say something like:

```powershell
On branch main
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   README.md

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        .npmrc
        .nvmrc
```

This tells us we are on the `main` branch and we have not staged or made any commits yet.

Let's commit our changes so far.

```powershell
git add .

git commit -m 'project initialization'
```

The first command will add and stage all files in your project directory that aren't ignored in `.gitignore`. The second will make a commit of the state of your current project with the message we wrote after the `-m` flag.

Hop over to your preferred git hosting provider ([Github](https://github.com/) for example) and create a new repository to host this project. Make sure the default branch is se tto the same name as the branch on your local machine to avoid any confusion.

On Github you can change your global default branch name to whatever you like by going to:

```powershell
Settings -> Repositories -> Repository default branch
```

Now you are ready to add the remote origin of your repository and push. Github will give you the exact instructions when you create it. Your syntax may be a little different than mine depending on if you are using HTTPS rather than SSH.

```powershell
git remote add origin git@github.com:{YOUR_GITHUB_USERNAME}/{YOUR_REPOSITORY_NAME}.git

git push -u origin {YOUR_BRANCH_NAME}
```

Note that from this point on we will be using the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/#summary) standard and specifically the Angular convention [described here](https://github.com/angular/angular/blob/22b96b9/CONTRIBUTING.md#type)

The reason being like many other features in this project to simply set a **consistent** standard for all developers to use to minimize train-up time when contributing to the project. I personally have very little concern as to what standard is chosen, as long as everyone agrees to follow it that is the most important thing.

Consistency is everything!

### Code Formatting and Quality Tools

In order to set a standard that will be used by all contributors to the project to keep the code style consistent and basic best practices followed we will be implementing two tools:

- [eslint](https://eslint.org/) - For best practices on coding standards
- [prettier](https://prettier.io/) - For automatic formatting of code files

### ESLint

We'll begin with ESLint, which is easy because it automatically comes installed and pre-configured with Next.js projects.

We are just going to add a little bit of extra configuration and make it a bit stricter than it is by default. If you disagree with any of the rules it sets, no need to worry, it's very easy to disable any of them manually. We configure everything in `.eslintrc.json` which should already exist in your root directory:

`.eslintrc.json`

```json
{
  "extends": ["next", "next/core-web-vitals", "eslint:recommended"],
  "globals": {
    "React": "readonly"
  },
  "rules": {
    "no-unused-vars": [1, { "args": "after-used", "argsIgnorePattern": "^_" }]
  }
}
```

In the above small code example we have added a few additional defaults, we have said that `React` will always be defined even if we don't specifically import it, and I have added a personal custom rule that I like which allows you to prefix variables with an underscore \_ if you have declared them but not used them in the code.

I find that scenario comes up often when you are working on a feature and want to prepare variables for use later, but have not yet reached the point of implementing them.

You can test out your config by running:

```powershell
yarn lint
```

You should get a message like:

```powershell
✔ No ESLint warnings or errors
Done in 1.47s.
```

If you get any errors then ESLint is quite good at explaining clearly what they are. If you encounter a rule you don't like you can disable it in "rules" by simply setting it to 1 (warning) or 0 (ignore) like so:

```json
  "rules": {
    "no-unused-vars": 0, // As example: Will never bug you about unused variables again
  }
```

Let's make a commit at this point with the message `build: configure eslint`

### Prettier

Prettier will take care of automatically formatting our files for us. Let's add it to the project now.

It's only needed during development, so I'll add it as a `devDependency` with `-D`

```powershell
yarn add -D prettier
```

I also recommend you get the [Prettier VS Code extension](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode) so that VS Code can handle the formatting of the files for you and you don't need to rely on the command line tool. Having it installed and configured in your project means that VSCode will use your project's settings, so it's still necessary to add it here.

We'll create two files in the root:

`.prettierrc`

```json
{
  "trailingComma": "es5",
  "tabWidth": 2,
  "semi": true,
  "singleQuote": true
}
```

Those values are entirely at your discretion as to what is best for your team and project.

`.prettierignore`

```plaintext
.yarn
.next
dist
node_modules
```

In that file I've placed a list of directories that I don't want Prettier to waste any resources working on. You can also use patterns like \*.html to ignore groups of types of files if you choose.

Now we add a new script to `package.json` so we can run Prettier:

`package.json`

```json
  ...
  "scripts: {
    ...
    "prettier": "prettier --write ."
  }
```

You can now run

```powershell
yarn prettier
```

to automatically format, fix and save all files in your project you haven't ignored. By default my formatter updated about 5 files. You can see them in your list of changed files in the source control tab on the left of VS Code.

Let's make another commit with `build: implement prettier`.

## Git Hooks

One more section on configuration before we start getting into component development. Remember you're going to want this project to be as rock solid as possible if you're going to be building on it in the long term, particularly with a team of other developers. It's worth the time to get it right at the start.

We are going to implement a tool called [Husky](https://typicode.github.io/husky/#/)

Husky is a tool for running scripts at different stages of the git process, for example add, commit, push, etc. We would like to be able to set certain conditions, and only allow things like commit and push to succeed if our code meets those conditions, presuming that it indicates our project is of acceptable quality.

To install Husky run

```powershell
yarn add -D husky

npx husky install
```

The second command will create a `.husky` directory in your project. This is where your hooks will live. Make sure this directory is included in your code repo as it's intended for other developers as well, not just yourself.

Add the following script to your `package.json` file:

`package.json`

```json
  ...
  "scripts: {
    ...
    "prepare": "husky install"
  }
```

This will ensure Husky gets installed automatically when other developers run the project.

To create a hook run

```powershell
npx husky add .husky/pre-commit "yarn lint"
```

The above says that in order for our commit to succeed, the `yarn lint` script must first run and succeed. "Succeed" in this context means no errors. It will allow you to have warnings (remember in the ESLint config a setting of 1 is a warning and 2 is an error in case you want to adjust settings).

Let's create a new commit with the message `ci: implement husky`. If all has been setup properly your lint script should run before the commit is allowed to occur.

We're going to add another one:

```powershell
npx husky add .husky/pre-push "yarn build"
```

The above ensures that we are not allowed to push to the remote repository unless our code can successfully build. That seems like a pretty reasonable condition doesn't it? Feel free to test it by committing this change and trying to push.

---

Lastly we are going to add one more tool. We have been following a standard convention for all our commit messages so far, let's ensure that everyone on the team is following them as well (including ourselves!). We can add a linter for our commit messages:

```powershell
yarn add -D @commitlint/config-conventional @commitlint/cli
```

To configure it we will be using a set of standard defaults, but I like to include that list explicitly in a `commitlint.config.js` file since I sometimes forget what prefixes are available:

`commitlint.config.js`

```js
// build: Changes that affect the build system or external dependencies (example scopes: gulp, broccoli, npm)
// ci: Changes to our CI configuration files and scripts (example scopes: Travis, Circle, BrowserStack, SauceLabs)
// docs: Documentation only changes
// feat: A new feature
// fix: A bug fix
// perf: A code change that improves performance
// refactor: A code change that neither fixes a bug nor adds a feature
// style: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
// test: Adding missing tests or correcting existing tests

module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'body-leading-blank': [1, 'always'],
    'body-max-line-length': [2, 'always', 100],
    'footer-leading-blank': [1, 'always'],
    'footer-max-line-length': [2, 'always', 100],
    'header-max-length': [2, 'always', 100],
    'scope-case': [2, 'always', 'lower-case'],
    'subject-case': [
      2,
      'never',
      ['sentence-case', 'start-case', 'pascal-case', 'upper-case'],
    ],
    'subject-empty': [2, 'never'],
    'subject-full-stop': [2, 'never', '.'],
    'type-case': [2, 'always', 'lower-case'],
    'type-empty': [2, 'never'],
    'type-enum': [
      2,
      'always',
      [
        'build',
        'chore',
        'ci',
        'docs',
        'feat',
        'fix',
        'perf',
        'refactor',
        'revert',
        'style',
        'test',
        'translation',
        'security',
        'changeset',
      ],
    ],
  },
};
```

Then enable commitlint with Husky by using:

```powershell
npx husky add .husky/commit-msg 'npx --no -- commitlint --edit "$1"'
# Sometimes above command doesn't work in some command interpreters
# You can try other commands below to write npx --no -- commitlint --edit $1
# in the commit-msg file.
npx husky add .husky/commit-msg \"npx --no -- commitlint --edit '$1'\"
# or
npx husky add .husky/commit-msg "npx --no -- commitlint --edit $1"
```

Feel free to try some commits that *don't* follow the rules and see how they are not accepted, and you receive feedback that is designed to help you correct them.

### VS Code Configuration

Now that we have implemented ESLint and Prettier we can take advantage of some convenient VS Code functionality to have them be run automatically.

Create a directory in the root of your project called `.vscode` and inside a file called `settings.json`. This will be a list of values that override the default settings of your installed VS Code.

The reason we want to place them in a folder for the project is that we can set specific settings that only apply to this project, and we can share them with the rest of our team by including them in the code repository.

Within `settings.json` we will add the following values:

`.vscode/settings.json`

```json
{
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll": true,
    "source.organizeImports": true
  }
}
```

The above will tell VS Code to use your Prettier extension as the default formatter (you can override manually if you wish with another one) and to automatically format your files and organize your import statements every time you save.

Very handy stuff and just another thing you no longer need to think about so you can focus on the important things like solving business problems.

I'll now make a commit with message `build: implement vscode project settings`.

### Debugging

Let's set up a convenient environment for debugging our application in case we run into any issues during development.

Inside of your `.vscode` directory create a `launch.json` file:

`launch.json`

```json
{
  "version": "0.1.0",
  "configurations": [
    {
      "name": "Next.js: debug server-side",
      "type": "node-terminal",
      "request": "launch",
      "command": "npm run dev"
    },
    {
      "name": "Next.js: debug client-side",
      "type": "pwa-chrome",
      "request": "launch",
      "url": "http://localhost:3000"
    },
    {
      "name": "Next.js: debug full stack",
      "type": "node-terminal",
      "request": "launch",
      "command": "npm run dev",
      "console": "integratedTerminal",
      "serverReadyAction": {
        "pattern": "started server on .+, url: (https?://.+)",
        "uriFormat": "%s",
        "action": "debugWithChrome"
      }
    }
  ]
}
```

With that script in place you have three choices for debugging. CLick the little "bug & play icon" on the left of VS Code or press `Ctrl + Shift + D` to access the debugging menu. You can select which script you want to run and start/stop it with the start/stop buttons.

In addition to this, or if you are not using VS Code, we can also set up some helpful debugging scripts in your project.

First we will install the [cross-env](https://www.npmjs.com/package/cross-env) which will; be necessary to set environment variables if you have teammates working on different environments (Windows, Linux, Mac, etc).

```powershell
yarn add -D cross-env
```

With that package installed we can update our `package.json` `dev` script to look like the following:

`package.json`

```json
{
  ...
  "scripts": {
    ...
    "dev": "cross-env NODE_OPTIONS='--inspect' next dev",
  },
}
```

This will allow you to log server data in the browser while working in dev mode, making it easier to debug issues.

At this stage I'll be making a new commit with message `build: add debugging configuration`

### Directory Structure

This section is now going to cover setting up the folder structure in our project. This is one of those topics that many people will have *extremely strong opinions about*, and for good reason! Directory structure can really make or break a project in the long term when it gets out of control, especially when fellow team members have to spend unnecessary time trying to guess where to put things (or find things).

I personally like to take a fairly simplistic approach, keep things separated basically in a class model/view style. We will be using three primary folders:

```plaintext
/components
/lib
/pages
```

- `component` - The individual UI components that make up the app will live in here
- `lib` - Business/app/domain logic will live in here.
- `pages` - Will be the actual routes/pages as per the required Next.js structure.

We will have other folders in addition to this to support the project, but the core of almost everything that makes up the unique app that we are building will be housed in these three directories.

Within `components` we will have subdirectories that kind of group similar types of components together. You can use any method you prefer to do this. I have used the MUI library quite a bit in my time, so I tend to follow the same organization they use for components in [their documentation](https://mui.com/getting-started/installation/)

For example inputs, surfaces, navigation, utils, layout etc.

You don't need to create these directories in advance and leave them empty. I would just create them as you go while building your components.

## Next.js meets Nx

In order to create a new Next.js application, we have two options mainly:

- use the [Next.js CLI](https://nextjs.org/docs/getting-started)
- use a [Nx workspace](https://nx.dev/latest/react/guides/nextjs)

We’re going to use Nx for this setup because it provides a series of advantages:

- support for multiple apps (we can easily add more apps to our workspace and share common logic)
- structure our code as [workspace libraries](https://nx.dev/latest/react/structure/creating-libraries), thus facilitating a cleaner architecture, code reuse and responsibility segregation
- improved build and test speed via Nx [affected commands](https://nx.dev/latest/react/core-concepts/affected) and [computation caching](https://nx.dev/latest/react/core-concepts/computation-caching)
- out of the box support for code generation, [Storybook](https://nx.dev/latest/react/storybook/overview) and [Cypress integration](https://nx.dev/latest/react/cypress/overview)

These parts will be covered in more detail in the upcoming articles that are part of this series.

To create a new Nx workspace, use the following command.

```powershell
npx create-nx-workspace juridev --packageManager=yarn
```

`juridev` here is the name of my organization and will be your namespace when you import libraries which we’ll see later.

When asked, use Next.js as the preset

![](https://juristr.com/blog/assets/imgs/nextjs-nx-series/create-nx-workspace.png)

During the setup, you’ll be asked to give the generated application a name. I use “site” for now as this is going to be my main Next.js website. Make sure to **choose CSS as the styling framework**. Because we’ll be using Tailwind later, we need pure CSS and PostCSS processing.

Once the installation and setup completes, run `yarn start` (or `npm start`) to launch the Next.js dev server and navigate to [http://localhost:4200](http://localhost:4200). You should see the running application.

## Nx Workspace structure

Let’s quickly explore the Nx workspace structure to learn some of the fundamentals.

### Apps and Libs

An Nx workspace is structured into **apps** and **libs**. Instead of having all the different features of our app just within folders of our application folder, we rather split them up into “workspace libraries”. Most of our business and domain logic should reside in those libraries. The apps can be seen as our “deployables”. They import the functionality in the libs as the building blocks to create a deployable app.

Although the libraries can be built and published (see [Publishable and Buildable Libraries](https://nx.dev/latest/react/structure/buildable-and-publishable-libraries/)), they don’t have to. They are referenced via TypeScript path mappings in the `tsconfig.base.json` configuration at the root of the Nx workspace. When we build the application, all referenced libraries are built into the app via the used bundler (e.g. Webpack or Rollup etc).

### Config files: workspace.json and nx.json

Let’s give a fast overview of the main configuration files. All the details can be found on the official docs page: [https://nx.dev/latest/react/core-concepts/configuration](https://nx.dev/latest/react/core-concepts/configuration)

The `workspace.json` is the main configuration file of an Nx workspace. It defines

- the projects in the workspace (e.g. apps and libs)
- the [Nx executor](https://nx.dev/latest/react/executors/using-builders) used to run operations on the projects (e.g. serve the app, build it, run Jest tests, Storybook etc..)

The `nx.json` defines mostly additional configuration properties used for the [Nx dependency graph](https://nx.dev/latest/react/structure/dependency-graph). Additionally, you can define the base branch (e.g. `master` or `main` or whatever you are using) and the [task runner](https://nx.dev/latest/react/core-concepts/configuration#tasks-runner-options) to be used.

### Serving, building and testing

The Nx workspace.json config defines what you can actually serve, build, test etc. Here’s a quick example of such a configuration for a project called `cart`.

```json
{
  "projects": {
    "cart": {
      "root": "apps/cart",
      "sourceRoot": "apps/cart/src",
      "projectType": "application",
      "targets": {
        "build": {
          "executor": "@nrwl/web:build",
          "options": {
            "outputPath": "dist/apps/cart",
            ...
          },
          ...
        },
        "serve": {...},
        "test": {
          "executor": "@nrwl/jest:jest",
          "options": {
            ...
          }
        }
      }
    }
  }
}
```

It defines targets for `build`, `serve` and `test`. These can be invoked using the following syntax:

```bash
npx nx run <proj-name>:<target> <options>
```

> Note, we use `npx` in front because we don’t have Nx installed globally. Thus npx will fallback and execute the installed binary in our node_modules folder. You can obviously also install Nx globally and get rid of having to prefix commands with `npx`

So to serve our app we run `nx run cart:serve`, to build it `nx run cart:build` and so on. There are also shortcuts, meaning we can alternatively invoke these commands like `nx serve cart` or `nx build cart`.

> In Nx “targets” are invocable commands. There are predefined commands such as build, serve, test that get set up when you generate a new application. You can also define your custom ones, either by building your own [Nx Executor](https://nx.dev/latest/react/executors/using-builders) or use the [Nx Run-Commands](https://nx.dev/latest/react/workspace/run-commands-executor).

## Working on our Next App

### Understanding Page Structures: Generating the About Page

When looking at the setup you’ll see a “pages” folder. Every file returning a React component in there, instructs Next.js to generate a new page. As you can see there is an `index.tsx` page, which you see when navigating to the root of the Next website [`http://localhost:4200`](http://localhost:4200). To better understand this, let’s create an About page that responds at [`http://localhost:4200/about`](http://localhost:4200/about).

Nx has some nice generators for that already. Hence, typing..

```bash
npx nx generate @nrwl/next:page --name=about --style=css
```

..generates a new `about.tsx` (with its according styling file).

```tsx
import './about.module.scss';

/* eslint-disable-next-line */
export interface AboutProps {}

export function About(props: AboutProps) {
  return (
    <div>
      <h1>Welcome to about!</h1>
    </div>
  );
}

export default About;
```

> Btw, if you’re not the terminal kind of person, you can also use the [Nx Console VSCode](https://marketplace.visualstudio.com/items?itemName=nrwl.angular-console) plugin.

If we now serve our app with `npx nx serve site` and navigate to `/about`, we should see something like the following:

![](https://juristr.com/blog/assets/imgs/nextjs-nx-series/next-webapp-running.png)

### Understanding `getStaticProps`

[Next.js Docs](https://nextjs.org/docs/basic-features/data-fetching#getstaticprops-static-generation)

`getStaticProps` allow us to return props to our React component that’s going to be pre-rendered by Next.js. It gets the `context` object as a parameter and should return an object of the form.

```tsx
return {
  props: { /* your own properties */ }
}
```

We can write our `getStaticProps` as follows:

```tsx
// apps/site/pages/about.tsx
import { GetStaticProps } from 'next';
...

export interface AboutProps {
  name: string;
}
...

export const getStaticProps: GetStaticProps<AboutProps> = async (context) => {
  return {
    props: {
      name: 'Juri'
    },
  };
};
```

Note how we use TypeScript to type the return value of our function to match our `AboutProps` from the `about.tsx` component. You can find more info about how to use the `getStaticProps` and others [with TypeScript on the official Next.js docs](https://nextjs.org/docs/basic-features/data-fetching#typescript-use-getstaticprops).

We can now use the props in our React component:

```tsx
export function About(props: AboutProps) {
  return (
    <div>
      <h1>Welcome, {props.name}!</h1>
    </div>
  );
}

export const getStaticProps: GetStaticProps<AboutProps> = async (context) => {
  ...
}
```

![](https://juristr.com/blog/assets/imgs/nextjs-nx-series/getstaticprops-page.png)

### Understanding `getStaticPaths`

[Next.js Docs](https://nextjs.org/docs/basic-features/data-fetching#getstaticpaths-static-generation)

If we want to create a blog, we’ll want to load pages dynamically. So we cannot really give them a static name as we did with our About page (`about.tsx`).

```bash
nx generate @nrwl/next:page --name=[slug] --style=none --directory=articles
```

This generates a new `articles` folder with a new `[slug].tsx` file. The `[slug]` part is where Next.js understands it is dynamic and needs to be filled accordingly. Let’s also clean up the generated part a bit, changing the React component name to `Article` as well as the corresponding TS interface.

So first of all let’s focus on the `getStaticPaths` function which we define as follows:

```tsx
// apps/site/pages/articles/[slug].tsx
import { ParsedUrlQuery } from 'querystring';

interface ArticleProps extends ParsedUrlQuery {
  slug: string;
}

export const getStaticPaths: GetStaticPaths<ArticleProps> = async () => {
  ...
}
```

[According to the docs](https://nextjs.org/docs/basic-features/data-fetching#getstaticpaths-static-generation) the function needs to return an object, having a `paths` as well as `fallback` property:

```tsx
return {
  paths: [
    { params: { ... } }
  ],
  fallback: true or false
};
```

The `paths` section contains the number of pages that should be pre-rendered. So we could have something like

```tsx
return {
  paths: [
    {
      slug: 'page1'
    },
    {
      slug: 'page2'
    }
  ],
  ...
}
```

From a mental model, this would instruct Next.js to “generate” (obviously it doesn’t) at the place of our `[slug].tsx` a `page1.tsx` and `page2.tsx` which are then converted to pages accessible at `/articles/page1` and `/articles/page2`.

This would be the place where you would go and read your file system or query the API for all the pages you wanna render. But more about that later. To simplify things, let us just generate a set of “pages”:

```tsx
export const getStaticPaths: GetStaticPaths<ArticleProps> = async () => {
  return {
    paths: [1, 2, 3].map((idx) => {
      return {
        params: {
          slug: `page${idx}`,
        },
      };
    }),
    fallback: false,
  };
};
```

The returned `params` object can be accessed from within the `getStaticProps` which we’ve seen before and potentially remapped to something else. Here’s the place where you could further elaborate the content, say we get the content in markdown, we could process and convert it to HTML here.

In this simple scenario we just pass it along:

```tsx
export const getStaticProps: GetStaticProps<ArticleProps> = async ({
  params,
}: {
  params: ArticleProps;
}) => {
  return {
    props: {
      slug: params.slug,
    },
  };
};
```

And finally we can access it from within the page React component:

```tsx
export function Article(props: ArticleProps) {
  return (
    <div>
      <h1>Visiting {props.slug}</h1>
    </div>
  );
}
```

![](https://juristr.com/blog/assets/imgs/nextjs-nx-series/getstaticpaths-page.png)

### What about `fallback`?

There’s another property returned by the `getStaticPaths` function: `fallback`. The Next.js docs are pretty clear about it, so make sure to [check them out](https://nextjs.org/docs/basic-features/data-fetching#the-fallback-key-required).

In short, `fallback: false` renders only the set of pages returned by the `paths` property. If a given page doesn’t find a match, a 404 page (that comes with Next.js) is being rendered.

> It’s also useful when the new pages are not added often. If you add more items to the data source and need to render the new pages, you’d need to run the build again.

If `fallback: true` the difference is that pages that have not been rendered during build time (e.g. that are not in the `paths` property) will not result in a 404 page. Rather, Next.js returns a [Fallback page](https://nextjs.org/docs/basic-features/data-fetching#fallback-pages) (e.g. a page where you could display a loading indicator) and then statically generates the page and the corresponding HTML and sends it back to the client, where the fallback page is swapped with the real one. Furthermore, it will be added to the sets of pre-rendered pages, s.t. any subsequent call will be immediate.

## Building and Exporting our Next.js application with Nx

Next.js defines two main options when it comes to generating your deployable:

- **build -** allows to generate an optimized bundle that can be served by the `next` CLI, e.g. when deploying to some [Vercel](https://vercel.com/) infrastructure. It requires a Node environment that can run the application. We will talk more about deployment of Next.js apps in an upcoming article
- **export -** allows to generate a static site out of your Next.js application. This is ideal if you don’t have a Node environment and you just want to serve the app from some static CDN.

Hence, also the Nx configuration (in `workspace.json`) has matching Nx targets (see the section about “Nx Workspace structure” to learn more).

We can invoke the “build” with

```plaintext
nx run site:build --configuration=production
```

or alternatively with `nx build site`.

Similarly, the `export` can be invoked with

```plaintext
nx run site:export --configuration=production
```

or `nx export site`. Using the `export` command will automatically build the Next.js app first.

By passing `--configuration=production` (or `--prod`) the production configuration is being used which is defined in the `workspace.json` and which can set additional production environment only properties:

```json
"build": {
    "executor": "@nrwl/next:build",
    "outputs": ["{options.outputPath}"],
    "options": {
        "root": "apps/site",
        "outputPath": "dist/apps/site"
    },
    "configurations": {
        "production": {}
    }
},
```

### For reference visit : [https://github.com/anzal1/Nx-monorepo-template](https://github.com/anzal1/Nx-monorepo-template)
