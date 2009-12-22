import sys, os, os.path, mimetypes
from optparse import OptionParser
from email import encoders
from email.message import Message
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
import smtplib

# Defaults (that can all be overriden easily)
DEFAULT_HOST = "localhost"
DEFAULT_FROM_ADDRESS = "alex@tpsitulsa.com"
DEFAULT_SUBJECT = "Automatic Email"

usage = "usage: python %prog [options] contents.txt to-person [to-person...]"
parser = OptionParser(usage=usage)
parser.add_option(
	"-s", "--subject", dest="subject", default=DEFAULT_SUBJECT, 
	help="""Specifies the subject for the sent mail"""
)

parser.add_option(
	"-b", "--bcc", dest="bcc", default=[], action="append",
	help="Specifies an address to Bcc:. Can be specified more than once."
)

parser.add_option(
	"-a", "--attach", dest="attach", action="append", default=[], type="string",
	help="Specifies an attachment to be attached. Can be specified more than once."
)
parser.add_option(
	"-f", "--from", dest="from_addr",
	help="Specifies who the email is from. Defaults: " + DEFAULT_FROM_ADDRESS,
	default=DEFAULT_FROM_ADDRESS
)
parser.add_option(
	"--headers", dest="headers", 
	help="Specifies a file containing a list of headers."
)
parser.add_option(
	"--host", dest="host", help="Specifies what SMTP server to use. Default: " + DEFAULT_HOST, default=DEFAULT_HOST
)
parser.add_option(
	"-u", "--user", dest="user", help="Specifies a username to authenticate with."
)
parser.add_option(
	"-p", "--password", dest="password", help="Specifies a password to authenticate with."
)
parser.add_option(
	"--port", dest="port", help="Specifies what SMTP port to use. Default: 25.", default=25
)
parser.add_option(
	"--html", dest="html", help="Specifies an HTML message to send along with the text."
)

# Load arguments
opts, args = parser.parse_args()
if len(args) < 2:
	parser.print_help()
	sys.exit(1)

# read contents
contents_file = args.pop(0)
contents_file = open(contents_file, "rb")
contents = contents_file.read()
contents_file.close()

# get to recipient list
to_list = args

# Create message
outer = MIMEMultipart()
outer.preamble = "If you are seeing this, your mail reader is not MIME aware, which means: problems."

# Set headers
outer["Subject"] = opts.subject
outer["From"] = opts.from_addr
outer["To"] = ", ".join(to_list)

# Custom headers
if opts.headers:
	for l in open(opts.headers):
		if l.strip() == "": continue
		try:
			header, content = l.lpartition(":")
			outer[header] = content
		except:
			print "Bad header: " + l
		

# First attachment: another email with attachments! (a text and html attachment)
inner = MIMEMultipart("alternative")
text_content = MIMEText(contents, 'plain');
inner.attach(text_content)

if opts.html:
	f = open(opts.html)
	html_content = MIMEText(f.read(), "html")
	f.close()
	inner.attach(html_content)

outer.attach(inner)

# Handle attachments
for filename in opts.attach:
	if not os.path.isfile(filename):
		print "WARNING: Unable to attach: " + filename
		continue
	
	# Guess the content type based on the file's extension.  Encoding
	# will be ignored, although we should check for simple things like
	# gzip'd or compressed files.
	ctype, encoding = mimetypes.guess_type(filename)
	if ctype is None or encoding is not None:
		# No guess could be made, or the file is encoded (compressed), so
		# use a generic bag-of-bits type.
		ctype = 'application/octet-stream'
	maintype, subtype = ctype.split('/', 1)
	
	fp = open(filename, 'rb')
	msg = MIMEBase("application", "octet-stream")
	msg.set_payload(fp.read())
	fp.close()
	
	# Encode the payload using Base64
	encoders.encode_base64(msg)
	
	# Set the filename parameter
	msg.add_header('Content-Disposition', 'attachment', filename=filename)
	outer.attach(msg)

s  = smtplib.SMTP()
s.connect(opts.host,opts.port)
if opts.user:
	s.login(opts.user, opts.password)
s.sendmail(opts.from_addr, to_list + opts.bcc, outer.as_string())
s.quit()