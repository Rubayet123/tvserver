import re
import requests
import json
import concurrent.futures

def get_token_from_url(url):
    """Fetch the token from the given URL with a timeout."""
    try:
        response = requests.get(url, timeout=10)  # Timeout after 10 seconds
        response.raise_for_status()
        return extract_token(response.url)  # Extract token from final URL
    except requests.RequestException as e:
        print(f"Failed to fetch token from {url}: {e}")
        return None

def extract_token(url):
    """Extract the token from the URL using regex."""
    pattern = r'token=([a-f0-9\-]+)'  # Regex to capture the token
    match = re.search(pattern, url)
    return match.group(1) if match else None

def fetch_token_parallel(urls):
    """Fetch tokens for all URLs in parallel using ThreadPoolExecutor."""
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(get_token_from_url, urls))
    return results

def generate_m3u_content(json_data):
    """Generate the M3U content from the JSON data."""
    m3u_lines = ["#EXTM3U"]
    urls = [channel["URL"] for channel in json_data]

    # Fetch all tokens in parallel
    tokens = fetch_token_parallel(urls)

    for channel, token in zip(json_data, tokens):
        logo = channel["tvg-logo"]
        name = channel["channel-name"]
        group = channel["group-title"]

        if token:
            # Construct stream URL with the token
            stream_url = f"http://10.99.99.99:8080/roarzone/bk/{name}/index.m3u8?token={token}"

            # Add M3U entry
            m3u_lines.append(f'#EXTINF:-1 group-title="{group}" tvg-logo="{logo}",{name}')
            m3u_lines.append(stream_url)
            m3u_lines.append("")  # Extra newline between entries

    return "\n".join(m3u_lines)

def save_m3u_file(content, filename="channels.m3u"):
    """Save the generated M3U content to a file."""
    with open(filename, "w") as f:
        f.write(content)
    print(f"M3U file saved as {filename}")

if __name__ == "__main__":
    # JSON input (replace this with your actual input if needed)
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
        }
    ]
    '''
    # Load the JSON input
    json_data = json.loads(json_input)

    # Generate M3U content
    m3u_content = generate_m3u_content(json_data)

    # Save the M3U content to a file
    save_m3u_file(m3u_content)
