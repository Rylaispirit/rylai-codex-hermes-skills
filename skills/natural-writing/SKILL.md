---
name: natural-writing
description: Make prose sound natural and human while preserving meaning, voice, facts, and format. Use for writing or requests to reduce generic AI-sounding patterns.
metadata:
  maintainer: Rylai
  adapted_by: Rylai
  edition: Codex-Hermes-Claude
  edition_version: 1.1.0
  provenance: adapted-open-source
  upstream:
    url: https://github.com/blader/humanizer
    revision: 523374dee72d67c7b2b5f858ea0094ffda49c3ac
    license: MIT
  hermes:
    category: content
  claude:
    category: content
---

> Rylai Codex-Hermes-Claude Edition | Maintained and adapted by Rylai

## Runtime Compatibility

- Codex: install under `~/.agents/skills/natural-writing`.
- Hermes: install under `~/.hermes/skills/natural-writing` or expose the bundle through `skills.external_dirs`.
- Claude Code: install under `~/.claude/skills/natural-writing` or `<project>/.claude/skills/natural-writing`.
- Claude.ai and Cowork: upload and enable the matching per-skill ZIP.
- Resolve bundled files relative to this skill directory; do not depend on paths from another machine.
- Check tools, packages, credentials, network access, and runtime capabilities before execution.

# Natural Writing

LLM text is detectable because it **regresses to the mean**: it replaces
specific, surprising, concrete details with generic, positive-sounding
language that could apply to almost anything. The subject becomes
simultaneously less specific and more exaggerated — like a portrait fading
from a sharp photograph into a blurry, generic sketch while someone shouts
louder and louder that the person in it is important.

Every pattern below is a concrete manifestation of that tendency. The fix is
almost always the same: be specific, be plain, and trust the reader.

---

## 1. Cut the Significance Inflation

The single most recognizable AI pattern is stuffing sentences with claims
about how important, pivotal, or transformative something is.

**What it looks like:**
- "marking a pivotal moment in the evolution of..."
- "representing a significant shift toward..."
- "part of a broader movement across..."
- "highlighting the enduring legacy of..."
- "reflecting the transformative power of..."
- "contributing to the rich tapestry of..."
- "underscoring its role as a dynamic hub of..."

**Why it happens:** LLMs are trained on text where notable things are
described with notable-sounding language. The model pattern-matches
"thing being discussed" → "must emphasize its importance" regardless of
whether the thing actually warrants it.

**The fix:** Delete the significance claim. State the fact. If the fact is
significant, the reader will notice. If you have to tell them it's
significant, it probably isn't — or you haven't presented the fact sharply
enough.

Bad: "The library was established in 1962, marking a pivotal moment in the
region's educational development and reflecting a broader commitment to
knowledge accessibility."

Good: "The library opened in 1962."

If context is needed, provide it with a concrete detail, not an
abstraction: "The library opened in 1962 — the first public lending
library within forty miles."

---

## 2. Kill the Trailing Analysis

AI text habitually tacks on a participial phrase or subordinate clause at the
end of sentences that "analyzes" what was just said, usually in vague terms
about significance, impact, or recognition.

**What it looks like:**
- "...creating a lively community within its borders."
- "...further enhancing its significance as a dynamic hub."
- "...showcasing the brand's dedication to craftsmanship."
- "...demonstrating the ongoing relevance of his research."
- "...reflecting the influence of French rotary designs on German manufacturers."

**The fix:** End the sentence at the fact. If the analysis adds nothing a
thoughtful reader couldn't infer, cut it entirely. If it contains a genuine
insight, promote it to its own sentence and make it concrete.

Bad: "The dam generates 2,400 MW annually, underscoring the region's
commitment to renewable energy infrastructure."

Good: "The dam generates 2,400 MW annually." Or, if the point matters:
"The dam generates 2,400 MW annually — enough to power roughly 1.8 million
homes."

---

## 3. Avoid the AI Vocabulary

Certain words spike in frequency in LLM output relative to human writing.
One or two is coincidence. A cluster is a tell. Avoid overusing:

