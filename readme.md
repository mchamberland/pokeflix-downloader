# Pokéflix Downloader

A Python script to download Pokémon anime episodes from Pokéflix. The downloader allows you to download entire seasons while keeping track of already downloaded episodes.

## Features

- Download complete seasons of Pokémon anime
- Automatically creates organized folders for each season
- Skips already downloaded episodes
- High-quality video downloads using yt-dlp
- Simple command-line interface

## Requirements

- Python 3.6+
- yt-dlp
- Internet connection

## Installation

1. Clone this repository:
```sh
git clone https://github.com/jakubCF/pokeflix-downloader.git
cd pokeflix-downloader
```

2. Install yt-dlp:
```sh
pip install yt-dlp
```

## Configuration

Edit the following variables in `main.py` to customize your settings:

```python
folder = "D:\\pokemon\\"  # download destination
```

## Usage

1. Run the script:
```sh
python main.py
```

2. Enter the season number you want to download when prompted:
```
Enter the series number to download (e.g., 1 for Season 1): 
```

The script will:
- Create a folder for the season
- Download all episodes in the highest quality available
- Skip any episodes that were previously downloaded
- Name files in format: `S01E01_Episode_Title_1080p.mp4`

## File Structure

```
D:\pokemon\
└── 01-Indigo League\
    ├── S01E01_Pokemon I Choose You!_1080p.mp4
    ├── S01E02_Pokemon Emergency!_1080p.mp4
    └── ...
```

## Error Handling

- The script checks if episodes already exist before downloading
- Invalid season numbers are handled gracefully
- Download folders are created automatically if they don't exist

## Disclaimer

This tool is for educational purposes only. Please support the official Pokémon releases.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.