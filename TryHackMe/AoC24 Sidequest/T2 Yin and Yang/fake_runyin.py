#!/usr/bin/python3                                                                                                                                                                                                                    
                                                                                                                                                                                                                                      
import rospy                                                                                                                                                                                                                          
import base64                                                                                                                                                                                                                         
import codecs                                                                                                                                                                                                                         
import os                                                                                                                                                                                                                             
from std_msgs.msg import String                                                                                                                                                                                                       
from yin.msg import Comms                                                                                                                                                                                                             
from yin.srv import yangrequest                                                                                                                                                                                                       
import hashlib                                                                                                                                                                                                                        
from Cryptodome.Signature import PKCS1_v1_5                                                                                                                                                                                           
from Cryptodome.PublicKey import RSA                                                                                                                                                                                                  
from Cryptodome.Hash import SHA256                                                                                                                                                                                                    
                                                                                                                                                                                                                                      
class Yin:                                                                                                                                                                                                                            
    def __init__(self):                                                                                                                                                                                                               
                                                                                                                                                                                                                                      
        self.messagebus = rospy.Publisher('messagebus', Comms, queue_size=50)                                                                                                                                                         
                                                                                                                                                                                                                                      
                                                                                                                                                                                                                                      
        #Read the message channel private key                                                                                                                                                                                         
        pwd = b'secret'                                                                                                                                                                                                               
        with open('private_key', 'rb') as f:                                                                                                                                                                            
            data = f.read()                                                                                                                                                                                                           
            self.priv_key = RSA.import_key(data,pwd)                                                                                                                                                                                  
                                                                                                                                                                                                                                      
        self.priv_key_str = self.priv_key.export_key().decode()                                                                                                                                                                       
                                                                                                                                                                                                                                      
        rospy.init_node('yin')                                                                                                                                                                                                        
                                                                                                                                                                                                                                      
        self.prompt_rate = rospy.Rate(0.5)                                                                                                                                                                                            
                                                                                                                                                                                                                                      
        #Read the service secret
        self.secret = "asdf"

        self.service = rospy.Service('svc_yang', yangrequest, self.handle_yang_request)

    def handle_yang_request(self, req):
        print(req.secret)
        # Check secret first
        if req.secret != self.secret:
            return "Secret not valid"

        sender = req.sender
        receiver = req.receiver
        action = req.command

        #os.system(action)

        response = "Action performed"

        return response


    def getBase64(self, message):
        hmac = base64.urlsafe_b64encode(message.timestamp.encode()).decode()
        hmac += "."
        hmac += base64.urlsafe_b64encode(message.sender.encode()).decode()
        hmac += "."
        hmac += base64.urlsafe_b64encode(message.receiver.encode()).decode()
        hmac += "."
        hmac += base64.urlsafe_b64encode(str(message.action).encode()).decode()
        hmac += "."
        hmac += base64.urlsafe_b64encode(str(message.actionparams).encode()).decode()
        hmac += "."
        hmac += base64.urlsafe_b64encode(message.feedback.encode()).decode()
        return hmac

    def getSHA(self, hmac):
        m = hashlib.sha256()
        m.update(hmac.encode())
        return str(m.hexdigest())  

    #This function will craft the signature for the message based on the specific system being talked to
    def sign_message(self, message):
        hmac = self.getBase64(message)
        hmac = SHA256.new(hmac.encode('utf-8'))
        signature = PKCS1_v1_5.new(self.priv_key).sign(hmac)
        sig = base64.b64encode(signature).decode()
        message.hmac = sig
        return message

    def craft_ping(self, receiver):
        message = Comms()
        message.timestamp = str(rospy.get_time())
        message.sender = "Yin"
        message.receiver = receiver
        message.action = 1
        message.actionparams = ['touch /home/yang/yin.txt']
        #message.actionparams.append(self.priv_key_str)
        message.feedback = "ACTION"
        message.hmac = ""
        return message

    def send_pings(self):
        # Yang
        message = self.craft_ping("Yang")
        message = self.sign_message(message)
        self.messagebus.publish(message)

    def run_yin(self):
        while not rospy.is_shutdown():
            self.send_pings()
            self.prompt_rate.sleep()

if __name__ == '__main__':
    try:
        yin = Yin()
        yin.run_yin()

    except rospy.ROSInterruptException:
        pass

