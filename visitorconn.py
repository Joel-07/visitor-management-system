import socket
from threading import Thread
import mysql.connector as mc
import time

def receiver(conn,addr):
    t=time.time()
    while True:
        try:
            a=conn.recv(1024)
            data=a.decode().rstrip('@')
            if data:
                print('recieving data from',addr)
            else:
                print("disconnected device",addr)
            d=data.split(",")
            myc.execute("select gid,in_time,out_time from info where meetingid=%s"%d[-1])
            res=myc.fetchone()
            if res[0]==d[2] and res[1]==None:
                myc.execute("update info set in_time=%s where meetingid=%s"%(int(t),d[-1]))
                db.commit()
                conn.send(("Allow user %s"%d[1]).encode())
            elif res[0]==d[2] and res[2]==None :
                myc.execute("update info set out_time=%s where meetingid=%s"%(int(t),d[-1]))
                db.commit()
                conn.send(("Thank you for visiting %s"%d[1]).encode())
            else:   
                conn.send(("%s has already visited"%d[1]).encode())
        except:
                break

if __name__=="__main__":
    host="192.168.29.192"
    port=1234
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    db=mc.connect(host="localhost",user="root",passwd="12345678",database="vms")
    myc=db.cursor()

    s.bind((host,port))
    s.listen()

    while True:
        try:
            conn,addr=s.accept()
            th1=Thread(target=receiver,args=(conn,addr,))
            th1.start()

        except KeyboardInterrupt:
            conn.close()
            break
            
