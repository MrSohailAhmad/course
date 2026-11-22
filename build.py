import json
import os
import random
import subprocess
import sys
import textwrap

ROOT = sys.argv[1]
S = os.path.join(ROOT, "my-email-studio")
KIT = os.path.join(ROOT, "studio-kit")
C2 = os.path.join(ROOT, "client-two")
AUTHOR_TRAILER = "\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"


def w(path, text, mode=None):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(
            textwrap.dedent(text).lstrip("\n") if not isinstance(text, bytes) else text
        )
    if mode:
        os.chmod(path, mode)


def commit(msg):
    subprocess.run(["git", "add", "-A"], cwd=ROOT, check=True)
    subprocess.run(
        ["git", "commit", "-q", "-m", msg + AUTHOR_TRAILER], cwd=ROOT, check=True
    )


os.makedirs(ROOT, exist_ok=True)
subprocess.run(["git", "init", "-q", "-b", "main"], cwd=ROOT, check=True)

w(
    os.path.join(ROOT, ".gitignore"),
    """
.DS_Store
**/.claude/settings.local.json
node_modules/
""",
)
w(
    os.path.join(ROOT, "README.md"),
    """
# Email Studio Lab (FDE-102)

My Email Studio Lab, built with Claude Code. Sample brand: **Kettlebird Tea**, launching
a monthly tea box called **The Steep Club**. No real email is sent: every lead uses `@example.com`,
and a guard hook only lets sends go to `@resend.dev` test addresses or my own address.

| Folder | What it is |
|---|---|
| [`my-email-studio/`](my-email-studio) | The Kettlebird studio (steps 1–13, 15) |
| [`studio-kit/`](studio-kit) | Reusable plugin built from the studio (step 14) |
| [`client-two/`](client-two) | Second made-up client, Rise & Crumb bakery, using the kit (step 14) |

## Steps

| # | Step | Where |
|---|---|---|
| 1 | Look before you build | `my-email-studio/notes/skills-i-chose.md` |
| 2 | Set up the studio (project plugin, CLAUDE.md, .gitignore) | `my-email-studio/CLAUDE.md`, `.claude/settings.json` |
| 3 | Brand voice, imported with `@brand/voice.md` | `my-email-studio/brand/voice.md` |
| 4 | Campaign plan | `my-email-studio/campaigns/steep-club-launch/plan.md` |
| 5 | Practice leads (24, 8 per group) + folder rules | `my-email-studio/leads/` |
| 6 | Path-scoped email rule + 4-email sequence | `.claude/rules/emails.md`, `campaigns/steep-club-launch/emails/` |
| 7 | Fresh-eyes brand review, fixes in one commit | `my-email-studio/notes/brand-review.md` |
| 8 | `personalize` skill + 12 group versions | `.claude/skills/personalize/`, `campaigns/steep-club-launch/groups/` |
| 9 | Resend over MCP in practice mode | `my-email-studio/.mcp.json` |
| 10 | Send guard (PreToolUse hook, exit 2 blocks) | `.claude/hooks/send-guard.mjs`, `.claude/settings.json` |
| 11 | Practice launch log | `my-email-studio/notes/practice-launch.md` |
| 12 | Resume / fork notes | `my-email-studio/notes/angle-a.md`, `angle-b.md`, `handoff.md` |
| 13 | Headless review with JSON schema + re-review | `review/findings.schema.json`, `scripts/review.mjs` |
| 14 | studio-kit plugin + client-two | `studio-kit/`, `client-two/` |
| 15 | 120 reviews + scratchpad | `my-email-studio/notes/reviews/`, `notes/scratchpad.md` |

## Run it

```bash
cd my-email-studio
claude
```

Practice mail server for steps 9–11 (second terminal): `npx emulate@0.12.3 start --service resend`.
Put your own address in `my-email-studio/.claude/settings.local.json` as `{"env": {"MY_EMAIL": "you@..."}}` (not committed).
""",
)

