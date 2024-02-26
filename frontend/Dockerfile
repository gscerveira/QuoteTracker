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
FROM builder as dev
WORKDIR /quotes_tracker/
EXPOSE 3000
# Start the development server
CMD ["npm", "start"]