# spotify-likes
A docker container project to save all liked tracks on Spotify to a playlist, currently configured to run hourly via a cron job.

## How to build and run the container
1. Copy template to `.env`
```
cp .env.template .env
```
2. Edit `.env` with your secrets
```
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here
SPOTIFY_REDIRECT_URI=your_redirect_uri_here
```
3. Build image
```
docker build -t spotify-likes .
```
4. Run container with env file
```
docker run --env-file .env spotify-likes
```



