---
id: mcp/tools/make-connection
title: make_connection
order: 342
group: MCP
parent: mcp/tools
generated: scripts/sync-mcp.py
updated: 2026-11-11
summary: >
  Make one of a Routine's Connections: connect an account you have signed in
  to, or make the webhook another system posts to.
concepts: [connections]
used_with: [mcp/tools/get-run, mcp/tools/list-connections]
---

[writes] [destructive] [dry run]

```
make_connection(routine_id, connection, account=None, confirm=False, plan_id=None, only=False)
```

**Accounts.** For an email, calendar, files or documents (Notion) Connection, call it without account first. When you have exactly one account it accepts, still signed in and allowing everything the Connection needs, that call goes on with that account: it answers with the dry run for it (or, with `confirm=true`, connects it). Otherwise it lists your accounts that can serve it, each with whether its sign-in allows everything the Connection needs; then call it with account, an address or ID from that list, for the dry run of what it will connect, what it replaces and what runs after. With `confirm=true` it connects the account, gives the Routine the access it needs, and starts the Routine's own follow-up to a Connection changing if its template has one, all in one call. The answer is each Connection made, and a run reference for that follow-up, which [`get_run`](https://docs.popcorn.ai/mcp/tools/get-run.md) follows. Only your own accounts can be connected; a teammate connects theirs.

**Asking first.** A person asking to connect a Connection with their own account ("connect my Gmail to #intake") has agreed to it: call with `confirm=true` straight away, and tell them what was connected. Otherwise, with a person there, show the dry run first and confirm only once they agree: when they haven't named the Connection, when there is more than one account to choose from, or when it replaces an account already connected or a webhook. Replacing an account or a webhook is confirmed only with the dry run's `plan_id`; a confirm without one is refused and changes nothing.

**Several Connections.** Connecting an account to a Connection that has none also connects it to the Routine's other Connections of its provider that have none yet and that its sign-in allows (one Google account serves the inbox, calendar and Drive together); the dry run names each one, and the answer says which were connected. Pass `only=true` to connect the named Connection alone. Replacing a Connection's account changes no other.

**Google sign-in.** A Google sign-in is done from here: when you have no Google account that can serve, or yours is signed out or lacks access, the answer (or the refusal) carries a sign-in link, asking for everything the Routine's unconnected Google Connections need. Pass the link to the person as it is, and nothing else from it: it works once, within minutes, and only for the person who asked, who finishes it signed in to Popcorn in the browser it opens. Once they say they have, call `make_connection` again (without account, to see the account, then with it). When no link can be given here (a Routine's own agent in Popcorn never gets one), and for an account of another provider, a person signs in in Popcorn; the answer says where.

**Webhooks.** For a webhook Connection, call it without account: a dry run of the webhook it makes, and of the one it replaces if one serves it already, whose address then stops working. Replacing one needs an admin of the Routine, a workspace admin, or whoever made it. A webhook Connection that starts no particular work gets one more webhook per call until it has enough, and is never replaced here. With `confirm=true` it makes the webhook and answers with its address, once. The address is a credential: anyone who has it can post to the Routine. Give it only to whoever sets up the other system; nothing here shows it again. The Routine's own agent is never given it, since its answers reach the whole Routine: the answer says [secret] in its place, and the person reads it on the Connection's card in Popcorn.

**E-signature.** An e-signature Connection isn't made here: its keys are workspace secrets a workspace admin or owner saves in Popcorn, and the refusal names them. Never pass a key or a password to this tool.

**Who may call.** It takes `routine_id`, the Routine's ID, as every tool that writes does. Making a Connection needs workspace admin, or membership of the Routine, and an archived Routine can't be changed.

## Arguments

| Argument | Type | Notes |
|---|---|---|
| `routine_id` [required] | `str` | The Routine's ID (not its name). |
| `connection` [required] | `str` | The Connection's id or label, as [`list_connections`](https://docs.popcorn.ai/mcp/tools/list-connections.md) shows it. |
| `account` | `str` | Your account's address or ID, for an email, calendar, files or documents Connection. Omit it to list your accounts. |
| `confirm` | `bool` | true to make it: at once on the person's own request to connect it, otherwise after they agree to the dry run. Default `False`. |
| `plan_id` | `str` | The `plan_id` the dry run gave, with `confirm=true` and the same request. Required to replace an account a Connection already uses, or its webhook. A Routine's own agent in Popcorn must pass it, from a dry run in an earlier run; an assistant connected from outside Popcorn is given none and needn't, except for a replace. |
| `only` | `bool` | true to connect the account to this Connection alone, not to the Routine's other unconnected ones it can serve. Default `False`. |

**Example** — “Connect the adjusters' calendar account to #intake so it can book inspections.”

```text
→ make_connection(routine_id="c7d2…5b", connection="Adjuster calendar")

Routine: #intake (c7d2…5b)
- Adjuster calendar (calendar): NOT CONNECTED
  Without it: the automations that use it can't run; the rest of the Routine keeps working.
It needs an account that allows seeing and changing calendar events.
Your accounts that can serve it:
- adjusters@acme.example (google), id 9a3e…71: allows everything it needs
- dana.smith@gmail.com (google), id 1c7d…94: its sign-in doesn't allow seeing and changing calendar events; a person reconnects it in Popcorn to add that
To connect one, call make_connection again with account set to its address or id, for a dry run.
To connect an account not listed, a person signs in to it in Popcorn, in the browser: open #intake (https://app.popcorn.ai/ws/acme/conversation/c7d2…5b), then its settings, then Automations, then Connect on the Adjuster calendar card. That can't be done from here. Only your own accounts are listed; a teammate connects theirs.

→ make_connection(routine_id="c7d2…5b", connection="gcal", account="adjusters@acme.example")

Routine: #intake (c7d2…5b)
**Dry run.** Nothing was changed.

- Connection: Adjuster calendar (calendar)
- Account: adjusters@acme.example (google), yours
- Connects it as gcal
- Lets this Routine use it for seeing and changing calendar events
- Then starts the Routine's own follow-up to a Connection changing, which its template defines

Call again with `confirm=true` to connect adjusters@acme.example (google) as Adjuster calendar.

→ make_connection(routine_id="c7d2…5b", connection="gcal", account="adjusters@acme.example", confirm=true)

Routine: #intake (c7d2…5b)
Connected adjusters@acme.example (google) as Adjuster calendar.
- Bound: gcal
- Started the Routine's own follow-up to a Connection changing. Run: run_WzEs…; get_run with it shows how it went.
- Adjuster calendar (calendar): connected
  Uses: adjusters@acme.example (google), connected by Dana Smith
  Without it: the automations that use it can't run; the rest of the Routine keeps working.
```
