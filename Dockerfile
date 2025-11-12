FROM node:20-alpine
WORKDIR /app
COPY app .
EXPOSE 3000
RUN npm install
CMD ["node","/app/index.js"]
