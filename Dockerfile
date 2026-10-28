# ChronosMCP (VeriGraph AI) Local Stdio & Containerized MCP Bridge
FROM node:20-alpine

LABEL org.opencontainers.image.title="ChronosMCP Atlassian Bridge"
LABEL org.opencontainers.image.description="Model Context Protocol (MCP) bridge connecting local AI IDEs to Atlassian Forge"
LABEL org.opencontainers.image.authors="Fokrul Islam <fokrulanthro16@gmail.com>"
LABEL org.opencontainers.image.source="https://github.com/fokrulanthro16-eng/chronos-mcp"

WORKDIR /app

# Copy bridge script and configuration
COPY package*.json ./
COPY scripts/ ./scripts/

ENV CHRONOS_MCP_ENDPOINT_URL="https://84d8afae-9ec0-47fc-8212-e27f79430216.hello.atlassian-dev.net/x1/6aHEWuegPcDuTaXG0bLOpPFUZ1Q"

EXPOSE 8080

CMD ["node", "scripts/mcp-bridge.js", "--check"]
