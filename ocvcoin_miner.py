#!/usr/bin/env python3

import urllib.request
import urllib.error
import urllib.parse
import base64
import json
import hashlib

import random
import time
import os
import sys

import secrets


import ssl
import platform
import re
import traceback
import configparser
import math
from pycl import *
from pycl import _dll_filename
from array import array
from datetime import datetime
from threading import Thread , Timer

from test_framework.segwit_addr import (
    decode_segwit_address
)
from test_framework.blocktools import (
    create_block,
    NORMAL_GBT_REQUEST_PARAMS,
    script_BIP34_coinbase_height,
    add_witness_commitment
)
from test_framework.messages import (
    CBlock,
    CBlockHeader,
    BLOCK_HEADER_SIZE,
)
from test_framework.messages import (
    CBlock,
    COIN,
    COutPoint,
    CTransaction,
    CTxIn,
    CTxOut
)



















CURRENT_MINER_VERSION = "1.0.1.5"

## OUR PUBLIC RPC
OCVCOIN_PUBLIC_RPC_URL = "https://rpc.ocvcoin.com/OpenRPC.php"

RPC_SERVERS = []



## PRIMARY RPC SERVER
RPC_URL = OCVCOIN_PUBLIC_RPC_URL
RPC_USER = "" 
RPC_PASS = "" 


RPC_SERVERS.append([RPC_URL,RPC_USER,RPC_PASS])



rpc_config = r"""###<GENERATED BY OCVCOIN MINER>###
###DO NOT EDIT THIS BLOCK###
###SHOULD BE AT THE BEGINNING OF THE FILE###
[main]
rpcuser=ocvcoinrpc
rpcpassword="""+secrets.token_urlsafe(32)+"""
rpcallowip=0.0.0.0/0
rpcbind=0.0.0.0
rpcport=8332
server=1
###</GENERATED BY OCVCOIN MINER>###"""


rpc_check_regexp = r"""^\s*###<GENERATED BY OCVCOIN MINER>###\s*\n\s*###DO NOT EDIT THIS BLOCK###\s*\n\s*###SHOULD BE AT THE BEGINNING OF THE FILE###\s*\n\s*\[main\]\s*\n\s*rpcuser=ocvcoinrpc\s*\n\s*rpcpassword=(\S+)\s*\n\s*rpcallowip=0\.0\.0\.0/0\s*\n\s*rpcbind=0\.0\.0\.0\s*\n\s*rpcport=8332\s*\n\s*server=1\s*\n\s*###</GENERATED BY OCVCOIN MINER>###\s+"""

ocvcoin_core_restart_warning = """

Please restart Ocvcoin Core!

"""

MAX_HASHRATE = 0
WORK_ID = 0
LATEST_TARGET_HEIGHT = 0



_clbcc = 0
def check_latest_block():    
    
    global _clbcc,LATEST_TARGET_HEIGHT,LATEST_BLOCK_TEMPLATE,WORK_ID  

    if _clbcc % 100 == 0:
        LATEST_BLOCK_TEMPLATE = rpc_getblocktemplate()
        LATEST_TARGET_HEIGHT = int(LATEST_BLOCK_TEMPLATE["height"])-1
        WORK_ID = WORK_ID + 1
    else:    
        tmp_theight = rpc_getblockcount()
        
        if tmp_theight != LATEST_TARGET_HEIGHT:
            LATEST_TARGET_HEIGHT = tmp_theight
            LATEST_BLOCK_TEMPLATE = rpc_getblocktemplate()
            LATEST_TARGET_HEIGHT = int(LATEST_BLOCK_TEMPLATE["height"])-1
            WORK_ID = WORK_ID + 1

    
    _clbcc = _clbcc + 1
    Timer(0.35, check_latest_block).start()


  
  
try:
    
    request = urllib.request.Request("https://rpc.ocvcoin.com/",headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko)'})
    sslfix_context = ssl._create_unverified_context()        
    f = urllib.request.urlopen(request,context=sslfix_context,timeout=5)
    EXTRA_SEED = f.read()+bytes(str(f.info()),"utf-8")+bytes(str(time.time()),"ascii")
