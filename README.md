# The Electric Cat

A tool for connecting and mapping whatever items you need to track to make
your software endeavour a success.

[The long story...](https://richard-taylor.github.io/threads/the-electric-cat)

## running the unit tests

The code was written with python 3.5.2 and also tested with python 3.7.3
```
bin/test_thelca.sh
```

If all the unit tests pass you have compatible dependencies.

## running the API server

```
bin/run_thelca.sh --help
```

## running the API tests

After you started the server...

```
bin/api_test_thelca.sh
```

The API tests also require the python 'requests' module.
