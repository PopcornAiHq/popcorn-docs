# Information architecture

Written before there is anything to reorganise, because the failure mode is
that "concepts", "guides" and "reference" blur by the thirtieth page and
nobody can say which one a new file belongs in.

Each section below states its audience, what belongs in it, and the one test
that decides a borderline case.

## `content/concepts/`

**Audience:** an agent answering a question mid-task, and a person who has hit
something surprising.

**Contains:** one addressable idea per file. Platform vocabulary — the things
that are true before any bundle exists.

**The test:** *would this still be true if every app were deleted?* A fork line
would. What `retained` means would not — that belongs to the app that declares
it.

**Shape:** frontmatter with a `summary` under 400 characters, then a body of a
few hundred words. The summary is the answer; the body is the explanation. A
concept whose body is three times its summary is probably two concepts.

**The one exception is `glossary`**: one short entry per term, each naming its
synonyms and collisions and linking to the concept that explains it. It is
where a new term is defined first. An entry that grows past three sentences is
a concept waiting to be written, and the glossary should link to it instead.

## `content/guides/`

**Audience:** someone doing a task from start to finish, usually once.

**Contains:** task-shaped walkthroughs — the fork → edit → publish loop, the
debug loop after a failed run, adding a table.

**The test:** *does it have a first step and a last step?* If it has neither,
it is a concept.

**Shape:** ordered, with the commands. Guides may repeat a concept's content
inline; they may not contradict it, and where they overlap the concept is
authoritative.

## `content/reference/`

**Generated. Never hand-edited.**

**Audience:** an agent that needs exact argument names, and a person checking
one.

**Contains:** the activity catalog. The flow rules, the CLI command surface,
the `template check` rule codes and a per-app states rendering belong here
too, and land here only once something generates them — never hand-written
in the meantime.

**The test:** *is there a symbol in the backend that already enforces this?*
Then it is generated, and hand-writing it creates a second source that will
disagree.

## What has no section, on purpose

**Rules a validator consumes.** Served by the API and vendored into the CLI.
Documented here only as prose about what they mean.

**One app's vocabulary.** The app declares its own states and labels;
`feature.state.spec` serves them per channel and per version. A page here
explains what a state machine *is* and then stops.

**Anything with a status field.** No roadmaps, no phase checklists. They are
wrong within a month and nobody re-reads them.
