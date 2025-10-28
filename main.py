"""CLI entrypoint for running SmallAgents examples."""

import argparse
from typing import Any, Dict

import yaml

from agents.search_agent import SearchAgent
from agents.api_agent import APIAgent
from agents.social_media_video_agent import SocialMediaVideoAgent


def load_config(path: str = "config.yaml") -> Dict[str, Any]:
    """Load configuration from YAML file."""
    try:
        with open(path, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        return {}


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Run an example SmallAgent")
    parser.add_argument(
        "--agent", 
        choices=["search", "api", "social-video"], 
        default="search",
        help="Type of agent to run"
    )
    parser.add_argument("--query", default="example", help="Query or topic for the agent")
    parser.add_argument("--config", default="config.yaml", help="Configuration file path")
    parser.add_argument("--platforms", nargs="+", help="Social media platforms (for social-video agent)")
    args = parser.parse_args()

    config = load_config(args.config)

    if args.agent == "search":
        agent_cfg = config.get("agents", {}).get("search", {})
        agent = SearchAgent(agent_cfg)
        out = agent.run(query=args.query)
        print(out)
        
    elif args.agent == "api":
        agent_cfg = config.get("agents", {}).get("api", {})
        agent = APIAgent(agent_cfg)
        # Example API call
        out = agent.run(method="GET", endpoint="/posts/1")
        print(out)
        
    elif args.agent == "social-video":
        agent_cfg = config.get("agents", {}).get("social_video", {})
        agent = SocialMediaVideoAgent(agent_cfg)
        platforms = args.platforms or ["instagram", "youtube"]
        out = agent.run(topic=args.query, platforms=platforms)
        print(f"✅ Posted to {out.get('successful_posts', 0)}/{out.get('total_platforms', 0)} platforms")
        print(f"🎬 Video: {out.get('steps', {}).get('video_url', 'N/A')}")


if __name__ == "__main__":
    main()