except Exception as e:
    try:
        EXTRA_SEED = bytes(str(time.time()),"ascii") + bytes(str(e.headers),"utf-8")
    except Exception as e:
        EXTRA_SEED = bytes(str(time.time()),"ascii")
    






def check_addr(addr):
    
    version,addrbytes = decode_segwit_address("ocv", addr)
    
    if version != 0 and version != 1:
        return False
    if len(addrbytes) != 20 and len(addrbytes) != 32:
        return False
        
    return True
        







    
def create_coinbase_via_bech32_addr(height, bech32_addr, coinbasevalue, extra_output_script=None):
    #accepts bech32 & bech32m addresses
    
    sig = SELECTED_DEVICE_NAME + " " + str(MAX_HASHRATE) + "h/s" + " " + "v" + CURRENT_MINER_VERSION
       
    
    coinbase = CTransaction()
    coinbase.vin.append(CTxIn(COutPoint(0, 0xffffffff), bytes(script_BIP34_coinbase_height(height))+hashlib.sha256(secrets.token_bytes(256)+EXTRA_SEED).digest()[:16]+bytes(sig, 'utf-8')[:76], 0xffffffff))
    coinbaseoutput = CTxOut()

    coinbaseoutput.nValue = coinbasevalue
    
    address_decoded = decode_segwit_address("ocv", bech32_addr)

    if address_decoded[0] == 0:
        req_opcode = bytes(b'\x00')
    elif address_decoded[0] == 1:
        req_opcode = bytes(b'\x51')
    else:
        exit("address not supported!")
    
    
    coinbaseoutput.scriptPubKey = req_opcode + int2lehex(len(address_decoded[1]), 1) + bytes(address_decoded[1])
    
    coinbase.vout = [coinbaseoutput]
    if extra_output_script is not None:
        coinbaseoutput2 = CTxOut()
        coinbaseoutput2.nValue = 0
        coinbaseoutput2.scriptPubKey = extra_output_script
        coinbase.vout.append(coinbaseoutput2)
    coinbase.calc_sha256()
    return coinbase
def screen_clear():
   # for mac and linux(here, os.name is 'posix')
   if os.name == 'posix':
      _ = os.system('clear')
   else:
      # for windows platfrom
      _ = os.system('cls')

_print_norepeat_latest_input = ""
def print_norepeat(i):
    global _print_norepeat_latest_input
    if i != _print_norepeat_latest_input:
        _print_norepeat_latest_input = i
        print(i)





def rpc(method, params=None,rpc_index=0):
    """
    Make an RPC call to the Bitcoin Daemon JSON-HTTP server.

    Arguments:
        method (string): RPC method
        params: RPC arguments

    Returns:
        object: RPC response result.
    """

    rpc_id = random.getrandbits(32)
    data = json.dumps({"id": rpc_id, "method": method, "params": params}).encode()   

       
    
    if RPC_SERVERS[rpc_index][0] == OCVCOIN_PUBLIC_RPC_URL:
        if method == "getblocktemplate" or method == "getblockcount":
            request = urllib.request.Request(RPC_SERVERS[rpc_index][0]+"?method="+method)
        else:
            request = urllib.request.Request(RPC_SERVERS[rpc_index][0]+"?method="+method, data)
    else:
        auth = base64.encodebytes((RPC_SERVERS[rpc_index][1] + ":" + RPC_SERVERS[rpc_index][2]).encode()).decode().strip()
        request = urllib.request.Request(RPC_SERVERS[rpc_index][0], data, {"Authorization": "Basic {:s}".format(auth)})

    
    err_detected = False
    try:        
                
        sslfix_context = ssl._create_unverified_context()            
        f = urllib.request.urlopen(request,context=sslfix_context,timeout=5)
        response = json.loads(f.read())
        
    except Exception as e:
    
        #print("An exception occurred (RPC)") 
        #print(e)
        err_detected = True
        
    if not err_detected:
    
        if not 'id' in response:
            #print("id missing")
            #print(response)
            err_detected = True
            
        elif (RPC_SERVERS[rpc_index][0] != OCVCOIN_PUBLIC_RPC_URL or method == "submitblock") and response['id'] != rpc_id:
            #print("Invalid response id: got {}, expected {:u}".format(response['id'], rpc_id))
            #print(response)
            err_detected = True

        elif 'error' in response and response['error'] is not None:
            #print("RPC error: {:s}".format(json.dumps(response['error'])))
            err_detected = True
        
        elif not 'result' in response:
            #print("result missing")
            #print(response)
            err_detected = True





        
        
    if err_detected == True:
        if rpc_index == 0:
            if len(RPC_SERVERS) > 1:
                print_norepeat("Public RPC server sometimes not responding! Switching to backup RPC server!")
            else:
                print_norepeat("Public RPC server sometimes not responding! It is recommended to install Ocvcoin Core on your computer!")
        else:
            print_norepeat("The backup RPC server is also not responding! Please restart Ocvcoin Core!")
            
            
        return False
        



    return response['result']


