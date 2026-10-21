#!/bin/zsh
# CI code review with Claude Code, the way a pipeline runs it:
#   1. one focused pass per changed file    (claude -p, its own session each time)
#   2. one integration pass across files     (catches what no single file shows)
#   3. merged JSON findings -> PR comments
# usage: ./review.sh            normal review
#        ./review.sh --vague    the same PR with a vague prompt and no criteria, for comparison
#        ./review.sh --rerun    re-review after new commits: report only new or still-open issues
set -e
cd ${0:A:h}
mkdir -p out
SCHEMA=$(cat findings.schema.json)
mode=${1:-normal}
changed=(${(f)"$(cd pr && find inventory -name '*.py' | sort)"})

review() {   # review <name> <prompt file> <input text>
  # -p: non-interactive, no prompts to hang the job.  --tools "": review only, no file or shell access.
  claude -p "$(cat $2)

$3" --output-format json --json-schema "$SCHEMA" --tools "" > out/$1.raw.json
  python3 -c "import json;print(json.dumps(json.load(open('out/$1.raw.json'))['structured_output']))" > out/$1.json
  echo "  $1: $(python3 -c "import json;print(len(json.load(open('out/$1.json'))['findings']))") findings"
}

if [[ $mode == --vague ]]; then
  all=$(for f in $changed; do diff -u base/$f pr/$f || true; done)
  echo "Vague single-pass review of ${#changed} files"
  review vague prompts/vague_review.md "Pull request diff:
$all"
  exit 0
fi

prior=""
[[ $mode == --rerun && -f out/findings.json ]] && prior="Findings already posted on this PR:
$(cat out/findings.json)
Report only issues that are new or still not fixed in the code below. Don't repeat fixed ones."

echo "Per-file passes (${#changed} files, each in its own session)"
for f in $changed; do
  [[ -f base/$f ]] && d=$(diff -u base/$f pr/$f || true) || d="(new file)"
  [[ -z $d ]] && continue
  review ${f:t:r} prompts/file_review.md "$prior
File: $f
Diff:
$d

Full new version of $f:
$(cat -n pr/$f)"
done

echo "Integration pass"
all=$(for f in $changed; do echo "=== $f"; cat -n pr/$f; done)
review integration prompts/integration_review.md "$prior
All changed files in the pull request (new versions):
$all"

python3 - <<'PY'
import json, glob
findings = []
for p in sorted(glob.glob("out/*.json")):
    if p.endswith((".raw.json", "findings.json", "vague.json")):
        continue
    findings += json.load(open(p))["findings"]
rank = {"critical": 0, "major": 1, "minor": 2}
findings.sort(key=lambda f: (rank[f["severity"]], f["file"], f["line"]))
json.dump(findings, open("out/findings.json", "w"), indent=2)
print(f"\n{len(findings)} PR comments:")
for f in findings:
    print(f"  [{f['severity']}] {f['file']}:{f['line']}  {f['issue']}  -> {f['fix']}")
PY
