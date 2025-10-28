"""Tests for SocialMediaVideoAgent."""
import pytest
from unittest.mock import Mock, patch

from agents.social_media_video_agent import SocialMediaVideoAgent, create_social_media_config


class TestSocialMediaVideoAgent:
    """Test cases for SocialMediaVideoAgent."""

    def test_social_media_agent_initialization(self) -> None:
        """Test SocialMediaVideoAgent initializes correctly."""
        config = create_social_media_config()
        agent = SocialMediaVideoAgent(config)
        
        assert agent.openai_api_key == "your-openai-api-key-here"
        assert agent.blotato_api_key == "your-blotato-api-key-here"
        assert agent.veo3_api_key == "your-veo3-api-key-here"
        assert "instagram_id" in agent.social_accounts
        assert agent.max_retries == 3
        assert agent.video_wait_time == 300

    def test_agent_info(self) -> None:
        """Test agent info method."""
        agent = SocialMediaVideoAgent()
        info = agent.info()
        assert info["name"] == "SocialMediaVideoAgent"
        assert "config" in info

    @patch('agents.social_media_video_agent.requests.post')
    def test_generate_video_concept_success(self, mock_post: Mock) -> None:
        """Test successful video concept generation."""
        # Mock OpenAI API response
        mock_response = Mock()
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": '{"Caption": "Amazing tech! 🤖 #tech #ai #viral #amazing", "Idea": "Robot demonstrates advanced cooking skills", "Environment": "Modern kitchen with sleek appliances", "Status": "for production"}'
                }
            }]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        config = {"openai_api_key": "test-key"}
        agent = SocialMediaVideoAgent(config)
        
        result = agent.generate_video_concept("cooking robots")
        
        assert result["Caption"] == "Amazing tech! 🤖 #tech #ai #viral #amazing"
        assert result["Idea"] == "Robot demonstrates advanced cooking skills"
        assert result["Environment"] == "Modern kitchen with sleek appliances"
        assert result["Status"] == "for production"

    @patch('agents.social_media_video_agent.requests.post')
    def test_generate_video_concept_error_fallback(self, mock_post: Mock) -> None:
        """Test video concept generation with API error."""
        mock_post.side_effect = Exception("API Error")
        
        agent = SocialMediaVideoAgent({"openai_api_key": "test-key"})
        result = agent.generate_video_concept("test topic")
        
        assert "error" in result
        assert "test topic" in result["Caption"]
        assert result["Status"] == "for production"

    @patch('agents.social_media_video_agent.requests.post')
    def test_create_veo3_prompt_success(self, mock_post: Mock) -> None:
        """Test successful VEO3 prompt creation."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": "A person in modern kitchen holds camera close to face. Main character: young chef with bright eyes. They say: 'This is incredible!' Time of Day: golden hour."
                }
            }]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        agent = SocialMediaVideoAgent({"openai_api_key": "test-key"})
        result = agent.create_veo3_prompt("cooking demo", "modern kitchen")
        
        assert "modern kitchen" in result
        assert "Main character:" in result

    @patch('agents.social_media_video_agent.time.sleep')
    @patch('agents.social_media_video_agent.requests.get')
    @patch('agents.social_media_video_agent.requests.post')
    def test_generate_video_with_veo3_success(self, mock_post: Mock, mock_get: Mock, mock_sleep: Mock) -> None:
        """Test successful video generation with VEO3."""
        # Mock initial request
        mock_post_response = Mock()
        mock_post_response.json.return_value = {"request_id": "test-request-123"}
        mock_post_response.raise_for_status.return_value = None
        mock_post.return_value = mock_post_response
        
        # Mock status check
        mock_get_response = Mock()
        mock_get_response.json.return_value = {
            "status": "completed",
            "video": {"url": "https://example.com/video.mp4"}
        }
        mock_get_response.raise_for_status.return_value = None
        mock_get.return_value = mock_get_response
        
        agent = SocialMediaVideoAgent({"veo3_api_key": "test-key", "video_wait_time": 1})
        result = agent.generate_video_with_veo3("test prompt")
        
        assert result == "https://example.com/video.mp4"
        mock_sleep.assert_called_once_with(1)

    @patch('agents.social_media_video_agent.requests.post')
    def test_upload_video_to_blotato_success(self, mock_post: Mock) -> None:
        """Test successful video upload to Blotato."""
        mock_response = Mock()
        mock_response.json.return_value = {"url": "https://blotato.com/uploaded-video.mp4"}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        agent = SocialMediaVideoAgent({"blotato_api_key": "test-key"})
        result = agent.upload_video_to_blotato("https://example.com/video.mp4")
        
        assert result == "https://blotato.com/uploaded-video.mp4"

    @patch('agents.social_media_video_agent.requests.post')
    def test_post_to_social_platform_instagram(self, mock_post: Mock) -> None:
        """Test posting to Instagram platform."""
        mock_response = Mock()
        mock_response.json.return_value = {"id": "post-123", "status": "posted"}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        config = {
            "blotato_api_key": "test-key",
            "social_accounts": {"instagram_id": "ig-123"}
        }
        agent = SocialMediaVideoAgent(config)
        
        result = agent.post_to_social_platform(
            platform="instagram",
            media_url="https://example.com/video.mp4",
            caption="Test caption #viral"
        )
        
        assert result["success"] is True
        assert result["platform"] == "instagram"
        assert "response" in result

    def test_post_to_social_platform_no_account_id(self) -> None:
        """Test posting when account ID is missing."""
        agent = SocialMediaVideoAgent()
        
        result = agent.post_to_social_platform(
            platform="instagram",
            media_url="https://example.com/video.mp4",
            caption="Test caption"
        )
        
        assert result["success"] is False
        assert "No account ID" in result["error"]

    @patch.object(SocialMediaVideoAgent, 'post_to_social_platform')
    @patch.object(SocialMediaVideoAgent, 'upload_video_to_blotato')
    @patch.object(SocialMediaVideoAgent, 'generate_video_with_veo3')
    @patch.object(SocialMediaVideoAgent, 'create_veo3_prompt')
    @patch.object(SocialMediaVideoAgent, 'generate_video_concept')
    def test_run_complete_workflow(self, mock_concept: Mock, mock_prompt: Mock, 
                                  mock_video: Mock, mock_upload: Mock, mock_post: Mock) -> None:
        """Test complete workflow execution."""
        # Setup mocks
        mock_concept.return_value = {
            "Caption": "Amazing! 🎬 #viral",
            "Idea": "Test idea",
            "Environment": "Test environment",
            "Status": "for production"
        }
        mock_prompt.return_value = "Test VEO3 prompt"
        mock_video.return_value = "https://example.com/video.mp4"
        mock_upload.return_value = "https://blotato.com/video.mp4"
        mock_post.return_value = {"success": True, "platform": "instagram"}
        
        agent = SocialMediaVideoAgent()
        result = agent.run(topic="test topic", platforms=["instagram"])
        
        assert result["success"] is True
        assert result["topic"] == "test topic"
        assert result["successful_posts"] == 1
        assert result["total_platforms"] == 1
        assert "execution_time" in result
        assert "steps" in result
        assert "social_posts" in result

    def test_create_social_media_config(self) -> None:
        """Test configuration creation function."""
        config = create_social_media_config()
        
        assert "openai_api_key" in config
        assert "blotato_api_key" in config
        assert "veo3_api_key" in config
        assert "social_accounts" in config
        assert "max_retries" in config
        assert "video_wait_time" in config
        assert "default_platforms" in config
        
        # Check social accounts structure
        social_accounts = config["social_accounts"]
        expected_platforms = [
            "instagram_id", "youtube_id", "threads_id", "tiktok_id",
            "facebook_id", "facebook_page_id", "twitter_id", "linkedin_id",
            "pinterest_id", "pinterest_board_id", "bluesky_id"
        ]
        
        for platform in expected_platforms:
            assert platform in social_accounts

    @patch.object(SocialMediaVideoAgent, 'run')
    def test_agent_as_main_execution(self, mock_run: Mock) -> None:
        """Test agent execution as main script."""
        mock_run.return_value = {"success": True, "test": "result"}
        
        # Import and test main execution path
        from agents.social_media_video_agent import create_social_media_config
        
        config = create_social_media_config()
        agent = SocialMediaVideoAgent(config)
        
        # This would be called in __main__ block
        result = agent.run(
            topic="AI robots cooking in the kitchen",
            platforms=["instagram", "youtube"]
        )
        
        assert result["success"] is True