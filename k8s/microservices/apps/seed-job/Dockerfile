FROM alpine:3.19
RUN apk add --no-cache bash curl python3
WORKDIR /app
COPY seed-data.sh /app/seed-data.sh
RUN sed -i 's/\r//' /app/seed-data.sh && chmod +x /app/seed-data.sh
ENTRYPOINT ["/app/seed-data.sh"]
