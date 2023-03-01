===
FAQ
===


#. **Can django-environ determine the location of .env file automatically?**

   ``django-environ`` will try to get and read ``.env`` file from the project
   root if you haven't specified the path for it when you call :meth:`.environ.Env.read_env`.
   However, this is not the recommended way. When it is possible always specify
   the path to the ``.env`` file. Alternatively, you can use a trick with an
   environment variable pointing to the actual location of ``.env`` file.
   For details see ":ref:`multiple-env-files-label`".

#. **What (where) is the root part of the project, is it the directory that contains settings.py file?**

   Where your ``manage.py`` file is (that is your project root directory).

#. **What kind of file should .env be?**

   ``.env`` is a plain text file.

#. **Should name of the file be simply .env (or something.env)?**

   Just ``.env``. However, this is not a strict rule, but just a common
   practice. Formally, you can use any filename.

#. **Is .env file going to be imported in settings file?**

   No need to import, ``django-environ`` automatically picks variables
   from there.
