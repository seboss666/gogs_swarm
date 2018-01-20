FROM frolvlad/alpine-python3

ADD files/* /app/

RUN chmod +x /app/init.sh /app/update_gogs_dns.py

WORKDIR /app/
CMD ["/app/init.sh"]

HEALTHCHECK --interval=30s \
    --timeout=10s \
    --start-period=30s \
    --retries=3 \
    CMD pgrep -f "crond" || exit 1
