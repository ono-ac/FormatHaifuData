import os

from classopt import classopt
import re
from urllib import parse
import json
import copy

@classopt(default_long=True)
class Args:
    filepath: str = os.getcwd() + '/' + "sample_haifudata.xml"
    savedir: str = "."
    csv: bool = False
    debug: bool = False
    detail: bool = False
        
        
def make_haifudic_from_haifuxml(url: str, debug:bool = False):
    url_tmp = parse.unquote(url)
    match = re.search(r'\{.*\}', url_tmp)
    org_haifu_dic = json.loads(match.group())

    haifu_dic = {} 
    haifu_dic['title'] = org_haifu_dic['title']
    haifu_dic['player'] = org_haifu_dic['name']
    haifu_dic['rule'] = org_haifu_dic['rule']
    haifu_dic['state'] = org_haifu_dic['log'][0][0]
    haifu_dic['start_point'] = org_haifu_dic['log'][0][1]
    haifu_dic['dora'] = org_haifu_dic['log'][0][2]
    haifu_dic['uradora'] = org_haifu_dic['log'][0][3]
    haifu_dic['start_player'] = org_haifu_dic['log'][0][0][0] % 4
    haifu_dic['start_hand'] = [org_haifu_dic['log'][0][4], org_haifu_dic['log'][0][7], org_haifu_dic['log'][0][10], org_haifu_dic['log'][0][13]]
    haifu_dic['tumo'] = [org_haifu_dic['log'][0][5], org_haifu_dic['log'][0][8], org_haifu_dic['log'][0][11], org_haifu_dic['log'][0][14]]
    haifu_dic['kiri'] = [org_haifu_dic['log'][0][6], org_haifu_dic['log'][0][9], org_haifu_dic['log'][0][12], org_haifu_dic['log'][0][15]]
    haifu_dic['end'] = {}
    haifu_dic['end']['name'] = org_haifu_dic['log'][0][16][0]
    if haifu_dic['end']['name'] != '流局':
        haifu_dic['end']['point_view'] = org_haifu_dic['log'][0][16][2][3]
    haifu_dic['end']['point_shift'] = org_haifu_dic['log'][0][16][1]
    
    if (debug):
        print(haifu_dic)
    
    return haifu_dic

def hainum2hainame(hainum):
    naki = ''
    if type(hainum) is str:
        if hainum[0] == 'r':
            naki = 'reach:'
            hainum = int(hainum[1:])
        else:
            return hainum

    haisyu = ''
    hainame = ''
    if hainum // 10 == 1:
        haisyu = 'm'
    elif hainum //10 == 2:
        haisyu = 'p'
    elif hainum //10 == 3:
        haisyu = 's'
    elif hainum //10 == 4:
        haisyu = 'j'

    if hainum == 60:
        hainame = 'tumogiri'
    elif hainum == 51:
        hainame = 'R5m'
    elif hainum == 52:
        hainame = 'R5p'
    elif hainum == 53:
        hainame = 'R5s'
    else:
        hainame = naki + str(int(hainum % 10)) + haisyu
    
    return hainame

def save_csv(haifu_data, savedir_path = ".", debug = False):
    str_tmps = []
    savefile_path = savedir_path + "/created_haifudata.csv"
    str_tmps.append(['', haifu_data['player'][0], haifu_data['player'][1], haifu_data['player'][2], haifu_data['player'][3]])
    #start
    tmp = ['0', '', '', '', '']
    tmp[haifu_data['start_player'] + 1] = 'start'
    str_tmps.append(tmp)
    check_tumo = [0, 0, 0, 0]
    check_dahai = [0, 0, 0, 0]
    num = 1
    p = haifu_data['start_player']
    tumo_f = False
    
    while len(haifu_data['tumo'][p]) > check_tumo[p]:
        tmp = [str(num), '', '', '', '']
        tmp[p + 1] = hainum2hainame(haifu_data['tumo'][p][check_tumo[p]])
        check_tumo[p] += 1
        str_tmps.append(tmp)
        num += 1
        
        # case > tumo finish
        if len(haifu_data['kiri'][p]) <= check_dahai[p]:
            tmp = [str(num), '', '', '', '']
            tmp[p + 1] = 'tumo_agari'
            str_tmps.append(tmp)
            tumo_f = True
            break
        
        tmp = [str(num), '', '', '', '']
        tmp[p + 1] = hainum2hainame(haifu_data['kiri'][p][check_dahai[p]])
        check_dahai[p] += 1
        str_tmps.append(tmp)
        
        p = (p + 1) % 4
        num += 1
    
    # case > the other finish
    if tumo_f == False :
        p = (p - 1) % 4
        tmp = [str(num), '', '', '', '']
        if haifu_data['end']['name'] == '和了' :
            tmp[p + 1] = 'ron_agari'
        else:
            tmp[p + 1] = 'ryukyoku' 
        str_tmps.append(tmp)
         
    with open(savefile_path, 'w') as cf:
        write_tmp = ''
        for raw in str_tmps:
            write_tmp += str(raw[0]) + ',' + str(raw[1]) + ',' + str(raw[2]) + ',' + str(raw[3]) + ',' + str(raw[4]) + '\n'
        cf.write(write_tmp)
        
    if (debug):
        print(" >> {}".format(savefile_path))
        print(write_tmp)
        
