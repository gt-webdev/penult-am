# penult.am

## Basic Setup
in order to run or work on this project, you will need to clone it (duh)
and setup a virtual python environment within your project folder. Depending
on the name of your virtualenv binary (usually just `virtualenv` although
some machines may have a separate one for python2 and python3, e.g.
`virtualenv3` on my machine). This can be done very simply with:

    (user@penult-am) # virtualenv3 env

After you run this command, you should have a folder named `env` within which
you will have a folder named `bin` which should contain some key python binaries
such as `python` and `pip`. Now you can install our requirements with:

    (user@penult-am) # env/bin/pip install -r requirements.txt

After doing this you will be able to run the server using:

    (user@penult-am) # env/bin/python runserver.py
