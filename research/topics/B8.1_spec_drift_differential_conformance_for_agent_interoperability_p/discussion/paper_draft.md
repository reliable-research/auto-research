# Conforming to Neither: Differential Conformance and Silent Authority Downgrades Across Agent-Protocol Versions

> Assembled from the six confirmed stage outputs in `discussion_trace.md`,
> post-audit (`taste_audit.md`: 🟢) and post stage-review (`stage_review.md`: two
> REVISE fixes applied). Status: **specification / paper draft — no experiments
> have been run.** All numbers below are pre-registered design targets with stated
> rationale, not results.

## Abstract

Agent-interoperability protocols such as the Model Context Protocol (MCP) and
Agent2Agent (A2A) are being adopted as the substrate for cross-vendor tool use and
delegation, and they are revised on a monthly cadence. A protocol revision is
normally assumed to move the ecosystem cleanly from one version to the next, so
that "conforms to MCP vX" remains a usable safety label throughout. We show this
assumption hides an unexamined possibility: a deployed server transitioning across
a normative-clause revision can, for a measurable interval, conform to *neither* the
old version nor the new one — a divergence window — and inside that window an
authority constraint the clause governs can silently degrade from *enforced* (the
server rejects an unauthorized action) to *visibility-only* (the constraint is
merely advertised while the action still succeeds), a regression that no single-
version conformance check and no static framework audit catches, because it exists
only *between* versions and only on the wire. We build a differential-conformance
measurement apparatus: for each normative-clause delta between adjacent spec
versions we synthesize a matched wire-probe pair that must provably discriminate two
pinned reference implementations before it may label any live server "neither"; we
witness authority enforcement non-destructively by reading the server's accept/deny
decision at the authorization boundary rather than performing the unauthorized
action; we separate drift-induced divergence from generic non-conformance with an
unchanged-clause placebo; and we estimate each window's temporal width with
interval-censored survival estimation over a fixed-cadence longitudinal sweep of a
public server directory. We measure the prevalence and width of divergence windows,
the prevalence of authority-to-visibility downgrades, and how both concentrate
across clause-delta types — and what this implies for whether conformance auditing
of agent protocols must be version-differential and continuous rather than single-
version and one-shot.

## Introduction

Agent-to-agent interoperability now runs on published protocols. As large language
model agents are delegated tool calls, resource access, and cross-vendor actions on
behalf of a principal, the Model Context Protocol (MCP) and Agent2Agent (A2A) have
become the wire formats those delegations travel over, and a growing amount of
security and governance reasoning rests on a server's advertised conformance to a
named protocol version. Framed this way, "conforms to MCP v2026-07" is doing the
work of a safety label: a client, a gateway, or an operator decides how much to
trust a server partly on the strength of it. This label is cheap to state and easy
to rely on, which is exactly why it is worth checking rather than assuming.

Yet these protocols are revised faster than the servers deployed against them can
be expected to move in lockstep. MCP shipped a release candidate on 2026-07-28; A2A
extended its 1.0.1 line in 2026-05; each revision changes a set of normative
(RFC-2119 MUST / SHALL / SHOULD) clauses. The tacit assumption is that a revision
moves the ecosystem cleanly from version N to version N+1. But a server that has
begun adopting N+1 while not yet fully abandoning N — or that has half-implemented a
changed clause — can, for some interval, satisfy the changed clause under *neither*
version's requirements. During that interval every client that negotiates with it is
interoperating against a behavior no published spec describes. And the clauses whose
degradation matters most are the *authority* clauses: a clause that in one version
requires the server to *reject* an unauthorized tool call can, mid-transition,
degrade so that the constraint is merely *advertised* — surfaced in a capability
descriptor or an error message — while the unauthorized call still succeeds. That is
a security regression, and it is invisible to the two kinds of check the field
currently has: a single-version conformance test never compares against the *other*
version, and a static framework audit never touches the wire during a live
transition.

The nearest existing work approaches this gap from adjacent but distinct angles.
The closest is a spec-side conformance line that compiles a protocol specification
into a typed intermediate representation, model-checks it, and replays counter-
examples into an SDK; it certifies the *specification*, not the deployed fleet, its
analysis is single-version, and its artifact is withheld under coordinated
disclosure, so no reproducible deployed-side check exists to build on. A cluster
of deployed-measurement studies — an authentication-security census of remote MCP
servers, a large-scale runtime-server study, and a dynamic security assessment of
internet-facing servers — demonstrates that wire-level measurement of the
installed base is publishable and informative, but each is single-version and
conformance-blind: none has a clause-diff, a notion of a divergence window, or a
per-server temporal axis. The nearest of these measures description-code
inconsistency in deployed MCP servers — what a server *advertises* can diverge
from what its code does — but statically, within one version, with no
enforcement-status transition over time. On the security side, one line of work establishes that a capability being
*visible* is not the same as it being *authorized*, and another proposes replacing
the execution layer with a fixed set of security invariants; both operate at the
framework or design layer and neither measures, on the wire, on deployed servers,
across a revision, whether an authority constraint's enforcement actually changes.
And an argumentative strand catalogs what these protocols *cannot express*, but as a
matrix of asserted gaps rather than one measured against deployed behavior.

Turning this into a measurable question surfaces its own difficulties. A normative
clause is a sentence of prose, so deciding whether a server "conforms to neither
version" on that clause requires a wire probe whose pass/fail actually tracks the
clause's meaning and not some incidental server behavior — and a probe that cannot
tell two known versions apart cannot be trusted to label an unknown server. A single
"neither" verdict could equally be a one-off error, a rate-limit, or a server that
was simply always broken, none of which is a divergence *caused by the revision*.
Witnessing whether an authority constraint is enforced seems to demand attempting an
unauthorized action — but on a live third-party server an unauthorized action that
is *not* rejected has, by definition, just been performed against someone's
production system, and a probe that mutates state corrupts every later observation
in the panel. And the *width* of a divergence window, which is the quantity that
turns "some servers are non-conformant" into "servers are exposed for a day versus a
quarter," can never be read directly off a coarse polling schedule: windows are
bracketed by sweeps and censored by servers appearing and disappearing.

