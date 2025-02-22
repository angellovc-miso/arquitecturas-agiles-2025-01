FROM node:20

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json first to leverage Docker cache
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy TypeScript config
COPY tsconfig.json ./

# Copy the source code
COPY src ./src

# Compile TypeScript
RUN npm run build



# Start the server
CMD ["node", "build/index.js"]
