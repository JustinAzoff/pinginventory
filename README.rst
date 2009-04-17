Pinginventory is a simple library for running a pingscan on a network and saving the results to a DB.

Why?
----

Many default OS installs block ICMP by default, making using 'ping' for
troubleshooting difficult.  If you find yourself asking yourself "Is the host
I'm trying to troubleshoot offline, or is it not normally pingable in the first
place?" then pinginventory can help ::

    $ pinginventory take_inventory site.ini
    $ pinginventory show_ip site.ini 1.2.3.4
    04/16/09 15:44:24 False
    04/16/09 16:10:30 False
    04/16/09 16:16:11 False
    04/16/09 16:28:38 True

