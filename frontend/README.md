How to build the front end
1. CD to this path
2. run `python -m http.server` and visit http://localhost:8000/ for front end.
3. For front up building purpose: Since we do not want to send an actual request for each change to front end, in another terminal in the same path, run `python mock.py` to start the mock flask server. `mock.py` will return consistent response without waiting for API calls, this would be convenient for front end dev purpose.
4. (optional) change mock.py to experiment different server response
