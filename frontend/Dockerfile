# Build stage
FROM node:20 AS build

WORKDIR /app
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Serve stage
FROM nginx:1.25-alpine

# Copy build output to nginx html folder
COPY --from=build /app/dist /usr/share/nginx/html

# Expose port 3000 for dev, nginx listens on 80
EXPOSE 3000 80

# Use nginx default CMD