Our approach turns each of these obstacles into a specific design choice rather than
a hedge. Every clause-delta is compiled into a matched probe pair that must first
*discriminate* two pinned reference implementations — a server built to version N and
one built to N+1 — before it is allowed to label any live server "neither," so a
wire verdict is grounded in known conformance rather than asserted. Every candidate
divergence is measured against a matched set of *unchanged* clauses, whose behavior
cannot be affected by the revision, so a "neither" is counted as drift only when it
exceeds that placebo and persists across sweeps. Authority enforcement is witnessed
non-destructively, by reading the server's accept-or-deny decision at the
authorization boundary rather than by carrying the unauthorized action through — and
any probe whose only faithful form must attempt a real mutation is confined to
consenting reference deployments. And each window's width is estimated as an
interval-censored duration with an explicit resolution floor, so a coarse sweep
schedule yields an honest distribution rather than a biased subtraction.

We evaluate this design across two protocols (MCP and A2A) and a longitudinally
re-sampled public directory of deployed servers, with two pinned reference
implementations per protocol as the only ground-truth conformance labels, an
unchanged-clause placebo as the null control, and a within-server changed-versus-
unchanged contrast as the isolation of drift from generic brokenness.

In summary, we contribute:
- A formalization of the *divergence window* — the interval in which a deployed
  server, transitioning across a normative-clause revision, conforms to neither the
  old nor the new version on that clause — with a version-bracket reference frame
  that distinguishes a genuine window from ordinary older/newer-version conformance,
  and its temporal width as the quantity that measures exposure duration.
- A differential-conformance instrument that synthesizes matched wire-probe pairs
  from a normative-clause diff and admits a probe to the live sweep only after it
  provably discriminates two pinned reference implementations, making a wire
  "neither" verdict a validated conformance judgment rather than an arbitrary
  failed request.
- A non-destructive authority-enforcement observable that reads the server's
  accept/deny decision at the authorization boundary, operationalizing the
  visibility-versus-authority distinction as a *measured wire transition* (enforced
  → advertise-only → silent) without performing the unauthorized action it tests.
- A pre-registered measurement of the prevalence and interval-censored width of
  divergence windows and of authority-to-visibility downgrades across deployed
  servers, and of how both concentrate across clause-delta types, with a design that
  would — if divergence windows and downgrades prove prevalent — license the
  conclusion that agent-protocol conformance auditing must be version-differential
  and continuous rather than single-version and one-shot.

## Problem Definition

**Formal setup.** Let $N$ and $N+1$ be two adjacent published versions of an
agent-interoperability protocol, each a set of normative (RFC-2119) clauses $C_N$
and $C_{N+1}$. The clause diff $\Delta = \Delta(N, N+1)$ is the set of clauses that
were added, removed, or modified (a requirement strengthened, weakened, or a
constraint re-typed) between the two versions; each $\delta \in \Delta$ is a
*normative-clause delta*. For each $\delta$ we construct a *matched probe pair*
$(p_\delta^N, p_\delta^{N+1})$: wire interactions whose responses classify a
server's behavior on $\delta$ as conforming to $N$, to $N+1$, to both, or to
neither. Let $S$ be a set of deployed servers, each reachable at a wire endpoint and
re-observable at times $t_1 < t_2 < \cdots < t_m$ on a fixed sweep cadence. For a
server $s \in S$, a delta $\delta$, and a time $t$, the verdict is

$$ v(s, \delta, t) \in \{\, N,\ N{+}1,\ \text{both},\ \text{neither},\ \text{out-of-frame} \,\}. $$

A server is *in-frame* for the pair $(N, N+1)$ when $N$ is the latest version whose
publication precedes $s$'s first observed conformance and $N+1$ is the next
published version; a server conforming on $\delta$ to some earlier $N-1$ or later
$N+2$ is labeled **out-of-frame** and excluded from window estimation, so that
ordinary older/newer-version conformance is never mistaken for a divergence. The
**divergence window** $W(s, \delta)$ is the maximal time interval over which
$v(s, \delta, t) = \text{neither}$, conditional on $s$ being in-frame. For an
authority-bearing $\delta$, the **enforcement status**
$e(s, \delta, t) \in \{\text{enforced},\ \text{advertise-only},\ \text{silent}\}$
records whether an unauthorized action is rejected on the wire, merely advertised
while succeeding, or neither; a **downgrade** $D(s, \delta)$ is a measured
transition $\text{enforced} \to \{\text{advertise-only}, \text{silent}\}$ coincident
with $\delta$. The estimands are the population prevalence and interval-censored
width distribution of $W$ over $S$, and the prevalence of $D$ among authority-
bearing deltas, each reported with a validity envelope (probe validity, directory
coverage, temporal resolution).

