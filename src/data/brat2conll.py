from os import listdir, path
from collections import namedtuple
import argparse
from collections import defaultdict

parser = argparse.ArgumentParser()
parser.add_argument(
    "--input_ann_file",
    dest="input_ann_file",
    type=str,
    default='',
    help="Input ann file",
)

parser.add_argument(
    "--input_txt_file",
    dest="input_txt_file",
    type=str,
    default='',
    help="Input txt file",
)

parser.add_argument(
    "--output_path",
    dest="output_path",
    type=str,
    default='',
    help="Output path",
)


def def_value():
    return []


def get_data_from_files(input_ann_file, input_txt_file):
    # with open(input_txt_file, 'r') as f:
    #     text_string = f.read()
    # l_texts = text_string.split('\n')
    # print(len(l_texts))

    l_texts = []
    with open(input_txt_file, 'r') as fi:
        for line in fi:
            l_texts.append(line)
    print(len(l_texts))

    with open(input_ann_file, 'r') as fi:
        id = 0
        last_estado = 'T'
        l_ann_id = []
        for line in fi:
            if last_estado == 'A':
                if line[0] == 'T':
                    last_estado = 'T'
                    l_ann_id.append({'line_id': id, 'line': line})
                else:
                    last_estado = line[0]
            elif last_estado != 'T':
                if line[0] == 'T':
                    last_estado = 'T'
                    id += 1
                    l_ann_id.append({'line_id': id, 'line': line})
                else:
                    last_estado = line[0]
            else:
                if line[0] == 'T':
                    last_estado = 'T'
                    l_ann_id.append({'line_id': id, 'line': line})
                else:
                    last_estado = line[0]

    print(len(l_ann_id))

    d_annotations = defaultdict(list)
    for ann in l_ann_id:
        line_id = ann['line_id']
        line = ann['line']

        d_annotations[line_id].append(line)

    print(len(d_annotations.keys()))

    print(l_texts[-1])
    print(d_annotations[1198])

    input_annotations = []
    for line, text in zip(l_annotations, l_texts):
        if line[0] == 'T':
            annotation_record = {}
            entry = line.split('\t')

            annotation_record["label"] = entry[1].split()[0].upper()

            str_limits = entry[1][len(annotation_record["label"]):-1]
            l_limits = []
            if ';' in str_limits:
                l_str_limits = str_limits.split(';')
                for str_limit in l_str_limits:
                    start, end = str_limit.split()
                    l_limits.append({
                        'start': int(start),
                        'end': int(end)
                    })
            else:
                start, end = str_limits.split()
                l_limits.append({
                    'start': int(start),
                    'end': int(end)
                })
            annotation_record["l_limits"] = l_limits

            annotation_record["l_chunk"] = entry[2].split()
            annotation_record["text"] = text
            input_annotations.append(annotation_record)

    return input_annotations


# def get_bioconll_from_brat_data(l_brat_data):
    # label l_limits (start, end) l_chunk text


def parse_text(input_ann_file, input_txt_file, output_path):
    l_data = get_data_from_files(input_ann_file, input_txt_file)
    # get_bioconll_from_brat_data(l_data)




if __name__ == '__main__':
    args = parser.parse_args()
    # format_convertor = Brat2ConllConvertor(args.input_ann_file, args.output_path)
    # format_convertor.parse_text()
    parse_text(args.input_ann_file, args.input_txt_file, args.output_path)