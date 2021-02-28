# Mailer-Spammer

Django boiler for spamming with emails. Backend models & views are ready to go. Content can be taken from both direct
typing or RSS etc. Feel free to fork and add your own frontend.

## Getting started

Make sure you are having the `.env` and `.env.dev` files.

### Build docker images

```console
docker-compose build
```

### Run docker containers with docker-compose

```console
docker-compose up
```

Django application should be available at `http://localhost:8000/`.

Docs are available at `/api/docs/`.

There are also `test` and `black` make commands inside `server` folder.

Frontend will be there, when you add it.

### If you are having problems with volumes read-only status

```console
sudo chown -R $USER:$USER server
```
