FROM node:18-alpine3.18 AS base

# Add a work directory
WORKDIR /app

# Cache and Install dependencies
COPY package.json .
COPY yarn.lock .
RUN yarn

# Copy app files
COPY . .

# Expose port
EXPOSE 3000


FROM base AS dev
# Start the app
CMD [ "yarn", "start" ]


FROM base AS production
CMD yarn build ; yarn preview
