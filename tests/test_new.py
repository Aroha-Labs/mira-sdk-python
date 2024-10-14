import pytest
from unittest.mock import Mock, patch
from src.mira.client.mira_client import MiraClient, Flow, FlowConfig, Prompt

@pytest.fixture
def mira_client():
    return MiraClient(config={"API_KEY": "test_api_key"})

def test_execute_flow(mira_client):
    flow = Flow("org/flow", FlowConfig({}), private=False, version="1.0.0")
    input_dict = {"key": "value"}

    with patch.object(mira_client.console, 'execute_flow') as mock_execute:
        mock_execute.return_value = {"result": "success"}
        result = mira_client.execute_flow(flow, input_dict)

    mock_execute.assert_called_once_with("org", "flow", input_dict, "1.0.0")
    assert result == {"result": "success"}

def test_run_flow(mira_client):
    flow_config = FlowConfig({"name": "test_flow"})
    input_dict = {"key": "value"}

    with patch.object(mira_client.console, 'run_flow') as mock_run:
        mock_run.return_value = {"result": "success"}
        result = mira_client.run_flow(flow_config, input_dict)

    mock_run.assert_called_once_with(flow_config.dict(), input_dict)
    assert result == {"result": "success"}

def test_get_flow(mira_client):
    with patch.object(mira_client.console, 'get_flow') as mock_get:
        mock_get.return_value = {
            "config": {"name": "test_flow"},
            "private": True,
            "version": "1.0.0"
        }
        flow = mira_client.get_flow("org/flow/1.0.0")

    mock_get.assert_called_once_with("org", "flow", "1.0.0")
    assert isinstance(flow, Flow)
    assert flow.org == "org"
    assert flow.name == "flow"
    assert flow.version == "1.0.0"
    assert flow.private == True

def test_get_flows_by_author(mira_client):
    with patch.object(mira_client.console, 'get_flows_by_author') as mock_get:
        mock_get.return_value = [{"org": "org", "name": "flow1"}, {"org": "org", "name": "flow2"}]
        flows = mira_client.get_flows_by_author("@author")

    mock_get.assert_called_once_with("author")
    assert len(flows) == 2
    assert flows[0]["name"] == "flow1"
    assert flows[1]["name"] == "flow2"

def test_deploy_flow(mira_client):
    flow = Flow("@org/flow", FlowConfig({"name": "test_flow"}), private=True, version="1.0.0")

    with patch.object(mira_client.console, 'deploy_flow') as mock_deploy:
        mock_deploy.return_value = {"result": "success"}
        result = mira_client.deploy_flow(flow)

    mock_deploy.assert_called_once_with("org", "flow", flow.config.dict(), True, "1.0.0")
    assert result == {"result": "success"}

def test_get_prompt(mira_client):
    with patch.object(mira_client.console, 'get_prompt_version') as mock_get:
        mock_get.return_value = {
            "author_name": "org",
            "prompt_name": "prompt",
            "content": "Test content",
            "version": "1.0.0",
            "variables": {},
            "prompt_id": "123"
        }
        prompt = mira_client.get_prompt("org/prompt/1.0.0")

    mock_get.assert_called_once_with("org", "prompt", "1.0.0")
    assert isinstance(prompt, Prompt)
    assert prompt.org == "org"
    assert prompt.name == "prompt"
    assert prompt.version == "1.0.0"
    assert prompt.content == "Test content"
    assert prompt.prompt_id == "123"

def test_create_prompt(mira_client):
    prompt = Prompt("org/prompt", "Test content", "1.0.0", {"var": "value"})

    with patch.object(mira_client.console, 'create_prompt') as mock_create:
        mock_create.return_value = {"prompt_id": "123"}
        result = mira_client.create_prompt(prompt)

    mock_create.assert_called_once_with("org", "prompt", "1.0.0", "Test content", {"var": "value"})
    assert result.prompt_id == "123"

def test_update_prompt(mira_client):
    prompt = Prompt("org/prompt", "Updated content", "1.1.0", {"var": "new_value"})

    with patch.object(mira_client.console, 'get_prompt_version') as mock_get:
        mock_get.return_value = {"prompt_id": "123"}
        with patch.object(mira_client.console, 'add_prompt_version') as mock_update:
            mock_update.return_value = {"prompt_id": "123"}
            result = mira_client.update_prompt(prompt)

    mock_get.assert_called_once_with("org", "prompt", None)
    mock_update.assert_called_once_with("123", "1.1.0", "Updated content", {"var": "new_value"})
    assert result.prompt_id == "123"

# def test_get_prompts_by_author(mira_client):
#     with patch.object(mira_client.console, 'get_prompts_by_author') as mock_get:
#         mock_get.return_value = [
#             {"org": "org", "name": "prompt1", "version": "1.0.0", "content": "Content 1"},
#             {"org": "org", "name": "prompt2", "version": "1.0.0", "content": "Content 2"}
#         ]
#         prompts = mira_client.get_prompts_by_author("@author")

#     mock_get.assert_called_once_with("author")
#     assert len(prompts) == 2
#     assert isinstance(prompts[0], Prompt)
#     assert prompts[0].name == "prompt1"
#     assert prompts[1].name == "prompt2"