**High-frequency AI words:**
delve, tapestry, multifaceted, nuanced, landscape (metaphorical),
underscores, realm, foster, leverage (verb), pivotal, comprehensive,
intricate, commendable, noteworthy, invaluable, meticulous, innovative,
groundbreaking, cutting-edge, revolutionary, game-changer, holistic,
synergy, robust, seamless, dynamic, vibrant, bustling, nestled, renowned,
esteemed, testament

**The principle:** Prefer the shorter, plainer, more common word. "Shows"
over "underscores." "Detailed" over "meticulous." "Useful" over
"invaluable." "Complex" over "multifaceted." Often the fancy word can just
be deleted — the sentence is stronger without it.

---

## 4. Use "Is" and "Are"

LLM text systematically avoids simple copulas (is, are, was, were) and
substitutes longer constructions. Research shows a >10% decline in "is"/"are"
usage in AI-era text. This is one of the subtlest but most measurable tells.

**AI pattern → Human equivalent:**
- "serves as a" → "is a"
- "stands as a" → "is a"
- "marks the" → "is the"
- "acts as the" → "is the"
- "offers a" → "has a" or "is a"
- "features a" → "has a"
- "represents a" → "is a"
- "constitutes a" → "is a"
- "ventured into politics as a candidate" → "was a candidate" / "ran for office"

**The fix:** When you catch yourself writing "serves as," ask whether "is"
works. It almost always does. Save the fancier constructions for the rare
cases where the distinction matters (e.g., something literally serving a
function for something else).

---

## 5. Drop the Negative Parallelisms

"Not only ... but also ..." and "It's not just about X, it's about Y"
are AI comfort-food constructions. They create an appearance of balanced,
thoughtful analysis while often saying nothing.

**What it looks like:**
- "not only a work of self-representation, but a visual document of..."
- "It's not just about the beat; it's part of the aggression and atmosphere."
- "not dissolution, but what Deleuze might describe as 'becoming'"

**The fix:** Just say the thing. If something is two things, say both
without the theatrical setup: "The portrait is a visual document of her
obsessions." If the contrast genuinely matters, a simple "but" or "though"
does the work without the formula.

---

## 6. Break the Rule of Three

LLMs default to triplets — three adjectives, three noun phrases, three
examples. Used occasionally, the rule of three is a fine rhetorical device.
Used compulsively, it's a fingerprint.

**What it looks like:**
- "global SEO professionals, marketing experts, and growth hackers"
- "keynote sessions, panel discussions, and networking opportunities"
- "bold proportions, refined dynamism, and historical reverence"

**The fix:** Vary your list lengths. Sometimes two items is enough. Sometimes
four is better. Sometimes a single well-chosen example beats a list entirely.
When you do use three, make each item carry real weight — not three vaguely
overlapping ways of saying the same thing.

---

## 7. Stop the Elegant Variation

Repetition-penalty mechanisms cause LLMs to compulsively find synonyms for
words they've already used, even when repeating the word would be clearer.
A person's name becomes "the protagonist," then "the key player," then
"the eponymous character."

**The fix:** Repeat the word. Good prose uses repetition deliberately.
If you mentioned "the bridge" in the last sentence, say "the bridge" again —
don't switch to "the structure" or "the crossing" or "the span" just because
you already used "bridge." Elegant variation is only elegant when the
variation adds meaning.

---

## 8. Don't Manufacture Ranges

LLMs love "from X to Y" constructions, but often the two endpoints don'
form a coherent scale. A real range has identifiable middle ground: "from
winter to spring" works because there's a clear continuum. A false range
jams unrelated concepts into the structure for rhetorical flourish.

**False range:** "from the singularity of the Big Bang to the grand cosmic
web, from the birth and death of stars to the enigmatic dance of dark matter"

**The fix:** If you can't identify a meaningful midpoint between X and Y,
don't use "from X to Y." Just mention the items: "stars, dark matter, the
cosmic web."

---

## 9. Restrain the Em Dashes

Em dashes (—) are useful punctuation. LLMs overuse them, particularly in a
formulaic, sales-pitch cadence that over-emphasizes clauses. Human writers
use commas, parentheses, and colons for variety.

**AI pattern:** "The temple — a counter-symbol of unity — stands at the
border, emphasizing togetherness — and transcendent faith."

**The fix:** Use em dashes sparingly. One per paragraph is plenty. For most
parenthetical asides, commas or actual parentheses work fine. For
explanations, try a colon.