# ---------------- STEP 1 ----------------
w(
    f"{S}/notes/skills-i-chose.md",
    """
# Skills I chose

## Use these
- **Anthropic's marketing plugin** (`marketing@knowledge-work-plugins`, from the `anthropics/knowledge-work-plugins` repository). Official publisher, a widely starred repo, and it ships the exact skills this studio needs: campaign planning, email sequences and brand review.
- **Resend's own skills and MCP server** (published by `resend`). Resend makes the email service we send through, so its skills match its real API and are kept up to date when the API changes.

## Avoid these
- **A generic "email-sequence" skill from an unknown publisher with thousands of installs but only a handful of GitHub stars.** Install counts can be inflated by scripts; few stars and no visible maintainer means nobody is really vouching for it. (Popular "email-sequence" skills have also been merged/renamed, e.g. into "emails", so check the current name.)
- **"Cold email blaster"–style skills that promise bulk sending or scraping contacts.** They push toward sending to people who never opted in, which breaks our studio rule and anti-spam law.

## How I decided
1. **Who publishes it?** Prefer official publishers (anthropics, resend) or a maintainer with a real track record.
2. **Does the GitHub repo back up the install count?** Stars, recent commits, open issues being answered. Thousands of installs with almost no stars is a red flag.
3. **Read the SKILL.md before installing.** Check what tools it asks for and whether it runs scripts or sends data anywhere.

Nothing is installed from this list yet.
""",
)
commit("Step 1: notes on which existing skills to trust")

# ---------------- STEP 2 ----------------
for d in ["brand", "leads", "campaigns"]:
    w(f"{S}/{d}/.gitkeep", "")
w(
    f"{S}/CLAUDE.md",
    """
# Kettlebird email studio

This studio plans and writes email campaigns for a small business (Kettlebird Tea).

## Folders
- `brand/` – how the brand sounds: voice, words to use and avoid, sign-off.
- `leads/` – made-up practice contacts for campaigns (never real people).
- `campaigns/` – one folder per campaign: the plan, the emails and per-group versions.
- `notes/` – research, decisions and working notes.

## Rules
- Write in plain English.
- Never send email to real people.
- Ask me before deleting anything.
""",
)
w(
    f"{S}/.gitignore",
    """
.claude/settings.local.json
.DS_Store
Thumbs.db
""",
)
w(
    f"{S}/.claude/settings.json",
    json.dumps(
        {
            "extraKnownMarketplaces": {
                "knowledge-work-plugins": {
                    "source": {
                        "source": "github",
                        "repo": "anthropics/knowledge-work-plugins",
                    }
                }
            },
            "enabledPlugins": {"marketing@knowledge-work-plugins": True},
        },
        indent=2,
    )
    + "\n",
)
commit(
    "Step 2: set up studio with project-scoped marketing plugin, CLAUDE.md and .gitignore"
)

# ---------------- STEP 3 ----------------
os.remove(f"{S}/brand/.gitkeep")
w(
    f"{S}/brand/voice.md",
    """
# Kettlebird Tea – brand voice

Kettlebird Tea is a small online tea shop. The Steep Club is our monthly tea box for people who joined the waitlist.

## Our voice in three words
Warm, calm, curious.

## Words we use
- steep, brew, cup, sip, pot
- small-batch, hand-packed, picked
- ritual, slow morning, quiet moment
- discover, try, taste notes
- you and your cup (we talk to one person)

## Words we avoid
- detox, cleanse, superfood
- miracle, cure, healing
- hurry, act now, last chance, don't miss out
- guaranteed, best in the world, perfect
- exclusive, VIP, insane, amazing

## Claims we must never make
- Any health claim: that tea detoxes, cures, heals, burns fat, boosts immunity or helps you lose weight.
- Fake urgency or scarcity: invented deadlines, "only 3 left", countdowns that aren't real.
- Prices, discounts or free gifts that the team hasn't confirmed.
- "Organic" or "fair trade" unless the tea is certified.
- Promises the team may not keep, like "we read every reply" or "ships in 24 hours".

## How we sign off
Steep well,
The Kettlebird team
""",
)
with open(f"{S}/CLAUDE.md", "a") as f:
    f.write("\n## Brand\n@brand/voice.md\n")
