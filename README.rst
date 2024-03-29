# OTFBot - The friendly Bot

Requirements
------------

For the core functionality are a *python interpreter* and the following 
modules necessary.

OTFBot is build around the *twisted framework*, so you need this with a 
version of 9.0.0 or newer as well. Currently the the ``words``, ``conch`` 
and ``web`` modules are used (Debian packages ``python-twisted``, 
``python-twisted-bin``, ``python-twisted-conch``, ``python-twisted-core``, 
``python-twisted-web`` and ``python-twisted-words``)

As the configuration is stored in a yaml-file, you need the *python-bindings
for yaml*. libyaml 0.1.1 and python-yaml 3.05 are tested and working.
If you intend to use a encrypted connection you need also
``python-pyopenssl``, ``pyasn1`` and ``python-crypto``.

Some plugins require additional modules. You'll need ``python-feedparser`` 
for ``feed``, ``youtube`` and ``quotesfromweb``, [python-xmltv](thtp://www.funktronics.ca/python-xmltv/) for ``tv``, 
``pysvn`` for ``svn``, python bindings for megahal for ``ki`` ``lxml`` with 
soupparser for ``url``-plugin or ``treq`` and ``lxml`` for ``weather``.
xmppClient needs [wokkel](http:s//wokkel.ik.nu/downloads). Debian has a package python-wokkel for it.

for building the needed modules from pypi with easy_install you need on debian:
build-essential libssl-dev python-dev python-setuptools

Note: if installed via pypi, the logging may behave a bit strange at the start. this is a known issue and does not make any trouble except a few very long lines at start of the log.
see http://www.otfbot.org/bugs/index.php?do=details&task_id=95


Initialize dropin.cache
-----------------------

If you installed the bot as root (i.e. via easy_install), run once
"twistd --help" as root. This avoids error messages because dropin.cache
cannot be written. If you cannot do this, because the bot is installed by root
and you're only having user priviledges, just ignore the error messages, the bot
will run fine nevertheless.


Setup
-----

To create a initial configuration for connecting to a network, joining a 
channel and creating a superuser, run

   twistd gen-otfbot-config -c otfbot.yaml

from the root directory of the bot and answer the questions.

Review the config and adjust some settings as necessary. Do not modify the
configuration while the bot is running, as it will be overwritten while
the bot shuts down.


Starting
--------

The bot is launched via twisteds ``twistd``:

   twistd otfbot -c otfbot.yaml

``twistd`` lets you also specify the user and group and some other settings.
Be aware that the logging is configured via otfbot.yaml and not via twistd.
Running the bot as root is neither needed nor supported. in fact it will not
even start as root, but give you an error.


Developing plugins
------------------

OtfBot is very easy extendable by developing your own plugins. Just have a 
look at example/example.py. All Callbacks are listed in this file. If you 
aren't sure what a specific callback does, just copy the plugin to 
otfbot/plugins/ircClient/, add it to config and start otfbot to test it.

If you have finished follow the steps to enable a plugin above.
If you think your plugin is of general interest, you are welcome to contact
us to include it into the repository.


Contact
-------

You can contact the developers via IRC in #otfbot at irc.libera.chat or by filing
a bug.