def test_get_prompts_by_author(mira_client):
    mock_prompts = [
        {
            'org': 'test_org',
            'name': 'prompt1',
            'version': '1.0.0',
            'content': 'Test content 1',
            'variables': {'var1': 'value1'}
        },
        {
            'org': 'test_org',
            'name': 'prompt2',
            'version': '2.0.0',
            'content': 'Test content 2',
            'variables': None
        }
    ]

    with patch.object(mira_client.console, 'get_prompts_by_author', return_value=mock_prompts):
        result = mira_client.get_prompts_by_author('@test_author')

    assert len(result) == 2
    assert all(isinstance(prompt, Prompt) for prompt in result)

    assert result[0].org == 'test_org'
    assert result[0].name == 'prompt1'
    assert result[0].version == '1.0.0'
    assert result[0].content == 'Test content 1'
    assert result[0].variables == {'var1': 'value1'}

    assert result[1].org == 'test_org'
    assert result[1].name == 'prompt2'
    assert result[1].version == '2.0.0'
    assert result[1].content == 'Test content 2'
    assert result[1].variables == {}

def test_get_all_versions_by_prompt(mira_client):
    mock_versions = [
        {
            'version': '1.0.0',
            'content': 'Test content 1',
            'variables': {'var1': 'value1'}
        },
        {
            'version': '2.0.0',
            'content': 'Test content 2',
            'variables': None
        }
    ]

    test_prompt = Prompt('test_org/test_prompt', 'Initial content', '1.0.0')
    test_prompt.prompt_id = 'test_id'

    with patch.object(mira_client.console, 'get_all_versions_by_prompt', return_value=mock_versions):
        result = mira_client.get_all_versions_by_prompt(test_prompt)

    assert len(result) == 2
    assert all(isinstance(prompt, Prompt) for prompt in result)

    assert result[0].org == 'test_org'
    assert result[0].name == 'test_prompt'
    assert result[0].version == '1.0.0'
    assert result[0].content == 'Test content 1'
    assert result[0].variables == {'var1': 'value1'}

    assert result[1].org == 'test_org'
    assert result[1].name == 'test_prompt'
    assert result[1].version == '2.0.0'
    assert result[1].content == 'Test content 2'
    assert result[1].variables == {}
# def test_get_all_versions_by_prompt(mira_client):
#     prompt = Prompt("org/prompt", "Content", "1.0.0")
#     prompt.prompt_id = "123"

#     with patch.object(mira_client.console, 'get_all_versions_by_prompt') as mock_get:
#         mock_get.return_value = [
#             {"version": "1.0.0", "content": "Content 1"},
#             {"version": "1.1.0", "content": "Content 2"}
#         ]
#         versions = mira_client.get_all_versions_by_prompt(prompt)

#     mock_get.assert_called_once_with("123")
#     assert len(versions) == 2
#     assert isinstance(versions[0], Prompt)
#     assert versions[0].version == "1.0.0"
#     assert versions[1].version == "1.1.0"

# @pytest.mark.parametrize("file_path,expected_result", [
#     ("/path/to/file.txt", {"result": "success"}),
#     ("/path/to/file.pdf", {"result": "success"}),
#     ("/path/to/file.csv", {"result": "success"}),
#     ("/path/to/file.md", {"result": "success"}),
#     ("/path/to/file.zip", {"result": "success"}),
# ])
# def test_add_knowledge(mira_client, file_path, expected_result):
#     with patch('os.path.exists', return_value=True), \
#          patch('os.access', return_value=True), \
#          patch('os.path.getsize', return_value=1024), \
#          patch.object(mira_client.console, 'add_knowledge') as mock_add:
#         mock_add.return_value = expected_result
#         result = mira_client.add_knowledge("org/knowledge", file_path)

#     mock_add.assert_called_once_with(file_path, "org", "knowledge")
#     assert result == expected_result

# @pytest.mark.parametrize("file_path,exception", [
#     ("/path/to/nonexistent.txt", FileNotFoundError),
#     ("/path/to/unreadable.txt", PermissionError),
#     ("/path/to/large_file.txt", ValueError),
#     ("/path/to/file.exe", ValueError),
# ])
# def test_add_knowledge_exceptions(mira_client, file_path, exception):
#     with patch('os.path.exists', return_value=file_path.endswith("nonexistent.txt")), \
#          patch('os.access', return_value=not file_path.endswith("unreadable.txt")), \
#          patch('os.path.getsize', return_value=300*1024*1024 if file_path.endswith("large_file.txt") else 1024):
#         with pytest.raises(exception):
#             mira_client.add_knowledge("org/knowledge", file_path)

# def test_get_knowledge_context_for_prompt(mira_client):
#     with patch.object(mira_client.console, 'get_knowledge_context_for_prompt') as mock_get:
#         mock_get.return_value = {"context": "Test context"}
#         result = mira_client.get_knowledge_context_for_prompt("org/knowledge", "Test prompt")

#     mock_get.assert_called_once_with("org", "knowledge", "Test prompt")
#     assert result == {"context": "Test context"}