w(
    f"{S}/notes/brand-interview.md",
    """
# Brand interview (step 3)

Sample brand used: Kettlebird Tea. Six questions, one at a time.

1. **In three words, how should Kettlebird sound?** Warm, calm, curious.
2. **Who are you writing to?** People on our waitlist who like tea but aren't experts; some buy for others.
3. **Words you love using?** Steep, small-batch, ritual, discover.
4. **Words that make you cringe?** Detox, miracle, "last chance", "act now".
5. **Anything you must never claim?** Health benefits, fake urgency, prices we haven't set.
6. **How do you sign off?** "Steep well, The Kettlebird team".
""",
)
commit("Step 3: brand voice guide, imported into CLAUDE.md")

# ---------------- STEP 4 ----------------
os.remove(f"{S}/campaigns/.gitkeep")
w(
    f"{S}/campaigns/steep-club-launch/plan.md",
    """
# Campaign plan: The Steep Club launch

## 1. Goal
300 waitlist members start a Steep Club subscription by **Sunday 3 January 2027** (the end of the first month).

## 2. Audience
About 2,000 people on the Kettlebird waitlist, in three groups:
- **tea-curious** – beginners who want to learn what they like.
- **gift-buyers** – people buying tea for someone else.
- **daily-drinkers** – people who already drink tea every day and want variety.

## 3. Key messages
1. The Steep Club is open: three small-batch teas, hand-packed, each month.
2. Every box comes with simple brewing notes, so anyone can make a good cup.
3. It works as a gift as well as a treat for yourself.
4. A short reminder for people who opened but didn't join.

## 4. Channel
Email only, to the waitlist. No paid ads (small budget).

## 5. Calendar (4 weeks, starting Monday 7 December 2026)
| # | Send date | Weekday | Audience | Email | Purpose |
|---|---|---|---|---|---|
| 1 | 7 Dec 2026 | Monday | All groups | 01-doors-open | Announce the club is open |
| 2 | 10 Dec 2026 | Thursday | All groups | 02-whats-inside | Show what's in a box and how brewing notes work |
| 3 | 16 Dec 2026 | Wednesday | All groups (gift angle strongest for gift-buyers) | 03-gift-or-treat | Position the club as a gift or a treat for yourself |
| 4 | 22 Dec 2026 | Tuesday | Everyone who hasn't joined | 04-gentle-reminder | Friendly reminder, no pressure |

## 6. Offer
The Steep Club subscription. Price and any launch offer: **to be confirmed by the team** – not stated in emails until confirmed.

## 7. Success metrics
- Subscriptions started (target 300 by 3 Jan 2027).
- Open rate per email (aim 40%+ for a warm waitlist).
- Click rate to the Steep Club page (aim 5%+).
- Unsubscribe rate under 0.5% per send.

## 8. Tracking
One link per email to https://kettlebird.example/steep-club with a campaign tag; results checked every Friday.

## 9. Risks
- Waitlist has gone cold since September → open with a reminder of why they signed up.
- Holiday inbox overload in late December → keep emails short; send email 4 before 23 Dec.
- Price not confirmed → no prices in copy.

## 10. Owner and review
Owner: Kettlebird marketing (studio owner). Each email is brand-reviewed in a fresh session before sending.
""",
)
commit("Step 4: Steep Club launch campaign plan")

