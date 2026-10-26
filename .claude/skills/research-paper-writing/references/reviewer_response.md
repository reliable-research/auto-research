# Reviewer Response: Rebuttals, Revisions, and Rejection

The review process for AI/ML conferences is famously high-variance. The path from submission to acceptance often runs through hostile reviews and a tightly time-boxed rebuttal. This file covers how to read reviews productively, how to write rebuttals that change minds, and how to handle rejection.

## Reading reviews without panic

Receiving reviews is hard. Even well-intentioned reviews can read as harsh, especially when you've spent months on a project. Some practical advice:

- **Read each review twice, with a day in between.** First pass for emotional reaction, second pass for substance. The substance is what matters; don't reply from the emotional pass.
- **Separate the *concerns* from the *tone*.** A reviewer who is dismissive may still have a real concern buried under the dismissiveness. Address the concern; ignore the tone.
- **Look for what's shared across reviewers.** If two or three reviewers raise a concern independently, it's almost certainly real and needs to be addressed. A concern raised by only one reviewer may be an idiosyncratic reading.
- **Believe reviewers when they say they don't understand something.** "I didn't understand section 3.2" is not (usually) a personal failing of the reviewer. It's evidence the writing wasn't clear. The fix is to clarify.

## Common categories of negative review

The WritingAIPaper handbook catalogues recurring complaints. Each suggests a different rebuttal strategy:

### "Important references are missing"

Or: poor structure, missing essential elements (like supplementary video for a video paper), experimental setup differs from prior work.

**Response strategy:** This is a fixable concern. In the rebuttal, acknowledge the missing references and incorporate them; align experimental setups; show you've understood the gap. Reviewers respect authors who respond constructively to specific, fixable complaints.

### "Results don't conform to common sense"

Or: exaggerated claims, obviously incorrect assertions, flaws in experimental setup or argumentation.

**Response strategy:** This is the most serious category. Either:
- The reviewer misread something — explain clearly, with reference to specific lines/figures.
- The reviewer is right — acknowledge it. Run the additional experiments they ask for if at all possible; soften overclaims; commit to revisions.
- Don't try to talk past a real flaw. Reviewers compare notes during discussion, and dismissive responses to legitimate concerns are noticed.

### "Doesn't respect prior work"

Or: missing recent results, low-benchmark experiments, demeaning predecessors, conflating own work with predecessors' contributions.

**Response strategy:** Compare more thoroughly with existing work in the rebuttal — concrete tables help. If the reviewer says you've been unfair to prior work, they're often right; soften the language. If you say someone did something poorly, you need evidence; provide it or remove the claim.

### "Lack of novelty"

Or: story isn't well-told, logic isn't clear, work feels incremental.

**Response strategy:** This is partly a writing problem and partly a substance problem. In the rebuttal, you can clarify what's actually novel — often reviewers under-rate novelty because the framing buried it. But if multiple reviewers say "this is incremental," that's a signal to consider whether the paper is making a sharper claim than it currently appears to.

### "Poor presentation quality"

Grammar errors, poor English, hard to follow, missing details.

**Response strategy:** Acknowledge and commit to a careful revision. Use AI tools or a colleague for grammar; have a non-expert read the paper and tell you what's confusing. In the rebuttal, you can fix specific cited issues and promise a thorough pass for camera-ready.

### "Disagreement on approach"

Reviewer doesn't believe in this technical route or experimental design.

**Response strategy:** Find supporting work in the literature that uses similar approaches. Run additional experiments if feasible. Try to win over the *other* reviewers — sometimes one reviewer's disagreement is overcome by the others' agreement during discussion.

## Writing the rebuttal

Most AI venues give you ~1 page for rebuttal, sometimes a few. Treat it like a constraint optimization problem:

1. **List every concern** raised by every reviewer.
2. **Prioritize.** Concerns raised by multiple reviewers go first. Concerns about correctness/validity go before concerns about presentation. Easy wins (we cite that paper now) are quick and worth doing.
3. **For each concern, decide: clarify, agree-and-revise, or push back.**
   - *Clarify:* "R2 raised concern X. We believe this is a misreading: as stated on line N, we actually do..."
   - *Agree-and-revise:* "R1 noted that comparison with method M was missing. We have run M and report results in the table below; we will incorporate this in the camera-ready."
   - *Push back:* "R3 suggests we use evaluation protocol P. We disagree because [substantive reason citing prior work]. Alternative: we have run protocol Q which addresses the same concern..."
4. **Use a clear structure.** Group by reviewer (R1, R2, R3) or by concern, but be consistent. Reviewers reread their own comments; make it easy for them to see your responses.
5. **Be polite but not obsequious.** "We thank R2 for the careful review" once at the top is enough. Don't insert it before every response.

The rebuttal's job is not to win an argument; it's to give reviewers the information they need to update their scores. Reviewers usually want to be convinced — they don't enjoy hostile responses any more than authors enjoy receiving them. A clear, evidence-based rebuttal often raises scores even when reviewers were originally skeptical.

## What happens after the rebuttal

After authors submit rebuttals, reviewers usually have a discussion period (1-2 weeks) on a private platform. They share their views, sometimes update scores, and reach a recommendation. The area chair makes the final call when reviewers don't converge.

Roughly half of papers are withdrawn during this period — typically those whose authors realize they're heading for rejection and would prefer a clean withdrawal. There's no general rule for whether to withdraw; it depends on how borderline the paper is and whether you have time to substantially improve before the next deadline.

## Dealing with rejection

Rejection is statistically the most likely outcome at top AI venues — acceptance rates run 14-31% at most major conferences (CVPR ~24%, NeurIPS ~26%, ICLR ~31%, AAAI ~24%, IJCAI ~14%, ICML ~27%). Most papers eventually published went through at least one rejection.

A few principles from the WritingAIPaper handbook and practitioner experience:

- **Reviews are noisy.** Multiple landmark papers (knowledge distillation, RoBERTa, MobileNet, DoReFa-Net) were initially rejected. Quality and acceptance are correlated, not identical.
- **But there's a golden rule: badly-written papers get bad reviews.** Quoting Fei-Fei Li: writing is critical, and engineers are some of the worst-trained writers in academia. Spend serious time on writing — leave time for it before deadlines, treat it as part of the work, revise repeatedly.
- **Use rejections.** Rejection feedback, even when partially wrong, almost always points at real things. Process the comments, take what's useful, and incorporate it.
- **The Fibonacci submission approach.** Many strong papers went through 2-3 (or more) submission cycles before acceptance, improving each time. The final published version is usually significantly better than the first submission. This is fine — embrace it.
- **Decide whether to resubmit thoughtfully.** Not every paper needs to chase a top venue. Sometimes a workshop, a less competitive conference, or arXiv-only is the right answer for the work's stage.

## A response-pass checklist

Before sending the rebuttal:

- Have I addressed every concern raised by every reviewer?
- For each concern, is it clear whether I'm agreeing, clarifying, or pushing back?
- Where I push back, do I have evidence (not just opinion)?
- Is the rebuttal under the page limit?
- Have I avoided defensive or hostile language even when frustrated?
- Have I committed to specific revisions for camera-ready, where promised?
- Has a co-author or trusted colleague read the rebuttal before I submit?

That last one matters — your judgment is at its worst right after reading reviews. A second pair of eyes catches the moments you're being unintentionally combative.
