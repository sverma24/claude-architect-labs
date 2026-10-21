"""WALKTHROUGH ONLY: the same extraction as a Message Batches job, as you'd run it overnight on the API.

The course shows this file on screen; the lab doesn't run it, because the Batches API needs an Anthropic
API key (the rest of the labs run on a Claude subscription). What it shows:
  - 50% cheaper, but results can take up to 24 hours and there's no latency guarantee
    -> fine for nightly invoice runs, wrong for anything someone is waiting on
  - every request carries a custom_id, and results come back in ANY order, so match them by custom_id
  - a batch is one request -> one response: no multi-turn tool calling inside a batch request
  - resubmit only the requests that failed, fixed (e.g. split a document that was too long)
"""
import json
import time
from pathlib import Path

import anthropic
from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.messages.batch_create_params import Request

HERE = Path(__file__).parent
SCHEMA = json.loads((HERE / "invoice.schema.json").read_text())
PROMPT = (HERE / "prompts/extract.md").read_text()
client = anthropic.Anthropic()


def request_for(doc: Path) -> Request:
    return Request(
        custom_id=doc.stem,  # how each result finds its document again
        params=MessageCreateParamsNonStreaming(
            model="claude-opus-5-5",
            max_tokens=16000,
            messages=[{"role": "user", "content": PROMPT + "\n" + doc.read_text()}],
            output_config={"format": {"type": "json_schema", "schema": SCHEMA}},
        ),
    )


docs = {d.stem: d for d in sorted((HERE / "docs").glob("*.txt"))}
batch = client.messages.batches.create(requests=[request_for(d) for d in docs.values()])
print(f"Batch {batch.id}: {batch.processing_status}")

while (batch := client.messages.batches.retrieve(batch.id)).processing_status != "ended":
    time.sleep(60)  # most batches finish within an hour; the limit is 24 hours

failed = []
for result in client.messages.batches.results(batch.id):
    if result.result.type == "succeeded":
        text = next(b.text for b in result.result.message.content if b.type == "text")
        print(result.custom_id, json.loads(text)["vendor"])
    else:
        failed.append(result.custom_id)  # errored or expired: resubmit just these

if failed:
    retry = client.messages.batches.create(requests=[request_for(docs[c]) for c in failed])
    print(f"Resubmitted {len(failed)} documents as batch {retry.id}")