def save_jsonl(haifu_data, savedir_path = ".", debug = False, detail = False):
    savefile_path = savedir_path + "/created_haifudata.jsonl"
    haifu_list = []
    haifu_list.append({'num':0, 'playernum': haifu_data['start_player'], 'playername': haifu_data['player'][haifu_data['start_player']], 'hainum': 0, 'action': "start", 'hand': []})
    check_tumo = [0, 0, 0, 0]
    check_dahai = [0, 0, 0, 0]
    num = 1
    p = haifu_data['start_player']
    players_hand = haifu_data['start_hand']
    
    def TumoChecker(hainum):
        if type(hainum) is str:
            if hainum[0] == 'c':
                return ['chi',  int(hainum[1:3]), int(hainum[3:5]), int(hainum[5:])]
            elif 'p' in hainum:
                tmp = re.sub('p', '', hainum)
                return ['pon',  int(tmp[0:2]), int(tmp[2:4]), int(tmp[4:])]

        else:
            return ["tumo", hainum]

    def DahaiChecker(hainum):
        if type(hainum) is str:
            if hainum[0] == 'r':
                return ['reach', int(hainum[1:])]
            else:
                return ['ankan', int(hainum[0:2]), int(hainum[2:4]), int(hainum[4:6]), int(hainum[7:])]
        else:
            return ["dahai", hainum]

    
    if (detail):
        print("-------------------------------------------------------------")
        print("{}".format(0))
        print("START HAND")
        for i in range(4):
            print( "({}p) {} : ".format(i, haifu_data['player'][i]) + ' '.join([ hainum2hainame(h_num) for h_num in sorted(haifu_data['start_hand'][i])] ))
        print("-------------------------------------------------------------")
    
    while len(haifu_data['tumo'][p]) > check_tumo[p]:
        
        # tumo turn
        tumoc = TumoChecker(haifu_data['tumo'][p][check_tumo[p]])
        before_hand = copy.copy(players_hand[p])
        players_hand[p].append(tumoc[1])
        haifu_list.append({'num':num, 'playernum': p, 'playername': haifu_data['player'][p], 'hainum':tumoc[1], 'action': tumoc[0], 'hand':  sorted(players_hand[p])})
        if (detail):
            print('{}'.format(num))
            print('\t({}p) {}   {} : {}'.format(p, haifu_data['player'][p], tumoc[0], hainum2hainame(tumoc[1])))
            print("[" + ' '.join([hainum2hainame(h_num) for h_num in sorted(before_hand)]) + "]")
            print(" -> [" + ' '.join([hainum2hainame(h_num) for h_num in sorted(players_hand[p])]) + "]")
            print("\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
        check_tumo[p] += 1
        num += 1

        
        # dahai turn
        if len(haifu_data['kiri'][p]) <= check_dahai[p]:  #tumo finish
            break
            
        dahaic = DahaiChecker(haifu_data['kiri'][p][check_dahai[p]])

        if dahaic[1] == 60:        # tumogiri
            players_hand[p].remove(tumoc[1])
            if dahaic[0] == 'reach':
                haifu_list.append(
                    {'num':num, 'playernum': p, 'playername': haifu_data['player'][p], 'hainum':tumoc[1], 'action': 'reach_tumogiri', 'hand': sorted(players_hand[p])})
            else:
                haifu_list.append(
                    {'num':num, 'playernum': p, 'playername': haifu_data['player'][p], 'hainum':tumoc[1], 'action': 'dahai_tumogiri', 'hand': sorted(players_hand[p])})
        else:
            players_hand[p].remove(dahaic[1])
            haifu_list.append({'num':num, 'playernum': p, 'playername': haifu_data['player'][p], 'hainum':dahaic[1], 'action': dahaic[0], 'hand': sorted(players_hand[p])})
        if (detail):
            print('{}'.format(num))
            print('\t({}p) {}   dahai : {}'.format(p, haifu_data['player'][p], hainum2hainame(dahaic[1])))
            print(" -> [" + ' '.join([hainum2hainame(h_num) for h_num in sorted(players_hand[p])]) + "]")
            print("\n-------------------------------------------------------------")
              
        check_dahai[p] += 1
        
        # ankan
        if dahaic[0] != 'ankan':
            p = (p + 1) % 4
            
        num += 1
          
    str_tmps = ''    
    for haifu_j in haifu_list:
        tmp = json.dumps(haifu_j, ensure_ascii=False)
        str_tmps += tmp + '\n'

    with open(savefile_path, 'w', encoding='utf-8') as f:
        f.write(str_tmps)
        

def main(args: Args):
    haifu_filepath: str = args.filepath
    savedir: str = args.savedir
    csv:bool = args.csv
    debug: bool = args.debug
    detail: bool = args.detail
    
    def open_xml(xml_filepath: str) -> str:
        with open(xml_filepath, 'r', encoding = 'utf-8') as f:
            _xml = f.read()
        return _xml
    
    haifuxml: str = open_xml(haifu_filepath)
    haifudic = make_haifudic_from_haifuxml(haifuxml, debug=debug)
    save_jsonl(haifudic, savedir_path = savedir , debug = debug, detail = detail)
    if (csv):
        save_csv(haifudic, debug = debug, savedir_path = savedir)
    
if __name__ == "__main__":
    args = Args.from_args()
    main(args)
