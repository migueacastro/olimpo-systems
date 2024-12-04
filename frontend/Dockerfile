FROM node:21.7.3-alpine

WORKDIR /frontend



COPY . .
RUN npm install -g vite
RUN npm install


EXPOSE 4173

CMD ["npm", "run", "dev", "--", "--port", "4173"]