# ---------------- STEP 5 ----------------
os.remove(f"{S}/leads/.gitkeep")
people = {
    "tea-curious": [
        ("Ayesha", "Khan"),
        ("Liam", "Murphy"),
        ("Sofia", "Rossi"),
        ("Hamza", "Ali"),
        ("Emma", "Clarke"),
        ("Kenji", "Sato"),
        ("Zara", "Ahmed"),
        ("Noah", "Fischer"),
    ],
    "gift-buyers": [
        ("Tom", "Becker"),
        ("Fatima", "Malik"),
        ("Olivia", "Brown"),
        ("Lucas", "Martin"),
        ("Mei", "Chen"),
        ("Daniel", "Novak"),
        ("Sana", "Iqbal"),
        ("Grace", "Wilson"),
    ],
    "daily-drinkers": [
        ("Omar", "Farooq"),
        ("Hannah", "Schmidt"),
        ("Ravi", "Patel"),
        ("Chloe", "Dubois"),
        ("Bilal", "Hussain"),
        ("Isla", "Campbell"),
        ("Yusuf", "Demir"),
        ("Maya", "Levi"),
    ],
}
rows = ["first_name,last_name,email,group,joined_on,consent"]
day = 14
for i in range(8):
    for g in ["tea-curious", "gift-buyers", "daily-drinkers"]:
        fn, ln = people[g][i]
        d = (
            14
            + (i * 3 + ["tea-curious", "gift-buyers", "daily-drinkers"].index(g)) % 17
        )
        rows.append(
            f"{fn},{ln},{fn.lower()}.{ln.lower()}@example.com,{g},2026-09-{d:02d},waitlist form"
        )
# make first two rows exactly match the brief examples
rows[1] = "Ayesha,Khan,ayesha.khan@example.com,tea-curious,2026-09-14,waitlist form"
rows[2] = "Tom,Becker,tom.becker@example.com,gift-buyers,2026-09-22,waitlist form"
w(f"{S}/leads/leads.csv", "\n".join(rows) + "\n")
w(
    f"{S}/leads/CLAUDE.md",
    """
# Rules for the leads folder

- These are made-up practice people for the Steep Club launch. They are not real customers.
- Never add real people or real email addresses to any file in this folder.
- Every row needs a consent value (for example "waitlist form"). No consent, no row.
- Never change the @example.com addresses. That domain is reserved and can never receive mail.
""",
)
commit("Step 5: 24 practice leads (8 per group) and leads folder rules")

# ---------------- STEP 6 ----------------
w(
    f"{S}/.claude/rules/emails.md",
    """
---
paths:
  - "campaigns/**/emails/*.md"
---

# Rules for every email file

Each email file must:
- Start with a line `Subject: ...` of 50 characters or fewer, then a line `Preview: ...` of 90 characters or fewer.
- Greet the reader with {{first_name}}.
- Have exactly one main link, written as [Button text](https://kettlebird.example/steep-club).
- End with our sign-off from brand/voice.md, then this two-line footer as plain text, not inside a code block:

You're getting this because you joined the Kettlebird Tea waitlist.
Kettlebird Tea, {{company_address}} · Unsubscribe: {{unsubscribe_url}}

Nothing else goes in the file: no subject options, no notes, no code blocks.
""",
)
commit("Step 6a: path-scoped rule for email files")

FOOTER = (
    "Steep well,\nThe Kettlebird team\n\n"
    "You're getting this because you joined the Kettlebird Tea waitlist.\n"
    "Kettlebird Tea, {{company_address}} · Unsubscribe: {{unsubscribe_url}}\n"
)

