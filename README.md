# YouTube Music to Spotify Playlist Converter

This is a simple Python3 script to convert a personal playlist on YTM to a new playlist of Spotify. It relies on a few credentials provided in a config.json file that is not uploaded to this repository for safety reasons. Here's the format:

```
{
	"clientID": "<YOUR_APPLICATION_CLIENTID>",
	"clientSecret": "<YOUR_APPLICATION_CLIENTSECRET>",
	"userID": "<YOUR_ACCOUNT_ID>",
	"oldPlayListID": "<YTM_PLAYLIST_ID>"
}

```

The client properties can be obtained by creating a new application on the Spotify developer dashboard.
