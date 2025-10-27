FROM sonarsource/sonar-scanner-cli:latest

WORKDIR /app

# Instalar dependencias adicionales si es necesario
RUN apt-get update && apt-get install -y python3 python3-pip

CMD ["sonar-scanner"]