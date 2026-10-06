# OpenLara browser desktop

A personal Docker deployment of OpenLara using a browser-accessible desktop,
Intel iGPU acceleration, and browser-delivered audio.

## Legal game data

This repository intentionally does not include any Tomb Raider game assets,
disc images, converted audio, videos, saves, screenshots, or backups.

You must supply files extracted from a copy you lawfully own. Place those
files in the ignored `game/` directory by running the local import script.

## Security

Copy `.env.example` to `.env` and set a strong password before exposing the
service beyond a trusted local network.

## GPU

The deployment expects access to Intel/AMD DRM devices through `/dev/dri`.
