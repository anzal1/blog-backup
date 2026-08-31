---
title: "Architecting an AI Frontend Engineer: A Deep Dive into Recursive Code Generation"
slug: "architecting-an-ai-frontend-engineer-a-deep-dive-into-recursive-code-generation"
date: "2025-10-04T11:57:45+00:00"
author: "Anzal Husain Abidi"
description: "The holy grail for many developers is to automate the mundane. We build CLIs, write scripts, and create boilerplate templates, all in service of spending more time on the creative, complex problems. But what if we could push that automation to its lo..."
cover: "https://cdn.hashnode.com/res/hashnode/image/upload/v1759578985136/bc9baa16-9979-4a9f-a27d-b892a3a5f4d3.png"
tags:
  - "React"
  - "AI"
  - "llm"
  - "agentic AI"
  - "Python"
canonical_url: "https://anzal.hashnode.dev/architecting-an-ai-frontend-engineer-a-deep-dive-into-recursive-code-generation"
source: "hashnode"
---

![Architecting an AI Frontend Engineer: A Deep Dive into Recursive Code Generation](https://cdn.hashnode.com/res/hashnode/image/upload/v1759578985136/bc9baa16-9979-4a9f-a27d-b892a3a5f4d3.png)

The holy grail for many developers is to automate the mundane. We build CLIs, write scripts, and create boilerplate templates, all in service of spending more time on the creative, complex problems. But what if we could push that automation to its logical extreme? What if we could describe a UI in plain English and have an AI agent build it, component by component, dependency by dependency?

This post is the technical deep dive into that very project. We'll walk through the creation of a context-aware, recursive AI agent designed to build a fully functional frontend. Its entire workflow is based on cloning a specific Vite + React starter template—in this case, the one found at `https://github.com/anzal1/junior-frontend-developer`—and then intelligently modifying it based on a user's prompt. This isn't just about generating code; it's about creating a system that understands a project's structure, manages its dependencies, and orchestrates a series of complex tasks—a true digital assistant.

We'll dissect the architecture, explore the critical (and often hilarious) bugs we encountered, and share the key principles that made the system actually work. This isn't just a story; it's a technical blueprint for building your own autonomous development agents.

### Part 1: The Core Architecture - A Society of Specialists

A common first instinct when building with LLMs is to create a single, massive prompt that tells one AI to do everything. This is a trap. A monolithic prompt is brittle, impossible to debug, and prone to hallucinations. Asking a single agent to "build a login page" might result in it hallucinating file creation, forgetting to install dependencies, and writing buggy code with mixed conventions all at once. A far more robust approach is a **multi-agent system**, where each agent is a specialist with a single, well-defined responsibility, akin to a well-organized software team.

Our system consists of a team of four specialist agents, orchestrated by a central Coordinator.

- **The Coordinator 🧠:** The project manager. Written in deterministic Python, it's the "adult in the room." It maintains the task queue, delegates work to the appropriate agent, and ensures the workflow progresses logically. It never talks to the LLM directly, providing a crucial layer of reliable control over the creative but sometimes unpredictable agents.
- **The Planner Agent 🏛️:** The System Architect. Its only job is to translate the user's high-level request into a structured JSON plan. This is the most creative agent, responsible for the initial vision. It doesn't write a line of code; it thinks about structure, dependencies, and the components needed to bring the user's idea to life. Its output is the foundational blueprint for the entire operation.
- **The Dependency Agent 📦:** The DevOps Specialist. It's an expert in package managers, a supply chain manager for our code. Given a list of dependencies, its only task is to generate and execute the correct `pnpm` or `npx` commands. It understands the subtle but critical difference between adding a library from npm and scaffolding a component from the shadcn-ui CLI.
- **The Component Agent 🧑‍💻:** The Senior Developer. This is the workhorse, the focused craftsman. It receives a single, specific task—"create this component with these features"—and its only job is to write the corresponding production-ready TSX code. It doesn't need to know about the overall project plan; it just executes its current ticket with precision.

This separation of concerns is the single most important architectural decision. It allows us to write highly-focused, simple prompts for each agent, making their behavior more predictable and their failures easier to diagnose and fix.

### Part 2: The Communication Layer - Tool Calling is Non-Negotiable

For agents to affect the real world (i.e., our filesystem), they need tools. We can't rely on an agent to output raw code as a text string within a markdown block; this is unreliable and prone to formatting errors, conversational fluff, and incomplete snippets. We need it to reliably call a function that we've defined.

This is where **Tool Calling** (or Function Calling) comes in. It establishes a formal API contract between our Python code and the LLM. We define our tools—`write_react_component` and `execute_shell_command`—as JSON schemas and provide them to the LLM in the API call.

Here’s a simplified look at the API payload sent to OpenRouter when asking the Component Agent to create a file:

```python
{
  "model": "google/gemini-2.5-pro",
  "messages": [
    {
      "role": "system",
      "content": "You are a senior React developer... Your ONLY output must be a call to the `write_react_component` tool."
    },
    {
      "role": "user",
      "content": "The project is at 'retro_feline'. Create the component: File Path: src/App.tsx, Description: The root component..."
    }
  ],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "write_react_component",
        "description": "Writes or overwrites a React component file...",
        "parameters": {
          "type": "object",
          "properties": {
            "file_path": { "type": "string" },
            "code": { "type": "string" },
            "project_path": { "type": "string" }
          },
          "required": ["file_path", "code", "project_path"]
        }
      }
    }
  ]
}
```

When the LLM responds, it won't just give us text. It will give us a structured `tool_calls` object, which our `BaseAgent` class can then parse and execute. This makes the agent's actions explicit, auditable, and far less prone to error.

```python
# Simplified logic within our BaseAgent's execute method
response_message = response['choices'][0]['message']
tool_calls = response_message.get("tool_calls")

if tool_calls:
    for tool_call in tool_calls:
        tool_name = tool_call['function']['name']
        tool_function = self.available_tools.get(tool_name)
        tool_args = json.loads(tool_call['function']['arguments'])

        # Execute the real Python function
        result = tool_function(**tool_args)
```

This request-execute loop is the fundamental heartbeat of any autonomous agent system, transforming the LLM from a passive text generator into an active participant in the software development process.

### Part 3: The Recursive Engine - A Humble Task Queue

The term "recursive" sounds complex, but our implementation is beautifully simple: a **First-In, First-Out (FIFO) task queue**, managed by the Python `collections.deque`. This approach elegantly avoids asking the LLM to manage its own state or remember the next step in a complex sequence, which is notoriously unreliable.

The process is straightforward:

1. **Plan:** The `PlannerAgent` generates the master plan, a JSON object containing lists of dependencies and components to create.
2. **Enqueue:** The `Coordinator` iterates through this plan and populates the `deque` with discrete task objects. The queue might look like this: `[npm_task, shadcn_task, component_task_1, component_task_2]`.
3. **Process:** The `Coordinator` enters a `while self.task_queue:` loop. In each iteration, it pops the next task, determines its `type` (e.g., "npm_dependencies", "component"), and delegates it to the appropriate specialist agent. The agent's world is simple: it receives one job, executes it, and is done.

This architecture is powerful because it's **deterministic** and **observable**. The Python `Coordinator` is in full control of the workflow. We can inspect the task queue at any time to see the remaining work, and because each task is small and isolated, failures are contained and easier to debug.

### Part 4: A Journey of a Thousand Bugs - Lessons from the Trenches

Building this system was a constant battle against the delightful unpredictability of LLMs. Here are the key technical challenges we faced and how we solved them.

#### Lesson 1: The AI Lies. Trust, but Verify.

The first agent confidently reported "All files created!" but the project folder was empty. We saw perfect logs but no results. It was hallucinating tool calls.

- **The Fix:** We rewrote the prompts to be brutally direct ("**Your ONLY output must be a call to the tool**") and, crucially, lowered the API `temperature` to `0.1`. The temperature setting controls randomness; a high value encourages creativity, while a low value promotes precision and determinism. This change turned our "creative artist" into a "dutiful factory worker" who would follow instructions to the letter.

#### Lesson 2: Context is Everything. A Blind Agent is a Useless Agent.

Initially, the agent had no knowledge of the template it was using, leading to errors like trying to import a CSS file that didn't exist in that location. It was like giving a builder a hammer and telling them to build a house without showing them the plot of land.

- **The Fix:** We implemented a "context injection" pipeline. A new `template_context.md` file was created, acting as a "style guide" or "company handbook" for the AI, explicitly documenting the template's file structure and import conventions. The `Coordinator` now loads this file and prepends it to the system prompt of the agents. The agent now has the "manual" for the project, making its output dramatically more accurate.

#### Lesson 3: JSON is Merely a Suggestion to an LLM.

The AI would frequently return malformed JSON. Sometimes it would wrap it in ```` ```json ```` fences. Other times, it would generate JavaScript-style objects with numbered keys instead of a proper JSON array. This is maddening when the only error is a single missing comma in a 200-line JSON object.

- **The Fix:** We built a "sanitizer" in the `PlannerAgent` that runs before `json.loads()`. It strips markdown and, most importantly, checks if a value is a dictionary with numeric keys and converts it to a list: `list(plan["components"].values())`. This simple defensive coding against the AI's quirks saved hours of debugging.

#### Lesson 4: Decompose, Decompose, Decompose.

Our initial `DependencyAgent` was asked to "install all these dependencies," a mix of npm and shadcn packages. It suffered from cognitive load, would reliably install the npm packages, and then stop, forgetting about the shadcn components.

- **The Fix:** We re-architected. The `PlannerAgent` was updated to produce two distinct lists: `npm_dependencies` and `shadcn_dependencies`. The `Coordinator` then creates two separate tasks. The `DependencyAgent`'s job became trivial: it receives a list and a specific command to use. This offloaded the complex sequencing logic from the unreliable LLM to our reliable Python code.

### Part 5: The Grand Finale - `Open` and the Preview Link

The final touch was to automate the preview. `subprocess.run("pnpm run dev")` would hang the script, as it's a blocking call that waits for the process to finish. We turned to its non-blocking sibling, `subprocess.Popen`, to launch the Vite dev server in the background.

To prevent "zombie processes" that would keep running after the app closes, we used Python's `atexit` module to register a cleanup function that ensures the server is terminated when the main script exits.

```python
# In the Coordinator's __init__
import atexit
self.dev_server_process = None
atexit.register(self._cleanup_dev_server)

def _cleanup_dev_server(self):
    if self.dev_server_process:
        self.dev_server_process.terminate()
```
