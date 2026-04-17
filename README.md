# jarvis-device-schlage

Schlage Encode WiFi smart lock integration for [Jarvis](https://github.com/alexberardi/jarvis-node-setup).

## Supported Devices

- Schlage Encode (BE489)
- Schlage Encode Plus (BE499)
- Schlage Encode Lever (FE789)

## Actions

| Action | Description |
|--------|-------------|
| `lock` | Lock the door |
| `unlock` | Unlock the door |
| `get_status` | Get lock state, jammed status, and battery level |

## Setup

1. Install from the Jarvis Pantry or directly:
   ```
   python scripts/command_store.py install --url https://github.com/alexberardi/jarvis-device-schlage
   ```
2. Set your Schlage Home app credentials in node settings:
   - **Email**: Your Schlage account email
   - **Password**: Your Schlage account password
3. Scan for devices in the mobile app

## How It Works

Uses [pyschlage](https://pypi.org/project/pyschlage/) to communicate with the Allegion/Yonomi cloud API — the same backend the Schlage Home app uses. No local API is available for Encode locks.

Credentials are stored encrypted on the node (pysqlcipher) and never leave it.

## License

MIT
