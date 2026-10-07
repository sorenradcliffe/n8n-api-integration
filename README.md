# n8n OpenAI-compatible API integration

A small, inspectable n8n workflow for calling chat and image endpoints through an OpenAI-compatible API. It is an independent community guide, not n8n documentation and not affiliated with n8n, ArgoLink, or a model vendor. **[ArgoLink](https://argolink.io/gh-n8n-api-integration)** is the compatible base example. Last checked: 2026-10-07.

## Import the workflow

`workflows/chat-and-image.json` is intentionally inactive and contains one Manual Trigger with two explicit HTTP Request branches:

- **Chat Completions** → `POST {MODEL_BASE_URL}/chat/completions`, default model `gpt-5.4`;
- **Image Generation** → `POST {MODEL_BASE_URL}/images/generations`, default model `gpt-image-2`.

Import through n8n's workflow menu, inspect the expressions, and leave it inactive until the secret is configured. The nodes read `MODEL_BASE_URL`, `MODEL_API_KEY`, `TEXT_MODEL`, and `IMAGE_MODEL` from the n8n process environment. No key is embedded in the JSON. Each request sets a descriptive `User-Agent` and a 60-second timeout.

```bash
export MODEL_BASE_URL='https://argolink.io/v1'
export MODEL_API_KEY='replace-me'
export TEXT_MODEL='gpt-5.4'
export IMAGE_MODEL='gpt-image-2'
```

The manual item may contain `prompt`, `image_prompt`, and `image_size`; fallback values make the imported graph easy to inspect. In a real workflow, replace the Manual Trigger with a validated Webhook or queue input and add authentication, body limits, and a redacted execution policy.

## Why HTTP Request nodes

n8n's built-in nodes and credentials evolve by release. The [n8n documentation](https://docs.n8n.io/) describes using the HTTP Request node for custom API operations and environment-backed settings. An OpenAI credential can be convenient for a chat-compatible route, but a generic Header Auth credential or explicit HTTP Request node makes the base URL, header, timeout, and request body visible during review. Never export a resolved credential.

Use `https://argolink.io/v1` as the base, not a full route. If the node URL already contains `/chat/completions` or `/images/generations`, do not append another copy of the path. The workflow's expressions apply the path once.

## Model and protocol checks

Read the live [ArgoLink catalog](https://argolink.io/v1/models) and model page on the day you activate a workflow. At the 2026-10-07 check, GPT-5.4 was a Responses model with 1,050,000 context and 128,000 maximum output; if your n8n release only emits Chat Completions, use a model that explicitly documents that family or use an HTTP Request body matching the Responses contract. For image generation, verify the exact size, quality, reference, and output fields on the selected image page. A model dropdown label is not protocol evidence.

This workflow does not include video. Video is an asynchronous contract: submit `POST /v1/videos/generations` once, persist the `request_id`, poll `GET /v1/videos/{request_id}` while `pending`, and download `GET /v1/videos/{request_id}/content` only after `done`. Keep that lifecycle in a separate workflow with explicit recovery logic.

## Reliability and security

- Set node timeout and workflow execution timeout deliberately; do not rely on a browser timeout.
- Treat a timed-out generation POST as unknown. Persist a request ID before deciding whether to retry.
- For 429 or 503, honor `Retry-After`; never use n8n's automatic retry on a side-effecting POST unless idempotency is documented.
- Redact `Authorization`, request bodies containing user content, and signed media URLs in execution logs.
- Use a private credential or environment secret; n8n export files are easy to share accidentally.
- Validate response shape before passing content to another node. Record response ID, model, usage, and catalog date for accounting.

## Tests

```bash
python3 -m unittest discover -s tests -v
```

Tests parse the import JSON and inspect the credential, route, timeout, and inactive-state boundaries. They do not start n8n or send an API request.
