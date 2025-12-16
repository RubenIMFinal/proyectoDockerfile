# Imagen base ligera
FROM python:3.11-slim

# Evitar que Python genere .pyc y usar un buffer estándar
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Crear directorio de trabajo
WORKDIR /app

# Copiar solo requirements primero (mejor cache)
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del proyecto
COPY . .

# Exponer puerto del backend
EXPOSE 8000

# Comando por defecto para arrancar Flask en 0.0.0.0:8000
CMD ["python", "-u", "app.py"]

#El -u fuerza un buffer sin buffering, más estable en Docker.
#La instalación de dependencias está cacheada de forma eficiente
#Primero se copia requirements.txt
#Luego se hace pip install
#Mientras requirements.txt no cambie, Docker no reinstala Flask ni nada, lo que acelera muchísimo.