
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

## BUILD files

I've added one [BUILD](spike/BUILD) file under the `spike` package, which is directly
underneath the directory with `WORKSPACE`. Using Bazel's convention, this is
in `//spike/BUILD`.

### Running the tests

```
$ bazel test --test_output=errors spike:test_spike
INFO: Found 1 test target...
FAIL: //spike:test_spike (see /home/jml/.cache/bazel/_bazel_jml/5349438f91eafd39f2b56a30e3eeae42/bazel-python-spike/bazel-out/local_linux-fastbuild/testlogs/spike/test_spike/test.log).
INFO: From Testing //spike:test_spike:
==================== Test output for //spike:test_spike:
Traceback (most recent call last):
  File "/home/jml/.cache/bazel/_bazel_jml/5349438f91eafd39f2b56a30e3eeae42/bazel-python-spike/bazel-out/local_linux-fastbuild/bin/spike/test_spike.runfiles/spike/tests/test_spike.py", line 4, in <module>
    from spike import square
ImportError: cannot import name square
================================================================================
Target //spike:test_spike up-to-date:
  bazel-bin/spike/test_spike
INFO: Elapsed time: 0.182s, Critical Path: 0.03s
//spike:test_spike                                                       FAILED

Executed 1 out of 1 tests: 1 fails locally.
```

The `--test_output=errors` option tells `bazel` to include errors in the test
output. Without it, we wouldn't get the stack trace.

The problem here is that `test_spike` doesn't actually have access to
`spike/__init__.py`, because it wasn't declared as a dependency. Let's fix
that:

```
+    deps=[
+        ':spike',
+    ],
```

Now run again:

```
$ bazel test --test_output=errors spike:test_spike
INFO: Found 1 test target...
Target //spike:test_spike up-to-date:
  bazel-bin/spike/test_spike
INFO: Elapsed time: 0.300s, Critical Path: 0.07s
//spike:test_spike                                                       PASSED

Executed 1 out of 1 tests: 1 test passes.
There were tests whose specified size is too big. Use the --test_verbose_timeout_warnings command line option to see which ones these are.
```

It passed, but there's a warning about test size. Let's fix that by correctly
pointing out that our test is "small".

```
$ bazel test --test_output=errors spike:test_spike
INFO: Found 1 test target...
Target //spike:test_spike up-to-date:
  bazel-bin/spike/test_spike
INFO: Elapsed time: 0.273s, Critical Path: 0.05s
//spike:test_spike                                                       PASSED

Executed 1 out of 1 tests: 1 test passes.
```

`bazel` caches results. Let's run again:

```
$ bazel test --test_output=errors spike:test_spike
INFO: Found 1 test target...
Target //spike:test_spike up-to-date:
  bazel-bin/spike/test_spike
INFO: Elapsed time: 0.119s, Critical Path: 0.00s
//spike:test_spike                                          (1/0 cached) PASSED

Executed 0 out of 1 tests: 1 test passes.
```

Note that it executed 0 tests, and that the elapsed time is lower.

## Open questions and actions

* Can I make `--test_output=errors` the default?
* What happens if I put spike's contents in a module, rather than
  `__init__.py`?
* Can I put the test rules in the `tests` directory?
