import json, re

def bibkey(k):
    return k

def escape(s):
    if s is None:
        return ""
    return s.replace('&', '\\&').replace('%', '\\%').replace('_', '\\_')

recs = []
with open('reference_candidates.jsonl') as f:
    for line in f:
        line = line.strip()
        if not line: continue
        r = json.loads(line)
        if r.get('verdict') == 'selected':
            recs.append(r)

entries = []
for r in recs:
    key = bibkey(r['key'])
    title = escape(r.get('title') or '')
    year = r.get('year') or ''
    venue = r.get('venue') or ''
    url = r.get('url') or ''
    ids = r.get('ids') or {}
    arxiv = ids.get('arxiv')
    # Optional verified author string (BibTeX `A and B and ...` form), captured in the
    # jsonl record from arXiv API metadata; emitted verbatim when present.
    author_line = ""
    if r.get('bib_authors'):
        author_line = f"  author = {{{r['bib_authors']}}},\n"
    if arxiv:
        entry = (
            f"@article{{{key},\n"
            f"{author_line}"
            f"  title = {{{{{title}}}}},\n"
            f"  year = {{{year}}},\n"
            f"  journal = {{arXiv preprint arXiv:{arxiv}}},\n"
            f"  eprint = {{{arxiv}}},\n"
            f"  archivePrefix = {{arXiv}},\n"
            f"  url = {{{url}}}\n"
            f"}}"
        )
    else:
        entry = (
            f"@misc{{{key},\n"
            f"{author_line}"
            f"  title = {{{{{title}}}}},\n"
            f"  year = {{{year}}},\n"
            f"  howpublished = {{{escape(venue)}}},\n"
            f"  note = {{Accessed via {escape(venue)}}},\n"
            f"  url = {{{url}}}\n"
            f"}}"
        )
    entries.append(entry)

with open('refs.bib', 'w') as f:
    f.write("% Auto-generated from reference_candidates.jsonl's `selected` records. Do not hand-edit — regenerate via gen_refs_bib.py.\n\n")
    f.write("\n\n".join(entries) + "\n")

print(f"Wrote {len(entries)} entries to refs.bib")
