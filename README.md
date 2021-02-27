# Mailer

Django and X app for mail spamming.

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

Django application should be available at http://localhost:8000/.

Frontend should be available at X.

### If you are having problems with volumes read-only status

```console
sudo chown -R $USER:$USER server
```
