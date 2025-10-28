"""Social Media Video Automation Agent using VEO3 and Blotato.

This agent replicates the n8n workflow functionality for automating
video creation with Google's VEO3 and posting to social media via Blotato.
"""
import json
import time
from typing import Any, Dict, List, Optional

import requests

from agents.base_agent import BaseAgent


class SocialMediaVideoAgent(BaseAgent):
    """Agent for automated video creation and social media posting."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """Initialize the Social Media Video Agent."""
        super().__init__(config)
        
        # API Keys and credentials
        self.openai_api_key = self.config.get("openai_api_key", "")
        self.blotato_api_key = self.config.get("blotato_api_key", "")
        self.veo3_api_key = self.config.get("veo3_api_key", "")
        self.google_sheets_credentials = self.config.get("google_sheets_credentials", {})
        
        # Social media account IDs
        self.social_accounts = self.config.get("social_accounts", {
            "instagram_id": "",
            "youtube_id": "",
            "threads_id": "",
            "tiktok_id": "",
            "facebook_id": "",
            "facebook_page_id": "",
            "twitter_id": "",
            "linkedin_id": "",
            "pinterest_id": "",
            "pinterest_board_id": "",
            "bluesky_id": ""
        })
        
        # Workflow settings
        self.max_retries = self.config.get("max_retries", 3)
        self.video_wait_time = self.config.get("video_wait_time", 300)  # 5 minutes

    def generate_video_concept(self, topic: str) -> Dict[str, Any]:
        """Generate video concept using OpenAI GPT-4."""
        system_prompt = """You are an AI designed to generate 1 immersive, realistic idea based on a user-provided topic. Your output must be formatted as a JSON object and follow all the rules below exactly.

RULES:
- Only return 1 idea at a time
- The Idea must be under 13 words
- Describe an interesting and viral-worthy moment, action, or event
- Can be as surreal as you can get, doesn't have to be real-world!
- Involves a character
- The Caption must be short, punchy, and viral-friendly
- Include one relevant emoji
- Include exactly 12 hashtags (4 topic-relevant, 4 popular, 4 trending)
- All hashtags must be lowercase
- Set Status to "for production" (always)
- The Environment must be under 20 words and match the action exactly

OUTPUT FORMAT:
{
    "Caption": "Short viral title with emoji #hashtags",
    "Idea": "Short idea under 13 words", 
    "Environment": "Brief vivid setting under 20 words matching the action",
    "Status": "for production"
}"""

        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.openai_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "gpt-4",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Give me an idea about {topic}"}
                    ],
                    "temperature": 0.8
                },
                timeout=30
            )
            response.raise_for_status()
            
            content = response.json()["choices"][0]["message"]["content"]
            return json.loads(content)
            
        except Exception as e:
            return {
                "error": f"Failed to generate concept: {str(e)}",
                "Caption": f"Amazing {topic} moment! 🎬 #viral #content #amazing #video",
                "Idea": f"Person demonstrates {topic} in creative way",
                "Environment": f"Studio setting with {topic} equipment, good lighting",
                "Status": "for production"
            }

    def create_veo3_prompt(self, idea: str, environment: str) -> str:
        """Create VEO3-compatible video prompt."""
        system_prompt = """You are an AI agent that writes hyper-realistic, cinematic video prompts for Google VEO3. Each prompt should describe a short, vivid selfie-style video clip featuring one unnamed character speaking or acting in a specific moment.

REQUIRED STRUCTURE:
[Scene paragraph prompt here]

Main character: [description of character]
They say: [insert one line of dialogue, fits the scene and mood].
They [describe a physical action or subtle camera movement].
Time of Day: [day / night / dusk / etc.]
Lens: [describe lens]
Audio: (implied) [ambient sounds]
Background: [brief restatement of what is visible behind them]

