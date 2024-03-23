import os                                                                                                                                                              
import re
from time import sleep                                                                                                                                                              
from get_post import send_request as send_post_request                                                                                                                 
from get_conversation import send_request as send_conversation_request                                                                                                 
from environment import BEARER                                                                                                                                       
import uuid
from urllib.parse import urlparse
import requests

def ensure_media_directory(directory: str):
    if not os.path.exists(directory):
        os.makedirs(directory)

def sanitize_title(title: str) -> str:                                                                                                                                             
    return re.sub(r'\W+', '_', title.strip())                                                                                                                          
                                                                                                                                                                        
def write_post_to_markdown(post_data: dict, conversation_data: dict, directory: str) -> str:                                                                                                   
    if not os.path.exists(directory):                                                                                                                                  
        os.makedirs(directory)                                                                                                                                         
    title = sanitize_title(post_data['title'])
    content: str = post_data['body']                                           


    media_urls = extract_media_urls(content)
    media_file_paths = []                                                                                                                                             
    for media_url in media_urls:                                                                                                                                      
        media_file_path = download_media(media_url, "posts/media/")                                                                                                 
        if media_file_path:                                                                                                                                           
            media_file_paths.append(media_file_path)               

    content = replace_media_urls_with_paths(content, media_urls, media_file_paths)                                                                                                                                                                      

    created_at = post_data['createdAt']                                                                                                                                
    markdown_content = f'# {title}\n\n{content}\n\n*Created at: {created_at}*\n\n## Comments\n\n'                                                                      
    for comment in conversation_data:
        first_name = comment['author'].get('firstName', '')
        last_name = comment['author'].get('lastName', '')
        if first_name == '' and last_name == '':
            author_name = comment['author'].get('email', 'Unknown')
        else:
            author_name = f'{first_name} {last_name}'                                                                       
        comment_body = comment['body']         

        media_urls = extract_media_urls(comment_body)
        media_file_paths = []
        for media_url in media_urls:
            media_file_path = download_media(media_url, "posts/media/")
            if media_file_path:
                media_file_paths.append(media_file_path)

        comment_body = replace_media_urls_with_paths(comment_body, media_urls, media_file_paths)


        comment_time = comment['createdAt']                                                                                                                            
        markdown_content += f'- **{author_name}**: {comment_body} (Posted on {comment_time})\n\n'                                                                      
    file_path = os.path.join(directory, f'{title}.md')                                                                                                                 
    with open(file_path, 'w', encoding='utf-8') as md_file:                                                                                                                              
        md_file.write(markdown_content)                                                                                                                                
    return file_path                                                                                                                                                   

def fetch_posts_and_write_markdown(number_of_posts: int, directory: str):                                                                                                        
    fetched_posts = 0                                                                                                                                                  
    before = None                                                                                                                                                      
    while fetched_posts < number_of_posts:                                                                                                                             
        remaining_posts = number_of_posts - fetched_posts                                                                                                              
        batch_size = min(20, remaining_posts)                                                                                                                          
        posts_data = send_post_request(batch_size, BEARER, before)                                                                                                     
        if not posts_data: 
            print(f"Finsihed after {fetched_posts} posts")                                                                                                                                            
            break                                                                                                                                                      
        for post_data in posts_data:                                                                                                                                   
            post_id = post_data['id']                                                                                                                                  
            conversation_data = send_conversation_request(post_id, BEARER)                                                                                             
            write_post_to_markdown(post_data, conversation_data, directory)                                                                                            
            fetched_posts += 1                                                                                                                                         
        before = posts_data[-1]['createdAt']   
        print("Sleeping for 5 seconds")
        sleep(5)                                                                                                                        
                                                                                                                                                                        
# Example usage:                                                                                                                                                       
# fetch_posts_and_write_markdown(2, 'posts/') 

# Updated regex pattern to capture all media types and possible media with different names
def extract_media_urls(text):
    pattern = r'https://files\.campuswire\.com/[a-zA-Z0-9-]+/[a-zA-Z0-9-]+/[^\s]+\.(?:png|jpg|jpeg|gif|bmp|svg)'
    return re.findall(pattern, text)

# Function to download media with a random name
def download_media(media_url: str, directory: str) -> str:
    ensure_media_directory(directory)
    response = requests.get(media_url)
    if response.status_code == 200:
        # Generate a random filename with the same extension
        _, ext = os.path.splitext(urlparse(media_url).path)
        filename = f'{uuid.uuid4()}{ext}'
        file_path = os.path.join(directory, filename)
        with open(file_path, 'wb') as file:
            file.write(response.content)
        return f'./media/{filename}'
    else:
        print(f'Failed to download media from {media_url}')
        return None

# Function to replace media URLs with relative paths in markdown content
def replace_media_urls_with_paths(markdown_content: str, media_urls: list[str], media_file_paths: list[str]) -> str:
    for url, path in zip(media_urls, media_file_paths):
        markdown_content = markdown_content.replace(url, path)
    return markdown_content

# Update the write_post_to_markdown function to include media download and URL replacement
fetch_posts_and_write_markdown(600, 'posts/')
