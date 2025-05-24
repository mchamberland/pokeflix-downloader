import json
import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import re

# Dictionary mapping seasons to their scraping URLs
SCRAPE_URLS = {
    "25": "https://www.pokeflix.tv/browse/pokemon-ultimate-journeys",
    "24": "https://www.pokeflix.tv/browse/pokemon-master-journeys", 
    "22": "https://www.pokeflix.tv/browse/pokemon-sun-and-moon-ultra-legends",
    "21": "https://www.pokeflix.tv/browse/pokemon-sun-and-moon-ultra-adventures",
    "18": "https://www.pokeflix.tv/browse/pokemon-xy-kalos-quest",
    "15": "https://www.pokeflix.tv/browse/pokemon-bw-rival-destinies",
    # Add more as needed
}

async def scrape_episodes(url, season_number):
    """Scrape episode data from given URL using Playwright"""
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            )
            page = await context.new_page()
            
            # Increase timeout and add specific waiting conditions
            try:
                await page.goto(url, timeout=60000)  # Increase timeout to 60 seconds
                # Wait for specific elements that indicate the page has loaded
                await page.wait_for_selector('.container .row', timeout=60000)
            except Exception as e:
                print(f"Navigation error: {str(e)}")
                await browser.close()
                return []
            
            # Get the page content after JavaScript execution
            content = await page.content()
            await browser.close()
            
            soup = BeautifulSoup(content, 'html.parser')
            episodes = []
            
            # Find all episode elements in the container>row structure
            episode_elements = soup.select('.container .row .col-sm-6')
            
            # Rest of your parsing logic remains the same
            for element in episode_elements:
                try:
                    img = element.find('img')
                    thumbnail = img['src'] if img else None
                    
                    title_elem = element.find('h4', class_='textTrim')
                    if not title_elem:
                        continue
                        
                    title_text = title_elem.text.strip()
                    episode_num = title_text.split('-')[0].strip()
                    title = title_text[title_text.find('-')+1:].strip()
                    
                    watch_link = element.find('a', class_='btn')
                    video_url = watch_link['href'] if watch_link else None
                    
                    if not all([episode_num, title, video_url]):
                        continue
                    
                    episode = {
                        "episode": int(episode_num),
                        "thumbnail": thumbnail,
                        "title": title_text,
                        "video_url": video_url
                    }
                    episodes.append(episode)
                    
                except Exception as e:
                    print(f"Error parsing episode: {str(e)}")
                    continue
                
            return sorted(episodes, key=lambda x: x['episode'])
    
    except Exception as e:
        print(f"Error scraping {url}: {str(e)}")
        return []

async def update_data_json(season_number, episodes):
    """Update data.json with scraped episodes"""
    try:
        # Load existing data
        with open('data.json', 'r') as f:
            data = json.load(f)
        
        # Find and update the correct series
        for gen in data['pokemon_generations']:
            for series in gen['series']:
                if str(series['season']) == str(season_number):
                    series['episodes'] = episodes
                    print(f"Updated season {season_number} with {len(episodes)} episodes")
                    break
        
        # Save updated data
        with open('data.json', 'w') as f:
            json.dump(data, f, indent=2)
            
    except Exception as e:
        print(f"Error updating data.json: {str(e)}")

async def main():
    """Main function to scrape all missing episodes"""
    for season, url in SCRAPE_URLS.items():
        print(f"\nScraping season {season} from {url}")
        episodes = await scrape_episodes(url, season)
        if episodes:
            await update_data_json(season, episodes)
            print(f"Found {len(episodes)} episodes for season {season}")
        else:
            print(f"No episodes found for season {season}")

if __name__ == "__main__":
    asyncio.run(main())
