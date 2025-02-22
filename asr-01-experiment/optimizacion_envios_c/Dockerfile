FROM gcc:13.2.0

WORKDIR /app

RUN apt-get update && apt-get install -y libmicrohttpd-dev

COPY . .

RUN gcc -o server.out server.c -lmicrohttpd

CMD ["./server.out"]
