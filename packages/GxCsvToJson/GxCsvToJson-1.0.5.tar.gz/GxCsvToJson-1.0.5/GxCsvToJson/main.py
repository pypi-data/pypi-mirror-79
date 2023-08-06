# -*- coding: utf-8 -*-

import os
import sys
import codecs
import json
from getopt import getopt

class CsvToJson(object):
    def __init__(self):
        self.msg_index = {}
        self.have_index = 0

    def get_msg_index(self, line):
        '''
        Exp:
        msg : Bit,Name,HEVC,H264,JPEG,Function,Default value,Signed,Width,Read/Write,Valid range,trace
        index: 0 ,  1 , 2  ,  3 ,  4 , 5      ,    6        ,   7  ,  8  ,  9       ,  10       ,  11
        '''
        line = line.strip('\n')
        msg = line.split(',')
        for i in range(len(msg)): 
            if msg[i].strip(' ') == 'Bit':
                self.msg_index['bit'] = i
            if msg[i].strip(' ') == 'Name':
                self.msg_index['name'] = i
            if msg[i].strip(' ') == 'Function':
                self.msg_index['des'] = i
            if msg[i].strip(' ') == 'Default value':
                self.msg_index['reset'] = i
            if msg[i].strip(' ') == 'Read/Write':
                self.msg_index['access'] = i
        if len(self.msg_index) > 0:
            self.have_index = 1

    def read_reg_csv(self, in_file, base_addr):
        js_dict = {}
        js_dict["module name"] = 'test'
        js_dict["memory_maps"] = [{
            "name":"cpu cfg bus",
            "register_blocks":[{
                "name":"test_block",
                "base_addr":base_addr,
                "registers":''
                }]
            }]
        js_regs = []
        reg = ''
        fields = ''
        fi = open(in_file, 'r')
        new_reg = 0
        while 1:
            line = fi.readline()
            if not line:
                break
            #print(line, end = '')
            line = line.strip('\n')
            if line.startswith(',,,,,'):
                reg_line = fi.readline()
                head_line = fi.readline()
                if not self.have_index:
                    self.get_msg_index(head_line)
                msg = reg_line.split(',')
                reg = {
                        "RegName": msg[self.msg_index['bit']],
                        "Description": msg[self.msg_index['des']],
                        "Step":"0x0004",
                        "Fields":[]
                        }
                fields  = reg['Fields']
                js_regs.append(reg)
                continue
            #if line == 'Bit,Name,HEVC,H264,JPEG,Function,Default value,Signed,Width,Read/Write,Valid range,trace':
            #    continue
            msg = line.split(',')
            fields.append({
                "name":msg[self.msg_index['name']],
                "range":msg[self.msg_index['bit']],
                "access":msg[self.msg_index['access']],
                "description":msg[self.msg_index['des']],
                "reset_value":msg[self.msg_index['reset']]
                })
            if fields[-1]['reset_value'].upper() == 'X':
                print(fields[-1]['reset_value'])
                fields[-1]['reset_value'] = '0'
                print(fields[-1]['reset_value'])

        fi.close()
        js_dict["memory_maps"][0]["register_blocks"][0]["registers"] = js_regs
        return js_dict

def usage():
    '''
    Usage:
        csvtojson -f csv_file (-n json_name)

    parameters:
        -f : 指定csv文件
        -n : 指定生成的json的名字, 不加-n, 名字默认为csv文件名替换后缀为json
    '''
    print(usage.__doc__)


def main():
    opts, args = getopt(sys.argv[1:], "f:n:b:h")
    csv_file = ''
    out_file = ''
    base_addr = '0x1000'
    #print(opts)
    for k,v in opts:
        if k == '-f':
            csv_file = v
        if k == '-n':
            out_file = v
        if k == '-b':
            base_addr = v

    if csv_file == '':
        usage()
        sys.exit()
    if out_file == '':
        out_file = csv_file.split('.csv')[0] + '.json'

    cj = CsvToJson()
    js_dict = cj.read_reg_csv(csv_file, base_addr)
    json_str = json.dumps(js_dict, indent = 2, ensure_ascii=False)
    of = codecs.open(out_file,"w",'utf-8')
    of.write(json_str)
    of.close()
    print('\n\tcreate ' + out_file + ' success')

if __name__ == "__main__":
    main()