**Why this is hard.** Four properties of the setting obstruct a naive measurement.
First, $\delta$ is prose: a probe pair earns the right to return "neither" on an
unknown server only if it *provably separates* a server known to implement $N$ from
one known to implement $N+1$; an unvalidated probe conflates its own defects with
the server's. Second, a single $v = \text{neither}$ is not yet a window: it must be
distinguished from transient error and from a server that is simply broadly non-
conformant, which requires a control of *unchanged* clauses — identical in $C_N$ and
$C_{N+1}$, hence incapable of a version-induced "neither" by construction — and
persistence across sweeps. Third, the enforcement status $e$ is defined by whether
an *unauthorized* action is rejected, yet carrying that action through against a live
$s$ both performs the unauthorized effect and mutates $s$'s state, confounding later
$v(s, \cdot, t')$; enforcement must therefore be read from the accept/deny decision
at the authorization boundary rather than from the action's completion. Fourth, the
width of $W$ is bounded below by the sweep cadence and censored by servers entering
and leaving $S$: entry and exit are each bracketed by two sweeps (interval
censoring), and a window still open at $t_m$ or ended by the server's disappearance
is right-censored — so the width distribution must be estimated, not subtracted.

## Method Overview

At a conceptual level the study is a single measurement pipeline with five
cooperating parts. A clause diff and a directory of deployed servers enter the
pipeline; a differential probe synthesizer and a non-destructive probing harness
turn each server's wire behavior into a validated per-clause verdict; an unchanged-
clause placebo turns a sequence of verdicts into a drift-attributed divergence
window; an authority classifier turns the same verdict stream into an enforcement-
status transition; and an interval-censored estimator turns a coarse sweep schedule
into an honest window-width distribution.

The **differential probe synthesizer** compiles each normative-clause delta into a
matched probe pair and admits it to the live sweep only after it correctly
classifies two pinned reference implementations. The **non-destructive probing
harness** expresses every authority probe as a read-only, idempotent, or dry-run
request that surfaces the server's accept/deny decision without performing the
unauthorized action, confining any irreducibly destructive probe to consenting
reference deployments. The **unchanged-clause placebo and persistence gate** runs
matched probes for clauses identical across the two versions, and counts a changed-
clause "neither" as a divergence only when it exceeds the placebo baseline and
persists across sweeps. The **authority-visibility classifier** labels each
authority-bearing delta's wire behavior as enforced, advertise-only, or silent, and
reads a downgrade off the transition. The **interval-censored window estimator**
treats each confirmed window as a censored duration and fits a survival model for
its width against an explicit resolution floor. The parts compose in one direction:
no width is estimated for a window that has not been attributed to drift, and no
drift is attributed on a verdict a validated probe did not produce.

## Methodology

### Differential Conformance Probe Synthesis

**Challenge.** A normative-clause delta is natural-language prose; a wire probe
whose pass/fail is taken as a conformance verdict must actually track the clause's
semantics, or every downstream divergence count is an artifact of the probe rather
than of the ecosystem.

**Insight.** The faithfulness of a probe cannot be argued from its text; it can be
*demonstrated* against known ground truth. A probe that provably tells two known
versions apart has earned the right to judge an unknown server — differential
discrimination on reference implementations is the instrument-validation step that
makes a wire "neither" meaningful.

**Method.** For each clause-delta $\delta$, we author a matched probe pair
$(p_\delta^N, p_\delta^{N+1})$ following the differential-testing discipline
[McKeeman 1998; Yang et al. 2011]: $p_\delta^N$ is an interaction a strictly-$N$-
conforming server passes and a strictly-$(N+1)$-conforming server fails, and
$p_\delta^{N+1}$ its converse, so that the pair's joint outcome maps to one of
$\{N, N+1, \text{both}, \text{neither}\}$. Before any live sweep, each pair is run
against two pinned reference implementations — the protocol's official reference
server built and tagged at $N$ and at $N+1$ — and admitted only if it classifies the
$N$-reference as $N$-only and the $(N+1)$-reference as $(N+1)$-only. Requirement
force and clause identity are read from the specifications' RFC-2119 keywords
[Bradner 1997]. Clause-delta labels (changed vs. unchanged; authority-bearing vs.
representational; delta type) are assigned by at least two independent annotators
with a Cohen's $\kappa \geq 0.7$ acceptance threshold [Cohen 1960] and a confusion-
structure inspection; a threshold miss blocks scale-up rather than being absorbed
into noisier verdicts.

### Non-Destructive Authority Probing

**Challenge.** Deciding whether an authority constraint is *enforced* appears to
require attempting an unauthorized action — but on a live third-party server an
unauthorized action that is not rejected has just been performed against a
production system, and a state-mutating probe corrupts every later sweep in the
panel.

**Insight.** Enforcement is a property of the *rejection decision*, not of the
mutation. Observing the server's accept-or-deny at the authorization boundary
witnesses enforcement without carrying the unauthorized effect through, decoupling
the measurement from the harm.

**Method.** Every authority probe is expressed in a non-destructive form — a read-
only or idempotent request, or a dry-run / check-only variant — that forces the
server to emit its accept/deny decision before any state change. A probe whose only
faithful form must attempt a real mutation is run solely against consenting
reference or self-hosted servers, never live third-party endpoints, and a harness-
level assertion refuses to emit a state-mutating unauthorized call to a live
endpoint at all. Where a live authority verdict still cannot be obtained safely, it
is reported as un-witnessable and excluded, with the count reported, rather than
being guessed. Any residual finding that would require a destructive live probe is
handled under a coordinated-disclosure protocol, consistent with the withheld-
artifact posture of prior spec-side conformance work.

### Unchanged-Clause Placebo and Persistence Gate

**Challenge.** A single "neither" verdict could be a transient error, a rate-limit,
or a server that was broadly non-conformant before the revision ever happened — none
of which is a divergence *caused by* the version delta.

**Insight.** Only spec drift can make a *changed* clause fail both ways while a
matched *unchanged* clause of similar difficulty does not. The changed-versus-
unchanged contrast is a within-server placebo, and persistence across sweeps
separates durable drift from transient noise.

**Method.** Alongside the changed-clause probes we run probes for a matched set of
*unchanged* normative clauses — same requirement force, similar request shape,
identical text in $C_N$ and $C_{N+1}$ — for which a version-induced "neither" is
impossible by construction. A changed-clause "neither" is admitted as a divergence
window only if it persists across at least $k$ consecutive sweeps and its rate
exceeds the unchanged-clause failure baseline. The same paired design yields two
separately-falsifiable readouts from one instrument: the *population* contrast
(changed-clause "neither" prevalence minus the placebo baseline) tests whether
divergence windows exist at all, and the *within-server* contrast (each server's
changed-minus-unchanged failure gap) tests whether "neither" is attributable to the
version delta rather than to generic non-conformance.

### Authority-Visibility Downgrade Classifier

**Challenge.** Not every "neither" is a security downgrade; conflating a
representational change (formatting, naming, transport) with a change in whether an
action is authorized would over-claim the security finding.

**Insight.** The enforce-versus-advertise distinction is exactly the visibility-
versus-authority axis that prior framework-layer work draws conceptually — but here
it is read directly off whether an unauthorized wire call is *rejected* or
*succeeds-while-advertised*, turning "authority degraded to visibility-only" from a
conceptual possibility into an observable wire transition.

**Method.** Each authority-bearing clause-delta's wire behavior is labeled at each
time as *enforced* (the unauthorized action is rejected at the boundary),
*advertise-only* (the constraint appears in a capability descriptor or error text
but the action still succeeds), or *silent* (neither rejected nor advertised); a
downgrade is a transition $\text{enforced} \to \{\text{advertise-only},
\text{silent}\}$ coincident with the delta. The same labeled verdict stream yields
two readouts from one scheme: the *rate* of enforced→advertise/silent transitions
gives the downgrade prevalence, and the *distribution* of downgrades and divergence
windows across clause-delta types (added-MUST, strengthened-SHOULD→MUST, retyped-
authority, representational) gives their concentration.

### Interval-Censored Divergence-Window Estimator

**Challenge.** A divergence window's width — the exposure duration that turns "some
servers are non-conformant" into a quantified risk — cannot be read directly off a
coarse, irregular polling schedule with servers entering and leaving the directory.

**Insight.** A polling schedule cannot be turned into an honest width by
subtracting first-"neither" from last-"neither"; only survival estimation with
explicit censoring and a stated resolution floor converts the schedule into a
defensible duration distribution.

**Method.** Each confirmed (server, clause) window is treated as an interval-
censored duration: its start is bracketed by the last-conforming and first-"neither"
sweeps, its end by the last-"neither" and first-reconforming sweeps, with right-
censoring when the window is still open at the final sweep or the server leaves the
directory. A window already open at a server's first observation has no
last-conforming sweep and enters as a left-truncated (delayed-entry) duration
rather than being dated from the first sweep; and because the panel is anchored to
a real revision date, servers that complete their transition before the first sweep
are invisible — a truncation that biases a naive prevalence downward and a naive
width upward, so both terms are carried explicitly in the estimator. A Turnbull / Kaplan-Meier survival estimator [Kaplan and Meier 1958;
Turnbull 1976] gives the median width and confidence intervals, and the fraction of
windows resolvably above the sweep-cadence floor is reported explicitly so that the
short-window tail below the floor is stated as censored rather than counted as zero.

## Experiments

### Experimental Setup

**Measurement targets.** Two adjacent published MCP versions bracketing the study
window (e.g. the 2026-07-28 release candidate and its predecessor) supply the
primary clause diff, chosen because it is recent, adjacent, and large enough to
yield a substantial normative-clause delta set [MCP 2024]. An A2A version pair
(1.0.0 → the 1.0.1 extension) is a second protocol used to test whether the
divergence-window phenomenon is protocol-independent rather than an MCP-specific
artifact [A2A 2025]; because A2A's transport and authorization model differ from
MCP's, the A2A pair carries the *existence* and *width* measurements (which need only
the differential probe and placebo, both of which transfer directly), while the
*authority-downgrade* measurement is reported for A2A only if a documented
precondition holds — that A2A exposes an accept/deny authorization boundary a non-
destructive probe can witness, checked on the A2A reference implementations before
any live sweep — and is otherwise scoped to MCP with the restriction stated rather
than silently dropped. A public remote-MCP-server directory, re-sampled on a fixed
sweep cadence, supplies the deployed population and the longitudinal panel, extending
the deployed-side measurement protocol demonstrated for remote MCP servers to a
version-differential, longitudinal axis. Two pinned reference implementations per
protocol (built and tagged at $N$ and at $N+1$) are the only ground-truth
conformance labels in the study.

