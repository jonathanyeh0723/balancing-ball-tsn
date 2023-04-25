import threading
import time
import json

class Intel_Kalycito_Opcus_Log_Processor():
    pub_msg_queue = {} 
    latency_result_queue = []
    pub_msg_queue_locker = threading.Semaphore(1)
    latency_result_queue_locker = threading.Semaphore(1)

    def __init__(self,  in_max_pub_queue_len  , in_max_latency_queue_len ) :
        self.max_pub_queue_len = in_max_pub_queue_len
        self.max_latency_queue_len = in_max_latency_queue_len
        self.limit = 40

    def parse_inform(self, in_string) :
        is_sub = True
        index = 0
        try:
            index = in_string.index("Sub:")
        except ValueError:
            is_sub = False
            try : 
                index = in_string.index("Pub:")
            except ValueError:
                #print("Unknown Log Type")
                return
        in_string.replace("\r", "\n")
        try:
            comma_index = in_string.index(",", index)
            nl_index = in_string.index("\n", index)
            data_id = in_string[index+4:comma_index]
            data_value = in_string[comma_index+1:nl_index]
        except :
            return


        if is_sub == True :
            self.latency_result_queue_locker.acquire()
            try:
                if len(self.latency_result_queue) + 1 > self.max_latency_queue_len:
                    del self.latency_result_queue[0]
            #    self.pub_msg_queue_locker.acquire()
                latency_value = float(data_value) - float(self.pub_msg_queue[data_id])
                self.latency_result_queue.append(latency_value)
                #print(latency_value)
                #else :
                #    print("Buffer Overflow, Drop Value.")
                self.pub_msg_queue_locker.acquire()
                self.pub_msg_queue.popitem()
                self.pub_msg_queue_locker.release()
            except KeyError as e:
                #print(str(e))
                pass
            #self.pub_msg_queue_locker.release()
            self.latency_result_queue_locker.release()
        else :
            if self.limit > 0 :
                self.limit = self.limit -1
                return
            else :
                self.limit = 400
            self.pub_msg_queue_locker.acquire()
            if len(self.pub_msg_queue) + 1 > self.max_pub_queue_len:
                    self.pub_msg_queue.popitem()
            #print("data_id: ", data_id)
            self.pub_msg_queue[data_id] = data_value
            self.pub_msg_queue_locker.release()
    

    def pop_latency_values_list(self, in_max_num) :
        self.latency_result_queue_locker.acquire()
        if in_max_num >= len(self.latency_result_queue) :
            num_entry = len(self.latency_result_queue)
        else :
            num_entry = in_max_num
        latency_json_data = self.latency_result_queue[0:num_entry]
        if len(self.latency_result_queue) > 0 :
            del self.latency_result_queue[0]
        self.latency_result_queue_locker.release()
        return latency_json_data

    def get_avg_latency_values(self, in_max_num) :
        latency_val_avg = 0
        if in_max_num >= len(self.latency_result_queue) :
            num_entry = len(self.latency_result_queue)
        else :
            num_entry = in_max_num
        if num_entry > 0 :
            self.latency_result_queue_locker.release()
            latency_val_avg=sum(self.latency_result_queue[0:num_entry])/num_entry
            self.latency_result_queue_locker.release()
        return latency_val_avg
           
    def get_max_latency_values(self, in_max_num) :
        latency_val_avg = 0
        if in_max_num >= len(self.latency_result_queue) :
            num_entry = len(self.latency_result_queue)
        else :
            num_entry = in_max_num
        if num_entry > 0 :
            self.latency_result_queue_locker.release()
            latency_val_avg=max(self.latency_result_queue[0:num_entry])
            self.latency_result_queue_locker.release()
        return latency_val_avg

    def get_min_latency_values(self, in_max_num) :
        latency_val_avg = 0
        if in_max_num >= len(self.latency_result_queue) :
            num_entry = len(self.latency_result_queue)
        else :
            num_entry = in_max_num
        if num_entry > 0 :
            self.latency_result_queue_locker.release()
            latency_val_avg=min(self.latency_result_queue[0:num_entry])
            self.latency_result_queue_locker.release()
        return latency_val_avg

    def print_queue(self, type) :
        if type == "pub" :
            self.pub_msg_queue_locker.acquire()
            print("Pub : ", self.pub_msg_queue, "\n")
            self.pub_msg_queue_locker.release()
        else : 
            self.latency_result_queue_locker.acquire()
            print("Latency : ", self.latency_result_queue, "\n")
            self.latency_result_queue_locker.release()

    def print_queue_len(self, type) :
        if type == "pub" :
            self.pub_msg_queue_locker.acquire()
            print("Pub Len: ", len(self.pub_msg_queue), "\n")
            self.pub_msg_queue_locker.release()
        else : 
            self.latency_result_queue_locker.acquire()
            print("Latency Len: ", len(self.latency_result_queue), "\n")
            self.latency_result_queue_locker.release()

#Code for Uni-test
#p=Intel_Kalycito_Opcus_Log_Processor(9999)
#f = open("opc-ua_log_console.txt")
#line = f.readline()
#i = 0
#while line:
#    i = i +1
#    p.parse_inform(line)
    #p.print_queue("pub")
    #p.print_queue("sub")
    #p.print_queue("latency")
    #time.sleep( 0.5 )
#    line = f.readline()
#print(p.pop_latency_values(10))
#print("=>",p.get_avg_latency_values(10))
#print(p.pop_latency_values(10))
#print("=>",p.get_avg_latency_values(10))
#print(p.pop_latency_values(10))
#print(p.pop_latency_values(10))

#f.close()
