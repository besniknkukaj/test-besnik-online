# test.besnik.online

Simple static website hosted on a Proxmox LXC container, exposed via Cloudflare Tunnel.

## Stack
- **Web server:** Nginx
- **Hosting:** Proxmox LXC (Ubuntu 22.04) — container ID 102, IP 10.1.10.47
- **Domain:** test.besnik.online (Cloudflare)
- **Tunnel:** Cloudflare Tunnel `57db5297-b177-4a86-8147-4611c2535f30`

## Deployment
Files are served from `/var/www/html/` on the container.
