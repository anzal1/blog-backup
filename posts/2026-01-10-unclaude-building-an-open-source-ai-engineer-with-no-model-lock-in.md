---
title: "UnClaude: Building an Open-Source AI Engineer with No Model Lock-In"
slug: "unclaude-building-an-open-source-ai-engineer-with-no-model-lock-in"
date: "2026-01-10T14:58:12+00:00"
author: "Anzal Husain Abidi"
description: "I believe the future of software engineering isn't just \"AI-assisted\"—it’s agentic. We are moving away from simple chat boxes and toward agents that can plan, execute, and verify tasks autonomously. While the market is flooded with proprietary tools,..."
cover: "https://cdn.hashnode.com/res/hashnode/image/upload/v1768056976004/132e96c6-678c-47fa-9640-c6909e3cde45.jpeg"
tags:
  - "AI"
  - "claude.ai"
  - "automation"
  - "Web Development"
canonical_url: "https://anzal.hashnode.dev/unclaude-building-an-open-source-ai-engineer-with-no-model-lock-in"
source: "hashnode"
---

![UnClaude: Building an Open-Source AI Engineer with No Model Lock-In](https://cdn.hashnode.com/res/hashnode/image/upload/v1768056976004/132e96c6-678c-47fa-9640-c6909e3cde45.jpeg)

I believe the future of software engineering isn't just "AI-assisted"—it’s **agentic**. We are moving away from simple chat boxes and toward agents that can plan, execute, and verify tasks autonomously.

While the market is flooded with proprietary tools, I wanted to build something that prioritized two things: **total model flexibility** and **local control**.

That experiment became **UnClaude**.

---

## What is UnClaude?

UnClaude is a CLI-based autonomous pair programmer. It sits between you and your Large Language Model (LLM) of choice, providing the agent with a "body" to interact with your local environment through three core tools:

- 📂 **File System**: Permission-based reading and editing of your codebase.
- 💻 **Terminal**: The ability to run compilers, linters, and test suites securely.
- 🌐 **Browser**: Real-time verification of web applications to "see" the UI.

Because it runs locally, your code stays on your machine, and you maintain full oversight of every command the agent executes.

---

## The Core Principles

### 1. Model Independence (Break the Lock-in)

Different tasks require different "brains." UnClaude is built on top of `LiteLLM`, allowing you to hot-swap providers instantly. Need the 2M context window of **Gemini 2.5 Pro**? No problem. Prefer the logic of **GPT-4o** or the privacy of a local **Llama 3** via Ollama? UnClaude supports them all.

### 2. Autonomy via Feedback Loops ("Ralph Mode")

Writing code is the easy part; getting it to compile and pass CI/CD is where the time goes. UnClaude features **"Ralph Mode,"** a self-correcting loop. When the agent writes code, it doesn't just stop. It runs your test suite, analyzes the exit codes and error logs, and iteratively fixes its own mistakes until the tests pass.

### 3. Integrated Project Memory

An assistant is only as good as its context. UnClaude uses a local vector database to index your project and conversation history. This means the agent "remembers" your architectural patterns and previous instructions, saving you from having to repeat yourself in every new session.

---

## Why Open Source?

I’ve released UnClaude under the **Apache 2.0 license**. Developer tools should be transparent. By making it open source, you can inspect the prompts, modify the agent's logic, and build custom tools that fit your specific workflow.

---

## Try it Out

UnClaude is available now on PyPI. You can get up and running in seconds, or you can visit: [https://github.com/anzal1/unclaude](https://github.com/anzal1/unclaude)

```bash
pipx install unclaude
unclaude login
```
