#!/usr/bin/env python3
import sys
import os
import socket
import urllib.request
import urllib.error
import json
import argparse

def check_dns_and_http(domain):
    """
    Check if the domain resolves to an IP or responds to HTTP/HTTPS.
    Returns: (is_active, reason)
    """
    # 1. DNS Resolution Check
    try:
        ip = socket.gethostbyname(domain)
        return True, f"Resolves to IP: {ip}"
    except socket.gaierror:
        pass

    # 2. HTTP/HTTPS Load Check
    for proto in ["https", "http"]:
        url = f"{proto}://{domain}"
        try:
            req = urllib.request.Request(
                url, 
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            )
            # Short timeout to avoid hanging
            with urllib.request.urlopen(req, timeout=3) as response:
                return True, f"Responded to {proto} (Status: {response.status})"
        except urllib.error.HTTPError as e:
            # Server responded with an error (e.g. 403, 500), but it exists!
            return True, f"Responded to {proto} with HTTP Error: {e.code}"
        except urllib.error.URLError:
            # Could not connect (dns or offline)
            pass
        except Exception as e:
            # Other errors (e.g., ssl handshake failed, which means server exists!)
            if "SSL" in str(e) or "handshake" in str(e):
                return True, f"SSL Handshake check confirmed host exists"
            pass

    return False, "Does not resolve or respond to HTTP requests"


def query_whois_socket(domain):
    """
    Perform a native WHOIS query using raw TCP sockets (port 43).
    Follows redirects from whois.iana.org to the authoritative TLD registry server.
    """
    def query_server(server, query):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((server, 43))
            s.sendall((query + "\r\n").encode("utf-8"))
            response = b""
            while True:
                data = s.recv(4096)
                if not data:
                    break
                response += data
            s.close()
            return response.decode("utf-8", errors="ignore")
        except Exception:
            return None

    # Step 1: Query IANA to find the authoritative whois server
    iana_response = query_server("whois.iana.org", domain)
    if not iana_response:
        return None

    refer_server = None
    for line in iana_response.splitlines():
        if line.lower().startswith("refer:") or line.lower().startswith("whois:"):
            parts = line.split(":", 1)
            if len(parts) > 1:
                refer_server = parts[1].strip()
                break

    # If no referral server found, default to standard guesses or whois.iana.org results
    if not refer_server:
        tld = domain.split(".")[-1]
        refer_server = f"whois.nic.{tld}"

    # Step 2: Query the authoritative registry server
    registry_response = query_server(refer_server, domain)
    return registry_response


def check_whois(domain):
    """
    Checks WHOIS records for availability indicators.
    Returns: (is_registered, details_or_raw)
    """
    raw_whois = query_whois_socket(domain)
    if not raw_whois:
        return False, "WHOIS lookup failed (network or server down)"

    # Look for availability keywords in WHOIS response
    availability_keywords = [
        "not found",
        "no match",
        "no object found",
        "available",
        "is free",
        "no entries found",
        "status: available",
        "incorrect domain name",
        "no registered unit",
        "not registered",
        "no match for",
        "available for registration",
        "no data found",
        "not exist",
        "no entries",
        "domain status: available",
        "status: free"
    ]
    
    raw_lower = raw_whois.lower()
    is_available = any(kw in raw_lower for kw in availability_keywords)
    
    if is_available:
        return False, "Available (No WHOIS records found)"
    else:
        return True, "Registered (WHOIS records exist)"


def check_cloudflare_api(domain, account_id, api_token):
    """
    Check domain availability using Cloudflare's Registrar API.
    Returns: (is_available, price_info, raw_json)
    """
    url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/registrar/domain-check"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    data = json.dumps({"domains": [domain]}).encode("utf-8")
    
    try:
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=10) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            
            if res_data.get("success") and res_data.get("result"):
                results = res_data["result"]
                # Find matching domain
                for item in results:
                    if item.get("domain") == domain:
                        supported = item.get("supported", True)
                        available = item.get("available", False)
                        price = item.get("price")
                        currency = item.get("currency", "USD")
                        
                        if not supported:
                            return False, "Extension not supported by Cloudflare Registrar", res_data
                        
                        if available:
                            price_str = f"${price:.2f} {currency}" if price is not None else "Unknown"
                            return True, price_str, res_data
                        else:
                            return False, "Registered / Unavailable", res_data
            return False, "Cloudflare API returned success=False or empty results", res_data
    except urllib.error.HTTPError as e:
        try:
            err_data = json.loads(e.read().decode("utf-8"))
            err_msg = err_data.get("errors", [{}])[0].get("message", str(e))
        except Exception:
            err_msg = str(e)
        return False, f"Cloudflare API HTTP Error: {err_msg}", None
    except Exception as e:
        return False, f"Cloudflare API Connection Error: {str(e)}", None


