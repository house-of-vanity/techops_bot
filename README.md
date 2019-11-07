# TechOps destiny bot

- Awared of the current TechOps team composition.
- Is able to */roll* for all team at once.
- ...

## Usage

There is a Docker image. Run your own bot:
```shell
export ALLOWED_CHAT=-11111111
export TG_TOKEN=<token>
export OPS_LIST=@ultradesu,@jesus_christ

docker run -ti -e ALLOWED_CHAT=${ALLOWED_CHAT} -e TG_TOKEN=${TG_TOKEN} -e OPS_LIST=${OPS_LIST} techops_bot:latest
```

