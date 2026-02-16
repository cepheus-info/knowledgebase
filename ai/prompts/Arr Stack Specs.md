Here are the finalized, production-ready prompts. These are the "Master Specs" that incorporate every architectural decision we have made: the "Atomic Move" storage strategy, the resource constraints, the expanded media types (Anime/Music/MV), and the Xray censorship circumvention.
You can copy and paste these directly into an AI coding assistant (like GitHub Copilot, ChatGPT, or back to me) to generate your exact configuration files.
Option 1: The "Laptop Lab" Prompt (PoC)
Best for: Your current 8GB Windows 11 Laptop.
Key Feature: Aggressive resource capping & local Xray proxying.

# ROLE
Act as a Senior DevOps Engineer. Generate a `docker-compose.yml` and `.env` file for a "Proof of Concept" Home Media Stack.

# ENVIRONMENT CONTEXT
* **Host:** Windows 11 running WSL2 (Ubuntu 22.04).
* **Hardware:** 8GB RAM total. **Strict Constraint:** The entire stack MUST use <3.5GB RAM.
* **Network:** Region-restricted internet (requires Xray proxy for metadata).

# ARCHITECTURE SPECIFICATION
## 1. Networking (Custom Bridge)
* **Network Name:** `media_net`
* **Subnet:** `172.20.0.0/24`
* **Gateway:** `172.20.0.1`
* **DNS:** Use internal Docker DNS.

## 2. Storage Strategy (Atomic Moves)
* **Unified Volume:** You MUST map `${HOST_DATA_PATH}:/data` for ALL media services.
* **Directory Structure (Internal):**
  - `/data/torrents` (Downloads)
  - `/data/media/{tv,movies,anime,music,music_videos}` (Library)
* **Forbidden:** Do not use separate volume mounts for downloads and media (prevents hardlinks).

## 3. Services & Resource Limits (Hard Caps)
* **Xray (Proxy):** Image `teddysun/xray`. Port `10808` (Socks), `10809` (HTTP). Mem: 64M.
* **Prowlarr:** Indexer Manager. Port `9696`. Mem: 128M.
* **Sonarr:** TV/Anime. Port `8989`. Mem: 256M. Env: `HTTP_PROXY=http://xray:10809`.
* **Radarr:** Movies. Port `7878`. Mem: 256M. Env: `HTTP_PROXY=http://xray:10809`.
* **Lidarr:** Music. Port `8686`. Mem: 256M. Env: `HTTP_PROXY=http://xray:10809`.
* **Bazarr:** Subtitles. Port `6767`. Mem: 128M.
* **Jellyseerr:** Request UI. Port `5055`. Mem: 300M.
* **qBittorrent:** Downloader. Port `8080`. Mem: 512M (Single Core).
* **Plex:** Media Server. Port `32400`. Mem: 1.5GB.
* **ytdl-sub:** Music Videos. Run-once container.

## 4. Proxy Configuration (Bypass GFW)
* **Sonarr/Radarr/Lidarr:** Must include `HTTP_PROXY`, `HTTPS_PROXY`, and `NO_PROXY` environment variables to route metadata traffic through the `xray` service while keeping local traffic (like `qbittorrent`) direct.
* **NO_PROXY Value:** `localhost,127.0.0.1,172.20.0.0/24,plex,qbittorrent`

# OUTPUT DELIVERABLES
1. **`.env` File:** Define `PUID=1000`, `PGID=1000`, `TZ=Asia/Shanghai`, and Paths.
2. **`docker-compose.yml`:** The complete, valid YAML file using `lscr.io/linuxserver` images.

Option 2: The "Synology NAS" Prompt (Production)
Best for: DS225+ (Intel J4125) with 18GB RAM.
Key Feature: Hardware Transcoding (QuickSync) & Performance.
# ROLE
Act as a Senior DevOps Engineer. Generate a "Production-Grade" `docker-compose.yml` for a Synology NAS (DS225+).

# ENVIRONMENT CONTEXT
* **Host:** Synology DSM 7.2.
* **Hardware:** Intel Celeron J4125 (Gemini Lake) w/ 18GB RAM.
* **Capability:** Intel QuickSync (Hardware Transcoding) is REQUIRED.

# ARCHITECTURE SPECIFICATION
## 1. Hardware Acceleration
* **Plex:** MUST map device `/dev/dri:/dev/dri` to enable `/dev/dri/renderD128`.
* **Privilege:** Grant necessary permissions for the container to access the GPU.

## 2. Storage & Permissions
* **Base Path:** `/volume1/docker/arr-stack` (Config).
* **Media Path:** `/volume1/data` (Content).
* **User Context:** `PUID=1026` (Typical Synology Admin).
* **Strategy:** Maintain the Unified Volume (`/data`) strategy for atomic moves.

## 3. Services & Configuration
* **Core Stack:** Xray, Prowlarr, Sonarr, Radarr, Lidarr, Bazarr, Jellyseerr, qBittorrent, Plex.
* **Proxy Integration:** Same `HTTP_PROXY` logic as the Lab environment to bypass blocked metadata agents.
* **Maintenance:** Add **Watchtower** to auto-update containers (Schedule: Every Sunday at 4 AM).

# OUTPUT DELIVERABLES
1. **`.env` File:** Tailored for Synology paths (`/volume1/...`).
2. **`docker-compose.yml`:**
   - Enable `restart: unless-stopped`.
   - Relax memory limits (e.g. Plex: 4GB, Others: 1GB) since hardware is upgraded.
   - Include specific comments on where to place the Xray `config.json`.

Bonus: The Xray config.json Template
Since the prompt asks for the file location but the AI might not generate the content of the Xray config (because it depends on your specific server provider), here is the standard "Client Side" template you need to save as config/xray/config.json.
You just need to paste your id (UUID), address (Server IP), and public key into this block:
{
  "log": { "loglevel": "warning" },
  "inbounds": [
    {
      "port": 10808,
      "protocol": "socks",
      "settings": { "auth": "noauth", "udp": true },
      "sniffing": { "enabled": true, "destOverride": ["http", "tls"] }
    },
    {
      "port": 10809,
      "protocol": "http",
      "settings": { "auth": "noauth", "udp": true }
    }
  ],
  "outbounds": [
    {
      "protocol": "vless",
      "settings": {
        "vnext": [
          {
            "address": "YOUR_VPS_IP",
            "port": 443,
            "users": [
              {
                "id": "YOUR_UUID",
                "encryption": "none",
                "flow": "xtls-rprx-vision"
              }
            ]
          }
        ]
      },
      "streamSettings": {
        "network": "tcp",
        "security": "reality",
        "realitySettings": {
          "fingerprint": "chrome",
          "serverName": "www.microsoft.com", 
          "publicKey": "YOUR_PUBLIC_KEY",
          "shortId": "YOUR_SHORT_ID",
          "spiderX": "/"
        }
      },
      "tag": "proxy"
    },
    {
      "protocol": "freedom",
      "tag": "direct"
    }
  ],
  "routing": {
    "domainStrategy": "IPIfNonMatch",
    "rules": [
      { "type": "field", "outboundTag": "direct", "domain": ["geosite:cn"] },
      { "type": "field", "outboundTag": "direct", "ip": ["geoip:cn", "geoip:private"] }
    ]
  }
}

