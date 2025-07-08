# =================
#  Builder Stage
# =================
# This stage installs dependencies and builds the package.
FROM python:3.12-slim AS builder

# Set the working directory
WORKDIR /usr/src/app

# Prevent python from writing pyc files and buffer output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create a virtual environment to isolate dependencies
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# Copy all files required for the build
COPY pyproject.toml ./
COPY src/ ./src/

# Install the project and its dependencies into the venv
RUN pip install --no-cache-dir .

# =================
#   Final Stage
# =================
# This stage creates the final, lean production image.
FROM python:3.12-slim

# Create a non-privileged user for security
RUN addgroup --system app && adduser --system --group app
WORKDIR /home/app/market-beacon
ENV HOME=/home/app

# Copy the virtual environment with installed packages from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy the entrypoint script
COPY entrypoint.sh ./entrypoint.sh
RUN chmod +x ./entrypoint.sh

# Activate the virtual environment for subsequent commands
ENV PATH="/opt/venv/bin:$PATH"

# Change ownership of the app directory to the non-root user
RUN chown -R app:app .

# Switch to the non-privileged user
USER app

# Healthcheck to ensure the application is importable
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "from market_beacon import __main__"

# Set the entrypoint for the container
ENTRYPOINT ["./entrypoint.sh"]

# Default command to run the application
CMD ["run"]
