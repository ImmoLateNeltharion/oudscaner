# Используем официальный образ Python
FROM python:3.10-slim

# Установка необходимых системных пакетов
RUN apt-get update && apt-get install -y \
    default-jdk \
    wget \
    unzip \
    git \
    && rm -rf /var/lib/apt/lists/*

# Установка OWASP Dependency Check
RUN mkdir /opt/dependency-check && \
    wget -q -O /tmp/dc.zip https://github.com/jeremylong/DependencyCheck/releases/download/v8.4.0/dependency-check-8.4.0-release.zip && \
    unzip /tmp/dc.zip -d /opt/dependency-check && \
    rm /tmp/dc.zip && \
    chmod +x /opt/dependency-check/dependency-check/bin/dependency-check.sh

# Установка apktool
RUN wget -q -O /usr/local/bin/apktool https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/linux/apktool && \
    wget -q -O /usr/local/bin/apktool.jar https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.7.0.jar && \
    chmod +x /usr/local/bin/apktool /usr/local/bin/apktool.jar

# Создаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY src/requirements.txt .
COPY src/scanners/ scanners/
COPY src/main.py .

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем Semgrep
RUN pip install --no-cache-dir semgrep

# Добавляем пути в PATH
ENV PATH="/opt/dependency-check/dependency-check/bin:${PATH}"
ENV JAVA_HOME="/usr/lib/jvm/java-11-openjdk-amd64"

# Создаем директорию для результатов
RUN mkdir /results

# Точка входа
ENTRYPOINT ["python", "main.py"] 