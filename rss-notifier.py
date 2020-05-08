import feedparser, base64, os, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
rss, sender, receiver, password, smtpsrv, port, tls = '','','','','','',''

def checkConfig(rss, sender, receiver, password, smtpsrv, port, tls):	
	script_path = os.path.abspath(__file__)
	dir_path = script_path.replace("rss-notifier.py","")
	config = open(dir_path+"config.txt","r")
	for line in config.readlines():
		if "rssfeed(=)" in line:
			rss_conf = line.split("(=)")
			rss = rss_conf[1].replace("\n","")
		elif "sender(=)" in line:
			sender_conf = line.split("(=)")
			sender = sender_conf[1].replace("\n","")
		elif "password(=)" in line:
			passwd_conf = line.split("(=)")
			b64passwd = passwd_conf[1].replace("\n","")
			b = b64passwd.encode("UTF-8")
			bytes_password = base64.b64decode(b)
			password = bytes_password.decode("UTF-8")
		elif "smtpsrv(=)" in line:
			smtpsrv_conf = line.split("(=)")
			smtpsrv = smtpsrv_conf[1].replace("\n","")
		elif "port(=)" in line:
			port_conf = line.split("(=)")
			port = int(port_conf[1].replace("\n",""))
		elif "receiver(=)" in line:
			receiver_conf = line.split("(=)")
			receiver = receiver_conf[1].replace("\n","")
		elif "tls(=)" in line:
			tls_conf = line.split("(=)")
			tls = tls_conf[1].replace("\n","")
		else:
			print("Nothing in config file.")
			exit()
	if all(value != '' for value in [rss, sender, receiver, password, smtpsrv, str(port), tls]):
		print("Configuration is good.")
		rssPoller(rss, sender, receiver, password, smtpsrv, port, tls)
	else:
		print("Error in the config file.")

def rssPoller(rss, sender, receiver, password, smtpsrv, port, tls):
	script_path = os.path.abspath(__file__)
	dir_path = script_path.replace("rss-notifier.py","")
	rss_data = open(dir_path+"rss_data","r")
	currents_links = []
	old_links = []
	new_links = []
	if ';' in rss:
		rss = rss.split(';')
		for url in rss:
			current_feed = feedparser.parse(url)
			for entry in current_feed.entries:
				currents_links.append(str(entry.link))
			for item in rss_data.readlines():
				if item != "" or item != "\n":
					old_links.append(item.replace('\n',''))
			for link in currents_links:
				if link not in old_links:
					for entries in current_feed.entries:
						if entries.link == link:
							title = entries.title
							url = entries.link
							summary = entries.summary
							sendMail(rss, sender, password, smtpsrv, port, tls, receiver,title, url, summary)
							new_links.append(url)
	else:
		current_feed = feedparser.parse(rss)
		for entry in current_feed.entries:
			currents_links.append(str(entry.link))
		for item in rss_data.readlines():
			if item != "" or item != "\n":
				old_links.append(item.replace('\n',''))
		for link in currents_links:
			if link not in old_links:
				for entries in current_feed.entries:
					if entries.link == link:
						title = entries.title
						url = entries.link
						summary = entries.summary
						sendMail(rss, sender, password, smtpsrv, port, tls, receiver,title, url, summary)
						new_links.append(url)
	if not new_links:
		print("No news. Goodbye")	
	else:
		print("Updating buffer file...")
		rss_data = open(dir_path+"rss_data","a+")
		for new_url in new_links:
			rss_data.write(new_url+'\n')
		rss_data.close()
		print("Buffer file was updated. Goodbye.")

def sendMail(rss, sender, password, smtpsrv, port, tls, receiver,title, url, summary):
	body = ""
	with open('template.html', 'r') as template:
	    html_code = template.read()
	    html_code = html_code.replace("Responsive HTML email templates",title)
	    html_code = html_code.replace("body body body body", summary)
	    body = html_code.replace("URL OF THE NEWS",url)
    

	print("One news detected. Sending email...")
	try:
		smtpserver = smtplib.SMTP(smtpsrv,port)
		msg = MIMEMultipart()
		msg['Subject'] = 'RSS-Notifier - New Alert'
		msg['From'] = sender
		msg['To'] = receiver
		msg.attach(MIMEText(body, 'html'))
	except:
		print("Failed to send email.")
		exit()
	try:
		if tls == "yes":
			smtpserver.ehlo()
			smtpserver.starttls()
			smtpserver.login(sender, password)
			smtpserver.sendmail(sender, receiver, msg.as_string())
		elif tls == "no":
			smtpserver.login(sender, password)
			smtpserver.sendmail(sender, receiver, msg.as_string())
			print("Email was sent.\n")
	except:
		print("An error occurred during authentication with the SMTP server. Check the configuration and try again.")
		exit()

def main():
	checkConfig(rss, sender, receiver, password, smtpsrv, port, tls)
	
main()
