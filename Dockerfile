# Stage 1 — compile the Kotlin fat jar
FROM gradle:8.10-jdk21 AS kotlin-build
WORKDIR /app
COPY build.gradle.kts settings.gradle.kts ./
COPY gradle ./gradle
COPY gradlew ./
COPY solvers/kt_solver.kt ./solvers/
COPY editions/2025 ./editions/2025
RUN chmod +x gradlew && ./gradlew shadowJar --no-daemon

# Stage 2 — slim runtime: Python + JRE only
FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends openjdk-21-jre-headless \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY webserver/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY webserver ./webserver
COPY editions ./editions
COPY solvers/py_solver.py ./solvers/py_solver.py
COPY --from=kotlin-build /app/build/libs/aoc-solver.jar ./build/libs/aoc-solver.jar

WORKDIR /app/webserver
ENV PORT=10000
EXPOSE 10000
CMD ["gunicorn", "-b", "0.0.0.0:10000", "app:aoc_webserver"]
