#!/bin/bash

if ! test -f ./.env; then
  cp .env.example .env
fi

git pull origin main
docker compose up -d --build
