# VPS gateway systemd restart receipts and pitfalls

Use this when restarting Hermes Gateway on the Sovereign Cloud VPS or any Linux host with a user-level `hermes-gateway.service`.

## Reliable restart sequence

1. Find the service user UID:

```bash
id -u hermes
loginctl show-user hermes -p RuntimePath -p Linger -p State
```

2. Patch the user service to use a safe workdir if it points into a risky/default path:

```bash
grep WorkingDirectory /home/hermes/.config/systemd/user/hermes-gateway.service
# Preferred for Prismtek/BMO VPS:
# WorkingDirectory=/opt/buddy-brain
```

3. Restart via the user bus with the *correct* runtime dir. Do not assume `/run/user/1000`; verify the UID first.

```bash
sudo -u hermes env XDG_RUNTIME_DIR=/run/user/1001 systemctl --user daemon-reload
sudo -u hermes env XDG_RUNTIME_DIR=/run/user/1001 systemctl --user restart hermes-gateway.service
sleep 5
sudo -u hermes env XDG_RUNTIME_DIR=/run/user/1001 systemctl --user --no-pager status hermes-gateway.service
```

## Verification receipts

```bash
ps -eo pid,user,cmd | grep -E 'hermes.*gateway|gateway run|hermes_cli.main' | grep -v grep
sudo -u hermes env XDG_RUNTIME_DIR=/run/user/1001 journalctl --user -u hermes-gateway.service --since '<restart timestamp>' --no-pager \
  | grep -Ei 'error|exception|traceback|failed|429|401|permission|empty response|gemini|gemma' || true
```

If `~/.hermes/logs/gateway.log` does not exist, that is not proof of no logging. The installed systemd unit may send stdout/stderr to journald (`StandardOutput=journal`, `StandardError=journal`), so `journalctl --user -u hermes-gateway.service` is the receipt source.

## Pitfalls observed

- Starting `hermes gateway run` over SSH in a background tool can keep the local tool session alive, but it is not the durable service state. Prefer restarting the installed user service and verify with `systemctl --user status`.
- `Failed to connect to bus: No such file or directory` usually means the wrong `XDG_RUNTIME_DIR` was used. Check `id -u hermes`; on the VPS it was `1001`, not `1000`.
- `pkill -f 'hermes_cli.main gateway run'` inside the same SSH command may kill the command/session that is trying to continue the restart. Stop and restart as separate actions or use systemd restart directly.
- Post-restart error checks must be timestamp-filtered; stale pre-restart provider errors are misleading.
