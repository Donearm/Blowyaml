[![Build Status](https://travis-ci.org/Donearm/Blowyaml.svg)](https://travis-ci.org/Donearm/Blowyaml)

Quick script to encrypt and decrypt a YAML file storing passwords with the 
Blowfish algorithm. The YAML file is used to store accounts' login credentials.
As its format is customized to my own needs, Blowyaml is more an example than a 
real use case. In any way, I hope it's at least of some inspiration to you.

##Requirements

* pycrypto
* pyyaml

##YAML file format

I'm using a customized way to keep login informations in the YAML format. 
Blowyaml is based on this so _it works for me_™.

Basically there is a key (the one you search for with Blowyaml's `-s` switch) 
that contains 1 or more (in the case of multiple accounts to the same site) 
associative arrays with the login name, password, url etc. A visual example will 
be clearer

	Sitename: { url: www.thissite.com, name: "myloginname", password: "mypassword"}

this is the basic. For multiple accounts I chose

	Sitename: { url: www.thesite.com,
		Account1: { name: "loginname1", password: "password1"},
		Account2: { name: "loginname2", password: "password2"},
	}

and so on. Self-explanatory.

Occasionally I add a

	disabled: true

at the end of the array to mark sites that I don't use anymore. It may be 
because the site died some time ago (and I like to keep login credentials anyway 
just to remember what passwords I already used) or because I don't find it 
useful anymore but it doesn't allow deleting the account (damn you!)

##Todo

* Python3 support
