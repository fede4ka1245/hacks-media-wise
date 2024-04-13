FROM node:16-alpine
WORKDIR /app
COPY . .
ARG BACKEND_URL
RUN npm i
RUN export NODE_ENV="production" && \
    npm run build
EXPOSE 8888
CMD [ "npx", "serve", "-l", "8888", "-s", "build" ]
