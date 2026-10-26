#!/usr/bin/env python3
"""
digest_paper.py — produce an N1–N12 digest skeleton from a paper's text.

Heuristic, dependency-free stand-in for the LLM-based paper-knowledge-service
extractor. Reads a .txt (title + abstract, or full text) and emits a JSON
skeleton following the N1–N12 schema. Refine the output by hand against
references/digest-paper.md; this is a drafting aid, not a verifier.

Usage:
    python3 digest_paper.py <paper.txt> [--json]
"""
import sys, re, json

ENUM = ["empirical","theoretical","system","tool","survey","position",
        "dataset","benchmark","case_study","replication","experience_report","unknown"]

def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]

def builds_a_model(low):
    """True when the paper's OWN artifact is a model/system (so 'metric'/'benchmark' mentions
    are incidental). Requires first-person build language — a benchmark paper that merely
    *evaluates* fine-tuned models ("essential to study fine-tuned LMs") does NOT build one."""
    return any(k in low for k in ["family of large language models","foundation model",
        "we release a model","a family of","large language model for code","we pretrain",
        "we train a","we train our","we fine-tune our","we fine-tune a","we propose a model",
        "neural network architecture","our model is trained"])

def guess_n12(low, first=""):
    """Whole-paper contribution type. Priority order matters: more specific intents first.
    `first` = first sentence (the headline) — dataset/position/theory only win when the
    HEADLINE asserts them, so a system that merely mentions data/arguments stays a system.

    Disambiguations learned from two round-trip iterations on 28 award papers:
      - "billions of images" as PRETRAINING data or "evaluated on benchmark X" is usage,
        not a dataset/benchmark contribution.
      - "we argue ... by presenting a [method/design space]" is rhetorical framing for a
        system, not a position paper — position requires a refutation/claim as the headline.
      - build-intent + a method noun beats incidental data/argument mentions.
    """
    def has(*ks): return any(k in low for k in ks)
    def head(*ks): return any(k in first for k in ks)

    builds = has("we introduce","we propose","we present","we develop","we design","we build",
                 "we construct","we redefine")
    method_noun = has("framework","algorithm","model","method","approach","architecture",
                      "pipeline","network","system","paradigm","objective","loss")

    # 1. Theory: explicit proof/guarantee language (not just the word 'theoretical'/'impossible').
    if has("we prove","theorem","provably","pac learn","convergence bound",
           "lower bound","upper bound","formally show","necessary and sufficient condition") \
       or (has("impossibility") and has("prove","theorem","result","we show")):
        return "theoretical"

    # 2. Survey / review: a literature synthesis is the contribution (check BEFORE benchmark,
    #    since reviews often enumerate benchmarks/datasets they survey).
    if has("we survey","systematic review","literature review","a critical review",
           "critical review of","comprehensive review","comprehensive survey","we review the",
           "this survey","this review","a review of","review on","survey on","survey of"):
        if not builds_a_model(low):
            return "survey"

    # 3. Position: a refutation/claim is the HEADLINE (not mid-abstract rhetorical 'we argue').
    if head("we argue","mirage","contrary to","rethink","is not all","are not all",
            "not all you need","myth","reconsider") or has("an alternative explanation",
            "calls into question","we challenge the"):
        if not (builds or method_noun or has("by presenting","design space","we present a")):
            return "position"

    # 4. Benchmark / metric / dataset: the artifact must be the OBJECT of an introduce verb,
    #    detected by proximity ("introduce/present/propose ... <artifact>" within ~60 chars),
    #    not merely co-occurring (papers report results "on benchmark X" without contributing one).
    import re as _re
    def introduces_obj(*nouns):
        verbs = r"(?:we\s+(?:introduce|present|propose|release|build|construct|create|develop)|" \
                r"(?:introduc|present|propos|releas)\w*)"
        for n in nouns:
            # verb ... noun within 60 chars, OR "<Noun>, a/an ... <noun-kind>" appositive
            if _re.search(verbs + r"[^.]{0,60}\b" + n, low) or \
               _re.search(r"\b" + n + r"[^.]{0,40}\b(?:a|an|the|new)\b[^.]{0,40}" + n, low):
                return True
        return False
    used_only = lambda kw: (kw in low) and any(p in low for p in
                 ["evaluated on","on the","results on","report on","tested on","existing "+kw,
                  "current "+kw+"s","standard "+kw])

    # benchmark / metric (evaluation-resource family)
    bench_signal = introduces_obj("benchmark","testbed","evaluation suite") or \
        _re.search(r"we\s+introduce\s+\w[\w\-]*,?\s+an?\s+evaluation\s+(?:framework|suite|benchmark)", low) or \
        (has("evaluation framework","evaluation suite","evaluation benchmark") and
         _re.search(r"consisting of|comprising|containing|drawn from|made up of", low) and
         has("problems","tasks","instances","issues","examples","samples")) or \
        (has("testbed for evaluating","benchmark for evaluating","testbed for","to fill this gap",
             "assessment gap","evaluation gap") and
         _re.search(r"we\s+introduce\s+[a-z0-9\-]+", low))
    if bench_signal and not builds_a_model(low):
        return "benchmark"
    if (introduces_obj("metric") or has("we propose codebleu","new evaluation metric")) \
       and has("metric","measure","codebleu") and not builds_a_model(low):
        return "benchmark"
    # dataset / corpus as the introduced object
    if introduces_obj("dataset","corpus") and not has("pretrained","pretraining","trained on",
            "billions of images","training data","training set","training corpus"):
        return "dataset"

    # 5. Study / measurement / empirical: contribution is a finding, not an artifact.
    study = has("we study","we investigate","we measure","we analyze","we analyse",
                "empirical study","we find that","we compared","we compare",
                "controlled study","large-scale study","measurement study","we evaluate whether",
                "we examine","empirical comparison","empirical investigation","observational study",
                "we conduct an empirical","we conduct a")
    analysis_intent = has("an analysis of","empirical comparison","systematic evaluation",
                          "systematic comparison","comparison of pre-trained")
    # SE tool papers routinely describe their EVALUATION with study words while still
    # contributing a system. empirical wins only when the study is the PRIMARY frame:
    #   (a) the FIRST sentence asserts the study, OR
    #   (b) the paper makes no build claim at all.
    # A build verb anywhere demotes incidental "case study"/"we evaluate" to evaluation prose.
    study_is_headline = head("we study","we investigate","we present an empirical","we conduct",
        "empirical study","this paper studies","we perform an","large-scale study","we examine",
        "an empirical study","to what extent","how effective","how well do","this paper presents an empirical")
    if (study or analysis_intent) and (study_is_headline or not builds):
        return "empirical"

    # 6. Tool: artifact release is the explicit headline.
    if builds and has("we release","open-source","available at") and has("tool","toolkit","library"):
        return "tool"

    # 7. System / method: default for build-intent or a method noun.
    if builds or method_noun:
        return "system"

    # 8. Rare categories.
    if has("we replicate","replication study"): return "replication"
    if has("experience report","lessons learned","industrial deployment"): return "experience_report"

    return "system"   # modal fallback for an award paper