RULES:
- Single paragraph only, 750–1500 characters. No line breaks or headings.
- Only one human character. Never give them a name.
- Include one spoken line of dialogue and describe how it's delivered.
- Character must do something physical, even if subtle.
- Use selfie-style framing. Always describe the lens and camera behavior.
- Scene must feel real and cinematic.
- Always include the five key technical elements."""

        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.openai_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "gpt-4",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Give me a Veo3 prompt for this idea:\n{idea}\n\nThis is the environment:\n{environment}\n\n"}
                    ],
                    "temperature": 0.7
                },
                timeout=30
            )
            response.raise_for_status()
            
            return response.json()["choices"][0]["message"]["content"]
            
        except Exception as e:
            # Fallback prompt
            return f"A person in {environment.lower()} holds a camera close to their face, creating a selfie-style shot. Main character: young content creator with expressive eyes. They say: 'This is absolutely incredible, you have to see this!' while gesturing excitedly. They pan the camera slightly to show the surroundings. Time of Day: golden hour. Lens: wide-angle smartphone camera with slight fish-eye effect. Audio: (implied) ambient environmental sounds. Background: {environment.lower()} visible in soft focus behind them."

    def generate_video_with_veo3(self, prompt: str) -> Optional[str]:
        """Generate video using VEO3 API."""
        try:
            # Start video generation
            response = requests.post(
                "https://queue.fal.run/fal-ai/veo3",
                headers={
                    "Authorization": f"Key {self.veo3_api_key}",
                    "Content-Type": "application/json"
                },
                json={"prompt": prompt},
                timeout=30
            )
            response.raise_for_status()
            
            request_id = response.json().get("request_id")
            if not request_id:
                return None
            
            # Wait for processing
            print(f"Video generation started. Request ID: {request_id}")
            print(f"Waiting {self.video_wait_time} seconds for processing...")
            time.sleep(self.video_wait_time)
            
            # Retrieve result
            result_response = requests.get(
                f"https://queue.fal.run/fal-ai/veo3/requests/{request_id}",
                headers={"Authorization": f"Key {self.veo3_api_key}"},
                timeout=30
            )
            result_response.raise_for_status()
            
            result_data = result_response.json()
            if result_data.get("status") == "completed":
                return result_data.get("video", {}).get("url")
            else:
                print(f"Video generation status: {result_data.get('status')}")
                return None
                
        except Exception as e:
            print(f"Error generating video: {str(e)}")
            return None

    def upload_video_to_blotato(self, video_url: str) -> Optional[str]:
        """Upload video to Blotato for social media posting."""
        try:
            response = requests.post(
                "https://backend.blotato.com/v2/media",
                headers={"blotato-api-key": self.blotato_api_key},
                data={"url": video_url},
                timeout=60
            )
            response.raise_for_status()
            
            return response.json().get("url")
            
        except Exception as e:
            print(f"Error uploading to Blotato: {str(e)}")
            return None

    def post_to_social_platform(self, platform: str, media_url: str, caption: str, title: Optional[str] = None) -> Dict[str, Any]:
        """Post content to specific social media platform via Blotato."""
        account_id = self.social_accounts.get(f"{platform}_id")
        if not account_id:
            return {"success": False, "error": f"No account ID for {platform}"}
        
        # Platform-specific configurations
        platform_configs = {
            "instagram": {"targetType": "instagram"},
            "youtube": {
                "targetType": "youtube",
                "title": title or "Auto-generated Video",
                "privacyStatus": "unlisted",
                "shouldNotifySubscribers": "false"
            },
            "tiktok": {
                "targetType": "tiktok",
                "isYourBrand": "false",
                "disabledDuet": "false",
                "privacyLevel": "PUBLIC_TO_EVERYONE",
                "isAiGenerated": "true",
                "disabledStitch": "false",
                "disabledComments": "false",
                "isBrandedContent": "false"
            },
            "facebook": {
                "targetType": "facebook",
                "pageId": self.social_accounts.get("facebook_page_id", "")
            },
            "threads": {"targetType": "threads"},
            "twitter": {"targetType": "twitter"},
            "linkedin": {"targetType": "linkedin"},
            "bluesky": {"targetType": "bluesky"},
            "pinterest": {
                "targetType": "pinterest",
                "boardId": self.social_accounts.get("pinterest_board_id", "")
            }
        }
        
        target_config = platform_configs.get(platform, {"targetType": platform})
        
        payload = {
            "post": {
                "accountId": account_id,
                "target": target_config,
                "content": {
                    "text": caption,
                    "platform": platform,
                    "mediaUrls": [media_url]
                }
            }
        }
        
        try:
            response = requests.post(
                "https://backend.blotato.com/v2/posts",
                headers={
                    "blotato-api-key": self.blotato_api_key,
                    "Content-Type": "application/json"
                },
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            
            return {
                "success": True,
                "platform": platform,
                "response": response.json()
            }
            
        except Exception as e:
            return {
                "success": False,
                "platform": platform,
                "error": str(e)
            }

    def run(self, topic: str = "amazing technology", platforms: Optional[List[str]] = None) -> Dict[str, Any]:
        """Run the complete social media video automation workflow."""
        if platforms is None:
            platforms = ["instagram", "youtube", "tiktok", "facebook"]
        
        start_time = time.time()
        results = {
            "topic": topic,
            "platforms": platforms,
            "start_time": start_time,
            "steps": {},
            "social_posts": {},
            "success": False
        }
        
        try:
            # Step 1: Generate video concept
            print("🎯 Step 1: Generating video concept...")
            concept = self.generate_video_concept(topic)
            results["steps"]["concept"] = concept
            
            if "error" in concept:
                print(f"⚠️ Concept generation had issues: {concept['error']}")
            
            # Step 2: Create VEO3 prompt
            print("📝 Step 2: Creating VEO3 prompt...")
            veo3_prompt = self.create_veo3_prompt(concept["Idea"], concept["Environment"])
            results["steps"]["veo3_prompt"] = veo3_prompt
            
            # Step 3: Generate video
            print("🎬 Step 3: Generating video with VEO3...")
            video_url = self.generate_video_with_veo3(veo3_prompt)
            
            if not video_url:
                # Use a demo video URL for testing
                video_url = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"
                print("⚠️ Using demo video URL for testing")
            
            results["steps"]["video_url"] = video_url
            
            # Step 4: Upload to Blotato
            print("📤 Step 4: Uploading video to Blotato...")
            blotato_media_url = self.upload_video_to_blotato(video_url)
            
            if not blotato_media_url:
                blotato_media_url = video_url  # Fallback
                print("⚠️ Using original video URL as fallback")
            
            results["steps"]["blotato_media_url"] = blotato_media_url
            
            # Step 5: Post to social platforms
            print("📱 Step 5: Posting to social media platforms...")
            for platform in platforms:
                print(f"  📤 Posting to {platform}...")
                post_result = self.post_to_social_platform(
                    platform=platform,
                    media_url=blotato_media_url,
                    caption=concept["Caption"],
                    title=concept.get("Idea", "Auto-generated Video")
                )
                results["social_posts"][platform] = post_result
                
                if post_result["success"]:
                    print(f"  ✅ {platform}: Posted successfully")
                else:
                    print(f"  ❌ {platform}: {post_result['error']}")
            
            # Check overall success
            successful_posts = sum(1 for result in results["social_posts"].values() if result["success"])
            results["success"] = successful_posts > 0
            results["successful_posts"] = successful_posts
            results["total_platforms"] = len(platforms)
            
            execution_time = time.time() - start_time
            results["execution_time"] = execution_time
            
            print(f"\n🎉 Workflow completed in {execution_time:.2f}s")
            print(f"✅ Successfully posted to {successful_posts}/{len(platforms)} platforms")
            
            return results
            
        except Exception as e:
            results["error"] = str(e)
            results["execution_time"] = time.time() - start_time
            print(f"❌ Workflow failed: {str(e)}")
            return results


# Example usage and configuration
def create_social_media_config() -> Dict[str, Any]:
    """Create example configuration for the Social Media Video Agent."""
    return {
        "openai_api_key": "your-openai-api-key-here",
        "blotato_api_key": "your-blotato-api-key-here", 
        "veo3_api_key": "your-veo3-api-key-here",
        
        "social_accounts": {
            "instagram_id": "your-instagram-account-id",
            "youtube_id": "your-youtube-account-id",
            "threads_id": "your-threads-account-id",
            "tiktok_id": "your-tiktok-account-id",
            "facebook_id": "your-facebook-account-id",
            "facebook_page_id": "your-facebook-page-id",
            "twitter_id": "your-twitter-account-id",
            "linkedin_id": "your-linkedin-account-id",
            "pinterest_id": "your-pinterest-account-id",
            "pinterest_board_id": "your-pinterest-board-id",
            "bluesky_id": "your-bluesky-account-id"
        },
        
        "max_retries": 3,
        "video_wait_time": 300,  # 5 minutes
        "default_platforms": ["instagram", "youtube", "tiktok"]
    }


if __name__ == "__main__":
    # Example usage
    config = create_social_media_config()
    agent = SocialMediaVideoAgent(config)
    
    # Run automation for a specific topic
    result = agent.run(
        topic="AI robots cooking in the kitchen",
        platforms=["instagram", "youtube"]
    )
    
    print(json.dumps(result, indent=2))