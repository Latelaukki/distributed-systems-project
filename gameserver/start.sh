hostname -I | while read x ; do python3 -m uvicorn fast-api:app --reload --host $x --port 7777; done