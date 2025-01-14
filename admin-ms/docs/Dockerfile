# Use an nginx base image
FROM nginx:latest

# Copy built Sphinx HTML files into nginx's default directory
COPY ./build/html /usr/share/nginx/html

# Expose port 80 for serving the documentation
EXPOSE 80