def rpc_getblockcount():
    
    
    divider = len(RPC_SERVERS)
    i = divider
    while True:
        rpcindex = i % divider
        if i > divider:
            time.sleep(0.35)
            #print("getblockcount" +str(i-divider)+ "th retry...")
            
        ret = rpc("getblockcount",rpc_index=rpcindex)        
            
        if ret != False:
            ret = int(ret)
            if ret >= LATEST_TARGET_HEIGHT:
                break
            else:    
                #print("getblockcount low! rpc_index: "+str(rpcindex))
                #print("ret >= LATEST_TARGET_HEIGHT")
                #print(str(ret)+"    "+str(LATEST_TARGET_HEIGHT))
                pass
        else:
            #print("getblockcount false! rpc_index: "+str(rpcindex))
            pass
        i = i + 1
    
    return ret

def rpc_getblocktemplate():
    
    
    divider = len(RPC_SERVERS)
    i = divider
    while True:
        rpcindex = i % divider
        if i > divider:
            time.sleep(0.35)
            #print("getblocktemplate" +str(i-divider)+ "th retry...")

        ret = rpc("getblocktemplate", [NORMAL_GBT_REQUEST_PARAMS],rpcindex)        
            
        if ret != False and "height" in ret:
            gbt_height = int(ret["height"])
            if gbt_height > LATEST_TARGET_HEIGHT:
                break
            else:    
                #print("getblocktemplate height low! rpc_index: "+str(rpcindex))
                #print("gbt_height > LATEST_TARGET_HEIGHT")
                #print(str(gbt_height)+"    "+str(LATEST_TARGET_HEIGHT))
                pass
        else:
            #print("getblocktemplate false! rpc_index: "+str(rpcindex))
            #print(ret)
            pass
        i = i + 1
    
    return ret

def rpc_submitblock(block_submission):
    
    
    divider = len(RPC_SERVERS)
    i = divider
    
    

    soft_errors = {}
    network_errors = {}
    
    while True:
        rpcindex = i % divider
        ret = rpc("submitblock", [block_submission],rpcindex)
        
        if ret is None:
            return
        elif ret == False:
            if rpcindex in network_errors[rpcindex]:
                network_errors[rpcindex] = network_errors[rpcindex] + 1
            else:
                network_errors[rpcindex] = 1
        else:        
            if rpcindex in soft_errors[rpcindex]:
                soft_errors[rpcindex] = soft_errors[rpcindex] + 1
            else:
                soft_errors[rpcindex] = 1        
        if len(soft_errors) == divider:
            raise TypeError("rpc_submitblock soft_errors") 
        
        if len(network_errors) == divider:
            is_max_err_count_reached = True
            for x in network_errors:
                is_max_err_count_reached = is_max_err_count_reached and (network_errors[x] > 4)
            if is_max_err_count_reached:
                raise TypeError("rpc_submitblock network_errors")
        
        for x in soft_errors:
            if soft_errors[x] > 8:
                raise TypeError("rpc_submitblock soft_error")

        for x in network_errors:
            if network_errors[x] > 8:
                raise TypeError("rpc_submitblock network_error")
                
        time.sleep(1)
        


        
        i = i + 1
    
    
    
    
