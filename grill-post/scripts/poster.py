import argparse
import os
import uuid
import requests
from dotenv import load_dotenv

load_dotenv()

def upload_local_to_r2(local_path):
    print(f"Uploading {local_path} to tmpfiles.org...")
    with open(local_path, "rb") as f:
        res = requests.post("https://tmpfiles.org/api/v1/upload", files={"file": f}).json()
    url = res["data"]["url"]
    public_url = url.replace("tmpfiles.org/", "tmpfiles.org/dl/")
    print(f"Uploaded: {public_url}")
    return public_url

def publish_media(args):
    ig_access_token = os.environ.get('IG_ACCESS_TOKEN')
    ig_account_id = os.environ.get('IG_ACCOUNT_ID')

    if not ig_access_token or not ig_account_id:
        print("Error: IG_ACCESS_TOKEN and IG_ACCOUNT_ID must be set in .env")
        return

    # Helper to get public URL
    def get_public_url(path):
        if args.source == 'local':
            return upload_local_to_r2(path)
        else:
            public_base = os.environ.get('R2_PUBLIC_URL', os.environ.get('R2_ENDPOINT_URL'))
            return f"{public_base}/{path}"

    base_url = f"https://graph.facebook.com/v22.0/{ig_account_id}/media"
    
    # --- CAROUSEL HANDLING ---
    if args.media_type == 'CAROUSEL':
        if len(args.path) < 2:
            print("Error: CAROUSEL requires at least 2 paths.")
            return
        
        print("Creating Carousel Item Containers...")
        children_ids = []
        for i, p in enumerate(args.path):
            m_url = get_public_url(p)
            payload = {
                'access_token': ig_access_token,
                'image_url': m_url,
                'is_carousel_item': 'true'
            }
            if i < len(args.alt_text):
                payload['alt_text'] = args.alt_text[i]
            if args.user_tags:
                payload['user_tags'] = args.user_tags
                
            res = requests.post(base_url, data=payload)
            data = res.json()
            if 'id' not in data:
                print(f"Error creating carousel item for {p}:", data)
                return
            children_ids.append(data['id'])
            print(f"Item container created: {data['id']}")
            
        print("Creating main Carousel Container...")
        payload = {
            'access_token': ig_access_token,
            'media_type': 'CAROUSEL',
            'caption': args.caption,
            'children': ','.join(children_ids)
        }
        if args.location_id:
            payload['location_id'] = args.location_id
            
        res = requests.post(base_url, data=payload)
        data = res.json()
        if 'id' not in data:
            print("Error creating main carousel container:", data)
            return
        container_id = data['id']
        print(f"Carousel container created: {container_id}")

    # --- SINGLE MEDIA HANDLING ---
    else:
        m_url = get_public_url(args.path[0])
        print(f"Creating Instagram {args.media_type} Container...")
        payload = {
            'access_token': ig_access_token,
            'caption': args.caption
        }
        if args.location_id:
            payload['location_id'] = args.location_id
            
        if args.media_type == 'IMAGE':
            payload['image_url'] = m_url
            if args.alt_text:
                payload['alt_text'] = args.alt_text[0]
            if args.user_tags:
                payload['user_tags'] = args.user_tags
        elif args.media_type == 'REELS':
            payload['media_type'] = 'REELS'
            payload['video_url'] = m_url
            if args.audio_name:
                payload['audio_name'] = args.audio_name
        elif args.media_type == 'STORIES':
            payload['media_type'] = 'STORIES'
            if m_url.endswith('.mp4') or m_url.endswith('.mov'):
                payload['video_url'] = m_url
            else:
                payload['image_url'] = m_url
        
        res = requests.post(base_url, data=payload)
        data = res.json()
        if 'id' not in data:
            print("Error creating media container:", data)
            return
            
        container_id = data['id']
        print(f"Container created: {container_id}")
    
    # 3. Publish Container
    print("Publishing container...")
    publish_url = f"https://graph.facebook.com/v22.0/{ig_account_id}/media_publish"
    pub_payload = {
        'creation_id': container_id,
        'access_token': ig_access_token
    }
    pub_res = requests.post(publish_url, data=pub_payload)
    pub_data = pub_res.json()
    
    if 'id' not in pub_data:
        print("Error publishing:", pub_data)
        if pub_data.get('error', {}).get('code') == 9007:
            print("Note: The media is still processing. You may need to retry publishing this container ID later.")
        return
        
    print(f"Successfully published! IG Media ID: {pub_data['id']}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Instagram Auto-Poster")
    parser.add_argument('--source', choices=['local', 'r2'], default='local', help='Source of the media')
    parser.add_argument('--path', nargs='+', required=True, help='Path(s) to local file or R2 key')
    parser.add_argument('--media-type', choices=['IMAGE', 'REELS', 'STORIES', 'CAROUSEL'], default='IMAGE', help='Type of Instagram post')
    parser.add_argument('--caption', default='', help='Caption for the post (ignored for STORIES)')
    parser.add_argument('--alt-text', nargs='*', default=[], help='Alt text(s) for IMAGE or CAROUSEL')
    parser.add_argument('--location-id', default='', help='Facebook Page ID for the location')
    parser.add_argument('--user-tags', default='', help='JSON array string of user tags (e.g., \'[{"username":"tag","x":0.5,"y":0.5}]\')')
    parser.add_argument('--audio-name', default='', help='Name for original audio track (REELS only)')
    
    args = parser.parse_args()
    publish_media(args)
