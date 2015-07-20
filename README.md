
Experiment to see if we can use [bazel](https://bazel.io) to run Python tests.

# Notes on bazel spike

## Introduction

* It's good to run the full test suite before every change, so you can be
  confident that the change doesn't break master
* Running the full test suite is often slow
* This means cost of making a change is some large constant that bears no
  relation to the size of the chhange
* Wouldn't it be better to only run the tests that change?

## Questions

* Can I use bazel to run tests in Python?
* If I specify wrong dependencies for tests, are they caught?
* How much work is involved in bazelifying a project?
* Does it properly cache test results?

## Initial set up

* Installed bazel using http://bazel.io/docs/install.html
  * https://github.com/google/bazel.git b16e71b29e1104d2475ccd1278910a92497dbee8
  * Ubuntu 15.04

* Simple Python project with one function and one test module that contains
  two tests

* Created `WORKSPACE` file in project root

* Confirmed installation worked:
```
$ bazel build examples/java-native/src/main/java/com/example/myproject:hello-world
..............
INFO: Found 1 target...
Target //examples/java-native/src/main/java/com/example/myproject:hello-world up-to-date:
  bazel-bin/examples/java-native/src/main/java/com/example/myproject/hello-world.jar
  bazel-bin/examples/java-native/src/main/java/com/example/myproject/hello-world
INFO: Elapsed time: 3.447s, Critical Path: 1.20s
```

* Directory contents:

```
jml@wit:~/src/bazel-python-spike$ ls -la
total 40
drwxrwxr-x  4 jml jml 4096 Jul 20 14:29 .
drwxrwxr-x 18 jml jml 4096 Jul 20 14:18 ..
lrwxrwxrwx  1 jml jml   85 Jul 20 14:29 bazel-bazel-python-spike -> /home/jml/.cache/bazel/_bazel_jml/5349438f91eafd39f2b56a30e3eeae42/bazel-python-spike
lrwxrwxrwx  1 jml jml  121 Jul 20 14:29 bazel-bin -> /home/jml/.cache/bazel/_bazel_jml/5349438f91eafd39f2b56a30e3eeae42/bazel-python-spike/bazel-out/local_linux-fastbuild/bin
lrwxrwxrwx  1 jml jml  126 Jul 20 14:29 bazel-genfiles -> /home/jml/.cache/bazel/_bazel_jml/5349438f91eafd39f2b56a30e3eeae42/bazel-python-spike/bazel-out/local_linux-fastbuild/genfiles
lrwxrwxrwx  1 jml jml   95 Jul 20 14:29 bazel-out -> /home/jml/.cache/bazel/_bazel_jml/5349438f91eafd39f2b56a30e3eeae42/bazel-python-spike/bazel-out
lrwxrwxrwx  1 jml jml  126 Jul 20 14:29 bazel-testlogs -> /home/jml/.cache/bazel/_bazel_jml/5349438f91eafd39f2b56a30e3eeae42/bazel-python-spike/bazel-out/local_linux-fastbuild/testlogs
drwxrwxr-x  8 jml jml 4096 Jul 20 14:21 .git
-rw-rw-r--  1 jml jml 1605 Jul 20 14:26 README.md
drwxrwxr-x  3 jml jml 4096 Jul 20 14:21 spike
-rw-rw-r--  1 jml jml    0 Jul 20 14:27 WORKSPACE
```


## Open questions and actions

* **XXX**: Can I put the test build targets in the main module?
* **XXX**: Can I make `--test_output=errors` the default?
