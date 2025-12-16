FROM nginx:alpine

# Copiar todo el contenido del frontend (HTML, JS, CSS) al directorio de Nginx
COPY . /usr/share/nginx/html/

# Exponer puerto 80. El puerto que mapea Docker Compose (8080:80).
EXPOSE 80

# CMD por defecto de nginx: usar foreground para que el contenedor no salga
CMD ["nginx", "-g", "daemon off;"]

#daemon off evita que Nginx se cierre y mantiene el contenedor Up.
