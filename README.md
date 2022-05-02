# WrapUp Discord Bot

Discord Bot for WrapUp

## Setting up the environment file

Add the file named `.env` to the `src` folder.

Following env variables are supported:

``` bash
BOT_TOKEN=<string> # Discord bot token
BACKEND_API=http://localhost:8000/api
BACKEND_API_KEY=<backend-api-key>
BOT_PREFIX=wu?
ICON_URL=<WrapUp-Icon-URL>
```

## Running using Docker

`docker run --env-file </path/to/.env> <container-name>`
