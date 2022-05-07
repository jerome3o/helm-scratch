sudo docker rm -f helm-postgres
sudo docker run -d --name helm-postgres -p 5432:5432 -e POSTGRES_PASSWORD=rocketlab postgres