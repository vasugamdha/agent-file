# Composio Example Agent 
This is an agent which uses a Composio tool to star an a provided repository. 

> ⚠️ **Warning:** Make sure you enable Composio in your desktop app by setting a Composio key, or run the Letta server with `COMPOSIO_API_KEY` set:
> ```
> docker run \
  -v ~/.letta/.persist/pgdata:/var/lib/postgresql/data \
  -p 8283:8283 \
  -e OPENAI_API_KEY="your_openai_api_key" \
  -e COMPOSIO_API_KEY="your_composio_api_key" \
  letta/letta:latest
> ```

<img width="1451" alt="image" src="https://github.com/user-attachments/assets/96aac113-64c0-47e7-ac36-037374c8ba8d" />
