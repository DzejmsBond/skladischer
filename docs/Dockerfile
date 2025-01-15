# Use an nginx base image
FROM nginx:latest

# Copy built Sphinx HTML files into nginx's default directory
COPY ./build/codes/html /usr/share/nginx/html/codes/docs
COPY ./build/credentials/html /usr/share/nginx/html/credentials/docs
COPY ./build/sensors/html /usr/share/nginx/html/sensors/docs
COPY ./build/users/html /usr/share/nginx/html/users/docs

# Expose port 80 for serving the documentation
EXPOSE 80