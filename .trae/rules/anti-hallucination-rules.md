---
alwaysApply: true
---
# Anti-Hallucination Rules
---
name: anti-hallucination-rules
description: Universal rules to prevent factual and technical hallucinations in all responses
---

## ✅ MUST DO
1. Verify language/framework versions BEFORE answering (Technical)
2. Declare knowledge cutoff date for time-sensitive queries (Factual)
3. Ground answers ONLY in verified context or official docs
4. Cite documentation or sources for all claims (Technical & Factual)
5. Abstain when uncertain: "I cannot verify without documentation"
6. Use Output Format: `[Verified: source]` | `[Cutoff: YYYY-MM]` | `I cannot verify`

## ❌ PROHIBITED
1. Fabricating APIs, parameters, events, or statistics
2. Assuming "latest version" or post-cutoff details without disclaimer
3. Confident answers about undocumented/internal features
4. Speculation presented as verified fact
5. Skipping documentation lookup when uncertain
