#!/bin/sh

if [ -z "${CRON_SCHEDULE}" ]; then
    echo -ne "Empty CRON_SCHEDULE variable\n"
    exit 1
fi

if [ -e "/app/requirements.txt" ]; then
    pip install -r /app/requirements.txt
fi

# variables crond
STDOUT_LOC=${STDOUT_LOC:-/proc/1/fd/1}
STDERR_LOC=${STDERR_LOC:-/proc/1/fd/2}

# settings crond
echo -ne "# Check and update DNS entry\n${CRON_SCHEDULE} cd /app/ && /app/update_gogs_dns.py > ${STDOUT_LOC} 2> ${STDERR_LOC}\n" | crontab -

# run cron
su -c "/usr/sbin/crond -f"
