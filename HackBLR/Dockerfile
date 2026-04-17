# 1. Build & Run Environment
FROM node:20-slim

# Set the working directory
WORKDIR /app

# Copy dependency files first for caching
COPY package*.json ./

# Install all dependencies (including devDependencies for 'vite build')
RUN npm install

# Copy the rest of the app's source code
COPY . .

# Build the React frontend for production
RUN npm run build

# Set environment variables for production
ENV NODE_ENV=production
ENV PORT=8080

# Expose the Cloud Run port
EXPOSE 8080

# Command to start the backend (which also serves the static frontend)
CMD ["node", "api/server.js"]
