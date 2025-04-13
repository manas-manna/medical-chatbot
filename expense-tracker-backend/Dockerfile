# Use a base image with Java runtime
FROM openjdk:17-jdk-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the built jar from the host to the container
COPY target/expense-tracker-backend-0.0.1-SNAPSHOT.jar app.jar

# Expose the port the app runs on
EXPOSE 9000

# Run the jar file
ENTRYPOINT ["java", "-jar", "app.jar"]
