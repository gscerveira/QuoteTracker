FROM nginx:latest as dev
COPY ./nginx.conf /etc/nginx/nginx.conf

FROM nginx:latest as prod
COPY ./nginx-prod.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]