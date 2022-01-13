# Playlisteo

Playlisteo extract MP3 files for these hours long Youtube mix.
It extract the metadata from the tracklist often seen in the video description and apply them to the resulting MP3.

## Installation

The installation is straigh-forward:

```bash
git clone https://github.com/RollinHugo/Playlisteo.git
cd Playlisteo
pip install -r requirements.txt
```
## Usage

Go to your Playlisteo folder
```bash
python playlisteo.py https://www.youtube.com/watch?v=GqlGkRlwQTA /home/hugo/Music
```

## Known Bugs

- Sometimes URLs with ~ don't work
