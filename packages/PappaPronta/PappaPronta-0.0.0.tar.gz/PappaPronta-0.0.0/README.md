# PappaPronta-python

**PappaPronta** is a `python` package of readymade stereotyped musical objects for lazy students to produce ugly electronic music.

You are welcome to browse this project and its object keeping in mind that the
music you will be able to create with the objects contained herein will not do
anything interesting for you, simply because *I* have written them rather than
*you yourself*. However, you can always `fork` this repository, derive *your
own* objects from these or just use it as a dependency for one or more
packages of yours.

## HOW TO BUILD THE PACKAGE

```sh
$ pip -m venv ./venv
$ . ./venv/bin/activate
$ make # will run all the tests
```

If the tests pass, then you can:

```sh
$ make install
```

## HOW TO USE THE PACKAGE

Check the examples in the [examples](./docs/examples/README.md) directory.

## AUTHOR

Nicola Bernardini (nicb@sme-ccppd.org) started it in July 2020 in a fit of
fury and desperation against his own students.

## REQUIREMENTS

In order to use the `PappaPronta` package, you need to have the following
`python` packages installed:

* `pathtools` (should come already with your `python` distribution) 
* `pyyaml` (should come already with your `python` distribution) 

## LICENSE

[GNU GPL version 3.0](./LICENSE)
