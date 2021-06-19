import json
from pprint import pprint

json_list = []
json_list2 = []
json_list3 = []
for i in range(1, 11):
    json_list.append({'id': i+20, 'name': f'test {i+20}'})
    json_list.append({'id': i+50, 'name': f'test {i+50}'})
    json_list = sorted(json_list, key=lambda x: x['id'])
    with open(f'data{2}.json', 'w') as f:
        json.dump(json_list, f)
with open(f'data{2}.json', 'r') as f:
    pprint(json.load(f))

# for i in range(21, 30):
#     json_list2.append({'id': i+10, 'name': f'test {i}'})
#     json_list2.append({'id': i+30, 'name': f'test {i+30}'})
#     json_list2 = sorted(json_list2, key=lambda x: x['id'])
#     with open(f'data2.json', 'w') as f:
#         json.dump(json_list2, f)


# pprint(json.load(json_list))

