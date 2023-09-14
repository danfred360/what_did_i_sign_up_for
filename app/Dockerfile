FROM node:20 as build-stage

WORKDIR /app

COPY package*.json /app/
COPY yarn.lock /app/

RUN yarn install

COPY ./ /app/

RUN yarn expo export:web

FROM nginx:1.25.2

COPY --from=build-stage /app/web-build/ /usr/share/nginx/html