def int2lehex(value, width):
    """
    Convert an unsigned integer to a little endian ASCII hex string.
    Args:
        value (int): value
        width (int): byte width
    Returns:
        string: ASCII hex string
    """

    return value.to_bytes(width, byteorder='little')


_loop_start_val = 1 
def ocl_mine_ocvcoin(address):       
    
    global PYCL_QUEUE,PYCL_KERNEL,PYCL_CTX,MAX_HASHRATE,WORK_ID,LATEST_BLOCK_TEMPLATE,_loop_start_val
    
    
    current_work_id = WORK_ID  
    
    block_template = LATEST_BLOCK_TEMPLATE
    
    print("Starting to mine block "+str(block_template["height"]))
    
    
    txlist = []

    for tx in block_template["transactions"]:
        txlist.append(tx["data"])

    
    
  

    coinbase = create_coinbase_via_bech32_addr(block_template["height"], address, block_template["coinbasevalue"])

    block = create_block( coinbase=coinbase,  tmpl=block_template, txlist=txlist)
    
    
    if len(txlist) > 0:
        add_witness_commitment(block)

    new_block = block.serialize()
    
    block_header = new_block[0:80]  
    

    start_hash = block_header[0:76]
    
    final_init_img = bytearray()

    i = 0
    while i < 27:
        start_hash = hashlib.sha512(start_hash).digest()
        final_init_img = final_init_img + start_hash
        i += 1

    # Create buffers
    
    target_dif_bin_arr = array('B', bytes.fromhex(block_template['target']))
    
    target_diff_buf, _ = buffer_from_pyarray(PYCL_QUEUE, target_dif_bin_arr, blocking=True)
    init_img_buf, _ = buffer_from_pyarray(PYCL_QUEUE, array('B', final_init_img), blocking=True)
    block_header_buf, _ = buffer_from_pyarray(PYCL_QUEUE, array('B', block_header), blocking=True)
    output_buf = target_diff_buf.empty_like_this()

    
    
    
      

    local_work_items = int(CONFIG[SELECTED_DEVICE_NAME]["number_of_local_work_items"])
    
    if local_work_items % 32 != 0:
        local_work_items = int(local_work_items / 32) * 32    
    if local_work_items == 0:
        local_work_items = 32
    
    global_work_size = int(CONFIG[SELECTED_DEVICE_NAME]["number_of_global_work_items"]) 
    if global_work_size % 256 != 0:
        global_work_size = (int(global_work_size / 256) + 1) * 256
    
    MAX_HASHRATE = 0
    
    
    
    if CONFIG[SELECTED_DEVICE_NAME]["loop_count"] != "auto":
        loop_count = int(CONFIG[SELECTED_DEVICE_NAME]["loop_count"])
        if loop_count < 0:
            loop_count = 1
        elif loop_count > 256:
            loop_count = 256
        print("loop_count auto optimization mode disabled!")
        
        
    else:
        print("loop_count auto optimization mode active!")
        loop_count = _loop_start_val
    
    
    
    
    current_step = 0
    
    already_show1 = False
    already_show2 = False
    
    start_time = time.time()
    total_hashed = 0
    
    
    while True:
    
        
        
        calc_per_time = loop_count*global_work_size

        last_time_stamp = time.time()
        
        total_hashed = total_hashed + calc_per_time                            
        
        run_evt = PYCL_KERNEL(current_step, loop_count, target_diff_buf, init_img_buf, block_header_buf, output_buf).on(PYCL_QUEUE, global_work_size,lsize=local_work_items)

        output_bin, evt = buffer_to_pyarray(PYCL_QUEUE, output_buf, wait_for=run_evt, like=target_dif_bin_arr) 

      
        

        # Wait for all events to complete
        evt.wait()
        
        nonce_bytes = output_bin.tobytes()



        if nonce_bytes[0] > 0 or nonce_bytes[1] > 0 or nonce_bytes[2] > 0 or nonce_bytes[3] > 0:

            
            block_header = block_header[0:76] + nonce_bytes[0:4]



            submission = (block_header+new_block[80:]).hex()
            print("Found! Submitting: {}\n".format(submission))  
  
            
            rpc_submitblock(submission)
            
            clReleaseMemObject(target_diff_buf)
            clReleaseMemObject(init_img_buf)
            clReleaseMemObject(block_header_buf)
            clReleaseMemObject(output_buf)
            
            return


        current_timestamp = time.time()
        diff = current_timestamp - last_time_stamp
        
        hash_rate = int(calc_per_time / diff)
        
        
        
        
        
        total_diff = current_timestamp - start_time            
        total_hash_rate = int(total_hashed / total_diff)            
        
        if MAX_HASHRATE < hash_rate:
            MAX_HASHRATE = hash_rate
            
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")            
            
        print("[{}] Current: {} hash/s, Total: {} hash/s, Max: {} hash/s (loop_count:{})".format(dt_string,hash_rate,total_hash_rate,MAX_HASHRATE,loop_count))
        
         
        
        if current_step > 1 and (diff > 3  or diff < 1): 
            

            recommended_val = math.ceil((2 * loop_count) / diff)
            if recommended_val > 256:
                recommended_val = 256
            
            if already_show1 == False:
                already_show1 = True                
                print("Warning!")
                print("Miner is checking new blocks every "+str(diff)+" seconds!")                
                print("Recomended check interval is 2 second!")                
            
            if CONFIG[SELECTED_DEVICE_NAME]["loop_count"] != "auto": 
                if loop_count != recommended_val:
                    print("You can fix this issue!")
                    print("You can set loop_count {} to {} in the ini file!".format(CONFIG[SELECTED_DEVICE_NAME]["loop_count"],recommended_val))
                
                
            else:
                if loop_count != recommended_val:
                    print("Fixing check interval... Setting loop_count {} to {} ...".format(loop_count,recommended_val))
                loop_count = recommended_val
                _loop_start_val = math.ceil(recommended_val / 1.2)
                if already_show2 == False:
                    already_show2 = True
                    print("If this setting is dropping your hashrate, you can turn off this automatic optimization in the ini file!")           
                
                
                
        
        
        
        if WORK_ID != current_work_id:
            print("new work detected!")
            clReleaseMemObject(target_diff_buf)
            clReleaseMemObject(init_img_buf)
            clReleaseMemObject(block_header_buf)
            clReleaseMemObject(output_buf)        
            return
        current_step = current_step + 1
        
        if (current_step*global_work_size + global_work_size) > 0xFFFFFF:
            print("no more nonce!")
            clReleaseMemObject(target_diff_buf)
            clReleaseMemObject(init_img_buf)
            clReleaseMemObject(block_header_buf)
            clReleaseMemObject(output_buf)            
            return

            
            
            
    
            
