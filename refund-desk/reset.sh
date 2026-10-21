#!/bin/zsh
# Put the lab back to its starting state between demo runs.
cd ${0:A:h}
rm -rf .claude/state .claude/last_tool_call.json data/.gateway_tried data/refunds.jsonl data/escalations.jsonl
echo "refund-desk reset"
