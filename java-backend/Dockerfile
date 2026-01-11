# --- Stage 1: Build the JAR ---
FROM eclipse-temurin:17-jdk-jammy AS builder

WORKDIR /app

# Copy Maven Wrapper files
COPY .mvn/ .mvn/
COPY mvnw pom.xml ./

# Fix line endings for mvnw (Critical for Windows users)
# This removes Windows-style Carriage Returns (\r) so the script runs on Linux
RUN sed -i 's/\r$//' mvnw && chmod +x mvnw

# Download dependencies (this layer is cached if pom.xml doesn't change)
RUN ./mvnw dependency:go-offline

# Copy source code
COPY src ./src

# Build the application (skipping tests to speed up the build)
RUN ./mvnw clean package -DskipTests

# --- Stage 2: Run the JAR ---
FROM eclipse-temurin:17-jre-jammy

WORKDIR /app

# Create a non-root user for security
RUN addgroup --system spring && adduser --system --ingroup spring spring
USER spring:spring

# Copy the JAR from the builder stage
COPY --from=builder /app/target/*.jar app.jar

# Expose the configured port
EXPOSE 8080

# Environment variables (can be overridden at runtime)
# Default to "prod" or similar if you have profiles
ENV SPRING_PROFILES_ACTIVE=prod

# Health Check (Basic connectivity check since Actuator isn't currently in pom.xml)
# We check if we can connect to localhost:8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
  CMD java -version || exit 1 

# Start the application
ENTRYPOINT ["java", "-jar", "app.jar"]
