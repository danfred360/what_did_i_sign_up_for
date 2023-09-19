FROM oven/bun as build-stage 
# node:20

WORKDIR /app

COPY package*.json /app/
COPY bun.lockb /app/
COPY jsconfig.json /app/

RUN bun install

COPY ./ /app/

RUN bun expo export:web

FROM nginx:latest

COPY --from=build-stage /app/web-build/ /usr/share/nginx/html