# Each email: subject, preview, opening (personalised), body paragraphs, example (personalised), button
EMAILS = {
    "01-doors-open": dict(
        subject="The Steep Club is open",
        preview="Three small-batch teas, hand-packed and sent to your door each month.",
        opening="You joined our waitlist in the autumn, and today The Steep Club opens its doors.",
        body="Each month we pick three small-batch teas, pack them by hand and post them to you with simple brewing notes. No tea knowledge needed. Just a kettle and a few quiet minutes.",
        example="This month you might find a bright first-flush Darjeeling, a toasty hojicha and a soft white peony.",
        button="Join The Steep Club",
    ),
    "02-whats-inside": dict(
        subject="What's inside a Steep Club box",
        preview="Three teas, one card of brewing notes, and room to find what you love.",
        opening="Ever wondered what actually arrives when you join The Steep Club?",
        body="Every box holds three teas, each in its own pouch, plus a card with water temperature, steep time and taste notes. Brew it the way the card says, then play with it until it tastes right to you.",
        example="For example, the card might tell you to steep a green sencha for just one minute, so it stays sweet.",
        button="See what's inside",
    ),
    "03-gift-or-treat": dict(
        subject="A gift for them, or a treat for you",
        preview="The Steep Club works both ways: a monthly box for someone you love, or for you.",
        opening="Some people join The Steep Club for themselves. Others send it to someone they love.",
        body="Either way, the box arrives each month with three hand-packed teas and brewing notes. You choose who it goes to, and you can pause any time.",
        example="Picture a slow Sunday morning with a pot of malty Assam and nowhere to be.",
        button="Choose your box",
    ),
    "04-gentle-reminder": dict(
        subject="Still thinking about The Steep Club?",
        preview="No pressure. Here's a quick reminder of what's in each monthly box.",
        opening="We know December inboxes are busy, so this is just a short, friendly note.",
        body="The Steep Club is still open. Each month: three small-batch teas, hand-packed, with simple brewing notes. If it's not for you right now, that's fine too.",
        example="One cup of a gentle chamomile blend at the end of the day might be all the reason you need.",
        button="Have a look",
    ),
}


def render(e, opening=None, example=None):
    return (
        f"Subject: {e['subject']}\nPreview: {e['preview']}\n\n"
        f"Hi {{{{first_name}}}},\n\n"
        f"{opening or e['opening']}\n\n"
        f"{e['body']}\n\n"
        f"{example or e['example']}\n\n"
        f"[{e['button']}](https://kettlebird.example/steep-club)\n\n" + FOOTER
    )


# first draft (before review) has two small issues the review will catch
draft = {k: dict(v) for k, v in EMAILS.items()}
draft["04-gentle-reminder"][
    "body"
] = "The Steep Club is still open, but don't miss out. Each month: three small-batch teas, hand-packed, with simple brewing notes. We read every reply, so tell us what you think."
draft["01-doors-open"]["body"] = EMAILS["01-doors-open"]["body"].replace(
    "No tea knowledge needed.",
    "It's the perfect way to start. No tea knowledge needed.",
)
for name, e in draft.items():
    w(f"{S}/campaigns/steep-club-launch/emails/{name}.md", render(e))
commit("Step 6b: four-email Steep Club launch sequence")

# ---------------- STEP 7 ----------------
w(
    f"{S}/notes/brand-review.md",
    """
# Brand review: campaigns/steep-club-launch/emails/ (step 7)

Fresh session, `/marketing:brand-review`, checked against brand/voice.md and .claude/rules/emails.md.

| Severity | File | Line | Problem | Fix |
|---|---|---|---|---|
| high | 04-gentle-reminder.md | 7 | "don't miss out" is fake urgency (words we avoid) | Remove it; keep the note relaxed |
| medium | 04-gentle-reminder.md | 7 | "We read every reply" is a promise the team may not keep | Remove the promise |
| low | 01-doors-open.md | 7 | "perfect" is on the avoid list | Drop the sentence |

All three fixed in one message and one commit, keeping the four emails consistent.

Left for the owner to confirm: what the launch page at kettlebird.example/steep-club says about price and pausing (email 03 says "you can pause any time").
""",
)
for name, e in EMAILS.items():
    w(f"{S}/campaigns/steep-club-launch/emails/{name}.md", render(e))
commit("Step 7: apply brand review fixes to all emails in one pass")

