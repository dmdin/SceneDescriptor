FROM node:18-alpine3.16 AS build

WORKDIR /app
COPY . .
RUN npm i
RUN npm run build

CMD ["node", "./build/index.js"]
