autoexec
========

Automatically turn python functions into executable scripts

Whenever you have written some code and want to run it on a cluster, the first step is to turn it into an executable. This typically leads to a quick stop over at the docs for `argparse`, together with a lot of duplicated effort in reproducing the function signature. This can be error-prone and annoying, especially if one edits the function.

This script automates this process, using information about types provided either through function annotation, default values in keyword arguments, or type information in `numpydoc`-style docstrings. Like any shell script, this limits the functions to arguments that can be passed in the terminal, (str, int, float,...).

Example
-------

Let's say you've written the following function in ``example.py``, which provides all kinds of different type information

.. code:: python

    def add(a: int, b, c=5, d=7., e=None):
    """Some cool addition.

        It's super complicated.
        You know, adding and stuff.

        Parameters
        ----------
        b : int
            This is the second complicated parameter
            super complicated
        e : int, optional
        """
        if e is None:
            e = 0
        return a + b + c + d + e

Now all you have to do to turn this into an executable is add the following code at the bottom

.. code:: python

    if __name__ == '__main__':
        import autoexec
        res = autoexec.execute_function(add)
        print(res)

and run ``chmod +x example.py``. Now if you run ``./example.py --help`` you get the following output

.. code::

    ❯❯❯ ./example.py --help
    usage: example.py [-h] --a A --b B [--c C] [--d D] [--e E]

    Some cool addition.

    It's super complicated.
    You know, adding and stuff.

    optional arguments:
      -h, --help  show this help message and exit
      --a A       int
      --b B       This is the second complicated parameter
                  super complicated
      --c C       int, default: 5
      --d D       float, default: 7.0
      --e E       int, default: None

And you're ready to call the script from the command line

.. code::

    ❯❯❯ ./example.py --a 1 --b 2 --c 3
    13.0

There is type-checking by argparse

.. code::

    ❯❯❯ ./example.py --a 1 --b stringy
    usage: example.py [-h] --a A --b B [--c C] [--d D] [--e E]
    example.py: error: argument --b: invalid int value: 'stringy'

and it complains about missing arguments

.. code::

    ❯❯❯ ./example.py --a 1
    usage: example.py [-h] --a A --b B [--c C] [--d D] [--e E]
    example.py: error: the following arguments are required: --b

There is also support for multiple functions via ``autoexec.execute_functions``.
