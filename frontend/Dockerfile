# Builder stage
FROM node:20-alpine as builder
WORKDIR /quotes_tracker/
# Copy contents of frontend/ into the container
COPY . .
# Use http registry
RUN npm config set registry http://registry.npmjs.org/
# Install dependencies (clean install)
RUN npm ci
# Build the frontend
RUN npm run build

# Development stage
FROM node:20-alpine as dev
WORKDIR /quotes_tracker/
COPY . .
RUN npm ci
EXPOSE 3000
# Start the development server
CMD ["npm", "start"]

# Production stage with nginx
FROM nginx:latest as prod
# Copy the built frontend into the container
COPY --from=builder /quotes_tracker/build /usr/share/nginx/html
# Expose port 80
EXPOSE 80
# Start the nginx server
CMD ["nginx", "-g", "daemon off;"]