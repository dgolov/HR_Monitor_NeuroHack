FROM node:18.15.0

WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH


COPY . /app

RUN npm run build
