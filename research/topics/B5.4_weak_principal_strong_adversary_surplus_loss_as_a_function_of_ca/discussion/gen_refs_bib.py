import json, re

def bibkey(k):
    return re.sub(r'[^A-Za-z0-9]', '', k)

def esc(s):
    return s.replace('&', r'\&')

recs = [json.loads(l) for l in open('discussion/reference_candidates.jsonl') if l.strip()]
sel = [r for r in recs if r.get('verdict') == 'selected']

entries = []
for r in sel:
    key = bibkey(r['key'])
    title = esc(r.get('title', ''))
    year = r.get('year', '')
    venue = r.get('venue', '') or 'arXiv'
    url = r.get('url', '')
    arxiv = (r.get('ids') or {}).get('arxiv')
    if arxiv:
        entries.append(f"""@misc{{{key},
  title = {{{{{title}}}}},
  year = {{{year}}},
  eprint = {{{arxiv}}},
  archivePrefix = {{arXiv}},
  url = {{{url}}}
}}""")
    else:
        entries.append(f"""@misc{{{key},
  title = {{{{{title}}}}},
  year = {{{year}}},
  howpublished = {{{esc(venue)}}},
  url = {{{url}}}
}}""")

with open('discussion/refs.bib', 'w') as f:
    f.write('\n\n'.join(entries) + '\n')

print(f"Wrote {len(entries)} entries to discussion/refs.bib")
