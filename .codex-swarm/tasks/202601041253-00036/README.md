---
id: "202601041253-00036"
title: "Harden agentctl depends_on parsing"
status: "DONE"
priority: "med"
owner: "DOCS"
depends_on: []
tags: ["agentctl", "tasks"]
commit: { hash: "0b222dfbd26ac511935b4a3026686a4685280d4f", message: "🔧 T-102 harden depends_on parsing" }
description: "Ignore literal '[]' and empty strings in --depends-on to avoid invalid dependencies in tasks.json, and update docs to prevent misuse."
---
