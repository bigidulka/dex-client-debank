import json
from pathlib import Path


def test_inventory_has_browser_harness_paths():
    data = json.loads(Path('endpoint_inventory.json').read_text())
    assert data['client'] == 'debank'
    assert data['browser_harness']['api_live_endpoints']
    assert '/history/list' in data['browser_harness']['js_extracted_paths']