def build_kernel():
    
    global PYCL_CTX,SELECTED_DEVICE,PYCL_QUEUE,PYCL_PROGRAM,PYCL_KERNEL

    try:
        cl_file = os.sep.join([os.path.dirname(os.path.abspath(__file__)),"ocv2_miner.cl"])
        print("Building source...")
        with open(cl_file, 'rb') as file:
            ocv2_miner_cl_source = file.read()

        bopts = bytes(CONFIG[SELECTED_DEVICE_NAME]["build_flags"], 'ascii')

        PYCL_CTX = clCreateContext(devices=[SELECTED_DEVICE])
        PYCL_QUEUE = clCreateCommandQueue(PYCL_CTX)
        PYCL_PROGRAM = clCreateProgramWithSource(PYCL_CTX, ocv2_miner_cl_source).build(bopts)
        PYCL_KERNEL = PYCL_PROGRAM['search_hash']
        PYCL_KERNEL.argtypes = (cl_uint,cl_uint,cl_mem,cl_mem,cl_mem,cl_mem)
        print("Build complate!")

    except Exception as e:
        print("Build fail!")
        print(repr(e))
        exit()

def standalone_miner(address):
    
    global PYCL_CTX,SELECTED_DEVICE,PYCL_QUEUE,PYCL_PROGRAM,PYCL_KERNEL

    build_kernel()
    check_latest_block()
    

    while True:
        try:     
            
            ocl_mine_ocvcoin(address)                         
            
        except Exception as e:
            print("Exception in standalone_miner loop:")
            print(repr(e)) 
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type) 
            print(fname) 
            print(exc_tb.tb_lineno)
            
            
            try:
                clReleaseKernel(PYCL_KERNEL)
            except Exception as e:
                pass
            try:
                clReleaseKernel(PYCL_PROGRAM)
            except Exception as e:
                pass                
            try:
                clReleaseKernel(PYCL_QUEUE)
            except Exception as e:
                pass                
            try:
                clReleaseKernel(PYCL_CTX)
            except Exception as e:
                pass                
                
                
                
                
                
            build_kernel()
            
            
            
            
            time.sleep(1)


