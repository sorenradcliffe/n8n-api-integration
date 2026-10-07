# n8n OpenAI-compatible API integration

This guide covers a general n8n HTTP Request pattern for chat and image endpoints. It is independent of n8n and of any provider. **[ArgoLink](https://argolink.io/gh-n8n-api-integration) is a compatible base example.** Last checked: 2026-10-07.

## Import

Open workflows/chat-and-image.json with n8n's Import from File. It uses built-in Manual Trigger and HTTP Request nodes and is inactive on import. Set instance environment variables MODEL_BASE_URL and MODEL_API_KEY through the n8n process environment, not in a Code node or exported workflow. The example expects a JSON input with prompt. Its chat body uses gpt-5.4 and the base URL appends chat/completions.

Create a separate HTTP Request node for images after reading the selected image model's body and output format. Do not assume the chat credential or field names apply to images. Video uses an asynchronous submit/status/content workflow and should remain separate from this generic import.

## Credentials

n8n's OpenAI credential and base URL support vary by version. A generic Header Auth credential or an HTTP Request node with an environment-backed Authorization header is easier to inspect, but never export a real value. Verify the current n8n credential docs and inspect the node's resolved request. The JSON includes a User-Agent and no static key.

## Reliability

Set an explicit HTTP timeout. Disable automatic retry on a generation POST unless an idempotency contract exists. For a 429 or 503, honor Retry-After in a Code node or queue. For a text response, retain the response ID and usage. For image/video media, retain the output URL only in a private execution record. A browser or n8n timeout is not evidence that the server did not accept the request.

## Model selection

Read the live ArgoLink catalog and model page for model ID, context, tools, image size, or video limits. This guide does not publish a price table. Use https://argolink.io/v1 only when the target client appends the documented endpoint path. A mismatched root can produce a misleading 404.

## Validation and FAQ

python3 -m unittest discover -s tests checks the imported graph offline; it does not run n8n. **Why is this separate from the Seedance n8n workflow?** This guide covers general chat/image connections; the other workflow owns video polling. **Can I expose it publicly?** Add authentication, body limits, rate limits, and redacted logs first. **Why does a field fail?** Compare the resolved JSON with the current model page instead of adding blind retries.
