#!/bin/bash
# fix_outbound_ip.sh
#
# Run this ON the DigitalOcean server at 165.22.218.229
# It installs tinyproxy as a forward proxy so all NSE traffic
# exits through the registered IP.
#
# Usage:
#   ssh root@165.22.218.229
#   bash fix_outbound_ip.sh

set -e

PROXY_PORT=8888
REGISTERED_IP="165.22.218.229"
ACTUAL_OUTBOUND_IP="152.57.183.219"

echo "=== Step 1: Confirm this machine's outbound IP ==="
CURRENT_IP=$(curl -s https://api.ipify.org)
echo "This machine's outbound IP: $CURRENT_IP"

if [ "$CURRENT_IP" = "$REGISTERED_IP" ]; then
    echo "✓ Outbound IP matches registered IP. No proxy needed."
    echo ""
    echo "The 403 is caused by a different machine sending the requests."
    echo "Make sure your FastAPI server runs on THIS machine (165.22.218.229),"
    echo "not on the machine with IP $ACTUAL_OUTBOUND_IP."
    exit 0
fi

echo ""
echo "Outbound IP ($CURRENT_IP) does NOT match registered IP ($REGISTERED_IP)."
echo "Installing tinyproxy to route NSE traffic through the correct interface..."
echo ""

# -----------------------------------------------------------------------
# Step 2: Install tinyproxy
# -----------------------------------------------------------------------
echo "=== Step 2: Install tinyproxy ==="
apt-get update -qq
apt-get install -y tinyproxy

# -----------------------------------------------------------------------
# Step 3: Configure tinyproxy
# -----------------------------------------------------------------------
echo "=== Step 3: Configure tinyproxy ==="
cat > /etc/tinyproxy/tinyproxy.conf << EOF
User tinyproxy
Group tinyproxy
Port $PROXY_PORT
Timeout 600
DefaultErrorFile "/usr/share/tinyproxy/default.html"
StatFile "/usr/share/tinyproxy/stats.html"
LogFile "/var/log/tinyproxy/tinyproxy.log"
LogLevel Info
MaxClients 100
MinSpareServers 5
MaxSpareServers 20
StartServers 10
MaxRequestsPerChild 0
# Only allow connections from localhost (FastAPI on same machine)
Allow 127.0.0.1
# Bind outbound connections to the registered IP
Bind $REGISTERED_IP
EOF

# -----------------------------------------------------------------------
# Step 4: Start tinyproxy
# -----------------------------------------------------------------------
echo "=== Step 4: Start tinyproxy ==="
systemctl enable tinyproxy
systemctl restart tinyproxy
sleep 2
systemctl status tinyproxy --no-pager

# -----------------------------------------------------------------------
# Step 5: Verify the proxy routes through the registered IP
# -----------------------------------------------------------------------
echo ""
echo "=== Step 5: Verify outbound IP through proxy ==="
PROXY_IP=$(curl -s --proxy "http://127.0.0.1:$PROXY_PORT" https://api.ipify.org)
echo "IP seen through proxy: $PROXY_IP"

if [ "$PROXY_IP" = "$REGISTERED_IP" ]; then
    echo "✓ Proxy correctly routes through $REGISTERED_IP"
else
    echo "✗ Proxy outbound IP is $PROXY_IP — expected $REGISTERED_IP"
    echo "  Check that the 'Bind' directive in /etc/tinyproxy/tinyproxy.conf"
    echo "  matches the interface that holds $REGISTERED_IP."
    echo "  Run: ip addr show | grep $REGISTERED_IP"
    exit 1
fi

# -----------------------------------------------------------------------
# Step 6: Print the .env line to set
# -----------------------------------------------------------------------
echo ""
echo "=== Step 6: Update .env on your FastAPI server ==="
echo ""
echo "Set this in your .env file:"
echo ""
echo "  NSE_PROXY=http://127.0.0.1:$PROXY_PORT"
echo ""
echo "Then restart FastAPI:"
echo "  systemctl restart your-fastapi-service"
echo "  # or: uvicorn main:app --reload"
echo ""
echo "Then verify with:"
echo "  curl http://127.0.0.1:8000/api/v1/auth/debug/outbound-ip"
echo "  # outbound_ip should be $REGISTERED_IP"
echo "  # proxy_configured should be true"
