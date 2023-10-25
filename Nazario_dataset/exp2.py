import mailbox
import re
import csv
import os


keys = ["Return-Path:", "X-Original-To:", "Delivered-To:", "Received:", "X-Forwarded-For:", "X-Forwarded-For:", "X-FDA:", "Authentication-Results:", "X-Spam-Summary:", "X-HE-Tag:", "Received:", "X-IronPort-Anti-Spam-Filtered:", "X-IronPort-Anti-Spam-Result:", "X-IronPort-AV:", "Received:", "Date:", "Message-Id:", "To:", "Subject:", "X-PHP-Script:", "From:", "Reply-To:", "Status:", "X-Status:", "X-Keywords:", "X-UID:"]
not_to_include = ["MIME-Version:", "Content-Type:", "Content-Transfer-Encoding:", "Content-Description:"]
def getBody(message):
    messageLines = message.split('\n')
    messageLines.reverse()
    s = ""
    for line in messageLines:
        line = str(line)
        x = re.search("^.*:", line)
        if(x):
            x = re.findall("^.*:", line)
            if x[0] in keys:
                break
            elif x[0] in not_to_include:
                continue
            else:
                 s = line + '\n' + s
        else:
            s = line + '\n' + s
    return s

def convertUTF8ToAscii(file_path):
    with open(file_path, 'rb') as file:
        data = file.readlines()
        s = ""
        for lines in data:
            lines = lines.decode("ascii", errors="ignore")
            s = s + lines
        text_file = open("dataset1/" + file_path, "w")
        text_file.write(s)
        text_file.close()        
                
        # udata=data.decode("utf-8")
        # asciidata=udata.encode("ascii","ignore")
        # text_file = open("dataset1/"+file_path, "w")
        # text_file.write(asciidata)

def readFile(filename):
    # mbox_file = filename + '.mbox'
    print(filename)
    messages = mailbox.mbox(filename)
    for message in messages:
        message_info = {}
        # print(message.get('Subject'))
        message_info["email_subject"] = message.get('Subject')
        message_str = (str(message))
        message_info["email_body"] = getBody(message_str)
        message_info["email_from"] = message.get("From")
        message_info["email_to"] = message.get("To")
        message_info["is_phishing"] = True
        message_info["is_spam"] = True
        emails.append(message_info)
        # break

    


emails = []
prev_len = 0
files = os.listdir("dataset")
for file in files:
    file_path = os.path.join("dataset", file)
    convertUTF8ToAscii(file_path)
    readFile("dataset1/" + file_path)
    print(len(emails)-prev_len)
    prev_len = len(emails)
    # break

with open("Nazario.csv", 'w') as f:  # You will need 'wb' mode in Python 2.x
    w = csv.DictWriter(f, emails[0].keys())
    w.writeheader()
    for email in emails:
        w.writerow(email)


