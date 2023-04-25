import subprocess
import threading
import time
import select
from Intel_Kalycito_Opcus_Log_Processor import Intel_Kalycito_Opcus_Log_Processor 

class Intel_Kalycito_Opcus_Runner(object):

    #start_opcus_pub = ['/home/root/open62541/pubsub_TSN_publisher', '-interface', 'br0', '-enableBlockingSocket', '-socketPriority', '7', '-enableconsolePrint']
    start_opcus_pub = ['/root/open62541/pubsub_TSN_publisher_multiple_thread', '-interface', '192.168.137.2', '-enableBlockingSocket', '-socketPriority', '7', '-enableconsolePrint', '-pubUri', 'opc.udp://192.168.137.1:4840', '-cycleTimeInMsec', '0.25'] 
#    start_opcus_pub = ['/home/root/open62541//pubsub_TSN_publisher_multiple_thread', '-interface', '192.55.75.12', '-enableBlockingSocket', '-socketPriority', '7', '-enableconsolePrint', '-pubUri', 'opc.udp://10.254.0.5:4840', '-cycleTimeInMsec', '50'] 
    opcua_pub_processor = None
    
    def __init__(self,  in_max_pub_queue_len  , in_max_latency_queue_len, in_interface_name = None ) :
        if in_interface_name !=  None:
            self.start_opcus_pub[2] = in_interface_name
        self.opcua_pub_processor=Intel_Kalycito_Opcus_Log_Processor( in_max_pub_queue_len , in_max_latency_queue_len)


    def run_test(self):
        self.thread=threading.Thread(target=self.opcua_pub_running_test_thread)
        self.thread.start() 
        
    def run(self):
        self.opcua_pub_process = subprocess.Popen(self.start_opcus_pub, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        time.sleep(2)
        self.poll_obj = select.poll()
        self.poll_obj.register(self.opcua_pub_process.stdout, select.POLLIN)
        self.thread=threading.Thread(target=self.opcua_pub_running_thread)
        self.thread.start() 

    def stop(self):
        if self.thread  != None :
           self.thread.do_run_thread = False
           self.thread.join()
           self.opcua_pub_process.kill()


    def opcua_pub_running_test_thread(self) :
        f = open("opc-ua_log_console.txt")
        line = f.readline()
        i = 0
        while line:
            i = i +1
            self.opcua_pub_processor.parse_inform(line)
            #p.print_queue("pub")
            #p.print_queue("sub")
            #p.print_queue("latency")
            time.sleep( 0.00025 )
            line = f.readline()
        f.close()

    def opcua_pub_running_thread(self) :
        while getattr(self.thread, "do_run_thread", True):
            try :
                if self.opcua_pub_process.poll() is None :
                    poll_result = self.poll_obj.poll(1500)
                    if poll_result:
                        opcua_pub_byte = self.opcua_pub_process.stdout.readline()
                        opcua_pub_byte_string =  opcua_pub_byte.decode()
                        self.opcua_pub_processor.parse_inform(opcua_pub_byte_string)
                        print("------=>[", opcua_pub_byte_string, "]")
                        #self.logger.print(False, "VERB", "[gPTP EVENT RAW DATA] ", daemon_cl_byte_string)
                    else : 
                       print("Nothing")
                       #self.logger.print(False, "ERROR", "[gPTP EVENT] gPTP error due to time sync stop")'
                       pass
                else :
                    self.opcua_pub_process = subprocess.Popen(self.start_opcus_pub, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            except Exception as e:
                print(str(e))
                return

#Code for Uni-test
#p=Intel_Kalycito_Opcus_Log_Processor(1024, 5000)
#p1=Intel_Kalycito_Opcus_Runner(1024, 5000)
#p1.run()
#while True:
#    print(p.pop_latency_values_list(60))
#    print("==>",p.get_avg_latency_values(60))
#    print("====>",p.print_queue_len("pub"))
#    print("====>",p.print_queue_len("sub"))
#    print("====>",p.print_queue_len("latency"))
#    time.sleep( 2 )

#f.close()
