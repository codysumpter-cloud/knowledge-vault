# Telegram `/model` Picker on VPS

## Symptom

On a remote Hermes gateway, `/model` in Telegram should open inline keyboard bubbles for provider/model selection. Instead, Hermes sends a text fallback asking the user to type the full provider and model name.

Common log clue:

```text
send_model_picker failed: Message thread not found
```

## Cause

The Telegram adapter sends the inline-keyboard picker directly via `bot.send_message(...)`. On VPS gateways with stale or invalid Telegram topic/thread metadata, Telegram can reject `message_thread_id` with `Message thread not found`. Because this direct picker path historically did not use the normal send retry/fallback logic, gateway falls back to text instructions.

## Fix pattern

Patch `gateway/platforms/telegram.py` in `send_model_picker` so the initial send is built as `send_kwargs`, then catches Telegram thread errors and retries after removing topic metadata:

```python
try:
    msg = await self._bot.send_message(**send_kwargs)
except Exception as exc:
    if "thread not found" not in str(exc).lower():
        raise
    logger.info(
        "[%s] send_model_picker retrying without thread metadata after: %s",
        self.name,
        exc,
    )
    fallback_kwargs = dict(send_kwargs)
    fallback_kwargs.pop("message_thread_id", None)
    fallback_kwargs.pop("direct_messages_topic_id", None)
    fallback_kwargs.pop("reply_to_message_id", None)
    msg = await self._bot.send_message(**fallback_kwargs)
```

For newer codebases that have `_is_thread_not_found_error()` and `_thread_kwargs_for_send()`, prefer those helpers over raw string matching.

## Deploy on a VPS

```bash
python3 -m py_compile /home/hermes/.hermes/hermes-agent/gateway/platforms/telegram.py
systemctl restart hermes-gateway.service
journalctl -u hermes-gateway.service -n 40 --no-pager
```

If Hermes is not installed as a service, restart the foreground/nohup process that runs `hermes gateway run --replace`.

## Verification

1. Confirm code patch exists:

```bash
grep -n "send_model_picker retrying without thread metadata" \
  /home/hermes/.hermes/hermes-agent/gateway/platforms/telegram.py
```

2. Confirm gateway is active:

```bash
systemctl is-active hermes-gateway.service
```

3. In Telegram, send:

```text
/model
```

Expected: provider buttons/bubbles appear. Tapping a provider drills into model buttons.

## Related domain/Web UI note

Do not treat a broken Telegram model picker as a DNS or Nginx issue. If the Web UI is reachable by direct VPS IP but the user's production domain already has working Hostinger/Cloudflare routing, avoid DNS changes unless explicitly authorized. Prefer a subdomain such as `hermes.<domain>` only after the user approves the DNS record.
