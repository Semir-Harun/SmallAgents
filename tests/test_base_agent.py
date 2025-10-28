from agents.base_agent import BaseAgent


def test_base_agent_info_returns_name_and_config():
    cfg = {"k": "v"}
    a = BaseAgent(cfg)
    info = a.info()
    assert info["name"] == "BaseAgent"
    assert info["config"] == cfg


def test_base_agent_run_not_implemented():
    a = BaseAgent()
    try:
        a.run()
        raised = False
    except NotImplementedError:
        raised = True
    assert raised
