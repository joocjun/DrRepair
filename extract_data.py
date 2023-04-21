import json 
import os
from tqdm import tqdm
from argparse import ArgumentParser

with open('/home/sejune/DrRepair/data/err-data-compiler--auto-corrupt--codeforce--deepfix-style/8A/34218.json') as f:
    data = json.load(f)


def merge_lines(data, err_idx=0):
    code = '' 
    mod_code = ''
    mod_com_code = ''
    err_lines = sorted([int(idx) for idx in data['errors'][err_idx]['action_name_list'].keys()])
    err_lines = [str(idx) for idx in err_lines]
    err_code = {str(idx): code for idx, code in zip(err_lines, data['errors'][err_idx]['mod_code'])}
    for idx, line in enumerate(data['lines']):
        code += '\t'*line['indent'] + line['code'] + '\n'
        if str(idx) in err_lines:
            mod_code += '\t'*line['indent'] + err_code[str(idx)] + '\n'
            if str(data['errors'][err_idx]['err_line']) == str(idx):
                mod_com_code += '\t'*line['indent'] + err_code[str(idx)] + f"  /*{data['errors'][err_idx]['err_msg']}*/"+ '\n'
            else:
                mod_com_code += '\t'*line['indent'] + err_code[str(idx)] + '\n'
        else:
            mod_code += '\t'*line['indent'] + line['code'] + '\n'

    return code, mod_code, mod_com_code



def main(args):
    shard_list = os.listdir(args.data_dir)
    reformatted_data = []
    for shard in tqdm(shard_list):
        data_list = os.listdir(os.path.join(args.data_dir, shard))
        for data in data_list:
            with open(os.path.join(args.data_dir, shard, data)) as f:
                data = json.load(f)
            for err_idx in range(len(data['errors'])):
                code, mod_code, err_msg = merge_lines(data, err_idx)
                reformatted_data.append({'code': code, 'mod_code': mod_code, 'err_msg': err_msg})
    os.makedirs(args.output_dir, exist_ok=True)
    with open(os.path.join(args.output_dir, 'train.json'), 'w') as f:
        json.dump(reformatted_data, f, indent=4)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--data_dir', type=str, default='/home/sejune/DrRepair/data/err-data-compiler--auto-corrupt--codeforce--deepfix-style')
    parser.add_argument('--output_dir', type=str, default='/home/ubuntu/LKLab-storage-texas/sejune/code_data/dr_repair')
    args = parser.parse_args()
    main(args)