import requests
from bs4 import BeautifulSoup
import datetime

REQUEST_HEADER = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def get_current_season_and_year():
    """Menentukan musim dan tahun saat ini berdasarkan tanggal sistem."""
    now = datetime.datetime.now()
    month = now.month
    year = now.year
    season = ""
    if 1 <= month <= 3: # Januari - Maret
        season = "winter"
    elif 4 <= month <= 6: # April - Juni
        season = "spring"
    elif 7 <= month <= 9: # Juli - September
        season = "summer"
    elif 10 <= month <= 12: # Oktober - Desember
        season = "fall"
    return year, season

def fetch_seasonal_anime_from_mal(target_year: int, target_season: str, limit: int = 15) -> str:
    current_year, current_season_name = get_current_season_and_year()

    year_to_fetch = target_year if target_year is not None else current_year
    season_to_fetch = target_season.lower() if target_season else current_season_name

    if not season_to_fetch:
        return "Error: Tidak dapat menentukan musim saat ini."

    url = f"https://myanimelist.net/anime/season/{year_to_fetch}/{season_to_fetch}"
    print(f"Tool 'fetch_seasonal_anime_from_mal' memanggil URL: {url}")

    try:
        response = requests.get(url, headers=REQUEST_HEADER, timeout=15)
        response.raise_for_status()  # Akan memunculkan error jika status code bukan 2xx
    except requests.exceptions.RequestException as e:
        return f"Error saat mengambil data dari MyAnimeList: {e}"

    soup = BeautifulSoup(response.content, "html.parser")
    anime_list_data = []

    anime_items_container = soup.find_all("div", class_="seasonal-anime", limit=limit + 5)
    
    if not anime_items_container:
        anime_items_container = soup.find_all("div", class_="js-anime-category-producer", limit=limit + 5)


    found_anime_count = 0
    for item_container in anime_items_container:
        if found_anime_count >= limit:
            break

        title_tag = item_container.find("h2", class_="h2_anime_title")
        title = title_tag.find("a", class_="link-title").text.strip() if title_tag and title_tag.find("a", class_="link-title") else "N/A"

        if title == "N/A" and item_container.find("a", class_="link-title"): 
            title = item_container.find("a", class_="link-title").text.strip()


        score_div = item_container.find("div", class_=["score", "score-label"]) 
        score = score_div.find("span", class_="text").text.strip() if score_div and score_div.find("span", class_="text") else "N/A"
        if score == "N/A" and score_div: 
             score_text = score_div.text.strip()
             if score_text.replace('.', '', 1).isdigit() or score_text == "N/A":
                  score = score_text

        genres_tags = item_container.find_all("span", class_="genre")
        genres = [genre.find("a").text.strip() for genre in genres_tags if genre.find("a")]
        genres_text = ", ".join(genres) if genres else "N/A"
        
        synopsis_tag = item_container.find("p", class_="preline")
        synopsis = synopsis_tag.text.strip() if synopsis_tag else "N/A"
        if len(synopsis) > 150: # Batasi panjang sinopsis
            synopsis = synopsis[:150] + "..."

        mal_link_tag = item_container.find("a", class_="link-title")
        mal_link = mal_link_tag['href'] if mal_link_tag and 'href' in mal_link_tag.attrs else "N/A"

        if title != "N/A" and mal_link != "N/A":
            anime_list_data.append(
                f"Judul: {title}\n"
                f"  Skor: {score}\n"
                f"  Genre: {genres_text}\n"
                f"  Sinopsis Singkat: {synopsis}\n"
                f"  Link MAL: {mal_link}\n"
            )
            found_anime_count += 1
    
    if not anime_list_data:
        return f"Tidak ada anime yang ditemukan untuk musim {season_to_fetch.capitalize()} {year_to_fetch} di MyAnimeList atau terjadi kesalahan saat parsing."

    header = f"Daftar Anime Musim {season_to_fetch.capitalize()} {year_to_fetch} dari MyAnimeList.net (Top {found_anime_count}):\n{'-'*40}\n"
    return header + "\n".join(anime_list_data)

if __name__ == '__main__':
    print("Menguji tool fetch_seasonal_anime_from_mal...")
    year, season = get_current_season_and_year()
    print(f"Musim dan tahun saat ini terdeteksi: {season.capitalize()} {year}")
    
    anime_data = fetch_seasonal_anime_from_mal(year, season, limit=5)
    print("\n--- Hasil Tes ---")
    print(anime_data)
    
