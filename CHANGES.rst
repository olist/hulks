Changelog
---------

0.4.1
~~~~~

* Fix check mutable defaults hook to work on python < 3.6

0.4.0
~~~~~

* Add new hook to check default django migration comment

0.3.0
~~~~~

* Add new hook to check print statements in code

0.2.7
~~~~~

* Fix check-mutable-default check to stop failing when a class attribute receives a classmethod instance

0.2.6
~~~~~

* Improve check-mutable-default to verify for mutable elements on class attributes

0.2.5
~~~~~~

* Improve error handling on invalid text files

0.2.4
~~~~~~

* Fixes config of invalid-domains hook to only check text files

0.2.3
~~~~~

* Improve check-mutable-default to verify for mutable elements inside tuples

0.2.2
~~~~~

* Fix check-mutable-default to work correctly for modules with many functions and methods

0.2.1
~~~~~

* check-mutable-default hook now supports coroutines

0.2.0
~~~~~

* Add new hook to check mutable default arguments in function/methods

0.1.1
~~~~~

* Bugfix: validate all files, even after the first failure
* Replace the usage of fstrings until we have a good reason for 3.6-specific feature

0.1.0
~~~~~

* Add new hook for defaults django migrations filename

0.0.2
~~~~~

* Improve check_logger to ignore getLogger(var) calls inside code blocks (functions/methods etc.)

0.0.1
~~~~~

* Initial release
