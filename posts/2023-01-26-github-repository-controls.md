---
title: "Github Repository Controls"
slug: "github-repository-controls"
date: "2023-01-26T18:00:05+00:00"
author: "Anzal Husain Abidi"
description: "Github Tutorial: How to Make Your First GitHub Repository A critical skill for developers of all experience levels is proficiency in GitHub. Github is a hosting platform for Git repositories that acts as a central location to store and manage code. G..."
cover: "https://cdn.hashnode.com/res/hashnode/image/upload/v1674756123788/ab07d909-05d7-4d40-847d-e2d50380b025.png"
tags:
  - "GitHub"
  - "Beginner Developers"
  - "start"
  - "news"
  - "github-actions"
canonical_url: "https://anzal.hashnode.dev/github-repository-controls"
source: "hashnode"
---

![Github Repository Controls](https://cdn.hashnode.com/res/hashnode/image/upload/v1674756123788/ab07d909-05d7-4d40-847d-e2d50380b025.png)

Github Tutorial: How to Make Your First GitHub Repository

A critical skill for developers of all experience levels is proficiency in GitHub. Github is a hosting platform for Git repositories that acts as a central location to store and manage code. GitHub is a popular choice for developers and their teams because it offers version control, collaboration capabilities, and a community of peers sharing their trials and successes in software engineering.

In this article, we’ll complete a tutorial on creating your first GitHub repository. First, let’s start with a closer look at the GitHub ecosystem and why I recommend students of my Web Developer Bootcamp course and all software developers take the time to understand this valuable tool.

### GitHub vs. Git

They may have similar names, but GitHub is not synonymous with Git. Some developers work with Git and never use GitHub.

What’s Git? It’s an open-source version control management system that tracks changes to projects. Version control software records and manages every change made to source code and files. Git is a type of version control system for developers and teams to manage and collaborate on versions of code, which are stored in project repositories as it moves through the development life cycle.

Git can be used on its own without GitHub or other similar platforms, but it’s difficult to collaborate and share code with coworkers or the developer community without a platform like GitHub.

How does GitHub compare to Git? GitHub is a web platform that hosts Git repositories. Think of GitHub as a project viewer to share different code versions and access remote repositories. Each repository contains all project files and the code history. Repositories contain all project files, code history, and can have multiple collaborators.

Developers clone (download) a repository to their computer and work on a local version of the project. After working on code or developing new features on a local computer, developers push the changes to the same GitHub repository. Then, other developers or team members can download the version to their computer and stay synced with the project’s development.

![enter image description here](https://blogthinkbig.com/wp-content/uploads/sites/4/2020/04/GitHub-Mascot.jpg?fit=1500,1000)

## 5 GitHub benefits for developers

We know how GitHub differs from Git, but why should developers take the time to learn and use it? There are several benefits that I share with students on why they should use GitHub:

Collaboration — Collaboration with the developer community is one of GitHub’s most common uses, and it’s also one of its biggest benefits. It’s a way for teammates to work together and provide feedback. GitHub is also an ideal way for open-source projects to see continued collaboration from individual developers. In fact, GitHub is the largest open-source code repository on the internet! Version control and backup — Git is the version control software, while GitHub is the platform where projects using Git are stored and accessed. Essentially, GitHub acts as the cloud backup to a software project. Project management — GitHub can be used as a technical project management tool to track issues and bugs. This helps projects stay on schedule throughout the software development life cycle. Developer portfolio — GitHub offers a free web hosting service called GitHub Pages. It’s a straightforward way to turn a GitHub repository into an easy-to-review portfolio website. Networking — GitHub is a bit like a social networking website for developers. Users can follow each other, give project ratings, collaborate, communicate, and meet other developers from around the world. How to create a GitHub repository Now that you know the why of GitHub, I’ll get you started on the platform with this tutorial on creating your first repository. We’ll start by creating a local project to demonstrate how to upload it to GitHub.

#### Step 1: Create a new local Git repository

Open up your terminal and navigate to your projects folder, then run the following command to create a new project folder and navigate into it:

```
mkdir hello-world

cd hello-world
```

To initialize a new local Git repository we need to run the `git init` command:

#### git init

After you run that command, you should get feedback that an empty Git repository was initialized for your project.

#### Step 2: Adding a new file to our Git repository

Create a new file in your project folder, we will call our sample file `hello.js`

You can use the graphical interface of your operating system to create the file, or use the following terminal commands:

Windows Powershell: ni hello.js Bash (Mac/Linux) terminal: touch hello.js

You can open the hello.js file with your text editor, and write the following JavaScript code which prints Hello World! to the console:

```
console.log("Hello World!");
```

Save the file changes and switch back to your terminal window. Note: Make sure to use the `git status` command frequently when working with Git. It’s a great way to check the status of your project files and the whole repository.

Step 3: Making our initial commit to the local repository Run the following commands to track your files and make the initial commit in the local repository:

#### git add .

#### git commit -m "Initial commit"

When that’s done, it means that we successfully prepared our new local repository to be pushed to GitHub!

#### Step 4: Creating a new GitHub repository

To create a new GitHub repository, navigate to github.com and press the plus symbol in the top right corner, then select the ‘New repository‘ option, as shown in the screenshot here:

You can also navigate to the GitHub page for creating new repositories by visiting this link: https://github.com/new

On that page, we first need to specify a Repository name and an optional Description.

For the Repository name, we can specify the same project name (hello-world) as the local repository that we are using in our example. If you want, you can also write a Description of your repository, but you can also skip that field as we did in the screenshot above.

You can set your repository to be Public or Private. When uploading your code to a public directory, make sure it doesn’t contain any sensitive data not intended to share with others. When creating a Private repository, you’ll manually choose who can access the new repository.

#### Step 5: Pushing our code to the GitHub repository

After the last step, you’ll be sent to the starting page of your new GitHub repository, which looks like this:

Since we’ve already created our Git repo locally, we’ll focus on the “…or push an existing repository from the command line” section of the page.

(Note: If we didn’t already have a local repository created, then we would follow the first set of commands to create a local repository from the remote GitHub one that was just created.)

The git remote add origin command will associate our local repository with the remote GitHub repository that we just created. We’re essentially telling your Git repo that we have a URL we want it to know about, and we give it the name “origin.” You do not have to name the remote “origin” but it is standard if you only have a single remote.

The git push command then pushes our local Git repository code to the remote GitHub repository.

Now, switch back to your local terminal and run the specified commands from your project folder:

```
git remote add origin <https://github.com/><your-username>/<your-repo-name>.gitgit push -u origin master
```

When you run the git push command you’ll be prompted to enter your GitHub username and password, to log in to your GitHub account from the terminal.

After the repository is pushed, navigate back to your GitHub account page or the repository link and refresh it: https://github.com/`<your-username>`/`<your-repo-name>`

Now, you can use that link to share your project repository with other people!

Anyone can click on the hello.js file to see the contents of our project files. Also, other developers can clone or download the remote repository to their local computer by clicking on the green button highlighted in the screenshot. Other data, including past commits, existing branches, etc. will be visible from the repository.
