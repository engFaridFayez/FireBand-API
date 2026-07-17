from urllib.parse import urlparse, parse_qs, quote


def get_youtube_embed_url(url: str):
    parsed = urlparse(url)

    if parsed.hostname in ["youtube.com", "www.youtube.com"]:
        if parsed.path == "/watch":
            video_id = parse_qs(parsed.query).get("v", [None])[0]
            if video_id:
                return f"https://www.youtube.com/embed/{video_id}"

        if parsed.path.startswith("/shorts/"):
            video_id = parsed.path.split("/shorts/")[1]
            return f"https://www.youtube.com/embed/{video_id}"

        if parsed.path.startswith("/embed/"):
            return url

    if parsed.hostname == "youtu.be":
        video_id = parsed.path.lstrip("/")
        return f"https://www.youtube.com/embed/{video_id}"

    return url


def get_facebook_embed_url(url: str):
    parsed = urlparse(url)

    if parsed.hostname in [
        "facebook.com",
        "www.facebook.com",
        "fb.watch",
    ]:
        if "plugins/video.php" in parsed.path:
            return url

        encoded = quote(url, safe="")
        return (
            "https://www.facebook.com/plugins/video.php"
            f"?href={encoded}&show_text=false"
        )

    return url