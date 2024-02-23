# Builder stage
FROM node:20-alpine as builder
WORKDIR /quotes_tracker/
# Copy package files for building
COPY package*.json ./
# Install dependencies (clean install)
RUN npm ci
# Copy contents of frontend/ into the container
COPY . .
# Build the frontend
RUN npm run build

# Development stage
FROM builder as dev
WORKDIR /quotes_tracker/
EXPOSE 3000
# Start the development server
CMD ["npm", "start"]

# Production stage
FROM nginx:alpine as prod
WORKDIR /quotes_tracker/
# Copy the built frontend from the builder stage into the nginx container
COPY --from=builder /quotes_tracker/build /usr/share/nginx/html
EXPOSE 80
# Start the nginx server
CMD ["nginx", "-g", "daemon off;"]