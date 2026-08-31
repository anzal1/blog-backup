---
title: "Stop Applying for Jobs Manually: Build an AI Agent That Does It for You"
slug: "stop-applying-for-jobs-manually-build-an-ai-agent-that-does-it-for-you"
date: "2025-07-12T12:34:16+00:00"
author: "Anzal Husain Abidi"
description: "Are you tired of the soul-crushing routine of job hunting? The endless cycle of finding a listing, filling out the same form fields, and uploading your resume for the hundredth time? It feels like a full-time job just to apply for a job. What if you ..."
cover: "https://cdn.hashnode.com/res/hashnode/image/upload/v1752323596756/f9171122-fbed-431e-9945-17a6926403d0.png"
tags:
  - "software development"
  - "AI"
  - "automation"
  - "Python"
  - "jobs"
canonical_url: "https://anzal.hashnode.dev/stop-applying-for-jobs-manually-build-an-ai-agent-that-does-it-for-you"
source: "hashnode"
---

![Stop Applying for Jobs Manually: Build an AI Agent That Does It for You](https://cdn.hashnode.com/res/hashnode/image/upload/v1752323596756/f9171122-fbed-431e-9945-17a6926403d0.png)

Are you tired of the soul-crushing routine of job hunting? The endless cycle of finding a listing, filling out the *same* form fields, and uploading your resume for the hundredth time? It feels like a full-time job just to apply for a job.

What if you could hand off that entire process to a smart AI agent? An assistant that opens your browser, searches for jobs on LinkedIn, intelligently fills out each application, and works 24/7 on your behalf.

This isn't a futuristic dream. It’s possible right now with a powerful open-source tool called [**Browser Use**](https://github.com/browser-use/web-ui). In this guide, I'll show you exactly how to build your own personal AI job-hunting assistant by teaching you how to write the perfect "master prompt" to command your agent.

Let's dive in.

### Part 1: Your Technical Toolkit & Setup

First, we need to get the `Browser Use` project set up on your computer. This part involves using the command line and requires that you have [**Git**](https://git-scm.com/) and [**Python**](https://www.python.org/downloads/) installed.

**Step 1: Clone the Project**

We need to download the project files from GitHub. Open your terminal and run these commands one by one:

Bash

```powershell
# Clone the repository for the web interface
git clone https://github.com/browser-use/web-ui.git

# Move into the new project folder
cd browser-use-web-ui
```

**Step 2: Create and Activate a Python Environment**

A virtual environment is like a clean, isolated workspace for our project's code.

Bash

```powershell
# Create the environment
python3 -m venv .venv

# Activate the environment (On Mac/Linux)
source .venv/bin/activate

# Or activate it on Windows
.venv\Scripts\activate
```

You'll know it's working when you see `(.venv)` at the start of your terminal prompt.

**Step 3: Install the Tools**

Now we install all the necessary packages and the browser automation framework, [**Playwright**](https://playwright.dev/).

Bash

```powershell
# Install all the required Python packages
pip install -r requirements.txt

# Install the browsers for the agent to control
playwright install
```

### Part 2: Giving Your Agent a Brain with AI

Our agent needs an AI model to think and follow instructions. We'll use the free tier of a powerful model through a service called [**OpenRouter**](https://openrouter.ai/).

**Step 4: Configure Your API Keys**

API keys are like secret passwords that let our script talk to the AI model.

1. In the project folder, find the file named `.env.example` and make a copy of it. Rename the copy to just `.env`.
2. Go to [**OpenRouter.ai**](https://openrouter.ai/models) and sign up.
3. Find a capable free model (like **DeepSeek Coder** or **Google's Gemma**).
4. Go to your **Keys** page, create a new key, name it, and copy the key itself.
5. Open your new `.env` file and paste in your key and the OpenRouter Base URL. It should look like this:

Code snippet

```xml
OPENAI_API_KEY="paste_your_secret_api_key_here"
OPENAI_BASE_URL="https://openrouter.ai/api/v1"
```

### Part 3: Launch and Test Run

Let's fire it up to make sure everything is connected correctly.

**Step 5: Launch the Web Interface**

In your terminal (with the `.venv` still active), run this command:

Bash

```powershell
python -m uvicorn main:app --reload
```

Your terminal will give you a local URL like `http://127.0.0.1:8000`. Copy it and open it in your browser.

**Step 6: Run Your First Test**

1. On the `Browser Use` page, click **"LM Settings"**.
2. For the **Model Name**, enter the name of the model you chose, like `deepseek/deepseek-coder`. Save it.
3. Go back to the **"Run Agent"** tab. There's a default test task already there.
4. Click **"Run Agent"**.

A new browser window should pop up and perform a quick Google search automatically. Success! You have a working AI agent ready for your commands.

### Part 4: The Core - Crafting the Perfect Prompt for Your Agent

This is where the magic happens. We will write a clear, step-by-step "master prompt" to command our agent. For complex prompts, using a powerful AI assistant like [**ChatGPT**](https://chatgpt.com/) can help you refine your logic and wording.

Here’s how to structure your prompt for the best results.

\1. Define the Goal and Starting Point

Start with a clear objective.

- **Goal:** My goal is to apply for jobs on LinkedIn.
- **Starting URL:** Start at this page: `https://www.linkedin.com/jobs/search/?keywords=Product%20Manager&location=Remote`

\2. Set the Rules of Engagement

Tell the agent exactly what to look for and what to avoid. This is crucial for getting relevant applications.

- **Inclusion Rules:**
  - The job title must include "Product Manager" or "Product Owner".
  - The location must be "Remote".
  - Only apply to jobs posted in the "Past week".
- **Exclusion Rules (Just as important!):**
  - Do NOT apply if the title includes "Senior", "Lead", or "Principal".
  - Do NOT apply to jobs from the companies "Meta" or "Google".

\3. Write the Step-by-Step Action Sequence

This is the main algorithm. Write it like you're explaining it to a person.

- **Action Plan:**
  1. Navigate to the Starting URL.
  2. Go through each job listing on the page one by one.
  3. For each job, check if it matches my Inclusion and Exclusion rules.
  4. If it is a match, click on the job listing.
  5. Click the "Easy Apply" button.
  6. The application form will now be open. Use the following information to fill it out:
     - My full name is: Jane Doe
     - My email is: jane.doe@email.com
     - My phone number is: 123-456-7890
     - My resume is located at: `C:\Users\JaneDoe\Documents\resume_v2.pdf`
  7. If you encounter a question like "Years of experience with SaaS products?", answer "5".
  8. After filling all required fields, click the button to "Review" and then "Submit application".
  9. Close the job tab and move to the next listing on the search results page.

**Putting It All Together**

Combine these sections into one big prompt inside the "Task Description" box in `Browser Use`. The more detailed you are, the better your agent will perform.

### Part 5: Unleash Your AI Job Hunter!

1. **Copy and paste your complete, detailed prompt** into the `Browser Use` interface.
2. Click **"Run Agent"**.

Now, sit back and watch. The browser window will spring to life, navigating, analyzing, and applying on your behalf, all based on the precise instructions you wrote. You've successfully delegated one of the most tedious tasks in modern life to your own personal AI agent.
