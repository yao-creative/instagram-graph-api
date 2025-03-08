#!/bin/bash

# Start the Docker Compose setup
echo "Starting Instagram Graph API with Supabase..."
docker-compose up -d

# Wait for the services to be up
echo "Waiting for services to start..."
sleep 5

# Display the status of services
echo "---------------------------------"
echo "Services Status:"
docker-compose ps

# Show URLs
echo "---------------------------------"
echo "Services are available at:"
echo "- Instagram Graph API: http://localhost:8000"
echo "- Supabase API: http://localhost:3000"
echo "- PgAdmin: http://localhost:5050 (Email: admin@example.com, Password: admin)"
echo "- Postgres Meta: http://localhost:8080"
echo "---------------------------------" 