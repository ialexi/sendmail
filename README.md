sendmail.py
===========
Sendmail scripts have been done many times before. However, I needed
something simple and very easy to use, but with several (rather simple)
capabilities. So I wrote this.

It is dirty and not the best organized, but I'd like to keep it somewhere,
and GitHub is my friend :). Perhaps someone will find it useful. 

I'm not sure I did everything right, but it seems to work (which is a good thing, of course).


Usage
-----
		python sendmail.py [options] contents.txt to-person [to-person...]

		Options:
		  -h, --help            show this help message and exit
		  -s SUBJECT, --subject=SUBJECT
		                        Specifies the subject for the sent mail
		  -b BCC, --bcc=BCC     Specifies an address to Bcc:. Can be specified more
		                        than once.
		  -a ATTACH, --attach=ATTACH
		                        Specifies an attachment to be attached. Can be
		                        specified more than once.
		  -f FROM_ADDR, --from=FROM_ADDR
		                        Specifies who the email is from. Defaults:
		                        alex@tpsitulsa.com
		  --headers=HEADERS     Specifies a file containing a list of headers.
		  --host=HOST           Specifies what SMTP server to use. Default: localhost
		  --html=HTML           Specifies an HTML message to send along with the text.
