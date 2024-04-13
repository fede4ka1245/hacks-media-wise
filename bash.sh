#!/bin/bash

cp .env.example .env

git pull origin main
docker compose up -d --build
