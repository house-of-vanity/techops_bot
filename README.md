# TechOps destiny bot

- Awared of the current TechOps team composition.
- Is able to */roll* for all team at once.
- ...

## Usage

There is a Docker image. Run your own bot:
```shell
export ALLOWED_CHAT=-11111111
export TG_TOKEN=<token>
export OPS_LIST=@ultradesu,@jesus_christ,156754155

docker run -ti \
    -e ALLOWED_CHAT=${ALLOWED_CHAT} \
    -e TG_TOKEN=${TG_TOKEN} \
    -e OPS_LIST=${OPS_LIST} \
    ultradesu/techops_bot:latest
```

Or via systemd unit.
```
git clone https://github.com/house-of-vanity/techops_bot /opt/techops-bot
cd /opt/techops-bot && pip3 install -r requirements.txt

cat > /lib/systemd/system/techops-bot.service <<EOF
[Unit]
Description=Telegram TechOps destiny bot
[Service]
Type=simple
User=conf-bot
Group=conf-bot
Restart=always
RestartSec=5
StartLimitInterval=60s
StartLimitBurst=3
Environment=ALLOWED_CHAT=-11111111
Environment=TG_TOKEN=<token>
Environment=OPS_LIST=@ultradesu,@jesus_christ,156754155
WorkingDirectory=/opt/techops-bot
ExecStart=/usr/bin/python3 /opt/techops-bot/bot.py
ExecStop=/usr/bin/killall -TERM /usr/bin/python3 /opt/techops-bot/bot.py
[Install]
WantedBy=multi-user.target
EOF

systemctl start  techops-bot.service
systemctl status techops-bot.service
```
