dolci-tickets
=============

Automates the process of obtaining tickets to Dolci -- a free (but space-limited) student-run restaurant at Middlebury College.  Currently broken and will not be updated, as Dolci ticket sign up now occurs over a larger window and includes a random element.

Usage
-----

Add names (with their corresponding email addresses and mailbox numbers) to names.txt and run dolci.py.  Note that the script has to be modified for non-Wednesday Dolci dinners and that you may need to install a few Python libraries if you don't already have them installed; this script depends on mechanize, datetime, time, random, and urllib2.