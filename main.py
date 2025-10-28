"""CLI entrypoint for running SmallAgents examples."""
import argparse
import yaml
from agents.search_agent import SearchAgent


def load_config(path: str = "config.yaml") -> dict:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        return {}


def main():
    parser = argparse.ArgumentParser(description="Run an example SmallAgent")
    parser.add_argument("--agent", choices=["search"], default="search")
    parser.add_argument("--query", default="example")
    parser.add_argument("--config", default="config.yaml")
    args = parser.parse_args()

    config = load_config(args.config)

    if args.agent == "search":
        agent_cfg = config.get("agents", {}).get("search", {})
        agent = SearchAgent(agent_cfg)
        out = agent.run(query=args.query)
        print(out)


if __name__ == "__main__":
    main()