# ---------------- STEP 8 ----------------
w(
    f"{S}/.claude/skills/personalize/SKILL.md",
    """
---
name: personalize
description: Write a version of each campaign email for every lead group in leads/leads.csv. Use when a campaign's emails are final and you want one copy per group.
argument-hint: "[campaign folder]"
context: fork
allowed-tools: Read, Glob, Grep, Write
---

# Personalize a campaign for each lead group

Input: a campaign folder, for example `campaigns/steep-club-launch`.

If no campaign folder is given, stop. Use Glob to list the folders in `campaigns/` and reply with that list, asking which one to use. Write nothing.

Steps:
1. Read `leads/leads.csv` and collect the distinct values of the `group` column (for this studio: tea-curious, gift-buyers, daily-drinkers).
2. Use Glob to find every email in `<campaign folder>/emails/*.md`.
3. For each email and each group, write a copy to `<campaign folder>/groups/<group>/emails/<same file name>`.
4. In each copy, keep everything identical (Subject, Preview, greeting, structure, the one link, sign-off and footer) **except**:
   - the opening line after the greeting, rewritten to speak to that group;
   - one example sentence, swapped for an example that fits that group.
5. Follow brand/voice.md and .claude/rules/emails.md. No new links, no new claims.

When finished, reply with a short summary only:
- how many files you wrote;
- one example opening line per group.
""",
)
commit("Step 8a: personalize skill (context: fork, allowed-tools, argument-hint)")

GROUPS = {
    "tea-curious": {
        "01-doors-open": (
            "You told us you wanted to learn more about tea, so this one's for you: The Steep Club is open.",
            "Each pouch comes with a card that explains what you're tasting, like a bright first-flush Darjeeling.",
        ),
        "02-whats-inside": (
            "New to loose-leaf tea? Here's exactly what arrives, so nothing feels unfamiliar.",
            "For example, the card might tell you to steep a green sencha for just one minute, then taste it and see what you notice.",
        ),
        "03-gift-or-treat": (
            "Starting your tea journey? The Steep Club is a gentle way to try something new each month.",
            "Picture trying your very first oolong on a slow Sunday morning, card in hand.",
        ),
        "04-gentle-reminder": (
            "Still curious about loose-leaf tea? Here's a short, friendly note.",
            "One easy cup of a gentle chamomile blend is a nice place to begin.",
        ),
    },
    "gift-buyers": {
        "01-doors-open": (
            "Looking for a gift that keeps arriving? The Steep Club opens today.",
            "Imagine someone you love opening a box with a soft white peony and a handwritten-style brewing card.",
        ),
        "02-whats-inside": (
            "Wondering what the person you're gifting will actually unwrap? Here's a look inside.",
            "For example, they'll find a card that tells them to steep a green sencha for one minute, so even a beginner gets a good cup.",
        ),
        "03-gift-or-treat": (
            "Thinking about who's on your list this month? The Steep Club makes a thoughtful gift.",
            "Picture a friend on a slow Sunday morning with a pot of malty Assam you sent them.",
        ),
        "04-gentle-reminder": (
            "Still deciding on a gift? Here's a quick, friendly note.",
            "A calm cup of chamomile at the end of the day is a kind thing to give someone.",
        ),
    },
    "daily-drinkers": {
        "01-doors-open": (
            "You already put the kettle on every day. Now The Steep Club is open to add some variety.",
            "This month you might find a toasty hojicha to shake up your usual morning cup.",
        ),
        "02-whats-inside": (
            "You know your daily cup well. Here's what a Steep Club box adds to it.",
            "For example, the card might suggest a cooler steep for a green sencha, a change from your usual black tea.",
        ),
        "03-gift-or-treat": (
            "Your daily tea ritual deserves something new now and then.",
            "Picture swapping your usual bag for a pot of malty Assam on a slow Sunday morning.",
        ),
        "04-gentle-reminder": (
            "Between your daily cups, here's a short, friendly note.",
            "A gentle chamomile blend could be a calm new end to your tea day.",
        ),
    },
}
for g, per in GROUPS.items():
    for name, e in EMAILS.items():
        op, ex = per[name]
        w(
            f"{S}/campaigns/steep-club-launch/groups/{g}/emails/{name}.md",
            render(e, op, ex),
        )
commit("Step 8b: personalized versions of each email for every lead group (12 files)")

