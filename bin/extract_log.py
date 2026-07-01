import json
import os

log_path = "/Users/jiucai/.gemini/antigravity-ide/brain/30275be6-6f47-4780-afc2-57adbc295385/.system_generated/logs/transcript.jsonl"
output_path = "/Users/jiucai/.gemini/antigravity-ide/brain/30275be6-6f47-4780-afc2-57adbc295385/scraped_notion_content.md"

if os.path.exists(log_path):
    with open(log_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data = json.loads(line)
                if data.get('step_index') == 382:
                    content = data.get('content', '')
                    with open(output_path, 'w', encoding='utf-8') as out:
                        out.write(content)
                    print(f"Successfully wrote content to {output_path}")
                    break
            except Exception as e:
                print(f"Error parsing line: {e}")
else:
    print(f"Log path does not exist: {log_path}")