---

## 10. Cut "It's Important to Note"

Didactic disclaimers — "it's important to note that," "it's worth
mentioning," "it should be noted that," "it's crucial to understand" —
are verbal throat-clearing. If something is important, stating it makes
that clear. The disclaimer adds nothing except an AI tell.

**The fix:** Delete the preamble. Start with the important thing itself.

Bad: "It's important to note that these regulations vary by jurisdiction."
Good: "These regulations vary by jurisdiction."

---

## 11. Don't Summarize What You Just Said

Older LLMs added "In summary" and "In conclusion" sections compulsively.
Newer ones still tend to end paragraphs or sections by restating the core
idea. In most contexts, this is pure padding.

**The fix:** End when you're done. Trust the reader to have read the
preceding paragraph. If your conclusion adds a genuinely new thought or
synthesis, keep it. If it just repeats the same point in different words,
cut it.

---

## 12. Avoid Vague Attribution

LLMs attribute opinions to unnamed authorities: "scholars note," "experts
agree," "it has been described as," "many have praised." This is weasel
wording. Even when a real source exists, the AI often exaggerates consensus
("several publications have cited" when there's one).

**The fix:** Name the source or drop the attribution. "Roger Ebert called
the film X" beats "critics have praised the film for X." If you don't have
a specific source, present the claim as your own analysis or reframe it as
observable fact.

---

## 13. Don't Inflate Promotional Language

LLMs struggle to maintain a neutral tone, particularly around anything
culturally or commercially significant. They slip into brochure language:
"nestled within the breathtaking region," "offering visitors a fascinating
glimpse," "a diverse range of experiences against the backdrop of stunning
natural beauty."

**The fix:** Describe, don't sell. State what exists, what happened, what
something does. Let the reader form their own impression. If you're writing
actual marketing copy, be specific about benefits rather than stacking
adjectives.

Bad: "Our revolutionary platform offers a seamless, cutting-edge experience
that empowers teams to unlock their full potential."

Good: "The platform syncs files across devices in under three seconds and
supports offline editing."

---

## 14. Don't Write "Challenges and Future Prospects"

AI-generated text often ends with a section that follows the formula:
"Despite its [achievements], [subject] faces challenges including [vague
list]... However, with ongoing initiatives, [subject] continues to [positive
vague statement]."

This is a content-free hedge that tries to appear balanced. If challenges
are worth discussing, name them specifically with evidence. If not, don'
add a "challenges" section just to look thorough.

---

## 15. Vary Your Sentence Architecture

Beyond specific patterns, AI text has a recognizable rhythm: medium-length
declarative sentences, each structured similarly, rarely interrupted by
fragments, questions, very short sentences, or very long ones. Human prose
breathes. It varies. Some sentences are four words. Others unspool across
a paragraph, piling clause upon clause, picking up momentum like a freight
train before finally, at the end, making their point.

Mix it up. Start some sentences with conjunctions. Use fragments for
emphasis. Occasionally let a sentence run. The variation itself signals
a human hand.

---

## Quick Self-Check

Before finalizing any piece of writing, scan for these clusters:

1. **Significance inflation** — Can you delete "pivotal," "transformative,"
   "broader," or "legacy" without losing meaning? Do it.
2. **Trailing analysis** — Do sentences end with "-ing" phrases that
   restate the obvious? Cut them.
3. **AI vocabulary clusters** — Three or more words from the AI vocab list
   in one paragraph? Rewrite.
4. **Copula avoidance** — Count your uses of "is" and "are." If they're
   suspiciously low, you're probably over-substituting.
5. **Compulsive triplets** — Every list has exactly three items? Vary it.
6. **Em dash density** — More than one em dash per paragraph? Switch some
   to commas or parentheses.
7. **Preamble throat-clearing** — "It's worth noting," "importantly,"
   "it should be mentioned" — delete on sight.

---

## The Meta-Principle

Every pattern above is a symptom of the same underlying tendency: the model
reaching for the statistically most probable way to say something, which
produces text that is simultaneously generic and overblown. The antidote is
always specificity and restraint. Say the concrete thing. Use the plain
word. Trust the reader. Stop when you're done.
