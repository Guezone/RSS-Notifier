# RSS-Notifier

RSS-Notifier is a script which probes the RSS feed to make an active watch by email.

With each new news on your / your RSS feed, an email sent you with the title, the summary and the link of the news.

During installation (setup.py), the script writes a configuration file (config.txt) with the information entered on the command line.

![desc](img/logo.png)


**WARNING** : your e-mail credentials (for sending news) are stored in this file with an encoding. Please run this script on a machine over which you have control and which is protected. No one should be able to read the file created.

![desc](img/email.jpg =484x880)

## Requirements 
RSS-Notifier require **feedparser** and **smtplib** python librairies, **Python 3** (tested with 3.7.3) and **Linux based system** (tested on Debian 10).

For install feedparser and smtplib : 
    
    pip3 install feedparser && pip3 install smtplib   

## Configuration
    root@host:~/Desktop/# git clone https://github.com/Guezone/RSS-Notifier && cd RSS-Notifier/
    root@host:~/Desktop/RSS-Notifier# python3 setup.py -h
**Output :** 

      -h, --help            show this help message and exit
      -rss RSS_URL          set your RSS url
      -sender email-addr    set sender email address
      -p your_password      set sender SMTP password
      -server smtp_server   set SMTP server name
      -port port            set SMTP port used by the server
      -tls yes|no           use TLS for SMTP authentication
      -r email-addr         set receiver email address

----------------
Start a setup script to build your configuration : 

    root@host:~/Desktop/RSS-Notifier# python3 setup.py -rss 'https://www.cert.ssi.gouv.fr/alerte/feed/;https://www.zataz.com/feed/' -sender account@mail.com -p 'mYPASSw0rd' -server smtp.mail.com -port 587 -tls yes -r johndoe@mail.com
    

**Output :** 
Please wait. A test message will be sent to test your configuration.

Current RSS feed recording in progress...

Successful recording of RSS entries in the buffer file.

RSS-Notifier is now ready. Execute rss-notifier.py now and automate it.



## Usage
    
If the script does not find new news in your RSS feed (s), here is the result:
    
    root@host:~/Desktop/RSS-Notifier# python3 rss-notifier.py 
**Output :** 
Configuration is good.
No news. Goodbye
    
  -------------------- 
  If the script finds new news in your RSS feed (s), here is the result:

    root@host:~/Desktop/RSS-Notifier# python3 rss-notifier.py


**Output :** 
Configuration is good.

One news detected. Sending email...
Email was sent.

Updating buffer file...
Buffer file was updated. Goodbye.



## Automating
  
You can (and must) automate it periodically with cron for example, in order to check your RSS feeds:

     root@host:~/Desktop/RSS-Notifier# crontab -e
     */10 * * * * python3 /root/Desktop/RSS-Notifier/rss-notifier.py (>> /root/Desktop/RSS-Notifier/rss-updates.log 2>&1)


