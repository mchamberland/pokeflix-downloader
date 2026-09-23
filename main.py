# website = "https://v2.pkflx.com"  # base website
# downloader = "yt-dlp"
# folder = "D:\\pokemon\\"

# https://v2.pkflx.com/hls/15-bw-rival-destinies/01/playlist.m3u8

# data.json - all information about the series, dont use other files for now
# outline: downloader for pokeflix episodes. user can specify the series and episodes to download or download all from a specific series/generation.
# script will create a folder for the series and download episodes into it.
# it will also check if the episode already exists before downloading.
# downloader needs HLS .m3u8 URL for each episode, which can be constructed from the series and episode number.
# numbers are padded with zeros for single-digit episodes (e.g., 01, 02, ..., 09) and series.
# we use if __name__ == "__main__": to allow the script to be run as a standalone program or imported as a module.
# command = f"{downloader} \"{hls_url}\" --extractor-args \"generic:impersonate\" -f \"bestvideo+bestaudio/best\" --output \"{output_file}\""

import os
import json
import glob
import re

website = "https://v1.pkflx.com"  # base website
downloader = "yt-dlp"
folder = "/Users/marc/Movies/Pokémon"

def load_data():
    """Load the data from data.json"""
    with open('data.json', 'r') as file:
        return json.load(file)

def download_episode(series_pkflx_name, series_number, episode_name, episode_num, folder_path=folder):

    hls_url = f"{website}/hls/{series_pkflx_name}/{episode_num}/playlist.m3u8"
    """Download the episode and save it to the specified folder"""
    # Create the folder if it doesn't exist
    os.makedirs(folder_path, exist_ok=True)
    # Construct the output file name
    output_file = os.path.join(folder_path, f"S{series_number}E{episode_num}_{episode_name}_%(height)sp.%(ext)s")
    command = f"{downloader} \"{hls_url}\" --extractor-args \"generic:impersonate\" -f \"bestvideo+bestaudio/best\" --output \"{output_file}\""
    os.system(command)

def download_series(series_number):
    """Download all episodes of a series"""
    data = load_data()
    for gen in data['pokemon_generations']:
        for series in gen['series']:
            print(f"Checking series: {series['title']} (Season {series['season']})")
            # Check if the series matches the requested season number
            if series['season'] == series_number:
                series_num_padded = str(series_number).zfill(2)
                series_name = series['title']
                series_pkflx_name = series['pkflx_name']
                for episode in series['episodes']:
                    episode_num = str(episode['episode']).zfill(2)
                    episode_name = episode['title']
                    # Check if the episode already exists
                    folder_path = os.path.join(folder, f"{series_num_padded}-{series['title']}")
                    pattern = os.path.join(folder_path, f"S{series_num_padded}E{episode_num}*")
                    existing_files = glob.glob(pattern)
                    if existing_files:
                        print(f"Skipping {series_name} Episode {episode_num}, file already exists.")
                        continue
                    download_episode(series_pkflx_name, series_num_padded, episode_name, episode_num, folder_path)
                break

def list_available_series():
    """List all available series from data.json"""
    data = load_data()
    print("\nAvailable Pokemon Series:")
    print("-" * 50)
    for gen in data['pokemon_generations']:
        print(f"\n{gen['region']}:")
        for series in gen['series']:
            print(f"  {series['season']:2d}. {series['title']}")
    print("-" * 50 + "\n")

def main():
    """Main function to run the downloader"""
    list_available_series()
    series_number = input("Enter the series number to download (e.g., 1 for Season 1): ")
    try:
        series_number = int(series_number)
        download_series(series_number)
    except ValueError:
        print("Invalid series number. Please enter a valid integer.")

if __name__ == "__main__":
    main()