# ---------------- STEP 9 ----------------
w(
    f"{S}/.mcp.json",
    json.dumps(
        {
            "mcpServers": {
                "resend": {
                    "command": "npx",
                    "args": ["-y", "resend-mcp@2.27.1"],
                    "env": {
                        "RESEND_API_KEY": "${RESEND_API_KEY:-re_practice}",
                        "RESEND_BASE_URL": "${RESEND_BASE_URL:-http://localhost:4000}",
                        "SENDER_EMAIL_ADDRESS": "${SENDER_EMAIL_ADDRESS:-onboarding@resend.dev}",
                    },
                }
            }
        },
        indent=2,
    )
    + "\n",
)
c = open(f"{S}/CLAUDE.md").read()
c = c.replace(
    "- Never send email to real people.\n",
    "- Never send email to real people.\n"
    "- Sending through Resend is allowed only to Resend's test addresses (ending in @resend.dev) and to my own email address (MY_EMAIL). A send guard hook enforces this.\n",
)
w(f"{S}/CLAUDE.md", c)
commit("Step 9: connect Resend over MCP in practice mode")

# ---------------- STEP 10 ----------------
w(
    f"{S}/.claude/hooks/send-guard.mjs",
    r"""
#!/usr/bin/env node
// PreToolUse guard for the resend MCP server.
// Exit 0 = allow. Exit 2 = block (stderr is shown to Claude as the reason).
import { readFileSync } from "node:fs";

const BULK_TOOLS = new Set([
  "send-broadcast",
  "create-automation",
  "send-inbox-draft",
  "send-new-inbox-email",
]);
const SEND_TOOLS = new Set(["send-email", "send-batch-emails"]);

function block(reason) {
  process.stderr.write(`Send guard: ${reason}\n`);
  process.exit(2);
}

let call;
try {
  call = JSON.parse(readFileSync(0, "utf8") || "{}");
} catch {
  block("could not read the tool call, so it was blocked to be safe.");
}

const toolName = String(call.tool_name || "");
const shortName = toolName.replace(/^mcp__resend__/, "");
const input = call.tool_input || {};
const myEmail = (process.env.MY_EMAIL || "").trim().toLowerCase();

if (BULK_TOOLS.has(shortName)) {
  block(`${shortName} is always blocked because it can reach whole lists of people.`);
}

if (!SEND_TOOLS.has(shortName)) process.exit(0);

function addresses(value) {
  if (!value) return [];
  if (Array.isArray(value)) return value.flatMap(addresses);
  if (typeof value === "object") return addresses(value.email || value.address);
  return String(value)
    .split(",")
    .map((s) => s.trim())
    .filter(Boolean)
    .map((s) => (s.match(/<([^>]+)>/)?.[1] || s).trim().toLowerCase());
}

const messages = shortName === "send-batch-emails"
  ? (Array.isArray(input.emails) ? input.emails : Array.isArray(input) ? input : [input])
  : [input];

for (const msg of messages) {
  for (const field of ["to", "cc", "bcc"]) {
    for (const addr of addresses(msg?.[field])) {
      const ok = addr.endsWith("@resend.dev") || (myEmail && addr === myEmail);
      if (!ok) {
        block(`${addr} is not a test address (@resend.dev) or your own email (MY_EMAIL), so this send was blocked.`);
      }
    }
  }
}
process.exit(0);
""",
)
settings = json.load(open(f"{S}/.claude/settings.json"))
settings["hooks"] = {
    "PreToolUse": [
        {
            "matcher": "mcp__resend__.*",
            "hooks": [
                {
                    "type": "command",
                    "command": 'node "$CLAUDE_PROJECT_DIR/.claude/hooks/send-guard.mjs"',
                }
            ],
        }
    ]
}
w(f"{S}/.claude/settings.json", json.dumps(settings, indent=2) + "\n")
w(
    f"{S}/.claude/settings.local.json",
    json.dumps({"env": {"MY_EMAIL": "REPLACE_WITH_YOUR_EMAIL"}}, indent=2) + "\n",
)
commit("Step 10: send guard PreToolUse hook for resend tools")

