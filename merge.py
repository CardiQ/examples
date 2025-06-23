import os
import json

src_dir = os.path.dirname(__file__)
merge_dir = os.path.join(src_dir, 'merged_examples')
os.makedirs(merge_dir, exist_ok=True)

def process_gold_dir(gold_dir, app_path, merge_app_dir, index):
    for fname in os.listdir(gold_dir):
        if not fname.endswith('.json'):
            print(f'{fname} not a json file')
            continue
        gold_path = os.path.join(gold_dir, fname)
        main_path = os.path.join(app_path, fname)
        if not os.path.isfile(main_path):
            print(f'{main_path} not found')
            continue
        try:
            with open(main_path, 'r') as f:
                main_data = json.load(f)
        except Exception as e:
            print(f'Error loading {main_path}: {e}')
            continue
        try:
            with open(gold_path, 'r') as f:
                gold_data = json.load(f)
        except Exception as e:
            print(f'Error loading {gold_path}: {e}')
            continue
        if isinstance(gold_data, list):
            gold_data = gold_data[1] if len(gold_data) > 1 else {}
        human_gt = {}
        if 'minimal' in gold_data:
            human_gt['single-action'] = gold_data['minimal']
        if 'batched' in gold_data:
            human_gt['grouped-action'] = gold_data['batched']
        main_data['human-ground-truth'] = human_gt
        out_path = os.path.join(merge_app_dir, fname)
        try:
            with open(out_path, 'w') as f:
                json.dump(main_data, f, ensure_ascii=False, indent=2)
            index[0] += 1
            print(f'{index[0]}/369 examples merged')
        except Exception as e:
            print(f'Error writing {out_path}: {e}')

for app_dir in os.listdir(src_dir):
    app_path = os.path.join(src_dir, app_dir)
    if not os.path.isdir(app_path):
        continue
    if app_dir in ['merged_examples', '.git']:
        continue
    gold_dir = os.path.join(app_path, 'gold')
    if not os.path.isdir(gold_dir):
        continue
    merge_app_dir = os.path.join(merge_dir, app_dir)
    os.makedirs(merge_app_dir, exist_ok=True)
    index = [0]
    process_gold_dir(gold_dir, app_path, merge_app_dir, index)
    notsure_dir = os.path.join(gold_dir, 'notsure')
    if os.path.isdir(notsure_dir):
        process_gold_dir(notsure_dir, app_path, merge_app_dir, index)