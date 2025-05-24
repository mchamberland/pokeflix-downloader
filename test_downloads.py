import json
import os
import subprocess
from main import download_episode

# Constants
website = "https://v2.pkflx.com"  # base website
downloader = "yt-dlp"  # command to run yt-dlp

def test_download_first_episodes():
    """Test downloading first episode from each season and report errors"""
    
    # Load data
    with open('data.json', 'r') as f:
        data = json.load(f)

    test_folder = "test_downloads"
    results = []

    # Create test folder
    os.makedirs(test_folder, exist_ok=True)

    # Try first episode from each season
    for gen in data['pokemon_generations']:
        for series in gen['series']:
            season = series['season']
            series_name = series['title']
            
            # Skip if no episodes
            if not series['episodes']:
                results.append({
                    'season': season,
                    'series': series_name,
                    'status': 'SKIPPED - No episodes available'
                })
                continue

            # Get first episode
            episode = series['episodes'][0] if series['episodes'] else None
            if episode:
                try:
                    episode_num = str(episode['episode']).zfill(2)
                    episode_name = episode['title']
                    series_num = str(season).zfill(2)
                    
                    print(f"\nTesting Season {season} ({series_name})")
                    print(f"Downloading episode {episode_num}: {episode_name}")
                    
                    # Test URL without downloading using yt-dlp simulate mode
                    test_url = f"{website}/hls/{series['pkflx_name']}/{episode_num}/playlist.m3u8"
                    result = subprocess.run(
                        [downloader, "-F", test_url],  # -F lists formats without downloading
                        capture_output=True,
                        text=True
                    )
                    
                    if result.returncode != 0:
                        raise Exception(f"Episode not available: {result.stderr}")
                    
                    print("✓ URL check passed")
                    results.append({
                        'season': season,
                        'series': series_name,
                        'status': 'SUCCESS'
                    })

                except Exception as e:
                    results.append({
                        'season': season,
                        'series': series_name,
                        'status': f'ERROR - {str(e)}'
                    })
                    print(f"Error testing {series_name}: {str(e)}")

    # Print report
    print("\n=== Download Test Results ===")
    print("\nSeason | Series | Status")
    print("-" * 50)
    for result in results:
        print(f"{result['season']:6d} | {result['series'][:20]:20} | {result['status']}")
    
    success_count = len([r for r in results if r['status'] == 'SUCCESS'])
    print(f"\nSuccessfully tested {success_count} out of {len(results)} series")

if __name__ == "__main__":
    test_download_first_episodes()
