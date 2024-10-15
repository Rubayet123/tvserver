import re
import requests
import json

def get_token_from_url(url):
    """Fetch the token from the given URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        token = extract_token(response.url)  # Extract token from the final URL
        return token if token else None
    except requests.RequestException as e:
        print(f"Failed to fetch token from {url}: {e}")
        return None

def extract_token(url):
    """Extract the token from the URL using regex."""
    pattern = r'token=([a-f0-9\-]+)'  # Regex to capture the token
    match = re.search(pattern, url)
    return match.group(1) if match else None

def generate_m3u_content(json_data):
    """Generate the M3U content from the JSON data."""
    m3u_lines = ["#EXTM3U"]
    
    for channel in json_data:
        url = channel["URL"]
        logo = channel["tvg-logo"]
        name = channel["channel-name"]
        group = channel["group-title"]

        # Fetch the token from the channel URL
        token = get_token_from_url(url)

        if token:
            # Construct the stream URL with the token
            stream_url = f"http://10.99.99.99:8080/roarzone/bk/{name}/index.m3u8?token={token}"

            # Add M3U entry with a newline separator between channels
            m3u_lines.append(f'#EXTINF:-1 group-title="{group}" tvg-logo="{logo}",{name}')
            m3u_lines.append(stream_url)
            m3u_lines.append("")  # Add an extra newline between entries

    return "\n".join(m3u_lines)

def save_m3u_file(content, filename="channels.m3u"):
    """Save the generated M3U content to a file."""
    with open(filename, "w") as f:
        f.write(content)
    print(f"M3U file saved as {filename}")

if __name__ == "__main__":
    # JSON input (replace this with your actual input)
    json_input = '''
    [
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/1",
            "tvg-logo": "http://tvassets.roarzone.info/images/1.png",
            "channel-name": "1",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/2",
            "tvg-logo": "http://tvassets.roarzone.info/images/2.png",
            "channel-name": "2",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/3",
            "tvg-logo": "http://tvassets.roarzone.info/images/3.png",
            "channel-name": "3",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/4",
            "tvg-logo": "http://tvassets.roarzone.info/images/4.png",
            "channel-name": "4",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/5",
            "tvg-logo": "http://tvassets.roarzone.info/images/5.png",
            "channel-name": "5",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/6",
            "tvg-logo": "http://tvassets.roarzone.info/images/6.png",
            "channel-name": "6",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/7",
            "tvg-logo": "http://tvassets.roarzone.info/images/7.png",
            "channel-name": "7",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/8",
            "tvg-logo": "http://tvassets.roarzone.info/images/8.png",
            "channel-name": "8",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/9",
            "tvg-logo": "http://tvassets.roarzone.info/images/9.png",
            "channel-name": "9",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/10",
            "tvg-logo": "http://tvassets.roarzone.info/images/10.png",
            "channel-name": "10",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/11",
            "tvg-logo": "http://tvassets.roarzone.info/images/11.png",
            "channel-name": "11",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/12",
            "tvg-logo": "http://tvassets.roarzone.info/images/12.png",
            "channel-name": "12",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/13",
            "tvg-logo": "http://tvassets.roarzone.info/images/13.png",
            "channel-name": "13",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/14",
            "tvg-logo": "http://tvassets.roarzone.info/images/14.png",
            "channel-name": "14",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/15",
            "tvg-logo": "http://tvassets.roarzone.info/images/15.png",
            "channel-name": "15",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/17",
            "tvg-logo": "http://tvassets.roarzone.info/images/17.png",
            "channel-name": "17",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/18",
            "tvg-logo": "http://tvassets.roarzone.info/images/18.png",
            "channel-name": "18",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/19",
            "tvg-logo": "http://tvassets.roarzone.info/images/19.png",
            "channel-name": "19",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/20",
            "tvg-logo": "http://tvassets.roarzone.info/images/20.png",
            "channel-name": "20",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/21",
            "tvg-logo": "http://tvassets.roarzone.info/images/21.png",
            "channel-name": "21",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/22",
            "tvg-logo": "http://tvassets.roarzone.info/images/22.png",
            "channel-name": "22",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/23",
            "tvg-logo": "http://tvassets.roarzone.info/images/23.png",
            "channel-name": "23",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/25",
            "tvg-logo": "http://tvassets.roarzone.info/images/25.png",
            "channel-name": "25",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/26",
            "tvg-logo": "http://tvassets.roarzone.info/images/26.png",
            "channel-name": "26",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/27",
            "tvg-logo": "http://tvassets.roarzone.info/images/27.png",
            "channel-name": "27",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/28",
            "tvg-logo": "http://tvassets.roarzone.info/images/28.png",
            "channel-name": "28",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/29",
            "tvg-logo": "http://tvassets.roarzone.info/images/29.png",
            "channel-name": "29",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/30",
            "tvg-logo": "http://tvassets.roarzone.info/images/30.png",
            "channel-name": "30",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/31",
            "tvg-logo": "http://tvassets.roarzone.info/images/31.png",
            "channel-name": "31",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/33",
            "tvg-logo": "http://tvassets.roarzone.info/images/33.png",
            "channel-name": "33",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/34",
            "tvg-logo": "http://tvassets.roarzone.info/images/34.png",
            "channel-name": "34",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/35",
            "tvg-logo": "http://tvassets.roarzone.info/images/35.png",
            "channel-name": "35",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/37",
            "tvg-logo": "http://tvassets.roarzone.info/images/37.png",
            "channel-name": "37",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/41",
            "tvg-logo": "http://tvassets.roarzone.info/images/41.png",
            "channel-name": "41",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/83",
            "tvg-logo": "http://tvassets.roarzone.info/images/43.png",
            "channel-name": "43",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/48",
            "tvg-logo": "http://tvassets.roarzone.info/images/48.png",
            "channel-name": "48",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/50",
            "tvg-logo": "http://tvassets.roarzone.info/images/50.png",
            "channel-name": "50",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/53",
            "tvg-logo": "http://tvassets.roarzone.info/images/53.png",
            "channel-name": "53",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/54",
            "tvg-logo": "http://tvassets.roarzone.info/images/54.png",
            "channel-name": "54",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/55",
            "tvg-logo": "http://tvassets.roarzone.info/images/55.png",
            "channel-name": "55",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/56",
            "tvg-logo": "http://tvassets.roarzone.info/images/56.png",
            "channel-name": "56",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/58",
            "tvg-logo": "http://tvassets.roarzone.info/images/58.png",
            "channel-name": "58",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/59",
            "tvg-logo": "http://tvassets.roarzone.info/images/59.png",
            "channel-name": "59",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/61",
            "tvg-logo": "http://tvassets.roarzone.info/images/61.png",
            "channel-name": "61",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/62",
            "tvg-logo": "http://tvassets.roarzone.info/images/62.png",
            "channel-name": "62",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/65",
            "tvg-logo": "http://tvassets.roarzone.info/images/65.png",
            "channel-name": "65",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/66",
            "tvg-logo": "http://tvassets.roarzone.info/images/66.png",
            "channel-name": "66",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/67",
            "tvg-logo": "http://tvassets.roarzone.info/images/67.png",
            "channel-name": "67",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/68",
            "tvg-logo": "http://tvassets.roarzone.info/images/68.png",
            "channel-name": "68",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/69",
            "tvg-logo": "http://tvassets.roarzone.info/images/69.png",
            "channel-name": "69",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/72",
            "tvg-logo": "http://tvassets.roarzone.info/images/72.png",
            "channel-name": "72",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/73",
            "tvg-logo": "http://tvassets.roarzone.info/images/73.png",
            "channel-name": "73",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/76",
            "tvg-logo": "http://tvassets.roarzone.info/images/76.png",
            "channel-name": "76",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/77",
            "tvg-logo": "http://tvassets.roarzone.info/images/77.png",
            "channel-name": "77",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/79",
            "tvg-logo": "http://tvassets.roarzone.info/images/79.png",
            "channel-name": "79",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/84",
            "tvg-logo": "http://tvassets.roarzone.info/images/84.png",
            "channel-name": "84",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/85",
            "tvg-logo": "http://tvassets.roarzone.info/images/85.png",
            "channel-name": "85",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/86",
            "tvg-logo": "http://tvassets.roarzone.info/images/86.png",
            "channel-name": "86",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/88",
            "tvg-logo": "http://tvassets.roarzone.info/images/88.png",
            "channel-name": "88",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/89",
            "tvg-logo": "http://tvassets.roarzone.info/images/89.png",
            "channel-name": "89",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/100",
            "tvg-logo": "http://tvassets.roarzone.info/images/100.png",
            "channel-name": "100",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=bk/102",
            "tvg-logo": "http://tvassets.roarzone.info/images/102.png",
            "channel-name": "102",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=ext/bijoy-tv",
            "tvg-logo": "http://tvassets.roarzone.info/images/bijoy-tv.jpg",
            "channel-name": "Bijoy Tv",
            "group-title": "BDIX"
        },
        {
            "URL": "http://10.99.99.99/player.php?stream=ext/ekhon-tv",
            "tvg-logo": "http://tvassets.roarzone.info/images/ekhon-tv.jpg",
            "channel-name": "Ekhon Tv",
            "group-title": "BDIX"
        }
    ]
    '''
    # Load the JSON input
    json_data = json.loads(json_input)

    # Generate M3U content
    m3u_content = generate_m3u_content(json_data)

    # Save the M3U content to a file
    save_m3u_file(m3u_content)
