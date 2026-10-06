# OpenLara Browser Desktop

A Docker-based, browser-accessible OpenLara desktop for legally owned
Tomb Raider files. It runs a lightweight Linux desktop environment with
OpenLara, Selkies streaming, GPU-accelerated H.264 encoding, browser audio,
persistent saves, and HTTP Basic authentication.

This repository contains only the reproducible deployment configuration.
Proprietary game assets, saves, credentials, certificates, and logs are
excluded from Git.

## Features

- Browser-based OpenLara desktop
- Selkies streaming over HTTPS
- Intel iGPU VA-API H.264 encoding
- Browser audio via PulseAudio-compatible output
- Persistent OpenLara saves
- Local file-transfer directory
- HTTP Basic authentication
- Self-signed TLS certificate
- Docker Compose deployment
- Automatic OpenLara startup

## Requirements

- Docker with Compose V2
- An Intel GPU with VA-API support
- `/dev/dri` available on the host
- A legally owned copy of Tomb Raider
- A local directory for extracted game assets

## Repository layout

    Dockerfile
    compose.yaml
    root/
    ├── custom-cont-init.d/
    │   └── 10-openlara-autostart
    └── etc/
        └── nginx/
            └── sites-enabled/
                └── default

    .env.example
    .gitignore
    README.md
    import-game.sh

## Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd open-lara
```

### 2. Create local configuration

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and set:

- `DESKTOP_USER`
- `DESKTOP_PASSWORD`
- `TZ`
- Any other deployment-specific values

Never commit `.env`.

### 3. Prepare the game directory

Create a local game directory:

```bash
mkdir -p game
```

Extract the required files from your legally owned Tomb Raider copy into
`game/`. The exact required files depend on your game edition and OpenLara
version.

The `game/` directory is ignored by Git and must never be published.

### 4. Import game assets

The included import script copies local assets into the persistent Docker
game directory:

```bash
./import-game.sh /path/to/your/legal/tomb-raider-files
```

Review the script before use and adjust paths for your local game edition.

### 5. Build and start

```bash
docker compose --env-file .env build
docker compose --env-file .env up -d
```

Check status:

```bash
docker compose ps
docker compose logs -f
```

## Browser access

Open the HTTPS URL exposed by the Compose configuration.

The default configuration uses a self-signed certificate, so the browser will
show a certificate warning. This is expected for a private LAN deployment.

Sign in using the username and password configured in `.env`.

## Saving games

Use the OpenLara save hotkey:

```text
5
```

Saved games persist in the host-side `saves/.openlara/` directory and remain
available after container recreation.

## Browser compatibility

| Browser | Streaming notes |
|---|---|
| Microsoft Edge | H.264/VA-API streaming works |
| Opera | Select the JPEG encoder in the Selkies video sidebar |

## Security notes

- Change the default password before exposing the service beyond a trusted LAN.
- Keep `.env`, certificates, authentication hashes, saves, and game assets private.
- The included self-signed certificate is suitable for private LAN use only.
- Do not expose this service directly to the public internet without additional
  hardening, such as a reverse proxy, firewall rules, and stronger secrets.

## Backup

Back up the entire deployment directory, including ignored local files:

```bash
tar --acls --xattrs --numeric-owner \
    -czf open-lara-backup.tar.gz \
    -C / \
    path/to/docker-compose/open-lara
```

Verify the archive:

```bash
gzip -t open-lara-backup.tar.gz
tar -tzf open-lara-backup.tar.gz > /dev/null
sha256sum open-lara-backup.tar.gz > SHA256SUMS
sha256sum -c SHA256SUMS
```

The backup will contain credentials and proprietary assets, so store it
privately.

## License

This repository contains deployment configuration only. It does not include,
distribute, or license any proprietary Tomb Raider game files. Users must
supply assets extracted from a legally owned copy.
