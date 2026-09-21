---
id: manifest-keys
title: Manifest keys and what install does to them
summary: >
  Each manifest key has its own install semantics, and an absent key is not the
  same as an empty one — omitting schedules leaves them alone, while declaring
  an empty list deletes every one. Scalars upsert on every install; runtime
  state must never be declared there.
concepts: [scalar-tiers, merge-policy, app-bundle]
applies_to: [cli, mcp, human]
source: [ParsedTemplateConfig, ChannelTemplateInstaller]
---

Every manifest key is optional, and each one has its own install semantics.
Getting this wrong is how a live channel's state gets wiped, so it is worth
reading once in full.

| Key | What install does |
|---|---|
| `tables` | additive reconcile — columns added and attributes fixed, never dropped or renamed |
| `channel_parameters` | upsert, types preserved; read as `$channel.<name>` |
| `scalars` | **upsert on every install** |
| `default_scalars` | **write once**, on first install only |
| `schedules` | **replace wholesale** |
| `webhooks` | create if missing; never updated, never deleted |
| `triggers`, `connections`, `documents`, `status_kinds` | replace |
| `app_type` | sets the channel's app |

## An absent key is not an empty one

This rule runs through every row above and it is the one to internalise:

- **Omitting** a key leaves whatever the channel has alone.
- **Declaring it empty** means "replace with nothing."

So `schedules: []` deletes every schedule on the channel. Omitting `schedules:`
deletes none. The same holds for connections, documents and status kinds.

## Two specific traps

**An untyped bundle clears `app_type`.** A manifest with no `app_type:` strips
whatever the channel had, which changes the client's entire interface. Never
install an untyped bundle into a channel running a real app.

**Table changes are additive, so a rename is not a rename.** The reconcile adds
the new column and orphans the old one, with the data still in the old. Renaming
a column means renaming every write site too, and only reading a row back
afterwards will tell you that you missed one.
