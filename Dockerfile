FROM registry.access.redhat.com/ubi8/ubi-minimal
USER root
LABEL maintainer="Gabriel Sampaio"
# Update image
RUN microdnf update -y && rm -rf /var/cache/yum
RUN microdnf install curl -y && microdnf clean all
# Start the service
COPY people.sh people.sh
COPY access.json access.json
ENTRYPOINT ["./people.sh"]