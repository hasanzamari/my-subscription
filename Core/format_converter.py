import json, os, base64, urllib.parse
from Core.logger import log

def parse_vmess(cfg):
    try:
        b64 = cfg[8:] + "=" * ((4 - len(cfg[8:]) % 4) % 4)
        data = json.loads(base64.b64decode(b64).decode("utf-8", errors="ignore"))
        return {
            "name": data.get("ps", "VMess"),
            "type": "vmess",
            "server": data.get("add"),
            "port": int(data.get("port", 443)),
            "uuid": data.get("id"),
            "alterId": int(data.get("aid", 0)),
            "cipher": "auto",
            "network": data.get("net", "tcp"),
            "tls": data.get("tls") == "tls",
            "servername": data.get("sni", data.get("host", "")),
            "ws-opts": {"path": data.get("path", "/"), "headers": {"Host": data.get("host", "")}} if data.get("net") == "ws" else None,
            "udp": True
        }
    except:
        return None

def parse_vless_trojan(cfg):
    try:
        is_vless = cfg.startswith("vless://")
        prefix = "vless://" if is_vless else "trojan://"
        parsed = urllib.parse.urlparse(cfg)
        
        # استخراج UUID یا Password
        auth = parsed.username or ""
        host_port = parsed.netloc.split("@")[-1] if "@" in parsed.netloc else parsed.netloc
        host, port = host_port.split(":") if ":" in host_port else (host_port, 443)
        
        query = urllib.parse.parse_qs(parsed.query)
        get_q = lambda k: query.get(k, [""])[0]
        
        security = get_q("security")
        sni = get_q("sni") or host
        fp = get_q("fp") or "chrome"
        pbk = get_q("pbk")
        sid = get_q("sid")
        net = get_q("type") or "tcp"
        path = get_q("path") or "/"
        host_header = get_q("host") or host
        
        name = urllib.parse.unquote(parsed.fragment) or ("VLESS" if is_vless else "Trojan")
        
        proxy = {
            "name": name,
            "type": "vless" if is_vless else "trojan",
            "server": host,
            "port": int(port),
            "uuid" if is_vless else "password": auth,
            "network": net,
            "udp": True
        }
        
        if security == "reality":
            proxy["tls"] = True
            proxy["servername"] = sni
            proxy["client-fingerprint"] = fp
            proxy["reality-opts"] = {"public-key": pbk, "short-id": sid}
        elif security == "tls":
            proxy["tls"] = True
            proxy["servername"] = sni
            proxy["client-fingerprint"] = fp
            
        if net == "ws":
            proxy["ws-opts"] = {"path": path, "headers": {"Host": host_header}}
            
        return proxy
    except:
        return None

def convert_to_clash(proxies):
    lines = ["# Clash Meta / Mihomo Configuration", "proxies:"]
    for p in proxies:
        if not p: continue
        lines.append(f"  - name: \"{p['name']}\"")
        lines.append(f"    type: {p['type']}")
        lines.append(f"    server: \"{p['server']}\"")
        lines.append(f"    port: {p['port']}")
        
        if p['type'] == "vmess":
            lines.append(f"    uuid: \"{p['uuid']}\"")
            lines.append(f"    alterId: {p['alterId']}")
            lines.append(f"    cipher: {p['cipher']}")
        else:
            lines.append(f"    uuid: \"{p.get('uuid', p.get('password', ''))}\"")
            
        lines.append(f"    network: {p.get('network', 'tcp')}")
        lines.append(f"    udp: {str(p.get('udp', True)).lower()}")
        
        if p.get('tls'):
            lines.append(f"    tls: true")
            if p.get('servername'): lines.append(f"    servername: \"{p['servername']}\"")
            if p.get('client-fingerprint'): lines.append(f"    client-fingerprint: {p['client-fingerprint']}")
            
        if p.get('reality-opts'):
            lines.append(f"    reality-opts:")
            lines.append(f"      public-key: \"{p['reality-opts']['public-key']}\"")
            lines.append(f"      short-id: \"{p['reality-opts']['short-id']}\"")
            
        if p.get('ws-opts'):
            lines.append(f"    ws-opts:")
            lines.append(f"      path: \"{p['ws-opts']['path']}\"")
            lines.append(f"      headers:")
            lines.append(f"        Host: \"{p['ws-opts']['headers']['Host']}\"")
            
    return "\n".join(lines)

def convert_to_singbox(proxies):
    outbounds = []
    for p in proxies:
        if not p: continue
        
        ob = {
            "tag": p['name'],
            "type": p['type'],
            "server": p['server'],
            "server_port": p['port'],
            "uuid": p.get('uuid', p.get('password', '')),
            "udp": True
        }
        
        if p['type'] == "vmess":
            ob["security"] = "auto"
            ob["alter_id"] = p['alterId']
            
        if p.get('tls'):
            ob["tls"] = {
                "enabled": True,
                "server_name": p.get('servername', p['server']),
                "utls": {"enabled": True, "fingerprint": p.get('client-fingerprint', 'chrome')}
            }
            if p.get('reality-opts'):
                ob["tls"]["reality"] = {
                    "enabled": True,
                    "public_key": p['reality-opts']['public-key'],
                    "short_id": p['reality-opts']['short-id']
                }
                
        if p.get('network') == 'ws' and p.get('ws-opts'):
            ob["transport"] = {
                "type": "ws",
                "path": p['ws-opts']['path'],
                "headers": {"Host": p['ws-opts']['headers']['Host']}
            }
            
        outbounds.append(ob)
        
    return json.dumps({"outbounds": outbounds}, indent=2, ensure_ascii=False)

def main():
    log("Starting Modern Format Conversion...")
    
    # خواندن ۱۰۰ کانفیگ برتر برای تبدیل به فرمت مدرن
    input_file = "output/Best100.txt"
    if not os.path.exists(input_file):
        log("⚠️ Best100.txt not found. Skipping conversion.")
        return
        
    with open(input_file, "r", encoding="utf-8") as f:
        configs = [line.strip() for line in f if line.strip()]
        
    parsed_proxies = []
    for cfg in configs:
        if cfg.startswith("vmess://"):
            proxy = parse_vmess(cfg)
        elif cfg.startswith("vless://") or cfg.startswith("trojan://"):
            proxy = parse_vless_trojan(cfg)
        else:
            proxy = None
            
        if proxy:
            parsed_proxies.append(proxy)
            
    log(f"✅ Successfully parsed {len(parsed_proxies)} configs for modern formats.")
    
    os.makedirs("output", exist_ok=True)
    
    # نوشتن Clash Meta
    clash_yaml = convert_to_clash(parsed_proxies)
    with open("output/clash_meta.yaml", "w", encoding="utf-8") as f:
        f.write(clash_yaml)
    log("✅ Generated output/clash_meta.yaml")
    
    # نوشتن Sing-Box
    singbox_json = convert_to_singbox(parsed_proxies)
    with open("output/singbox.json", "w", encoding="utf-8") as f:
        f.write(singbox_json)
    log("✅ Generated output/singbox.json")
    
    log("✅ Modern Format Conversion completed successfully!")

if __name__ == "__main__":
    main()
