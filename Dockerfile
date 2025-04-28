FROM ghcr.io/astral-sh/uv:python3.12-bookworm

ENV DEBIAN_FRONTEND=noninteractive \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    DISPLAY=:0

# Install system dependencies required for GUI applications and optional tools
RUN apt-get update && apt-get install -y \
    git \
    curl \
    unzip \
    libx11-6 \
    libxext6 \
    libxrender1 \
    libxtst6 \
    libxi6 \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Install trufflehog
RUN curl -sSfL https://raw.githubusercontent.com/trufflesecurity/trufflehog/main/scripts/install.sh | sh -s -- -b /usr/local/bin

# Install gitleaks
RUN curl -sSfL https://raw.githubusercontent.com/gitleaks/gitleaks/main/scripts/install.sh | sh -s -- -b /usr/local/bin

# Install subfinder
RUN curl -sSfL https://raw.githubusercontent.com/projectdiscovery/subfinder/main/install.sh | sh -s -- -b /usr/local/bin

WORKDIR /app

COPY . .

RUN uv sync --frozen

CMD ["python", "main.py"]
