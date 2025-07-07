packet:
	python3 makePacket.py $(ARGS)
api:
	python3 qb-api.py
qb:
	python3 getTossupDiff.py
clean:
	rm *.mp3
