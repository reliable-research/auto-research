# Venue Guide

This file is a starting reference on AI/ML conference timelines, venue characteristics, and how to think about venue choice. Conference details change yearly — for current deadlines and acceptance rates, check [aideadlin.es](https://aideadlin.es) and the venue's official website. Treat the numbers below as approximate.

## How AI/ML conferences work

AI/ML differs from many fields in that conferences, not journals, are the primary publication venue. The cycle is:

1. **Submission deadline** — paper plus supplementary material uploaded.
2. **Desk-reject screening** — papers exceeding page limits, missing anonymization, or with severe formatting issues are rejected before review (sometimes within days).
3. **Review period** — typically ~2 months. Each paper gets ~3 reviewers, who score it and write comments.
4. **Rebuttal period** — authors get the reviews and have ~1 week to respond (usually 1 page max).
5. **Discussion period** — reviewers and area chairs discuss for ~1-2 weeks.
6. **Notification** — accept/reject decisions, typically ~3-4 months after submission.
7. **Camera-ready period** — accepted papers get a few weeks to revise based on review feedback before the final published version.

Conferences typically have an associated proceedings (IEEE, ACM, MLR, OpenReview, etc.) where accepted papers are archived.

## Major AI/ML venues at a glance

Approximate submission months and recent acceptance rates. Always verify with the official call for papers.

| Conference | Field | Submission month | Recent acceptance rate |
|---|---|---|---|
| IJCAI | AI broadly | January | ~14% |
| ICML | Machine learning | January | ~27% |
| ICCV/ECCV | Computer vision | March | ~27% |
| BMVC | Vision | April | ~26% |
| ACMMM | Multimedia | April | ~26% |
| NeurIPS | Machine learning | May | ~26% |
| EMNLP | NLP | May | ~23% |
| WACV | Vision | June, August | ~45% |
| ACCV | Vision (Asia) | July | ~33% |
| AAAI | AI broadly | July | ~24% |
| ICASSP | Signal processing | September | ~45% |
| ICLR | Machine learning | September | ~31% |
| NAACL | NLP (Americas) | September | ~23% |
| ICRA | Robotics | September | ~45% |
| AISTATS | Stats + ML | October | ~28% |
| CVPR | Computer vision | November | ~24% |
| ACL | NLP | Rolling (ARR) | ~23% |

Tier and competitiveness vary; the above is a rough community consensus, not a formal ranking.

## Notes on specific venues

- **NeurIPS, ICML, ICLR** — the "big three" general ML venues. NeurIPS and ICML are traditional conferences with single deadlines; ICLR uses OpenReview with public reviews and has a strong emphasis on reproducibility.
- **CVPR, ICCV, ECCV** — the "big three" computer vision venues. CVPR is annual, ICCV biennial (odd years), ECCV biennial (even years).
- **ACL, EMNLP, NAACL** — major NLP venues. ACL has moved to a rolling-review model (ACL Rolling Review, ARR) where papers can be reviewed continuously and submitted to specific venues based on those reviews.
- **AAAI, IJCAI** — broad AI venues with somewhat different cultures. AAAI is more application-oriented; IJCAI tends to be theoretical and is highly selective.
- **Workshops** at the major conferences are typically less competitive (~50%+ acceptance) and often a good first publication venue or place to share early-stage work.

## Choosing a venue

Considerations:

- **Topical fit.** Submitting an NLP paper to a vision conference (or vice versa) is rarely a good idea even if the technique generalizes — reviewers don't share assumptions and may not have context to evaluate the work.
- **Timeline.** What's the next deadline you can realistically hit with a strong submission? A paper rushed to ICML when it could be a strong NeurIPS submission is usually a worse outcome.
- **Length and detail.** Some venues allow 8-page main text + appendix; some allow 10. If your paper genuinely needs 10 pages of detail, an 8-page venue means cutting essentials or hand-waving.
- **Review culture.** Some venues (e.g., ICLR) have public reviews; some (most) don't. Some require code release, some don't. Check the call for papers carefully.
- **Camera-ready expansions.** Some venues let you add a page for camera-ready (helpful for incorporating reviewer requests); some don't.

## Journal options

For work that doesn't fit a conference cycle or needs more space, journals are an option:

- **JMLR** — Journal of Machine Learning Research. Open access, strong reputation, no page limit.
- **TMLR** — Transactions on Machine Learning Research. Newer, faster turnaround, transparent reviewing, no acceptance rate target.
- **TPAMI** — IEEE Transactions on Pattern Analysis and Machine Intelligence. Vision/ML, high prestige, slow review cycle.
- **Computational Linguistics, TACL** — NLP journals.
- **Nature, Nature Machine Intelligence, Science** — for work with broad scientific impact, not just methodological contribution.

Journal submission is generally slower (months to a year+) but allows more space and a more iterative review cycle.

## Cross-cutting venues

Some venues sit between fields:

- **KDD, WSDM, WWW** — data mining / web search.
- **SIGGRAPH** — graphics with significant ML content.
- **RSS, CoRL** — robotics with learning.
- **ISMIR** — music information retrieval.
- **MICCAI** — medical image computing.

For interdisciplinary work, picking the right venue often means thinking about which audience needs to see this paper — the ML audience, or the domain audience? They often differ in what they reward.

## Workshops as a stepping stone

Workshop papers don't carry the same weight as main-track papers, but they're useful for:

- Getting early feedback on a research direction before committing to a long paper.
- Sharing work that's preliminary or doesn't yet have a complete experimental story.
- Building visibility with a specialized community.
- Getting a first publication as a junior researcher.

Most workshops accept 4-6 page papers; some allow extended abstracts. Some prohibit subsequent publication of the same work as a full paper, others explicitly encourage it. Check the call.

## arXiv and preprints

Most AI/ML venues allow arXiv preprints concurrent with submission (some explicitly require concurrent or earlier posting; some require a quiet period; check the call). Posting to arXiv:

- **Establishes priority.** If two groups are working on similar things, the arXiv timestamp matters.
- **Improves reach.** arXiv papers get cited even before formal publication.
- **Doesn't break double-blind for most venues** as long as authors don't actively advertise the paper during review (no tweets pointing at it, no presentations naming it). Reviewers are expected not to actively search for the arXiv version.

If unsure about a venue's arXiv policy, the call for papers will state it explicitly.

## A note on building a publication strategy

A research career is rarely well-served by always aiming at the most prestigious venue. Some patterns that work:

- **Strong main contributions go to top venues.** Save the NeurIPS/ICML/CVPR/ACL slot for work where the contribution is sharp.
- **Solid contributions go to second-tier venues** that fit the topic well. WACV, ACCV, EMNLP-Findings, AAAI, COLING are all reasonable homes.
- **Preliminary work goes to workshops or arXiv.** Don't burn a top-venue submission on something half-baked; you'll get better reviews from sharing it more informally first.
- **Survey, reproduction, and infrastructure work** sometimes fit better in journals or specialized tracks (Datasets and Benchmarks at NeurIPS, for example).

The goal of publication is to get the work to the people who'll use it, not to maximize CV prestige in isolation.
