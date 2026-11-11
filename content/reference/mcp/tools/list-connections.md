---
id: mcp/tools/list-connections
title: list_connections
order: 328
group: MCP
parent: mcp/tools
generated: scripts/sync-mcp.py
updated: 2026-11-11
summary: >
  List the Connections a Routine needs: the accounts and other services its
  template works through.
concepts: [connections]
used_with: [mcp/tools/make-connection]
---

[read-only]

```
list_connections(routine)
```

For each, whether it is connected, whose account it uses, and what stops while it is missing.

A Connection whose account is connected but hasn't given the Routine all the access it needs counts as not connected. Whether an account has since been revoked isn't checked.

[`make_connection`](https://docs.popcorn.ai/mcp/tools/make-connection.md) makes one: from an account you have already signed in to, or its webhook. For a Google account not yet signed in to, `make_connection` can hand out a sign-in link for the person; any other account is signed in to by a person in Popcorn, in the browser, and the response says where.

Seeing a Routine's Connections needs workspace admin, or membership of the Routine. A Routine shared in from another workspace is refused: its Connections are made and shown there.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `routine` [required] | `str` | Routine name ("#intake") or ID. |

**Example** — “Why hasn't #intake booked any inspections?”

```text
→ list_connections(routine="#intake")

Routine: #intake (c7d2…5b)
3 Connections, 1 not connected:
- Claims inbox (email): connected
  Uses: claims@acme.example (google), connected by Dana Smith
  Without it: the Routine's automations are paused, and claim intake can't run.
- Adjuster calendar (calendar): NOT CONNECTED
  Without it: book inspection can't run; the rest of the Routine keeps working.
- Carrier portal (webhook): connected
  Uses: webhook carrier-portal
  Without it: the Routine's automations are paused, and nothing from the other system starts claim intake.
Whether a connected account has since been revoked or its sign-in has expired isn't checked here.
make_connection makes a Connection from an account the person has already signed in to, or makes its webhook. For a Google account not yet signed in to, or one whose sign-in lacks access, make_connection gives a sign-in link to pass on when it can. Any other account is signed in to in Popcorn, in the browser: open #intake (https://app.popcorn.ai/ws/acme/conversation/c7d2…5b), then its settings, then Automations, which lists its Connections.
```
