FROM nginxinc/nginx-unprivileged:alpine

COPY index.html /usr/share/nginx/html/index.html
COPY style.css app.js /usr/share/nginx/html/assets/
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget -q -O /dev/null http://127.0.0.1:8080/ || exit 1