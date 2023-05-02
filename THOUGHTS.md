1. Had to register for an API key
2. Had to work out how to make the hash
3. Python code setup
   - venv for dependency management
   - implement colourful logging
   - use dotenv to load in private and public keys for the marvel api
   - made a `MarvelService` to abstract the API
3. Downloaded the data using `curl` to see what the structure was
   - Saw that it is paginated, so needed to consider that in the `MarvelService` implementation.
     - eg: set `offset=x&limit=x` until `offset+limit >= total`
   - I noticed the characters endpoints shows the comics anyway, but that is also paginated, so we should find each collection: `.data.results[].comics.collectionURI`
   - Actually no, we only need to see how many they are in, nothing more. `.data.results[].comics.available`
4. Implemeted the pagination
   - It was slow to create and teardown the http requests, so I realised I should be using a session (done, but not much faster).
   - On top of that, I should be using a generator (`yield`) so the caller can just iterate over the results and begin working on them. See: https://stackoverflow.com/a/50259251/8148609
5. Output
   - used a lambda to tidy up the data structure, and used `map` and `sorted` ready for outputting as a table
   - used tabulate for pretty printing the table
5. Improvements:
   - testing (mock requests using local data to save hitting the API)
   - caching via Etag (store files by etag, do HEAD requests to ssee if we have a copy with the same Etag from a previous run)
   - on the first request, we can get the total, then run the remainder concurrently (with a max parallelism setting)
   - decided not to use pandas, but could do if we wanted to run many queries across the data.
   - document the methods in `lib.py`

I'm unsure if this was done correctly, as some of the stuff returned from the characters API has groups (like x-men), and also has counts of 0 for some characters.
