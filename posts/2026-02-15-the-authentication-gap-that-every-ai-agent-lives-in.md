---
title: "The Authentication Gap That Every AI Agent Lives In"
slug: "the-authentication-gap-that-every-ai-agent-lives-in"
date: "2026-02-15T15:38:18+00:00"
author: "Anzal Husain Abidi"
description: "Why existing auth was never built for autonomous agents — and how we fixed it with open-source cryptography The Uncomfortable Truth Your AI agent is authenticating like it's 2009. Every day, millions of AI agents make HTTP requests on behalf of the h..."
cover: "https://cdn.hashnode.com/res/hashnode/image/upload/v1771169810948/3465544d-b695-41f1-939f-dbab319f43a3.jpeg"
tags:
  - "AI"
  - "agentic AI"
  - "authentication"
  - "authorization"
  - "Computer Science"
  - "Security"
  - "Artificial Intelligence"
canonical_url: "https://anzal.hashnode.dev/the-authentication-gap-that-every-ai-agent-lives-in"
source: "hashnode"
---

![The Authentication Gap That Every AI Agent Lives In](https://cdn.hashnode.com/res/hashnode/image/upload/v1771169810948/3465544d-b695-41f1-939f-dbab319f43a3.jpeg)

*Why existing auth was never built for autonomous agents — and how we fixed it with open-source cryptography*

## The Uncomfortable Truth

Your AI agent is authenticating like it's 2009.

Every day, millions of AI agents make HTTP requests on behalf of the humans who run them. They create pull requests. They read databases. They call third-party services. And every single time, they authenticate with the same mechanism a curl script would — a static API key or an OAuth token designed for a human clicking "Allow" in a browser.

This works. Until it doesn't.

---

## The Gap Nobody Talks About

![The Identity Gap](https://res.cloudinary.com/dho3mopsg/image/upload/v1771169540/pact-blog/identity-gap.jpg)

Here's what's broken — not in theory, but in production, right now:

**No provenance.** When an agent hits your API with a bearer token, you see the token. You don't see the human behind it. You don't see the chain of trust. If the agent goes rogue — context poisoned, prompt injected, session hijacked — the token still works.

**No scope boundaries.** A human gives their agent access to "the GitHub API." They mean "create PRs on this one repo." The token doesn't know that. It carries the full blast radius of every permission the human has.

**No accountability.** When something goes wrong — and it will — there's no audit trail that says "this specific agent, delegated by this specific human, with these specific permissions, signed this specific request at this specific time." There's a token in a log. Maybe.

**No identity.** The agent has no cryptographic existence. Clone its token, and nobody can tell you apart.

---

## Why Existing Solutions Don't Fit

![Broken Lock](https://res.cloudinary.com/dho3mopsg/image/upload/v1771169529/pact-blog/broken-auth.jpg)

We looked at everything:

→ **OAuth 2.0** — A delegation framework where the delegator is a browser redirect and the scope is a string the provider invented. Designed for users clicking buttons, not agents operating autonomously.

→ **API Keys** — Shared secrets with no provenance, no enforced expiry, and no capability narrowing. The skeleton key approach.

→ **mTLS** — Proves a machine, not a delegation chain. No concept of "who authorized this machine to do this specific thing."

→ **OIDC for Agents** — Adds agent claims to existing identity providers. Still centralized. Still requires token introspection endpoints.

None of them answer the three questions every provider should be asking:

1. **Which human authorized this agent?**
2. **What specifically is the agent allowed to do?**
3. **Can I verify all of this without calling anyone?**

---

## Enter Pact

![Pact Protocol](https://res.cloudinary.com/dho3mopsg/image/upload/v1771169544/pact-blog/pact-protocol.jpg)

Pact is a **protocol** — not a service, not a platform. Like HTTPS, but for agents proving who they are, who sent them, and what they're allowed to do.

**The core idea is simple:**

Humans sign cryptographic delegations to agents. Agents carry these delegation chains with every request. Providers verify everything locally — no token introspection, no authorization servers, no network calls. Just math.

---

## How It Works

![Architecture](https://res.cloudinary.com/dho3mopsg/image/upload/v1771169527/pact-blog/architecture.jpg)

The protocol has five primitives:

| Primitive | What It Does |
| --- | --- |
| **Identity** | Ed25519 keypair. ID = `sha256(public_key)`. No registration needed. |
| **Delegation** | Signed capability grant: human → agent, narrowing-only, with expiry |
| **Capability** | Machine-parseable permission: `resource:action,constraint=value` |
| **Request Signing** | Per-request Ed25519 signature over method + path + timestamp + body |
| **Verification** | Walk chain → check sigs → check caps → check freshness. All local. |

### The Flow

```
Human (Alice)
  │
  │  Signs delegation: "Agent X can do api:read, api:write for 1 hour"
  │
  ▼
Agent (carries chain)
  │
  │  Makes HTTP request, signs it with own key
  │  Attaches: identity + delegation chain + signature
  │
  ▼
Provider
  │
  │  Walks delegation chain (every signature valid?)
  │  Capabilities cover this endpoint?
  │  Request signature fresh?
  │  → All local. Zero network calls.
  │
  ▼
  Verified. ✓
```

---

## Capability Narrowing — The Key Insight

![Capability Narrowing](https://res.cloudinary.com/dho3mopsg/image/upload/v1771169532/pact-blog/capability-narrowing.jpg)

This is what makes Pact fundamentally different from scope-based auth.

Delegations are **narrowing-only**. A human can delegate `storage:*` to an agent. That agent can sub-delegate `storage:read` to a sub-agent. But the sub-agent can never escalate back to `storage:write`. It's mathematically enforced — not by policy, but by cryptographic signatures.

```
Human: storage:*
  └→ Agent A: storage:read, storage:write
       └→ Agent B: storage:read          ← Can narrow
       └→ Agent C: storage:delete        ← REJECTED (escalation)
```

Capabilities support glob patterns, numeric constraints, and hierarchical resources:

```
github:pr:create,repo=myorg/*           ← Only PRs in myorg repos
api:write,max_cost<100                  ← Spend limit
storage:read,path=/data/public/**       ← Path-scoped access
```

---

## Cross-Language Proof

We didn't just build a protocol spec. We built two complete implementations — **Go** and **Python** — and proved they work together.

A Python agent creates an Ed25519 keypair, obtains a delegation from a Go server, signs HTTP requests with the Python SDK, and the Go server verifies every signature. Different languages. Same bytes. Same math.

**The test:** 88 cross-language test vectors validating byte-level compatibility — seed derivation, canonical JSON, capability narrowing, content digests, delegation signatures.

**The demo:** A 7-step end-to-end flow:

1. ✓ Python agent creates identity
2. ✓ Obtains delegation from Go server
3. ✓ Authenticated read (api:read)
4. ✓ Authenticated write (api:write)
5. ✓ Correctly denied (lacks deploy:create)
6. ✓ Ephemeral session identity works
7. ✓ Sub-delegation (agent → sub-agent) works

---

## What Makes Pact Different

|  | OAuth 2.0 | API Keys | mTLS | **Pact** |
| --- | --- | --- | --- | --- |
| **Proves delegation chain** | No | No | No | **Yes** |
| **Capability narrowing** | Provider-defined | No | No | **Delegator-defined** |
| **Per-request signatures** | No (bearer) | No (shared secret) | Yes (TLS) | **Yes (app layer)** |
| **Offline verification** | No (introspection) | No (DB lookup) | Partial | **Fully local** |
| **Agent-native** | No | No | No | **Yes** |
| **Zero dependencies** | Auth server | Key store | CA | **Nothing** |

---

## The Technical Choices

**Ed25519 everywhere.** Fast, small signatures (64 bytes), deterministic, no random number generator needed during signing. The same algorithm Signal, SSH, and WireGuard use.

**Canonical JSON (RFC 8785).** Delegation payloads are serialized deterministically — sorted keys, no whitespace ambiguity. Same bytes in Go and Python. Same bytes on every platform.

**RFC 9421 signatures.** Request signatures cover method, path, authority, timestamp, and body digest. This isn't a custom scheme — it's the IETF standard for HTTP message signatures.

**Zero dependencies in Go.** The entire implementation uses only the Go standard library. No crypto imports beyond `crypto/ed25519`. No frameworks. No build complexity.

---

## Session Identity — Solving Agent Ephemerality

![Session Identity](https://res.cloudinary.com/dho3mopsg/image/upload/v1771169548/pact-blog/sessions.jpg)

Agents are ephemeral. They spin up, do work, and disappear. But they need stable, verifiable identity during their lifetime.

Pact introduces **hierarchical session identity:**

```
Human (long-lived)
  └→ Root Agent (medium-lived, stored keypair)
       └→ Session Agent (ephemeral, in-memory only)
```

Session agents get their own Ed25519 keypair, a delegation from the root, and automatic key zeroization when the session ends. The provider still sees a clean delegation chain back to the human.

---

## Try It

Pact is open source. MIT licensed. Zero dependencies.

```bash
# Go
go get github.com/anzal1/pact

# Python
pip install pact-auth

# CLI
pact init --name alice --type human
pact delegate --to agent.pub --capabilities "api:read" --ttl 1h
```

The full spec, implementations, and cross-language demo are at [github.com/anzal1/pact](https://github.com/anzal1/pact).

---

## The Bigger Picture

AI agents are the fastest-growing category of API consumers. They're operating autonomously, at scale, with credentials designed for a different era.

The question isn't whether agent authentication needs to evolve. It's whether the evolution will be centralized — agents authenticating through platforms, gatekeepers, and introspection endpoints — or decentralized, where any agent can prove its authorization to any provider using nothing but cryptography.

Pact bets on the latter. No servers. No platforms. No trust assumptions. Just a keypair, a delegation chain, and a signature on every request.

---
