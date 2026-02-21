FROM postgres:18
WORKDIR /app
RUN apt update && apt install curl -y;
RUN curl -fsSL -o /usr/local/bin/dbmate https://github.com/amacneil/dbmate/releases/latest/download/dbmate-linux-amd64; \
  chmod +x /usr/local/bin/dbmate;
RUN mkdir -p /app/db/migrations
COPY migrations /app/db/migrations