**Controls** (ground-truth and null, not competitors to beat — this is a
measurement study, and no research question is framed as "our procedure beats
baseline X"). The *unchanged-clause placebo* — matched clauses identical across the
two versions — is the null baseline every changed-clause claim is measured against;
a version-induced "neither" there is impossible by construction, so any elevated
failure indexes generic server flakiness. The *pinned reference implementations*
supply the verdicts the probes are validated against. The *generic-non-conformance
rival* is isolated by the within-server changed-minus-unchanged contrast, which
distinguishes drift from servers that are simply broadly non-conformant.

**Metrics.** Per-(server, clause, time) verdict and enforcement status; changed-
versus-unchanged "neither" prevalence and its gap; interval-censored median window
width and the fraction above the resolution floor; enforced→advertise/silent
downgrade prevalence among authority clauses; and the distribution of windows and
downgrades across clause-delta types.

**Research questions:**
1. RQ1 — Do the differential probe pairs correctly discriminate the two pinned
   reference implementations?
2. RQ2 — Do divergence windows exist: does persistent changed-clause "neither"
   prevalence exceed the unchanged-clause placebo?
3. RQ3 — How wide are divergence windows once censoring is accounted for?
4. RQ4 — How prevalent are authority-to-visibility downgrades among authority-
   bearing clause deltas?
5. RQ5 — Is "neither" attributable to the version delta rather than to generic
   non-conformance?
6. RQ6 — Do divergence windows and downgrades concentrate in specific clause-delta
   types?
7. RQ7 — Does the non-destructive protocol reproduce full-interaction verdicts
   without performing any unauthorized action on a live server?

#### RQ1: Do the differential probe pairs discriminate the pinned reference implementations?

**Setup.** For every clause-delta, run the matched probe pair against the two pinned
reference implementations (the reference server tagged at $N$ and at $N+1$) and
record whether the pair classifies the $N$-reference as $N$-only and the
$(N+1)$-reference as $(N+1)$-only. Any misclassification is inspected by hand and
attributed either to genuinely ambiguous clause text or to probe error.

**Expected outcome.** The probe pairs correctly classify both references on at least
95% of the clause-delta set; residual misclassifications are attributable on
inspection to genuinely ambiguous clause text, not probe error.

**Falsification condition.** Refuted if the pairs discriminate the references on
fewer than 95% of clause-deltas, or if the residual failures are traced to probe
error rather than clause ambiguity — either would mean the instrument cannot ground
a wire "neither" verdict, and no live divergence claim may be scored until the probe
set is repaired (this is a blocking instrument-validity gate).

**Hypothesis (plain language).** A probe may judge an unknown server only after it
provably tells two known versions apart.

**Metrics.** Per-delta reference-discrimination accuracy; adjudicated cause of each
residual failure.

**Result.** *[placeholder — fill in after experiments are run]*

#### RQ2: Do divergence windows exist above the placebo baseline?

**Setup.** Across the swept deployed population, compare the prevalence of persistent
(at least $k$ consecutive sweeps) "neither" verdicts on changed clauses against the
matched unchanged-clause placebo baseline, via a paired two-proportion / McNemar test
Holm-corrected across clause-deltas at $\alpha = 0.05$ [Holm 1979]. Pilot stage:
one protocol (MCP), one directory, $k = 2$; scale-up: both protocols, $\geq 2$
directories, $k$ set to the persistence needed to exceed the transient-error rate
observed in the pilot.

**Sample-size rationale.** The directory and sweep count are sized so that a 10-
percentage-point changed-versus-placebo gap is detectable at $\approx 80\%$ power
under the pilot's observed error variance; a smaller observed gap in the pilot
triggers a pre-committed directory enlargement, not a null claim.

**Expected outcome.** Persistent changed-clause "neither" prevalence exceeds the
unchanged-clause placebo baseline by at least 10 percentage points under the
corrected test.

**Falsification condition.** Refuted if the changed-clause "neither" prevalence is
within 10 percentage points of, or below, the placebo baseline — deployed servers
would then be tracking versions cleanly (or failing changed and unchanged clauses
alike), and the divergence-window phenomenon is absent; this pre-registered null is
itself reported as a robustness certification that the ecosystem's rapid iteration
does not produce measurable differential-conformance gaps.

**Hypothesis (plain language).** A measurable fraction of deployed servers really do
sit, for a while, between two versions.

**Metrics.** Changed-clause vs. placebo persistent-"neither" prevalence and the
corrected gap; per-clause-delta breakdown.

**Result.** *[placeholder — fill in after experiments are run]*

#### RQ3: How wide are divergence windows once censoring is accounted for?

**Setup.** For every confirmed (server, clause) divergence window, fit the interval-
censored Turnbull / Kaplan-Meier estimator with entry/exit bracketed by the
surrounding sweeps and right-censoring for windows still open at the final sweep or
ended by directory departure; report the median width, its confidence interval, and
the fraction of windows resolvably above the sweep-cadence resolution floor.

**Expected outcome.** The interval-censored median divergence-window width exceeds
the sweep-cadence resolution floor by a factor of at least 2 — windows are multi-
sweep durations, not single-sweep blips — with the estimator's lower confidence
interval above the floor.

**Falsification condition.** Refuted if the median width's lower confidence interval
falls at or below the resolution floor, i.e. the data cannot distinguish real
multi-sweep windows from single-sweep transients at the chosen cadence; the honest
report is then that windows exist (RQ2) but their durations are unresolved at this
cadence, motivating a finer sweep rather than a width claim.

**Hypothesis (plain language).** Divergence is a durable state a server can be stuck
in, not an instantaneous flicker.

**Metrics.** Interval-censored median width with CI; fraction of windows above the
resolution floor; right-censoring rate.

**Result.** *[placeholder — fill in after experiments are run]*

#### RQ4: How prevalent are authority-to-visibility downgrades?

**Setup.** Among authority-bearing changed clauses, classify each transitioning
server's enforcement status (enforced / advertise-only / silent) before and across
the delta using the non-destructive authority probe, and count the fraction of
servers exhibiting an enforced→advertise-only or enforced→silent transition
coincident with the delta.

**Expected outcome.** At least a pre-registered floor (15%) of servers observed
transitioning across an authority-bearing delta exhibit an enforced→advertise-only or
enforced→silent downgrade coincident with the delta.

**Falsification condition.** Refuted if fewer than 15% of transitioning servers show
an enforcement downgrade, and refuted more strongly if zero downgrades are observed
among authority clauses — the security half of the claim then does not reproduce,
and the finding narrows to interoperability divergence without a security-regression
component, reported at full prominence rather than buried.

**Hypothesis (plain language).** When a server drifts between versions on an
authority clause, a meaningful share stop actually enforcing the constraint while
still advertising it.

**Metrics.** Enforced→advertise/silent transition rate among authority clauses;
per-clause and per-server breakdown; count of un-witnessable (safely un-probeable)
authority verdicts excluded.

**Result.** *[placeholder — fill in after experiments are run]*

#### RQ5: Is "neither" attributable to the version delta, not generic non-conformance?

**Setup.** For each server, compute the paired within-server gap between its changed-
clause failure rate and its matched unchanged-clause failure rate; test whether the
gap is greater than zero across servers (paired sign / Wilcoxon test). This is the
rival-explanation ablation: if servers that fail changed clauses fail matched
unchanged clauses at the same rate, "neither" indexes generic brokenness, not drift.

**Expected outcome.** The within-server changed-minus-unchanged failure gap is
greater than zero across the population — servers fail *changed* clauses more than
matched *unchanged* clauses — so "neither" is attributable to the version delta.

**Falsification condition.** Refuted if the within-server changed-minus-unchanged
gap is not significantly greater than zero — servers failing changed clauses would
then fail unchanged clauses just as often, meaning the "neither" verdicts index
broad non-conformance rather than spec drift; under this outcome the divergence-
window claim is downgraded to a general deployed-conformance measurement and the
drift-specific framing is retired (the pre-committed rival-survives wording).

**Hypothesis (plain language).** The failures cluster on exactly the clauses that
changed, which is what makes them about the revision.

**Metrics.** Within-server changed-vs-unchanged failure gap and its test statistic;
fraction of servers with a positive gap.

**Result.** *[placeholder — fill in after experiments are run]*

#### RQ6: Do windows and downgrades concentrate by clause-delta type?

**Setup.** Partition clause-deltas into types (added-MUST, strengthened-
SHOULD→MUST, retyped-authority, representational) and compute, per type, the
divergence-window prevalence and the authority-downgrade rate; test for non-uniform
concentration via per-type enrichment with a pre-registered minimum support.

**Expected outcome.** Divergence windows and authority downgrades are non-uniformly
distributed across clause-delta types — concentrated (at least 2× enrichment,
log-odds greater than zero with pre-registered minimum support) in added-MUST,
strengthened-SHOULD→MUST, and retyped-authority deltas relative to representational
deltas.

**Falsification condition.** Refuted if window and downgrade rates are statistically
uniform across clause-delta types (no type reaches 2× enrichment above support), which
would mean drift is a generic property of *any* clause change rather than
structured by requirement-force and authority semantics — a weaker, less actionable
finding that is reported as such rather than dressed as structure.

**Hypothesis (plain language).** Drift bites hardest exactly where a requirement was
newly imposed or an authority constraint was re-typed, not on cosmetic changes.

**Metrics.** Per-type window prevalence and downgrade rate; enrichment / log-odds
with support.

**Result.** *[placeholder — fill in after experiments are run]*

#### RQ7: Does the non-destructive protocol match full-interaction verdicts without unauthorized effects?

**Setup.** On the reference implementations (where a full destructive interaction is
permissible), compare the conformance verdict produced by the non-destructive
authority probe against the verdict from the full interaction, per clause-delta; and
run a harness-level audit that every authority probe issued to a *live* server is
non-destructive, asserting zero state-mutating unauthorized calls to any live third-
party endpoint.

**Expected outcome.** The non-destructive protocol reproduces the full-interaction
conformance verdict on at least 98% of reference-server clause deltas, and the
harness audit confirms zero state-mutating unauthorized calls to any live server.

**Falsification condition.** Refuted on the validity side if the non-destructive
protocol disagrees with the full interaction on more than 2% of reference clause-
deltas (the safe observable does not faithfully witness enforcement, so authority
verdicts must be restricted to reference-only), and refuted on the safety side if
the harness audit finds any state-mutating unauthorized call issued to a live server
(a stop-the-run condition, not a metric).

**Hypothesis (plain language).** We can see whether the guard fired without actually
walking through the door.

**Metrics.** Non-destructive-vs-full verdict agreement on references; harness audit
count of live state-mutating unauthorized calls (target: zero).

**Result.** *[placeholder — fill in after experiments are run]*

**Further evaluation.** With more time, a natural extension is to measure divergence
windows across *non-adjacent* version jumps (a server upgrading N → N+2, skipping
N+1) and across a third protocol (ACP), both explicitly out of scope here: the first
changes the reference-frame definition from an adjacent pair to a version *path* and
needs its own out-of-frame accounting, and the second requires re-validating the
authority observable against a different authorization model rather than extending
the present instrument.

### Threats to Validity

**Construct validity.** The divergence-window and downgrade constructs are only as
sound as the probes and labels behind them. Probe faithfulness is not asserted but
demonstrated against two pinned reference implementations before any live sweep
(RQ1), and clause-delta labels (changed/unchanged, authority/representational, delta
type) are validated by at least two independent annotators at Cohen's $\kappa \geq
0.7$ with a confusion-structure inspection; a threshold miss blocks scale-up. A
distinct construct threat is the version reference frame itself: a server pinned to
$N-1$ or $N+2$ would be spuriously scored as "neither," which is why every verdict is
computed relative to the adjacent pair straddling the server's observation window and
out-of-frame servers are excluded with their count reported.

**Internal validity.** Two confounds threaten a causal reading of "neither" as
drift. First, transient errors and rate-limits could masquerade as divergence; this
is controlled by the persistence gate (at least $k$ consecutive sweeps) and by the
unchanged-clause placebo, whose "neither" rate bounds the transient-error floor.
Second, and more consequentially, a server that is simply broadly non-conformant
would fail changed clauses for reasons unrelated to the revision; this is isolated by
the within-server changed-minus-unchanged contrast (RQ5), and its failure is pre-
committed to downgrade the drift-specific claim to a general deployed-conformance
measurement rather than to invalidate the whole run. A third internal threat is
measurement-induced state change from the probes themselves, which would confound the
longitudinal panel; the non-destructive probing harness (RQ7) plus a harness
assertion against live state-mutating unauthorized calls is designed to hold this to
zero.

**External validity.** The study is scoped to sandboxable, wire-reachable MCP (and,
conditionally, A2A) servers listed in a public directory; a prevalence estimate is
valid only for that sampled population, which over-represents hosted and well-
maintained servers relative to self-hosted deployments — reported as a directory-
composition sensitivity across at least two directories, not generalized silently.
Findings are further scoped to the two protocol version pairs actually measured and
are not asserted to hold for non-adjacent version jumps, other protocols, or servers
that do not advertise a resolvable version.

**Conclusion validity.** A single sweep cannot distinguish a transient blip from a
durable window, so every width claim is licensed only through the interval-censored
survival estimator with an explicit resolution floor (RQ3), never from a raw first-
to-last subtraction, and windows below the floor are reported as censored rather than
as zero. Symmetrically, windows already open at a server's first observation are
treated as left-truncated durations, and the prevalence estimate is scoped to
windows overlapping the panel — transitions completed before the first sweep are
stated as unobservable rather than silently absorbed. Prevalence tests are Holm-corrected across the clause-delta set to control
the family-wise error rate, and any cell under-powered even after the pre-committed
directory enlargement is reported as inconclusive rather than as a null.

## Related Work

The single closest prior work to this paper is the spec-side agent-protocol
conformance line represented by AgentRFC [AgentRFC 2026], and the delta is worth
stating plainly before the wider survey: AgentRFC compiles a protocol specification
into a typed intermediate representation, model-checks it, and replays counter-
examples into an SDK — but it certifies the *specification* against its own model,
single-version, with an artifact withheld under coordinated disclosure, whereas this
paper measures *deployed servers on the wire*, differentially across a version
revision, longitudinally, with a reproducible instrument. On the security side, the
visibility-versus-authority distinction is owed to prior framework-layer work
[Capability Gates 2026] and a metadata-is-not-authority invariant to a proposed
replacement execution layer [HCP 2026]; the contribution here is not that
distinction but its *measurement*, on the wire, on deployed servers, across a
normative-clause revision, where an authority constraint's degradation to
visibility-only becomes an observable transition rather than a conceptual
possibility.

**Protocol conformance and differential testing.** Conformance checking of the
agent-interoperability protocols is nascent: AgentRFC [AgentRFC 2026] establishes the
spec-side, model-checking route, and a growing deployed-measurement cluster — an
authentication-security census of remote MCP servers [Remote-MCP 2026], a
large-scale runtime-server study [MCPZoo 2026], and a dynamic security assessment
of internet-facing servers [Exposed-by-Design 2026] — establishes that wire-level
measurement of the installed base is publishable and informative. None of these
compares two adjacent versions or tracks a server's conformance over time: the
spec-side line is single-version, and the deployed-side studies are
conformance-blind snapshots (repeated crawls there grow coverage; they do not form
a per-server conformance panel). A mechanism-design line runtime-checks A2A/MCP
messages against negotiation-rationality constraints [Negotiate 2026]; it verifies
wire traffic, but against strategic properties the protocols deliberately do not
specify, on a single version, with no deployed-fleet measurement and no temporal
axis. The instrument here inherits the classical differential-
testing idea of using two implementations (here, two spec *versions*) as each other's
oracle [McKeeman 1998; Yang et al. 2011], applied for the first time to a normative-
clause diff between protocol versions rather than to compilers.

**Authority, visibility, and protocol governance.** A framework-layer line argues
that a capability being visible is not the same as it being authorized [Capability
Gates 2026], and a systems line proposes replacing the execution layer with a fixed
set of security invariants and attack benchmarks [HCP 2026]; both operate on design
or configuration, not on deployed wire behavior across a revision. The closest
*measured* antecedent of the downgrade construct is the description-code
inconsistency study [DCI 2026], which shows on real-world MCP servers that
advertised capabilities and security boundaries can diverge from implemented
behavior; this paper concedes that advertised-versus-actual divergence is
established there, and claims the part a static, single-version inspection cannot
see — enforcement status as a *transition over time coincident with a
normative-clause delta*, read at the authorization boundary on the wire rather
than from code. An argumentative
strand catalogs what MCP, A2A, and ACP cannot express as a matrix of asserted gaps
[Governance Gaps 2026], and a context-governance mechanism proposes verifiable
provenance for agent context [ContextNest 2026]. This paper's authority classifier
turns the *argued* visibility-vs-authority gap into a *measured* enforcement-status
transition, and its divergence-window estimand turns the *argued* what-cannot-be-
expressed matrix into a measured what-is-not-conformed question — a measurement
where these lines offer a conceptual frame.

**Censored-duration estimation.** The window-width estimand is a survival-analysis
problem: windows are interval-censored by the sweep schedule and right-censored by
directory churn, so their widths are estimated with the Kaplan-Meier and Turnbull
estimators [Kaplan and Meier 1958; Turnbull 1976] rather than subtracted. The use is
standard; the point of citing it is that treating a coarse polling schedule as a
censoring mechanism, rather than as ground truth, is what makes the width claim
honest — a discipline the single-snapshot deployed-measurement prior work had no
occasion to apply.

## Conclusion

This work reframes a governance assumption — that a server's advertised conformance
to a protocol version is a stable safety label across a revision — as an empirical
question with a precise identifiability structure, rather than treating conformance
as self-evidently monotone. The central methodological wager is that a divergence
window (conformance to neither adjacent version) and an authority-to-visibility
downgrade are only credibly distinguishable from ordinary non-conformance once
probes are validated to discriminate two known versions, "neither" is measured
against an unchanged-clause placebo, enforcement is witnessed non-destructively, and
window width is estimated under explicit censoring; weaker designs would mistake a
broken server for a drifting one, or a transient blip for a durable window. Whatever
the measured prevalence, the finding is decision-relevant: prevalent, wide windows
with authority downgrades would mean that conformance auditing of agent protocols
must be version-differential and continuous rather than single-version and one-shot,
and that "conforms to vX" cannot be trusted during the exposure interval of a
revision; a measured null would, just as usefully, certify that the ecosystem's
rapid iteration does *not* strand deployed servers between versions. Two limitations
bound this claim from the outset and are natural next steps rather than afterthoughts:
the divergence-window width is bounded below by the sweep cadence, so the true
short-window tail is censored and quantified only above a stated resolution floor,
pointing toward finer or event-triggered sweeps; and the prevalence estimates are
scoped to a public directory that over-represents hosted servers, pointing toward
broader deployment sampling as the next measurement target.

## References

> Grounded in `trend_scan_2026-08.md` §2.1's cited neighbors and in certain,
> well-known published methodology anchors; see `discussion/refs.bib`. The `.tex`
> build uses `\citep`/`\citet` keys resolving to that file; this list is the
> Markdown-readable mirror. All 2026 arXiv IDs were live-verified against the arXiv API on
> 2026-08-15 (original set) and 2026-08-21 (review-pass additions); titles and
> authors below match the published records.

- Model Context Protocol Specification. Anthropic, 2024. https://modelcontextprotocol.io
- Agent2Agent (A2A) Protocol Specification. 2025.
- S. Zheng, Q. Zhang. AgentRFC: Security Design Principles and Conformance Testing for Agent Protocols. arXiv:2603.23801, 2026.
- D. Mellafe Zuvic. Capability Gates Are Not Authorization: Confused-Deputy Failures in LLM Agent Frameworks. arXiv:2606.28679, 2026.
- T. Liu. From Tool Connection to Execution Control: Benchmarking Security Invariants in MCP-Style Agent Runtimes (HCP). arXiv:2606.29073, 2026.
- H. Zhou et al. A First Measurement Study on Authentication Security in Real-World Remote MCP Servers. arXiv:2605.22333, 2026.
- Y. Shi et al. Description-Code Inconsistency in Real-world MCP Servers: Measurement, Detection, and Security Implications. arXiv:2606.04769, 2026.
- P. Chen et al. Rethinking MCP Security: A Large-Scale Study of Runtime MCP Servers and Security Scanner Reliability. arXiv:2607.11086, 2026.
- N. Padilla. Exposed by Design: A Dynamic Security Assessment of Internet-Facing MCP Servers at Scale. arXiv:2608.00150, 2026.
- W. Albayaydh, R. Zhao. Do LLM Agents Negotiate Rationally? A Mechanism-Design Framework for Verifiable Multi-Agent Interaction over A2A/MCP. arXiv:2608.14613, 2026.
- Governance Gaps in Agent Interoperability Protocols: What MCP, A2A, and ACP Cannot Express. arXiv:2606.31498, 2026.
- M. Sulpovar et al. ContextNest: Verifiable Context Governance for Autonomous AI Agent. arXiv:2607.02116, 2026.
- W. M. McKeeman. Differential Testing for Software. Digital Technical Journal, 10(1):100–107, 1998.
- X. Yang, Y. Chen, E. Eide, J. Regehr. Finding and Understanding Bugs in C Compilers. PLDI, 2011.
- S. Bradner. Key words for use in RFCs to Indicate Requirement Levels. RFC 2119, IETF, 1997.
- J. Cohen. A Coefficient of Agreement for Nominal Scales. Educational and Psychological Measurement, 20(1):37–46, 1960.
- S. Holm. A Simple Sequentially Rejective Multiple Test Procedure. Scandinavian Journal of Statistics, 6(2):65–70, 1979.
- E. L. Kaplan, P. Meier. Nonparametric Estimation from Incomplete Observations. Journal of the American Statistical Association, 53(282):457–481, 1958.
- B. W. Turnbull. The Empirical Distribution Function with Arbitrarily Grouped, Censored and Truncated Data. Journal of the Royal Statistical Society: Series B, 38(3):290–295, 1976.

---

## Pre-handoff checklist

- **Organization/navigation** — narrative flows problem → method → experiments →
  related work with no forward references to undefined terms.
- **Terminology discipline** — "divergence window," "clause-delta," "enforcement
  status," "out-of-frame," "matched probe pair" each defined at first use in
  Problem Definition and used consistently; no internal stage IDs (`sp_*`, `m_*`,
  `rq_*`) in prose — checked directly against `discussion_trace.md`.
- **Notation with formal setup** — the Problem Definition defines
  $(N, N+1, \Delta, \delta, v, W, e, D)$ and the Methodology reuses this notation;
  no worked numeric example is included since no numbers exist yet (would require
  fabricating results).
- **RQ framing matches outcomes** — all 7 RQs are graded/quantitative
  (accuracies, prevalence gaps, censored widths, enrichment), each answered in its
  own subsection with an explicit falsifiable Expected outcome *and* a Falsification
  condition, not a binary yes/no.
- **No typesetting artifacts** — no `[CITE]`/`[TODO]`; only explicit
  `[placeholder — fill in after experiments are run]` in Results.
- **Artifact plan** — the probe-synthesis + non-destructive probing harness and the
  clause-diff/probe corpus are the natural release artifacts; not yet built, so not
  claimed as available; any destructive-probe finding is gated behind coordinated
  disclosure.

## Hand-off

This is a Markdown draft, not a finished paper — experiments have not run. Natural
next steps: run the pilot sweep (one protocol, one directory) to instantiate the
Result placeholders, or return to this pipeline if a stage needs revision (e.g. if
the pilot shows the reference-discrimination rate in RQ1 is far below 95%, that is a
blocking instrument-validity problem that surfaces only once a real spec diff is
probed).
