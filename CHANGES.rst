Changelog
---------


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
