---
id: strings-yaml
title: The Bundle's strings.yaml
order: 8
group: What a Bundle holds
summary: >
  `strings.yaml` holds the words Popcorn shows for a Routine Template,
  under a locale such as `en:`: the Routine's noun, the new-Routine dialog,
  the setup checklist (`today.onboarding_steps`), Reference cards
  (`documents.<id>.*`), promoted settings (`settings.fields`) and the
  automations list. Changing it needs a Copy; nothing in it changes what a
  Flow does.
lede: >
  The file that holds a template's words: what Popcorn calls its Routines,
  its setup checklist, its Reference cards and its settings' labels.
concepts: [setup-checklist, scalar-tiers, app-bundle, manifest-keys]
---

An [App Bundle](https://docs.popcorn.ai/app-bundle.md)'s `strings.yaml`
holds the words Popcorn shows for its template: what a
[Routine](https://docs.popcorn.ai/routines.md) made from it is called, the
steps of its setup checklist, what its
[References](https://docs.popcorn.ai/reference-documents.md) are for and
how its settings are labelled. This page lists every key the
[Questionnaire](https://docs.popcorn.ai/questionnaire-template.md)
template's file uses, with its value, and where it shows. The words are
the template's, so changing one needs a
[Copy](https://docs.popcorn.ai/copying-a-template.md).

> "Show me #team-offsite's strings.yaml."

> [!TIP] MCP tool call
> Your assistant calls `read_routine_file` for `strings.yaml`.

## How the file is read

The top-level keys are locales, and every other key sits under one.
Questionnaire writes only `en:`, the default. A section for another
locale, such as `es-mx:`, is kept beside it, and Popcorn shows each key in
the best match for a person's locale: the exact tag, then its language,
then `en`. A top-level key that isn't shaped like a locale tag is refused,
which catches a file that leaves the locale out.

Nested keys are read as one dotted path, so `today:` then
`onboarding_intro:` is the key `today.onboarding_intro`. A list, such as
the setup checklist, is kept whole as one value. Every key is stored on
the Routine under the template's `app_type` from the
[Manifest](https://docs.popcorn.ai/manifest-keys.md), so a `strings.yaml`
needs one. A `copy:<app_type>.<key>` entry under the Manifest's `scalars:`
replaces the same key from `strings.yaml`.

A `{name}` in a value is filled in only where the key below says so.
Elsewhere it is text, as in the setup checklist's `{reply_by}`.

## The Routine's words

```yaml title="strings.yaml"
en:
  project:
    noun: questionnaire
  new_project:
    name_placeholder: e.g. Supplier check-ins
    subtitle: >-
      Connect Gmail and add your questions, then add the recipients to ask.
```

| Key | Where it shows |
|---|---|
| `project.noun` | What Popcorn calls one Routine made from the template, lowercase: "Name your questionnaire" when a Routine is created, the search box and menu that list them, and the warning before disconnecting an account |
| `new_project.subtitle` | Under "Name your questionnaire" when a Routine is created |
| `new_project.name_placeholder` | The empty name box when a Routine is created |

## The setup checklist

```yaml title="strings.yaml"
en:
  today:
    onboarding_intro: >-
      Connect the Gmail account to send from, add your questionnaire and set
      the date to reply by. Then add a recipient, and I'll email them your questions and follow up
      until they've answered.
    progress_summary: "{done} of {total} done"
    progress_icon: box
    waiting_title: You're all set
    waiting_body: >-
      Add a recipient by asking me, for example "Send our questionnaire to
      jane@example.com". I check for new recipients and replies every fifteen
      minutes.
    onboarding_steps:
      # … three steps: connect_inbox, questionnaire, reply_by
```

| Key | Where it shows |
|---|---|
| `today.onboarding_steps` | The setup checklist: Popcorn's checklist on the Routine's Today tab, and what an assistant reads. Every step key is in [Give a template a setup checklist](https://docs.popcorn.ai/setup-checklist.md) |
| `today.onboarding_intro` | Above the checklist on the Today tab |
| `today.progress_summary` | The checklist's progress line in the Popcorn iOS app; `{done}` and `{total}` are filled in with the steps done and the steps listed |
| `today.waiting_title`, `today.waiting_body` | The screen the Popcorn iOS app shows once setup is finished |
| `today.progress_icon` | `box` or `users`; nothing shows it |

## Reference copy

```yaml title="strings.yaml"
en:
  documents:
    questionnaire:
      title: Questionnaire
      body: >-
        The questions every recipient is asked, and the email's subject,
        opening and closing around them.
      replace_confirm: >-
        Replacing this changes the questions from the next pass on, for
        recipients still waiting as well as new ones. Answers already
        recorded stay on their rows.
```

The `<id>` in `documents.<id>` is the id of the Reference's entry under
`documents:` in the Manifest, `questionnaire` here.

| Key | Where it shows |
|---|---|
| `documents.<id>.title` | The Reference's card in Popcorn, and its name when an assistant lists the Routine's References |
| `documents.<id>.body` | What the card, and that listing, say the Reference is used for |
| `documents.<id>.replace_confirm` | The confirmation Popcorn shows before Replace on the card; an assistant replacing it shows its own |

When the file has no `title` or `body` for a Reference, an assistant
listing the References uses the `title` and `used_for` of its entry in the
Manifest instead: see
[Manifest keys](https://docs.popcorn.ai/manifest-keys.md#declaring-references).

> "Which References does #team-offsite use?"

> [!TIP] MCP tool call
> Your assistant calls `list_references`.

## Promoted settings

```yaml title="strings.yaml"
en:
  settings:
    fields:
      - key: popcorn.email_send_mode
        label: Email sending
        input: mode
        description: >-
          Off asks nobody and follows nobody up, though replies are still
          read; Draft leaves each first email in Gmail's Drafts for a
          person to send, and follows nobody up; Send emails each
          recipient and follows up. A new Routine starts on Send.
        options:
          - value: "off"
            label: "Off"
          - value: draft
            label: Draft
          - value: send
            label: Send
            note: Real emails are sent to recipients from the connected Gmail.
```

`settings.fields` puts a switch in the Routine's settings with a label,
a description and labelled options; a `note` on an option is a warning
shown before the switch is set to it. Which switches to promote, and how
a Scalar becomes a setting, is in
[Scalar tiers and Routine Settings](https://docs.popcorn.ai/scalar-tiers.md).

A template that reads `popcorn.email_send_mode` without promoting it
still offers it: the Routine Settings tools show the platform's words for
it, *Email sending* with the options Off, Draft and Send, and on Send the
note "Real emails are sent from the connected inbox." A promoted entry
replaces all of them.

## Automations

```yaml title="strings.yaml"
en:
  today:
    automations:
      - id: ask
        name: Emails your questions to new recipients
        schedule: {flow: questionnaire_tick}
        required_connection: gmail
      - id: replies
        name: Records answers from replies
        schedule: {flow: questionnaire_tick}
        required_connection: gmail
      - id: follow_up
        name: Follows up on unanswered questions
        schedule: {flow: questionnaire_tick}
        required_connection: gmail
```

`today.automations` lists what the Routine does, in a person's words. In
Popcorn each entry shows under the Connection it names in
`required_connection`, with its `name` and `schedule`, and reads *Needs
connection* while that Connection isn't made. An entry can also name a
`required_document`, a Reference's id, and read *Needs document* while it
is missing; Questionnaire's don't.

`schedule` is text, or, as in Questionnaire, the
[Schedule](https://docs.popcorn.ai/schedules.md) it describes, named by
its Flow. Publish writes that Schedule's cadence in its place, from the Manifest's
`schedules:`: *Every 15 minutes* for Questionnaire's `interval: 900`,
*Every hour*, *Every day at 8:00 (America/Los_Angeles)* or *Every Monday
at 2:30*. A daily `deadline` or `window` Schedule runs at a minute inside
its hour, so it reads *Every day between 8:00 and 9:00*. A Copy that
changes the interval changes the line with it. Add
`slug:` beside `flow:` when the Flow has several Schedules. Publish
refuses a mapping that names no Schedule, or more than one, or a cron it
can't put in words, and the message names the entry. A line written as
text, such as `schedule: Every 15 minutes`, is shown as written, so a Copy
that changes the interval has to change the text too.

## Audit lines and the Connection subline

```yaml title="strings.yaml"
en:
  connections:
    email_subline: Sends your questions and reads the replies
  today:
    audit:
      row_created: Recipient added
      row_updated: Recipient updated
      row_deleted: Recipient removed
```

| Key | Where it shows |
|---|---|
| `today.audit.row_created`, `row_updated`, `row_deleted` | Meant as the line a Row's history shows for a change with no other description; Popcorn shows its own "Row created", "Row updated" and "Row deleted" there instead |
| `connections.email_subline` | Nothing shows it |
