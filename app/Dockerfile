FROM oven/bun:1.0 as build-stage 

COPY . /app

WORKDIR /app

RUN bun install --production --frozen-lockfile

# RUN bun run build

# FROM nginx:latest

# COPY --from=build-stage /app/web-build/ /usr/share/nginx/html