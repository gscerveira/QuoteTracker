FROM node:20-alpine

WORKDIR /quotes_tracker/

# Copy contents of frontend/ into the container
COPY . .
# Perform a clean install of dependencies and build the frontend
RUN npm ci
RUN npm run build

EXPOSE 3000

# Start the development server
CMD ["npm", "start"]