def get_affiliate_link(domain, affiliate_id):
    """
    Generate an affiliate link for Namecheap.
    """
    encoded_domain = urllib.parse.quote(domain)
    aff_param = f"&aff={affiliate_id}" if affiliate_id else ""
    return f"https://www.namecheap.com/domains/registration/results/?domain={encoded_domain}{aff_param}"


def get_cloudflare_link(domain):
    """
    Generate the Cloudflare domain registration lookup link.
    """
    # Extracts the second-level domain name (e.g. "cofounderpack" from "cofounderpack.com")
    sld = domain.split(".")[0]
    return f"https://domains.cloudflare.com/?domain={sld}"


def load_tld_list():
    """Load default domain extensions from tld_list.txt or fallback to standard defaults."""
    tld_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tld_list.txt")
    defaults = ["com", "co", "io", "ai", "xyz", "net", "app"]
    if os.path.exists(tld_path):
        try:
            with open(tld_path, "r", encoding="utf-8") as f:
                tlds = [line.strip().lstrip(".") for line in f if line.strip()]
                return tlds if tlds else defaults
        except Exception:
            pass
    return defaults

def main():
    parser = argparse.ArgumentParser(description="Check domain availability.")
    parser.add_argument("candidates", nargs="+", help="One or more domains or base brand names to check")
    parser.add_argument("--tlds", help="Comma-separated list of domain extensions (tails) to check (e.g., com,co,net,ca)")
    parser.add_argument("--cf-token", help="Cloudflare API Token")
    parser.add_argument("--cf-account", help="Cloudflare Account ID")
    parser.add_argument("--aff-id", help="Namecheap Affiliate ID")
    
    args = parser.parse_args()

    # Load from environment variables if not provided as arguments
    cf_token = args.cf_token or os.environ.get("CLOUDFLARE_API_TOKEN")
    cf_account = args.cf_account or os.environ.get("CLOUDFLARE_ACCOUNT_ID")
    affiliate_id = args.aff_id or os.environ.get("NAMECHEAP_AFFILIATE_ID")

    # Determine TLD extensions to check
    if args.tlds:
        tld_list = [t.strip().lstrip(".") for t in args.tlds.split(",") if t.strip()]
    else:
        tld_list = load_tld_list()

    # Expand brand candidates if they do not specify a TLD (no dot in the name)
    domains_to_check = []
    for candidate in args.candidates:
        candidate = candidate.strip().lower()
        if not candidate:
            continue
        if "." in candidate:
            # Full domain name provided (e.g. google.com)
            domains_to_check.append(candidate)
        else:
            # Base brand name provided (e.g. google), check all TLDs
            for tld in tld_list:
                domains_to_check.append(f"{candidate}.{tld}")

    results = []

    for domain in domains_to_check:
        info = {
            "domain": domain,
            "status": "Unknown",
            "active": False,
            "price": "See Registrar (Requires API authentication for live quote)",
            "check_method": "None",
            "namecheap_link": get_affiliate_link(domain, affiliate_id),
            "cloudflare_link": get_cloudflare_link(domain)
        }

        # Step 1: Check if the site is actively hosted / resolving (fastest, no credentials)
        is_active, active_reason = check_dns_and_http(domain)
        if is_active:
            info["status"] = "Taken (Active Website/DNS)"
            info["active"] = True
            info["price"] = "N/A"
            info["check_method"] = f"HTTP/DNS Load ({active_reason})"
            results.append(info)
            continue

        # Step 2: Authoritative API check if Cloudflare credentials are provided
        if cf_token and cf_account:
            available, price_or_err, raw = check_cloudflare_api(domain, cf_account, cf_token)
            info["check_method"] = "Cloudflare Registrar API"
            if available:
                info["status"] = "Available"
                info["price"] = price_or_err
            else:
                info["status"] = f"Unavailable ({price_or_err})"
                info["price"] = "N/A"
            results.append(info)
            continue

        # Step 3: WHOIS fallback check (direct socket querying)
        is_registered, whois_detail = check_whois(domain)
        info["check_method"] = "Native WHOIS Query"
        if is_registered:
            info["status"] = f"Taken (WHOIS record found)"
            info["price"] = "N/A"
        else:
            info["status"] = "Available"
            
        results.append(info)

    # Output clean JSON results
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
