# --- Этап 1: Сборка приложения (Build Stage) ---
FROM node:20-alpine AS build

WORKDIR /usr/src/app
COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build


# --- Этап 2: Обслуживание статики (Serve Stage) ---
FROM nginx:stable-alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]