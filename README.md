# The Electric Cat

A tool for connecting and mapping whatever items you need to track to make
your software endeavour a success.

[The long story...](https://richard-taylor.github.io/threads/the-electric-cat)

## running the unit tests

The code was written with python 3.5.2 and also tested with python 3.10.6
```
bin/test_thelca.sh
```

If all the unit tests pass you have compatible dependencies.

## running the API server

Generate [an encryption certificate](https://richardtaylor.co.uk/threads/the-electric-cat/https-observability.html) first if you haven't got one and put both PEM files in a folder called
`config` if you want to use it with the default options.

Then run
```
bin/run_thelca.sh --help
```

## running the API tests

After you started the server...
```
bin/api_test_thelca.sh
```

The API tests also require the python 'requests' module.
