run:

server:
	touch storage.txt
	python3 server.py

tests:
	python3 tests.py

manyclients:
	python3 manyclients.p 20 10 1000

clean:
	rm -rf __pycache__

