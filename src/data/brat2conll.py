# from os import listdir, path
# from collections import namedtuple
import argparse

from collections import defaultdict
from nltk.tokenize import word_tokenize

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


def get_data_from_files(input_ann_file, input_txt_file):
    """
    Funcion que lee de los ficheros ann y txt. Devuelve una tupla, un diccionario donde la key es la linea del txt y el value
    el string de las líneas T del fichero ann, y una lista con todas las lineas del txt.
    :param input_ann_file:
    :param input_txt_file:
    :return:
        {
            0: ["T1	Action 3 12	presencia", "T2	Concept 17 20	gen", ...],
            1: ["T6	Concept 101 109;110 112;113 119	factores de riesgo", "T7	Concept 133 137;138 151	raza afroamericana", ...],
            ...
        },
        [
            "La presencia del gen de células falciformes y otro normal se denomina rasgo drepanocítico.",
            "Entre los factores de riesgo están ser de raza afroamericana o el exceso de peso.",
            ...
        ]
    """

    l_texts = []
    with open(input_txt_file, 'r') as fi:
        for line in fi:
            l_texts.append(line)

    with open(input_ann_file, 'r') as fi:
        id = 0
        last_estado = 'R'
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
                    l_ann_id.append({'line_id': id, 'line': line})
                    id += 1
                else:
                    last_estado = line[0]
            else:
                if line[0] == 'T':
                    last_estado = 'T'
                    l_ann_id.append({'line_id': id, 'line': line})
                else:
                    last_estado = line[0]

    d_annotations = defaultdict(list)
    for ann in l_ann_id:
        line_id = ann['line_id']
        line = ann['line']

        d_annotations[line_id].append(line)

    return d_annotations, l_texts


def get_bioconll_from_brat_data(d_data_ann, l_texts):
    # Sentiros libres de hacerla como creais conveniente
    for num_linea, l_anotaciones in d_data_ann.items():
        linea = l_texts[num_linea]
        linea = linea.replace('\n', '') # Lo elimino antes por si da por culo
        linea_tokens = word_tokenize(linea, language='spanish')

        for anotacion in l_anotaciones:
            # T28	Concept 432 437;438 440;441 445	menor de edad
            l_anotacion = anotacion.split('\t')
            etiqueta = l_anotacion[1]
            str_etiqueta = l_anotacion[3]
            str_pos_etiqueta = l_anotacion[2]

            l_pos_etiqueta = []
            for str_pos in str_pos_etiqueta.split(';'):
                l_tmp_ = str_pos.split()

                l_pos_etiqueta.append({
                    'ini': int(l_tmp_)[0],
                    'fin': int(l_tmp_)[1]
                })



def parse_text(input_ann_file, input_txt_file, output_path):
    d_data_ann, l_texts = get_data_from_files(input_ann_file, input_txt_file)
    get_bioconll_from_brat_data(d_data_ann, l_texts)




if __name__ == '__main__':
    args = parser.parse_args()
    # format_convertor = Brat2ConllConvertor(args.input_ann_file, args.output_path)
    # format_convertor.parse_text()
    parse_text(args.input_ann_file, args.input_txt_file, args.output_path)