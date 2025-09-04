import os
import json
from confluent_kafka import Consumer
from discord import SyncWebhook, Embed

# -------------------------------
# Configuration
# -------------------------------
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_TOKEN")

# -------------------------------
# Initialize Discord webhook
# -------------------------------
webhook = SyncWebhook.from_url(DISCORD_WEBHOOK_URL)

# -------------------------------
# Kafka consumer setup
# -------------------------------
consumer_conf = {
    "bootstrap.servers": "kafka:9092",
    "group.id": "discord-consumer-group",
    "auto.offset.reset": "earliest"
}
consumer = Consumer(consumer_conf)
consumer.subscribe(["notifications.send"])

# -------------------------------
# Build Discord embed
# -------------------------------
def build_discord_embed(payload: str) -> Embed:
    try:
        data = json.loads(payload)
    except Exception:
        return Embed(title="Invalid message", description=payload[:200], color=0xff0000)

    raw = data.get("raw", {}).get("raw", {})
    instance = raw.get("instanceName") or raw.get("source", "Unknown")
    event_type = data.get("event", raw.get("event_type", "Unknown Event"))

    embed = Embed(title=f"{instance} Notification", color=0x00ff00)
    embed.add_field(name="Event Type", value=event_type, inline=False)
    embed.add_field(name="Source", value=instance, inline=False)

    description = ""
    image_url = None

    # Sonarr
    if instance.lower() == "sonarr" and "series" in raw:
        series = raw["series"]
        title = series.get("title", "Unknown Series")
        episodes = raw.get("episodes", [])
        episode_info = ""
        if episodes:
            ep = episodes[0]
            episode_info = f"Season {ep.get('seasonNumber')} Episode {ep.get('episodeNumber')}: {ep.get('title')}"
        description = f"{instance} is downloading TV series **{title}**\n{episode_info}"
        images = series.get("images", [])
        for img in images:
            if img.get("coverType") == "poster":
                image_url = img.get("remoteUrl")
                break

    # Radarr
    elif instance.lower() == "radarr" and "movie" in raw:
        movie = raw["movie"]
        title = movie.get("title", "Unknown Movie")
        description = f"{instance} is downloading movie **{title}**"
        images = movie.get("images", [])
        for img in images:
            if img.get("coverType") == "poster":
                image_url = img.get("remoteUrl")
                break

    # Jellyseerr
    elif instance.lower() == "jellyseerr":
        subject = raw.get("subject", "Unknown Title")
        msg = raw.get("message", "")
        description = f"**{subject}**\n{msg}"
        image_url = raw.get("image")

    else:
        description = f"Event: {event_type} from {instance}"

    embed.description = description
    if image_url:
        embed.set_image(url=image_url)

    return embed

# -------------------------------
# Main loop: poll Kafka & send Discord
# -------------------------------
print("[Kafka -> Discord] Starting consumer...")

try:
    while True:
        msg = consumer.poll(0.5)  # small timeout for fast polling
        if msg is None:
            continue
        if msg.error():
            print(f"Kafka error: {msg.error()}")
            continue

        payload = msg.value().decode("utf-8")
        embed = build_discord_embed(payload)
        try:
            webhook.send(embed=embed)
            print(f"[Discord] Sent embed for message: {payload[:100]}...")
        except Exception as e:
            print(f"[Discord] Failed to send embed: {e}")

except KeyboardInterrupt:
    print("Stopping consumer...")

finally:
    consumer.close()
