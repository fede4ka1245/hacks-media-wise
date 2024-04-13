FROM nginx:stable-alpine
ARG NGINX_PORT
ARG FRONTEND_PORT
ARG BACKEND_PORT
EXPOSE $NGINX_PORT
COPY /nginx/default /etc/nginx/conf.d/default.conf.template
RUN export NGINX_PORT=$NGINX_PORT && \
    export FRONTEND_PORT=$FRONTEND_PORT && \
    export BACKEND_PORT=$BACKEND_PORT && \
    envsubst '${NGINX_PORT} ${FRONTEND_PORT} ${BACKEND_PORT}' < "/etc/nginx/conf.d/default.conf.template" > "/etc/nginx/conf.d/default.conf"
CMD ["nginx", "-g", "daemon off;"]