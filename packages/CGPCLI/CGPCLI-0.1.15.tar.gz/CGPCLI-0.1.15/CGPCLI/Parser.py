# -*- coding: utf-8 -*-

import re
from datetime import datetime

from CGPCLI.Errors import NotValidCGPStringError

lbr_check_regex = re.compile(r'.*\"[^,)(]*(\(+)[^)(]*\".*', re.DOTALL)
rbr_check_regex = re.compile(r'.*\"[^)(]*(\)+)[^,)(]*\".*', re.DOTALL)

def parse_to_CGP_object(python_object):
    result = ''
    
    if isinstance(python_object,int):
        result += '"#' + str(python_object) + '"'
    
    elif isinstance(python_object,str):
        result += '"' + python_object + '"'
    
    elif isinstance(python_object,datetime):
        result += datetime.strftime(python_object, '#T%d-%m-%Y_%H:%M:%S')
        
    elif isinstance(python_object,dict):
        result += '{' + ''.join(f'"{str(x)}" = {parse_to_CGP_object(y)};' for x, y in zip(list(python_object.keys()), list(python_object.values()))) + '}'
            
    elif isinstance(python_object,list):
        result += '(' + ''.join(parse_to_CGP_object(x) + ', ' for x in python_object)[:-2] + ')'
        
    return result

def parse_to_python_object(string, from_CLI=True):
    def preparse_from_CLI(string):
        return string.replace('\n', '')
    
    def parse_array(string):
        def quotes_check(el, pos, values):
            while el.count('"')%2 != 0:
                pos = values.find(',', pos+1)
                if pos == -1:
                    el = values[:]
                    values = ''
                else:
                    el = values[:pos]
            
            return el, pos, values
                    
        def brackets_check(el, pos, values):
            lb_counter = el.count('(')
            rb_counter = el.count(')')
            
            while lb_counter != rb_counter:
                lb_counter = el.count('(')
                rb_counter = el.count(')')
                
                lbr = lbr_check_regex.match(el)
                rbr = rbr_check_regex.match(el)
                if lbr:
                    lb_counter -= len(lbr.groups()[0])
                if rbr:
                    rb_counter -= len(rbr.groups()[0])                    
                if lb_counter == rb_counter:
                    break

                pos = values.find(')', pos+1)
                if pos == -1:
                    el = el[:]
                else:
                    el = values[:pos + 1]
                    
            return el, pos, values
                    
        result_arr = list()
        values = string[1:-1]
        
        pos = values.find(',')
        
        while pos != -1:            
            el = values[:pos]  
           
            el, pos, values = brackets_check(el, pos, values)
            el, pos, values = quotes_check(el, pos, values)
            el, pos, values = brackets_check(el, pos, values)
                
            result_arr.append(parse_to_python_object(el.strip()))
            
            values = values[pos+1:]
            if values.startswith(','):
                values = values[1:]
            pos = values.find(',')

        values = values.strip()
        
        if values != '':
            result_arr.append(parse_to_python_object(values))

        return result_arr
    
    def parse_dict(string):
        result_dict = dict()
        values = string[1:-1]
        
        pos = values.find(';')
        el = values
        
        while pos != -1:
            el = values[:pos]
            while el.count('"')%2 != 0:
                el = values[:values.find(',', pos+1)]
                pos = values.find(',', pos+1)
                
            while el.count('{') != el.count('}'):
                pos = values.find('};', pos+1) + 1
                el = values[:pos]            
                
            k = el[:el.find('=')]
            v = el[el.find('=')+1:]
    
            result_dict.update({k.strip().replace('"',''): parse_to_python_object(v.strip())})
            
            values = values[pos+1:]
            pos = values.find(';')
    
        return result_dict
        
    string.strip()
    
    if from_CLI:
        string = preparse_from_CLI(string)
        
    #if dict
    if string[0] == '{':
        return parse_dict(string)
    #if arr
    elif string[0] == '(':
        return parse_array(string)
    else:
        if string[0] == '"' and string[-1] == '"':
            string = string[1:-1]
            
        if string.startswith('#T'):
            string = datetime.strptime(string, '#T%d-%m-%Y_%H:%M:%S')
            
        if string == 'true':
            string = True
        
        if string == 'false':
            string = False
            
        return string
    
print(parse_to_python_object('(\n  (\n    1,\n    "#Redirect",\n    (("Human Generated", "---")),\n    (("Mirror to", schreiber.alisa@gmail.com))\n  )\n)'))