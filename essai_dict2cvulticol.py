import csv
import PySimpleGUI as sg
# convert the dict to a multicolumn csv file
# key name transformed by its ascii value

# input dict
input_dict={10: 14344391, 97: 8840897, 101: 7215609, 49: 6734380, 48: 5740291, 105: 5561841, 50: 5237479, 111: 5183289, 110: 4834279, 114: 4583500, 108: 4468017, 115: 4163001, 57: 3855490, 51: 3767584, 56: 3567258, 116: 3436156, 52: 3391342, 53: 3355180, 109: 3210393, 54: 3118364, 55: 3100596, 99: 2615356, 100: 2489245, 121: 2376512, 104: 2342106, 117: 2310646, 98: 2113153, 107: 2014184, 103: 1721051, 112: 1626136, 106: 1238200, 118: 1052686, 102: 983982, 119: 803872, 122: 763971, 65: 604870, 120: 481014, 69: 459998, 73: 357135, 76: 331897, 79: 330478, 82: 320192, 78: 316845, 83: 315458, 77: 260296, 46: 253548, 84: 249590, 67: 209435, 68: 199573, 95: 193780, 66: 188255, 113: 179143, 72: 163121, 89: 161134, 75: 144155, 33: 143170, 85: 137387, 45: 134634, 80: 131718, 71: 130282, 42: 123988, 74: 122475, 64: 108303, 32: 100814, 70: 81449, 86: 76328, 87: 59776, 90: 53620, 47: 53062, 35: 49228, 36: 36173, 88: 36085, 224: 34760, 184: 30697, 44: 30187, 92: 28677, 43: 27513, 38: 27483, 61: 24486, 41: 19012, 63: 18778, 81: 17956, 40: 17087, 39: 15590, 59: 12791, 34: 12235, 60: 11176, 93: 10847, 37: 10707, 126: 8371, 58: 8168, 91: 7769, 195: 7574, 94: 6402, 96: 5679, 185: 5497, 177: 4352, 62: 3584, 136: 2839, 159: 2609, 153: 2537, 133: 2078, 163: 2029, 132: 1871, 194: 1723, 160: 1712, 183: 1658, 182: 1575, 179: 1478, 176: 1442, 150: 1388, 129: 1360, 149: 1302, 151: 1264, 167: 1200, 216: 1182, 180: 1106, 123: 1072, 178: 1065, 125: 983, 196: 921, 170: 895, 162: 872, 158: 862, 181: 837, 128: 811, 171: 766, 217: 764, 137: 749, 169: 727, 226: 725, 124: 714, 161: 637, 173: 607, 188: 537, 145: 527, 165: 516, 215: 450, 206: 430, 164: 425, 148: 363, 168: 354, 186: 336, 135: 310, 197: 297, 152: 269, 156: 263, 208: 244, 138: 237, 130: 227, 209: 195, 131: 192, 155: 162, 134: 159, 207: 152, 140: 145, 143: 137, 141: 136, 166: 136, 174: 125, 147: 117, 191: 117, 172: 114, 189: 101, 241: 100, 175: 97, 187: 95, 225: 88, 190: 86, 154: 85, 239: 82, 139: 73, 142: 58, 144: 51, 146: 43, 157: 39, 227: 29, 231: 21, 229: 19, 228: 19, 230: 17, 203: 11, 246: 11, 198: 8, 232: 7, 210: 7, 204: 7, 252: 7, 248: 6, 240: 6, 192: 6, 8: 6, 233: 5, 250: 5, 253: 5, 237: 4, 219: 3, 236: 3, 247: 3, 213: 3, 205: 3, 201: 3, 243: 2, 249: 2, 238: 2, 200: 2, 223: 2, 3: 2, 211: 1, 127: 1, 214: 1, 234: 1, 221: 1, 26: 1, 4: 1}

def to_csv(header, compt, nb_col):
# 1st param : header example ["key_name", "value_name":]
# 2nd param : dict to present
# 3rd param : col number
    data = []
    try:
        f = open("/winbad/output_file.csv", "w")
        writer = csv.writer(f)
    except Exception as e1:
        print(e1)
    else:
            # write csv column header
            header_line=[]
            for i in range(nb_col):
                for head_k in header:
                    header_line.append(head_k+"_"+str(i))
            try:
                # write input dict to csv file
                writer.writerow(header_line)
            except Exception as e2:
                print(e2)
            else:
                row_line=[]
                nb_elem=0
                for elem in compt.keys():
                    # if elem is not printable give its ascii number value instead
                    if elem > 32 and elem < 127:
                            prn_elem = chr(elem)
                    else:
                        prn_elem = "ASCII("+str(elem)+")"
                    if nb_elem < nb_col:
                        row_line.append(prn_elem)
                        row_line.append(compt[elem])
                        nb_elem = nb_elem + 1
                    else:
                       writer.writerow(row_line)
                       data.append(row_line)
                       row_line=[prn_elem]
                       row_line.append(compt[elem])
                       nb_elem=1
            finally:
                f.close()
    return header_line, data, 2*nb_col

header = ["Key_col", "Val_col"]
header_line, data, num_rows = to_csv(header,input_dict,5)

print(header_line, data, num_rows)
layout = [[sg.Table(data, headings=header_line, num_rows=10)]]
window = sg.Window('Titre', layout)


while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
            break
window.close()
