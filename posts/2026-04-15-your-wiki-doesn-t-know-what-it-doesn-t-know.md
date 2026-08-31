---
title: "Your Wiki Doesn't Know What It Doesn't Know"
slug: "your-wiki-doesn-t-know-what-it-doesn-t-know"
date: "2026-04-15T06:06:07+00:00"
author: "Anzal Husain Abidi"
description: "Why every LLM-powered knowledge base is broken the same way — and what we built instead The Karpathy Moment On April 4, 2026, Andrej Karpathy published a gist describing a pattern: use an LLM to mai"
cover: "https://cdn.hashnode.com/uploads/covers/63d276afa763c508ab870f55/3792e842-e3dd-4002-83e9-b14a7b71c14d.png"
tags:
  - "llm"
  - "Wikipedia"
  - "AI"
  - "knowledge"
  - "software development"
canonical_url: "https://anzal.hashnode.dev/your-wiki-doesn-t-know-what-it-doesn-t-know"
source: "hashnode"
---

![Your Wiki Doesn't Know What It Doesn't Know](https://cdn.hashnode.com/uploads/covers/63d276afa763c508ab870f55/3792e842-e3dd-4002-83e9-b14a7b71c14d.png)

*Why every LLM-powered knowledge base is broken the same way — and what we built instead*

![Hero Image](https://res.cloudinary.com/dho3mopsg/image/upload/v1776182710/quicky-wiki-blog/hero-vangogh.jpg)

---

## The Karpathy Moment

On April 4, 2026, Andrej Karpathy published a [gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) describing a pattern: use an LLM to maintain a personal wiki from raw source documents. Within 48 hours: 5,000+ stars, 1,300+ forks, and a dozen implementations.

Everyone rushed to build it. We looked at what they all built — and noticed they all missed the same things.

---

## The Six Gaps Nobody Filled

Every implementation that appeared — MindOS, agent-wiki, obsidian-wiki, second-brain, cerefox, LLM-wiki — shares the same blind spots:

**1. Static snapshots.** The wiki is a pile of current-state markdown. You can't ask "what did I believe about X last month?" or "how has my thesis evolved?" Git blame shows file changes. It doesn't show *belief changes*.

**2. Binary confidence.** A fact is either in the wiki or it isn't. But some claims are backed by five peer-reviewed papers and others by a single tweet. There's no way to know which is which.

**3. No metabolism.** Once a page is written, it sits there forever. That competitive analysis from three months ago? Probably stale. That API reference from last week? Still fresh. Nothing models freshness or decay.

**4. No gap discovery.** Lint finds broken links. It doesn't find *blind spots*. If your wiki covers ML architectures but never mentions training data quality, no existing system will notice.

**5. No knowledge diffs.** When you ingest a new source, you get updated pages. You don't get "before this paper, you believed X; now the evidence suggests Y; these 3 claims are stronger, this 1 is weaker."

**6. Single output format.** Everything renders to markdown. But knowledge has many useful forms — flashcards, slide decks, interactive graphs, timelines, fine-tuning datasets.

These aren't edge cases. These are fundamental properties of how human knowledge actually works. And no one was building for them.

---

## The Core Thesis

![Knowledge Compiler](https://res.cloudinary.com/dho3mopsg/image/upload/v1776182713/quicky-wiki-blog/knowledge-compiler-vangogh.jpg)

> A wiki is not a document store. It's a **knowledge compiler** — a system that takes raw sources as input and produces *verified, temporally-aware, confidence-scored, interlinked knowledge* as output, compilable to any format.

That's the idea behind [Quicky Wiki](https://github.com/anzal1/quicky-wiki). An open-source, CLI-first tool that treats your knowledge the way a compiler treats code: with rigor, with type safety, and with the understanding that correctness is a spectrum, not a binary.

---

## How It Works

```
Source Document (PDF, URL, markdown, notes)
     ↓
LLM Extraction → Claims (atomic, verifiable, with confidence scores)
     ↓                               ↓
Knowledge Graph (SQLite)          Epistemic Events (temporal log)
     ↓
Compiled Outputs → Wiki pages, slides, flashcards, graph, timeline
     ↓
Dashboard (interactive visualization + chat)
```

You drop a document into `raw/`. The compiler breaks it into atomic *claims* — not paragraphs, not summaries, but individual verifiable statements. Each claim gets a confidence score based on source quality, corroboration, and recency. These claims link into a knowledge graph that tracks how they relate to each other.

```bash
npx quicky-wiki init --name "My Research"
qw ingest paper.pdf --type paper --quality peer-reviewed
qw ingest https://arxiv.org/abs/2401.12345
qw serve    # → http://localhost:3737
```

Three commands and you have a confidence-scored knowledge base with an interactive dashboard.

---

## Confidence Isn't a Feature. It's the Architecture.

![Confidence Scoring](https://res.cloudinary.com/dho3mopsg/image/upload/v1776182706/quicky-wiki-blog/confidence-vangogh.jpg)

Every claim in Quicky Wiki carries a confidence score from 0.0 to 1.0, computed from:

- **Source count** — More independent sources confirming a claim → higher confidence
- **Source quality** — A peer-reviewed paper weighs more than a blog post, which weighs more than a tweet
- **Recency** — Newer sources are weighted higher for fast-moving fields
- **Corroboration** — Do your sources agree or contradict?
- **Dependency depth** — If a claim depends on other claims, confidence compounds downward

This isn't decoration. It's the foundation. When you query your wiki, you can ask:

```bash
qw query --min-confidence 0.8 "quantum error correction"   # only high-confidence claims
qw query --contested "scaling laws"                         # where sources disagree
qw claims --weakest --limit 10                              # your shakiest beliefs
```

When a foundational claim gets weakened by new evidence, Quicky Wiki doesn't just update that one claim. It runs a **cascade** — tracing every downstream claim that depends on it and adjusting their confidence accordingly. One challenged assumption can ripple through your entire knowledge graph.

---

## Knowledge That Decays, Resurfaces, and Challenges Itself

![Metabolism](https://res.cloudinary.com/dho3mopsg/image/upload/v1776182715/quicky-wiki-blog/metabolism-vangogh.jpg)

We call it the **metabolism engine**. It's what keeps a knowledge base alive instead of slowly rotting.

**Decay.** Claims that haven't been reinforced by new sources gradually lose confidence. That competitive analysis from six months ago auto-flags as potentially stale. This isn't arbitrary — it models the real-world phenomenon that knowledge has a half-life.

**Resurfacing.** Like spaced repetition for your entire wiki. The system surfaces concepts you haven't engaged with recently: "You haven't revisited your notes on X in 45 days. 3 new sources have appeared since then."

**Red-teaming.** Periodic adversarial self-critique powered by the LLM: "What claims in this wiki would a domain expert challenge? What's the strongest counter-argument to your central thesis?"

```bash
qw metabolism --report        # full knowledge health report
qw metabolism --decay         # apply confidence decay
qw metabolism --resurface     # find stale claims worth revisiting
qw metabolism --redteam       # challenge your high-confidence claims
```

```
┌─────────────────────────────────────────────┐
│  KNOWLEDGE HEALTH REPORT                    │
├─────────────────────────────────────────────┤
│  Total claims: 847                          │
│  High confidence (>0.8): 312 (37%)          │
│  Medium (0.4-0.8): 419 (49%)               │
│  Low (<0.4): 116 (14%)                      │
│                                             │
│  ⚠️  Stale (>30 days, no reinforcement): 23 │
│  ⚡ Contested (sources disagree): 8          │
│  🔗 Cascade risk (depends on weak claims): 5│
│  🕳️  Gaps detected: 12                      │
└─────────────────────────────────────────────┘
```

No other LLM wiki does this. Most don't even have the concept.

---

## Differential Ingestion: See What Changed in Your Understanding

When you ingest a new source, the system doesn't silently update pages. It shows you a **knowledge diff** — exactly how your understanding shifted:

```
$ qw ingest paper-new-scaling-laws.pdf

📄 Ingested: "Scaling Laws Revisited" (Chen et al., 2026)

KNOWLEDGE DIFF:
━━━━━━━━━━━━━━
  REINFORCED (3 claims):
  ✅ "Loss scales as power law with compute" — confidence 0.72 → 0.88
  ✅ "Data quality matters more than quantity" — confidence 0.65 → 0.78

  CHALLENGED (1 claim):
  ⚠️  "Scaling laws plateau above 1T parameters"
      Your wiki says: plateau likely (confidence 0.60)
      This paper says: no plateau observed up to 10T
      New confidence: 0.35
      → 2 downstream claims affected

  NEW CONCEPTS (2):
  🆕 "Inference-time scaling" — new concept page created
  🆕 "Test-time compute" — linked to existing "inference optimization" page

  GAPS IDENTIFIED (1):
  🕳️  Paper references "mixture of experts efficiency" — no wiki page exists
```

Every ingestion is a learning event. And the system makes the learning visible.

---

## The Discovery Engine: What Should You Learn Next?

![Discovery](https://res.cloudinary.com/dho3mopsg/image/upload/v1776182708/quicky-wiki-blog/discovery-vangogh.jpg)

Most wikis wait passively for you to feed them. Quicky Wiki identifies what's missing and suggests where to look:

```bash
qw discover --mode gaps            # what's missing in your knowledge?
qw discover --mode horizon         # frontier topics you should explore
qw discover --mode bridges         # connections between distant concepts
qw discover --mode contradictions  # conflicting claims to resolve
```

**Gap analysis** finds blind spots: "Your wiki discusses concepts A, B, and D but never C, which connects them."

**Horizon scanning** looks ahead: "Based on your research interests, here are 5 recent papers you should consider ingesting."

**Bridge detection** finds cross-domain connections: "Your neuroscience notes and your ML notes both discuss attention mechanisms but never cross-reference."

---

## Compile Your Knowledge Into Anything

The wiki is the source of truth. But the output doesn't have to be markdown:

```bash
qw compile slides --topic "quantum error correction"    # Marp slide deck
qw compile anki --topic "ML scaling laws"               # Anki flashcards
qw compile graph --interactive                          # D3 knowledge graph
qw compile timeline --topic "quantum computing"         # temporal visualization
qw compile markdown                                     # Obsidian-compatible wiki
```

Same knowledge. Different lenses. A concept you explore as a graph, study as flashcards, and present as slides — all generated from the same underlying claims.

---

## Built for AI Agents

![MCP Server](https://res.cloudinary.com/dho3mopsg/image/upload/v1776182714/quicky-wiki-blog/mcp-vangogh.jpg)

Quicky Wiki includes a built-in [Model Context Protocol](https://modelcontextprotocol.io/) server. Point Claude Desktop, Cursor, or any MCP client at it:

```bash
qw mcp              # stdio mode (for Claude Desktop, etc.)
qw mcp --http       # HTTP mode for remote agents
```

Your AI agent can query the knowledge base, search across content with full-text search, list and filter entities, ingest new sources, and update metadata — all through the MCP protocol. The wiki becomes a first-class tool in any AI agent's toolkit.

You can also embed the engine directly in your Node.js application:

```javascript
import { KnowledgeStore, ingestSource, queryKnowledge } from "quicky-wiki";

const store = new KnowledgeStore("./data/graph.sqlite");
await ingestSource(store, "research-paper.pdf", { kind: "paper" });
const answer = await queryKnowledge(store, "What are the key findings?");
// → Answer with confidence scores and citations
```

No subprocess, no server, no MCP overhead. Just the knowledge compiler as a library.

---

## The Dashboard

The web dashboard gives you everything at a glance:

- **Knowledge Graph** — Interactive canvas visualization. Hover to see connections, click to explore.
- **Claims** — Every extracted claim with its confidence score, sources, and history.
- **Pages** — Wiki pages grouped by entity kind. Obsidian-style wikilinks work: `[[Page Title]]` is clickable.
- **Timeline** — Temporal view of how your knowledge has evolved.
- **Health** — Stale claims, contradictions, gaps, cascade risks.
- **Ask Wiki** — Chat with your knowledge base. Get answers with confidence scores and source citations.

---

## Why This Matters

We're in an era where LLMs can generate convincing text about anything. That's the problem — *everything sounds equally true*. There's no built-in mechanism to tell you "this fact is well-supported" vs. "this fact came from one source and contradicts newer evidence."

Quicky Wiki doesn't solve hallucination. What it does is make the *epistemic status* of your knowledge explicit. Every claim has a provenance trail. Every confidence score has a reason. When something decays, you know. When something contradicts, you see it. When there's a gap, the system finds it.

Knowledge management shouldn't be a filing system. It should be a living process — one that strengthens over time, weakens when evidence changes, and tells you honestly what it doesn't know.

---

## Get Started

```bash
npm install -g quicky-wiki
qw init --name "My Research"
qw ingest your-sources/
qw serve
```

Open `http://localhost:3737`. That's it.

The source is at [github.com/anzal1/quicky-wiki](https://github.com/anzal1/quicky-wiki). MIT licensed. Stars and contributions welcome.

---