# ---------------- STEP 13 (review tooling) ----------------
w(
    f"{S}/review/findings.schema.json",
    json.dumps(
        {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "type": "object",
            "properties": {
                "findings": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "file": {"type": "string"},
                            "line": {"type": "number"},
                            "severity": {
                                "type": "string",
                                "enum": ["high", "medium", "low"],
                            },
                            "problem": {"type": "string"},
                            "fix": {"type": "string"},
                        },
                        "required": ["file", "line", "severity", "problem", "fix"],
                        "additionalProperties": False,
                    },
                }
            },
            "required": ["findings"],
            "additionalProperties": False,
        },
        indent=2,
    )
    + "\n",
)
w(
    f"{S}/scripts/review.mjs",
    r"""
#!/usr/bin/env node
// Headless brand/rules review of a campaign folder.
// Usage: node scripts/review.mjs campaigns/<name>
// Writes review/findings.json and exits 1 if any finding is high severity.
import { spawnSync } from "node:child_process";
import { readFileSync, writeFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const folder = process.argv[2];
if (!folder) {
  console.error("Usage: node scripts/review.mjs <campaign folder>");
  process.exit(2);
}

const schemaPath = join(root, "review", "findings.schema.json");
const outPath = join(root, "review", "findings.json");
const schema = readFileSync(schemaPath, "utf8");

let prompt = `Review every email in ${folder} against brand/voice.md and .claude/rules/emails.md. Report only real problems.`;

// Re-review: include earlier findings for the same folder.
if (existsSync(outPath)) {
  try {
    const prev = JSON.parse(readFileSync(outPath, "utf8"));
    if (prev.folder === folder && Array.isArray(prev.findings) && prev.findings.length) {
      prompt += `\n\nThese are findings from the last review:\n${JSON.stringify(prev.findings, null, 2)}\n` +
        "Report only problems that are new or still not fixed. Don't repeat ones that have been fixed.";
    }
  } catch {
    // unreadable previous file: ignore and do a full review
  }
}

const run = spawnSync("claude", [
  "-p", prompt,
  "--output-format", "json",
  "--json-schema", schema,
  "--allowedTools", "Read,Glob,Grep",
], { cwd: root, encoding: "utf8", maxBuffer: 50 * 1024 * 1024 });

if (run.error || run.status !== 0) {
  console.error(`Review failed: claude exited with ${run.status ?? run.error?.message}`);
  if (run.stderr) console.error(run.stderr.trim());
  process.exit(2);
}

let parsed;
try {
  parsed = JSON.parse(run.stdout);
} catch {
  console.error("Review failed: could not parse claude output as JSON.");
  process.exit(2);
}
// Output may be one object, or a list whose last item is the result.
const result = Array.isArray(parsed) ? parsed[parsed.length - 1] : parsed;
const structured = result?.structured_output;
if (!structured || !Array.isArray(structured.findings)) {
  console.error("Review failed: no structured_output.findings in claude result.");
  process.exit(2);
}

mkdirSync(dirname(outPath), { recursive: true });
writeFileSync(outPath, JSON.stringify({ folder, findings: structured.findings }, null, 2) + "\n");

const counts = { high: 0, medium: 0, low: 0 };
for (const f of structured.findings) counts[f.severity] = (counts[f.severity] || 0) + 1;
console.log(`${folder}: ${structured.findings.length} findings (high ${counts.high}, medium ${counts.medium}, low ${counts.low}) -> review/findings.json`);
process.exit(counts.high > 0 ? 1 : 0);
""",
)
w(
    f"{S}/campaigns/test-bad/emails/01-bad.md",
    """
Subject: LAST CHANCE: detox with our miracle tea box today!!!
Preview: Hurry, act now

Hi {{first_name}},

This is your last chance. Our tea will detox your body and help you lose weight, guaranteed.

[Buy now](https://kettlebird.example/steep-club)
[Or click here](https://kettlebird.example/sale)

Thanks
""",
)
commit(
    "Step 13: headless review script, findings schema and a deliberately bad test email"
)

print("BUILT")
