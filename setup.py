import sys, base64, time, os, smtplib,argparse, feedparser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def mailTester(rss, sender, passwd, smtpsrv, port, tls, receiver):
    body = "Test message sent by FeedNotifier.\n\n"+rss
    try:
        print("\nPlease wait. A test message will be sent to test your configuration.")
        smtpserver = smtplib.SMTP(smtpsrv,port)
        msg = MIMEMultipart()
        msg['Subject'] = 'FeedNotifier - TEST.'
        msg['From'] = sender
        msg['To'] = receiver
        msg.attach(MIMEText(body, 'plain'))
    except:
        print("Incorrect configuration. Exit")
        exit()
    try:
        if tls == "yes":
            smtpserver.ehlo()
            smtpserver.starttls()
            smtpserver.login(sender, passwd)
            smtpserver.sendmail(sender, receiver, msg.as_string())
        elif tls == "no":
            smtpserver.login(sender, passwd)
            smtpserver.sendmail(sender, receiver, msg.as_string())
        else:
            print("You must specify if you want to use TLS(-tls yes|no). Exit.")
            exit()      
    except:
        print("An error occurred during authentication with the SMTP server. Check the configuration and try again.")
        exit()
    if rssTester(rss) == True:
        configBuilder(rss, sender, passwd, smtpsrv, port, tls, receiver)
        time.sleep(0.3)
        print("RSS-Notifier is now ready. Execute rss-notifier.py now and automate it.")

def rssBuild(rss):
    script_path = os.path.abspath(__file__)
    dir_path = script_path.replace("setup.py","")
    print("\nCurrent RSS feed recording in progress...\n")
    if ';' in rss:
        rss = rss.split(';')
        rss_data_file = open(dir_path+"rss_data","w")
        data = ""
        for feed in rss:
            base_feed = feedparser.parse(feed)
            for entry in base_feed.entries:
                data+=entry.link
                data+='\n'
        rss_data_file.write(data)
        print("Successful recording of RSS entries in the buffer file.\n")
    else:
        time.sleep(0.3)
        rss_data_file = open(dir_path+"rss_data","w")
        base_feed = feedparser.parse(rss)
        for entry in base_feed.entries:
            rss_data_file.write("{}\n".format(entry.link))
        print("Successful recording of RSS entries in the buffer file.\n")

def rssTester(rss):
        if ';' in rss:
            rss_list = rss.split(';')
            for feed_url in rss_list:
                try:
                    rss_test = feedparser.parse(feed_url)
                    my_feed = rss_test.feed.keys()
                    if not my_feed :
                        print("Error with : "+feed_url)
                        raise
                except:
                    print("Unable to retrieve the RSS feed. Check your url and retry.")
                    exit()
            rssBuild(rss)
            return True
        else:
            rss_test = feedparser.parse(rss)
            my_feed = rss_test.feed.keys()
            if my_feed:
                rssBuild(rss)
                return True
            else:
                print("Unable to retrieve the RSS feed. Check your url and retry.")
                exit()

def configBuilder(rss, sender, passwd, smtpsrv, port, tls, receiver):
    script_path = os.path.abspath(__file__)
    dir_path = script_path.replace("setup.py","")
    encoded_pass = (str(base64.b64encode(passwd.encode("UTF-8"))).replace("b'","")).replace("'","")
    conf = open(dir_path+"config.txt","w")
    conf.write("rssfeed(=)"+rss+"\n"+"sender(=)"+sender+"\n"+"password(=)"+encoded_pass+"\n"+"smtpsrv(=)"+smtpsrv+"\n"+"port(=)"+str(port)+"\n"+"receiver(=)"+receiver+"\n"+"tls(=)"+tls+"\n")
    conf.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-rss",nargs=1,required=True,metavar="RSS_URL",help="set your RSS url")
    parser.add_argument("-sender",nargs=1,required=True,metavar="email-addr",help="set sender email address")
    parser.add_argument("-p",nargs=1,required=True,metavar="your_password",help="set sender SMTP password")
    parser.add_argument("-server",nargs=1,required=True,metavar="smtp_server",help="set SMTP server name")
    parser.add_argument("-port",nargs=1,required=True,metavar="port",help="set SMTP port used by the server", type=int)
    parser.add_argument("-tls",nargs=1,required=True,metavar="yes|no",help="use TLS to send email")
    parser.add_argument("-r",nargs=1,required=True,metavar="email-addr",help="set receiver email address")
    
    args = parser.parse_args()
    rss = ''.join(args.rss)
    sender = ''.join(args.sender)
    passwd = ''.join(args.p)
    server = ''.join(args.server)
    port = args.port[0]
    tls = ''.join(args.tls)
    receiver = ''.join(args.r)

    mailTester(rss, sender, passwd, server, port, tls, receiver)
main()