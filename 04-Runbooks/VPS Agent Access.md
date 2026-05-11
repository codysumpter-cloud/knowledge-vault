# VPS Agent Access

## Alpaca
- VPS config path: `~/.hermes/secrets/alpaca.json`
- Mode: Paper trading (`use_paper: true`)
- Endpoint: `https://paper-api.alpaca.markets/v2`

## Verification Command
```bash
ssh root@187.77.223.224 'python3 - <<"PY"
import json, pathlib
p=pathlib.Path.home()/".hermes/secrets/alpaca.json"
d=json.loads(p.read_text())
print({"exists": p.exists(), "use_paper": d.get("use_paper"), "has_key": bool(d.get("api_key")), "has_secret": bool(d.get("api_secret"))})
PY'
```
