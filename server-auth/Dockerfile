FROM openjdk:11

RUN apt-get update && apt-get install -y maven
COPY . /app
RUN cd /app && mvn package

EXPOSE 8088
ENTRYPOINT ["java", "-jar", "/app/target/com.dromakin-server-auth-0.0.1-SNAPSHOT.jar"]