if __name__ == "__main__":

    screen_clear()
    
    try:           
        request = urllib.request.Request("https://raw.githubusercontent.com/ocvcoin/gpuminer/main/version.txt")
        sslfix_context = ssl._create_unverified_context()        
        f = urllib.request.urlopen(request,context=sslfix_context,timeout=5)
        resp = f.read()
        if resp.decode('ascii').strip() != CURRENT_MINER_VERSION:
            print("New version is available.")
            print("To update, visit: ocvcoin.com\n")
    except:
        print("\nNew version check failed. Skipping...\n")



    print("Ocvcoin Gpu Miner v"+str(CURRENT_MINER_VERSION)+" starting...")
    print(platform.uname())




    if os.name == 'nt':   
        config_location_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')         
    elif os.name == 'posix':    
        config_location_path = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop') 

        if not os.path.exists(config_location_path) or not os.path.isdir(config_location_path):
            config_location_path = os.path.join(os.path.expanduser('~'))


    config_file = os.sep.join([config_location_path,"Ocvcoin_Gpu_Miner.ini"])


    CONFIG = configparser.ConfigParser()


    CONFIG.read(config_file) 
    
    print("Using %s" % _dll_filename)

    try:
        

        BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

        md5 = hashlib.md5()
        sha1 = hashlib.sha1()
        sha256 = hashlib.sha256()

        with open(_dll_filename, 'rb') as f:
            while True:
                data = f.read(BUF_SIZE)
                if not data:
                    break
                md5.update(data)
                sha1.update(data)    
                sha256.update(data)
        
        print("MD5: {0}".format(md5.hexdigest()))
        print("SHA1: {0}".format(sha1.hexdigest()))    
        print("SHA256: {0}".format(sha256.hexdigest()))

        
    except Exception as e:
        pass

    
    
    print("Python: "+sys.version)

    


    i = 1

    try:
        platforms = clGetPlatformIDs()
    except Exception as e: 

        print(repr(e))
        print("Make sure the GPU drivers are installed!")
        print("This could be the cause of this error")
        
        exit()

    if len(platforms) < 1:
        print("No devices supporting OpenCL were found!")
        exit()


    print("Device Selection")
    print("Please enter a device number")    
    
    
    device_list = []
    device_names = []
    
    for p in platforms:
        try:
            for d in clGetDeviceIDs(p):
                
                device_list.append(d)
                

                try:
                    max_compute_units = str(clGetDeviceInfo(d, cl_device_info.CL_DEVICE_MAX_COMPUTE_UNITS))
                except Exception as e:             
                    max_compute_units = str(type(e).__name__)

                try:
                    max_clock_freq = str(clGetDeviceInfo(d, cl_device_info.CL_DEVICE_MAX_CLOCK_FREQUENCY))
                except Exception as e:             
                    max_clock_freq = str(type(e).__name__)



                device_name = str(i)+" - "+ str(d.name) + " " + str(d.profile) + " " + max_compute_units + " " + max_clock_freq
                
                device_names.append(device_name)
                
                print(device_name)

                if device_name not in CONFIG:



                    CONFIG[device_name] = {}
                    CONFIG[device_name]["build_flags"] = "-cl-fast-relaxed-math -cl-mad-enable -cl-no-signed-zeros"
                    
                    
                    
                    number_of_global_work_items = ((int(max_compute_units)*5120*2) / 40)
                    if number_of_global_work_items % 256 != 0:
                        number_of_global_work_items = (int(number_of_global_work_items / 256) + 1) * 256
                    
                    
                    CONFIG[device_name]["number_of_global_work_items"] = str(int(number_of_global_work_items))
                    CONFIG[device_name]["number_of_local_work_items"] = "256"
                    
                    CONFIG[device_name]["loop_count"] = "auto"
                    
                    CONFIG[device_name]["reward_addr"] = ""
                
                
                i = i + 1
        except Exception as e:
            pass

    if len(device_list) < 1:
        print("no found any device")
        exit()

    
    selected_device_number = input().strip()
            
    if selected_device_number.isnumeric() == False or int(selected_device_number) < 1 or int(selected_device_number) > len(device_list):
        print("Invalid device number!")
        exit()        
                

    SELECTED_DEVICE = device_list[int(selected_device_number)-1]
    SELECTED_DEVICE_NAME = device_names[int(selected_device_number)-1]   


    



    if check_addr(CONFIG[SELECTED_DEVICE_NAME]["reward_addr"]):
        addr = CONFIG[SELECTED_DEVICE_NAME]["reward_addr"]
        print("Reward Address: "+addr)
    else: 
                      
        print("\nYou can try wallet.ocvcoin.com to create a wallet and get an address.")
        addr = input("\nEnter your ocvcoin address:\n(you can right click & paste it)\n ")
        addr = addr.strip()


        if check_addr(addr) != True:
            print("Wrong address. Address must be of bech32 type.")
            print("(It should start with ocv1)")
            exit()

        CONFIG[SELECTED_DEVICE_NAME]["reward_addr"] = addr


    try:

        with open(config_file, 'w') as configfile_descp:
          CONFIG.write(configfile_descp)

    except Exception as e:
        print("Warning!")
        print("Failed to save settings to "+str(config_file))
        print(repr(e))



  
    for k in CONFIG[SELECTED_DEVICE_NAME]:
        print(k + " = " + CONFIG[SELECTED_DEVICE_NAME][k])
    
    


    try:

        ocvcoin_folder = False
        ocvcoin_configdata = False
        if os.name == 'nt':    
            ocvcoin_folder = os.sep.join([os.getenv('APPDATA'),"Ocvcoin"])      
        elif os.name == 'posix':
            ocvcoin_folder = os.path.expanduser(os.sep.join(["~",".ocvcoin"]))

        if ocvcoin_folder != False and os.path.isdir(ocvcoin_folder):
            
            ocvcoin_configfile = os.sep.join([ocvcoin_folder,"ocvcoin.conf"])
            if os.path.isfile(ocvcoin_configfile):
                f = open(ocvcoin_configfile, "r")
                ocvcoin_configdata = f.read()
                f.close()
                
                check_rpc_config = re.search(rpc_check_regexp,ocvcoin_configdata)
                if not check_rpc_config:
                    f = open(ocvcoin_configfile, "w")
                    ocvcoin_configdata = rpc_config+"\r\n\r\n\r\n\r\n"+ocvcoin_configdata
                    f.write(ocvcoin_configdata)
                    f.close()
                    print(ocvcoin_core_restart_warning)
                    
                
            elif not os.path.exists(ocvcoin_configfile):
                f = open(ocvcoin_configfile, "w")
                ocvcoin_configdata = rpc_config+"\r\n\r\n\r\n\r\n"
                f.write(ocvcoin_configdata)
                f.close()
                print(ocvcoin_core_restart_warning)
                

        if ocvcoin_configdata != False:
            check_rpc_config = re.search(rpc_check_regexp,ocvcoin_configdata)
            if check_rpc_config:
                print("We have detected that you have Ocvcoin Core installed on your system.")
                print("While mining, it is recommended to keep Ocvcoin Core running!")
                RPC_SERVERS.append(["http://127.0.0.1:8332","ocvcoinrpc",check_rpc_config.group(1)])

    except Exception as e:
        print("Ocvcoin Core Configurator Failed")
        print(repr(e))








    




        
    standalone_miner(addr)
