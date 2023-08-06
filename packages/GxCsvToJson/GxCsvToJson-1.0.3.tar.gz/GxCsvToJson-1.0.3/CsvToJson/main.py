# -*- coding: utf-8 -*-

import os
import sys
import codecs
import json
from getopt import getopt

class CsvToJson(object):
    def __init__(self):
        pass

    def read_reg_csv(self, in_file, base_addr):
        '''
        msg : Bit,Name,HEVC,H264,JPEG,Function,Default value,Signed,Width,Read/Write,Valid range,trace
        index: 0 ,  1 , 2  ,  3 ,  4 , 5      ,    6        ,   7  ,  8  ,  9       ,  10       ,  11
        '''
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
            if line.startswith(',,,,,,,,,,,'):
                line = fi.readline()
                msg = line.split(',')
                reg = {
                        "RegName": msg[0],
                        "Description": msg[5],
                        "Step":"0x0004",
                        "Fields":[]
                        }
                fields  = reg['Fields']
                js_regs.append(reg)
                continue
            if line == 'Bit,Name,HEVC,H264,JPEG,Function,Default value,Signed,Width,Read/Write,Valid range,trace':
                continue
            msg = line.split(',')
            fields.append({
                "name":msg[1],
                "range":msg[0],
                "access":msg[9],
                "description":msg[5],
                "reset_value":msg[6]
                })
        fi.close()
        js_dict["memory_maps"][0]["register_blocks"][0]["registers"] = js_regs
        return js_dict

def usage():
    '''
    Usage:
        csvtojson -f csv_file (-n json_name) (-b base_addr)
        csvtojson -f reg.csv -n output.json -b 0x1200

    parameters:
        -f : 指定csv文件
        -n : 指定生成的json的名字, 不加-n, 名字默认为csv文件名替换后缀为json
        -b : 指定base_addr, 默认为0x1000
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
