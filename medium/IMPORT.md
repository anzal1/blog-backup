# Medium migration checklist

Medium stopped issuing API tokens on **2025-01-01**, so these cannot be
pushed programmatically. Two working paths, in order of preference:

**A. Import Story (recommended)** — open <https://medium.com/p/import> and
paste the post URL from the table below (the importer has no documented
query-string prefill, so this stays a copy-paste step). Medium pulls the
text and images and sets
`rel=canonical` back to Hashnode automatically, so you keep SEO credit and
avoid a duplicate-content penalty.

**B. Paste rendered HTML (fallback)** — if an import fails or mangles code
blocks, open the matching file in `medium/html/`, select all, copy, and paste
into a fresh Medium draft. Then set the canonical URL by hand under
*⋯ → More settings → Advanced settings → Canonical link*.

> **Order matters:** import into Medium *before* you take the Hashnode posts
> down. The importer fetches the live URL — once it 404s, only path B works.

Tags: Medium allows a maximum of 5 per story.

| ✓ | Date | Post | URL to paste into the importer | Paste fallback | Suggested tags |
| --- | --- | --- | --- | --- | --- |
| [ ] | 2026-04-15 | [Your Wiki Doesn't Know What It Doesn't Know](https://anzal.hashnode.dev/your-wiki-doesn-t-know-what-it-doesn-t-know) | `https://anzal.hashnode.dev/your-wiki-doesn-t-know-what-it-doesn-t-know` | `html/your-wiki-doesn-t-know-what-it-doesn-t-know.html` | llm, Wikipedia, AI, knowledge, software development |
| [ ] | 2026-02-15 | [The Authentication Gap That Every AI Agent Lives In](https://anzal.hashnode.dev/the-authentication-gap-that-every-ai-agent-lives-in) | `https://anzal.hashnode.dev/the-authentication-gap-that-every-ai-agent-lives-in` | `html/the-authentication-gap-that-every-ai-agent-lives-in.html` | AI, agentic AI, authentication, authorization, Computer Science |
| [ ] | 2026-02-06 | [Building Production-Grade Voice AI: The Pain Points Nobody Talks About](https://anzal.hashnode.dev/building-production-grade-voice-ai-the-pain-points-nobody-talks-about) | `https://anzal.hashnode.dev/building-production-grade-voice-ai-the-pain-points-nobody-talks-about` | `html/building-production-grade-voice-ai-the-pain-points-nobody-talks-about.html` | voice ai, AI, llm, agentic AI, RAG |
| [ ] | 2026-01-10 | [UnClaude: Building an Open-Source AI Engineer with No Model Lock-In](https://anzal.hashnode.dev/unclaude-building-an-open-source-ai-engineer-with-no-model-lock-in) | `https://anzal.hashnode.dev/unclaude-building-an-open-source-ai-engineer-with-no-model-lock-in` | `html/unclaude-building-an-open-source-ai-engineer-with-no-model-lock-in.html` | AI, claude.ai, automation, Web Development |
| [ ] | 2025-10-04 | [Architecting an AI Frontend Engineer: A Deep Dive into Recursive Code Generation](https://anzal.hashnode.dev/architecting-an-ai-frontend-engineer-a-deep-dive-into-recursive-code-generation) | `https://anzal.hashnode.dev/architecting-an-ai-frontend-engineer-a-deep-dive-into-recursive-code-generation` | `html/architecting-an-ai-frontend-engineer-a-deep-dive-into-recursive-code-generation.html` | React, AI, llm, agentic AI, Python |
| [ ] | 2025-07-12 | [Stop Applying for Jobs Manually: Build an AI Agent That Does It for You](https://anzal.hashnode.dev/stop-applying-for-jobs-manually-build-an-ai-agent-that-does-it-for-you) | `https://anzal.hashnode.dev/stop-applying-for-jobs-manually-build-an-ai-agent-that-does-it-for-you` | `html/stop-applying-for-jobs-manually-build-an-ai-agent-that-does-it-for-you.html` | software development, AI, automation, Python, jobs |
| [ ] | 2025-07-08 | [Building a High-Performance Graph: From SVG Hell to Canvas Heaven](https://anzal.hashnode.dev/building-a-high-performance-graph-from-svg-hell-to-canvas-heaven) | `https://anzal.hashnode.dev/building-a-high-performance-graph-from-svg-hell-to-canvas-heaven` | `html/building-a-high-performance-graph-from-svg-hell-to-canvas-heaven.html` | React, Browsers, Rendering, optimization, canvas |
| [ ] | 2025-03-13 | [Lynx vs. React Native: A Comprehensive Comparison](https://anzal.hashnode.dev/lynx-vs-react-native-a-comprehensive-comparison) | `https://anzal.hashnode.dev/lynx-vs-react-native-a-comprehensive-comparison` | `html/lynx-vs-react-native-a-comprehensive-comparison.html` | React, React Native, Android, iOS, Web Development |
| [ ] | 2024-09-15 | [A Beginner’s Guide to RTSP Streaming with WebSockets Using Node.js and FFmpeg](https://anzal.hashnode.dev/a-beginners-guide-to-rtsp-streaming-with-websockets-using-nodejs-and-ffmpeg) | `https://anzal.hashnode.dev/a-beginners-guide-to-rtsp-streaming-with-websockets-using-nodejs-and-ffmpeg` | `html/a-beginners-guide-to-rtsp-streaming-with-websockets-using-nodejs-and-ffmpeg.html` | Node.js, streaming, video, FFmpeg, Programming Blogs |
| [ ] | 2024-05-01 | [Coinbase Interview Experience [SDE-1 Remote]](https://anzal.hashnode.dev/coinbase-interview-experience-sde-1-remote) | `https://anzal.hashnode.dev/coinbase-interview-experience-sde-1-remote` | `html/coinbase-interview-experience-sde-1-remote.html` | software development, software architecture, Web Development, DSA, remote |
| [ ] | 2024-04-16 | [Zomato SDE Interview Experience](https://anzal.hashnode.dev/zomato-sde-interview-experience) | `https://anzal.hashnode.dev/zomato-sde-interview-experience` | `html/zomato-sde-interview-experience.html` | interview, software development, technology, Software Engineering, Web Development |
| [ ] | 2023-10-16 | [A Deep Dive into Retryable Jobs with BullMQ](https://anzal.hashnode.dev/a-deep-dive-into-retryable-jobs-with-bullmq) | `https://anzal.hashnode.dev/a-deep-dive-into-retryable-jobs-with-bullmq` | `html/a-deep-dive-into-retryable-jobs-with-bullmq.html` | Web Development, Node.js, server, JavaScript, TypeScript |
| [ ] | 2023-06-07 | [Monerepo Architecture with Nx and Next.js](https://anzal.hashnode.dev/monerepo-architecture-with-nx-and-nextjs) | `https://anzal.hashnode.dev/monerepo-architecture-with-nx-and-nextjs` | `html/monerepo-architecture-with-nx-and-nextjs.html` | newbie, Web Development, Next.js, Developer, webdev |
| [ ] | 2023-05-28 | [Embracing Failure: A Journey of Growth and Resilience](https://anzal.hashnode.dev/embracing-failure-a-journey-of-growth-and-resilience) | `https://anzal.hashnode.dev/embracing-failure-a-journey-of-growth-and-resilience` | `html/embracing-failure-a-journey-of-growth-and-resilience.html` | software development, Web Development, newbie, #codenewbies, Stress, |
| [ ] | 2023-04-18 | [Freelancing, a deception, or a magic wand.](https://anzal.hashnode.dev/freelancing-a-deception-or-a-magic-wand) | `https://anzal.hashnode.dev/freelancing-a-deception-or-a-magic-wand` | `html/freelancing-a-deception-or-a-magic-wand.html` | Freelancing, coding, Web Development, news, Developer |
| [ ] | 2023-03-08 | [Let's Get Rusty](https://anzal.hashnode.dev/lets-get-rusty) | `https://anzal.hashnode.dev/lets-get-rusty` | `html/lets-get-rusty.html` | Rust, Programming Blogs, coding, technology, Web Development |
| [ ] | 2023-01-28 | [NEO4j , A Modern day ninja.](https://anzal.hashnode.dev/neo4j-a-modern-day-ninja) | `https://anzal.hashnode.dev/neo4j-a-modern-day-ninja` | `html/neo4j-a-modern-day-ninja.html` | Databases, Beginner Developers, technology, Web Development, webdev |
| [ ] | 2023-01-26 | [Why you need to learn PHP](https://anzal.hashnode.dev/why-you-need-to-learn-php) | `https://anzal.hashnode.dev/why-you-need-to-learn-php` | `html/why-you-need-to-learn-php.html` | PHP, Beginner Developers, Web Development, Developer, languages |
| [ ] | 2023-01-26 | [My work from home workstation](https://anzal.hashnode.dev/my-work-from-home-workstation) | `https://anzal.hashnode.dev/my-work-from-home-workstation` | `html/my-work-from-home-workstation.html` | workathome, Beginner Developers, layoff, HTML5, news |
| [ ] | 2023-01-26 | [Github Repository Controls](https://anzal.hashnode.dev/github-repository-controls) | `https://anzal.hashnode.dev/github-repository-controls` | `html/github-repository-controls.html` | GitHub, Beginner Developers, start, news, github-actions |
| [ ] | 2023-01-26 | [Virtual Assistant , What ,When and how.](https://anzal.hashnode.dev/virtual-assistant-what-when-and-how) | `https://anzal.hashnode.dev/virtual-assistant-what-when-and-how` | `html/virtual-assistant-what-when-and-how.html` | virtual assistant, newbie, technology, Amazon |
| [ ] | 2023-01-26 | [What you need to know about programming.](https://anzal.hashnode.dev/what-you-need-to-know-about-programming) | `https://anzal.hashnode.dev/what-you-need-to-know-about-programming` | `html/what-you-need-to-know-about-programming.html` | Programming Blogs, Beginner Developers, Programming Tips, C++, Python |
| [ ] | 2023-01-26 | [Artificial Intelligence and Robotics In A Nutshell](https://anzal.hashnode.dev/artificial-intelligence-and-robotics-in-a-nutshell) | `https://anzal.hashnode.dev/artificial-intelligence-and-robotics-in-a-nutshell` | `html/artificial-intelligence-and-robotics-in-a-nutshell.html` | AI, chatgpt, Machine Learning, Computer Science, Artificial Intelligence |
