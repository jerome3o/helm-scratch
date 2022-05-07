sudo docker build . -t jerome3o/scratch:0.0.1

# test it out
# sudo docker run -p 8000:8000 --env-file=.env.dev jerome3o/scratch:0.0.1

sudo docker push jerome3o/scratch:0.0.1