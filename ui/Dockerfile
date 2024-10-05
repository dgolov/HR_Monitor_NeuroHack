FROM node:16

WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH

COPY ./hr-metrics-app/package.json ./

RUN npm install

COPY ./hr-metrics-app .

RUN npm run build