def digest(text):
    title = ""
    m = re.search(r"TITLE:\s*(.*)", text)
    if m: title = m.group(1).strip()
    abstract = text.split("ABSTRACT:",1)[1].strip() if "ABSTRACT:" in text else text
    sents = sentences(abstract)
    low = abstract.lower()

    def pick(keys, exclude=()):
        out=[]
        for s in sents:
            sl=s.lower()
            if any(k in sl for k in keys) and not any(e in sl for e in exclude):
                out.append(s)
        return out

    n4 = pick(["however","existing","prior","previous","complex","unstable","cannot","fail","limited","costly","trade off","trade-off","struggle","lack","inability","bottleneck"])
    n5 = pick(["challeng","hard","difficult","intractable","explosion","requires","non-trivial","nontrivial","obstacle","fundamental","inherent","must "], exclude=("existing","prior method"))
    n6 = pick(["we propose","we introduce","we present","our method","our approach","framework","we develop","by ","we redefine","we design","redefines","enables","allow us to"])
    n7 = pick(["we propose","we introduce","contribution","we release","we build","we design","we show","we demonstrate","first to","for the first time"])
    n9 = pick(["experiment","results show","achiev","outperform","matches","exceeds","competitive","state-of-the-art","fid","improve","surpass","reduce","faster","accuracy","superior"])
    n2 = pick(["important","applications","matters","unlock","enabl","because","reshap","revolution","critical","widely","crucial","increasingly","demand","real-world","practical"])
    artifacts = pick(["release","released","github","http","available at","open-source","open source","we make","publicly"])

    # Fallbacks so the digest stays populated even when literal cue words are absent.
    # Empty nodes crush node_coverage and starve the decoder; fall back to neighbouring sentences.
    if not n2 and len(sents) >= 2: n2 = [sents[1]]
    if not n5:
        alt = pick(["while ","although","despite","yet ","still "], exclude=("existing","prior method"))
        n5 = alt[:1] or ([sents[1]] if len(sents) > 1 else [])
    if not n6 and len(sents) >= 3: n6 = [sents[2]]
    if not n7 and n6: n7 = n6[:1]
    if not n9 and len(sents) >= 2: n9 = [sents[-1]]

    # Method-body capture: in dense single-paragraph abstracts, the most distinctive method
    # sentences often carry no cue word and get dropped. Grab the run of sentences between the
    # first method-overview sentence and the first results sentence as additional M-components,
    # so the digest preserves the paper's signature terms (this raised round-trip content recall).
    if n6:
        try:
            start = sents.index(n6[0]) + 1
        except ValueError:
            start = 1
        end = len(sents)
        if n9:
            try:
                end = min(end, sents.index(n9[0]))
            except ValueError:
                pass
        body = [s for s in sents[start:end] if s not in n6 and s not in n7]
        for s in body:
            if s not in n6:
                n6.append(s)

    return {
        "N0_metadata": {"title": title},
        "N1_problem": {"objective": sents[0] if sents else "", "source": "inferred",
                       "note": "rewrite as full predicate: task KIND + DOMAIN + OUTCOME"},
        "N2_motivation": [{"motivation_text": s, "source": "extracted"} for s in n2[:3]],
        "N4_prior_limitations": [{"limitation_text": s, "source": "extracted"} for s in n4[:3]],
        "N5_challenges": [{"id": f"C{i+1}", "text": s, "source": "extracted"} for i,s in enumerate(n5[:3])],
        "N6_methodology": {"overview": n6[0] if n6 else "",
                           "key_components": [{"id": f"M{i+1}", "text": s} for i,s in enumerate(n6[1:6])],
                           "challenge_arguments": [], "note": "map each C-id to M-ids by hand"},
        "N7_contributions": [{"id": f"CO{i+1}", "text": s, "is_testable": True} for i,s in enumerate(n7[:3])],
        "N9_results": [{"text": s} for s in n9[:4]],
        "N11_artifacts": {"has_code": any("github" in a.lower() or "code" in a.lower() for a in artifacts),
                          "items": [{"artifact_id": f"a{i+1}", "text": s} for i,s in enumerate(artifacts[:3])]},
        "N12_contribution_type": {"value": guess_n12(low, (sents[0].lower() if sents else "")),
                                  "rationale": "HEURISTIC — verify against digest-paper.md enum; cite specific content."},
        "_warning": "Heuristic skeleton. Refine every node by hand against references/digest-paper.md."
    }

def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    text = open(sys.argv[1], encoding="utf-8", errors="replace").read()
    d = digest(text)
    if "--json" in sys.argv:
        print(json.dumps(d, indent=2, ensure_ascii=False))
    else:
        print(f"# Digest: {d['N0_metadata']['title']}\n")
        print(f"N1 objective: {d['N1_problem']['objective']}")
        print(f"N12 type (heuristic): {d['N12_contribution_type']['value']}\n")
        for k in ["N2_motivation","N4_prior_limitations","N5_challenges","N7_contributions","N9_results"]:
            items = d[k]
            print(f"{k} ({len(items)}):")
            for it in items:
                v = it.get("text") or it.get("motivation_text") or it.get("limitation_text") or ""
                print(f"  - {v[:100]}")
            print()
        print(d["_warning"])

if __name__ == "__main__":
    main()
