# Scrapoxy and Splash Setup Guide

This guide provides instructions for setting up Scrapoxy and Splash using Docker and Docker Compose.

## Prerequisites

Ensure the following are installed on your system:

-   [Docker](https://docs.docker.com/get-docker/)
-   [Docker Compose](https://docs.docker.com/compose/)

---

## Scrapoxy Setup

### Docker Command to Run Scrapoxy

Use the following command to run Scrapoxy with necessary environment variables and volume mappings:

```bash
docker run -d -p 8888:8888 -p 8890:8890 \
  -e AUTH_LOCAL_USERNAME=admin -e AUTH_LOCAL_PASSWORD=password \
  -e BACKEND_JWT_SECRET=secret1 -e FRONTEND_JWT_SECRET=secret2 \
  -e STORAGE_FILE_FILENAME=/etc/scrapoxy/config.json \
  -v ./scrapoxy:/etc/scrapoxy \
  fabienvauchelles/scrapoxy
```

### Docker-Compose Configuration for Scrapoxy

For easier management, use the following `docker-compose.yml`:

```yaml
version: "3.8"
services:
    scrapoxy:
        image: fabienvauchelles/scrapoxy
        ports:
            - "8888:8888"
            - "8890:8890"
        environment:
            AUTH_LOCAL_USERNAME: "admin"
            AUTH_LOCAL_PASSWORD: "password"
            BACKEND_JWT_SECRET: "secret1"
            FRONTEND_JWT_SECRET: "secret2"
            STORAGE_FILE_FILENAME: "/etc/scrapoxy/config.json"
        volumes:
            - ./scrapoxy:/etc/scrapoxy
```

### Run Scrapoxy with Docker-Compose

To start Scrapoxy:

```bash
docker-compose up -d
```

To stop Scrapoxy:

```bash
docker-compose down
```

## Splash Setup

Splash is used for rendering JavaScript in web scraping workflows. This guide assumes Splash is running alongside Scrapoxy.

### Docker Command to Run Splash

Run Splash in detached mode with the following command:

```bash
docker run -d -p 8050:8050 \
  --restart always \
  scrapinghub/splash
```

### Docker-Compose Configuration for Splash

Add Splash to your `docker-compose.yml`:

```yaml
services:
    splash:
        image: scrapinghub/splash
        ports:
            - "8050:8050"
        restart: always
```

### Run Splash with Docker-Compose

Start Splash:

```bash
docker-compose up -d
```

Stop Splash:

```bash
docker-compose down
```

## Networking Scrapoxy and Splash

Ensure Scrapoxy and Splash can communicate within the same Docker network.

### Create a Shared Docker Network

```bash
docker network create scrapoxy-network
```

### Use the Shared Network

Update the `docker-compose.yml` to specify the shared network:

```yaml
networks:
    scrapoxy-network:
        external: true

services:
    scrapoxy:
        networks:
            - scrapoxy-network

    splash:
        networks:
            - scrapoxy-network
```

### Verify Communication

To test connectivity between Scrapoxy and Splash:

```bash
docker exec -it <scrapoxy_container_id> ping splash
```

If `splash` resolves, networking is correctly configured.

## Useful Commands

### Manage Containers

-   List running containers:

    ```bash
    docker ps
    ```

-   Stop a container:

    ```bash
    docker stop <container_id>
    ```

-   Remove a stopped container:

    ```bash
    docker rm <container_id>
    ```

### View Logs

-   View logs for Scrapoxy:

    ```bash
    docker logs -f <scrapoxy_container_id>
    ```

-   View logs for Splash:

    ```bash
    docker logs -f <splash_container_id>
    ```

### Cleanup Docker Resources

To remove unused containers, networks, and images:

```bash
docker system prune -f
```

## Debugging

### Testing Scrapoxy and Splash

1. Test Scrapoxy with Curl:

    ```bash
    curl -u "REPLACEAD:REPLACEPW" http://localhost:8888
    ```

2. Test Splash with Curl:

    ```bash
    curl http://localhost:8050/render.html?url=https://example.com
    ```

### Check DNS Resolution

Ensure DNS works between Scrapoxy and Splash by running:

```bash
docker exec -it <scrapoxy_container_id> ping splash
```

## Notes

-   Replace `<container_id>` with the appropriate container ID when running commands.
-   Update the environment variables and secrets in the configuration files to suit your setup.

This Markdown content is fully formatted and ready for your `README.md`. It incorporates both Scrapoxy and Splash setup instructions, including Docker commands, Docker Compose configurations, networking, and debugging steps. Let me know if you need additional adjustments! 🚀
