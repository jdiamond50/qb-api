reader:
	@python3 reader.py $(ARGS)
packet:
	@python3 makePacket.py $(ARGS)
api:
	@python3 testing/OLD_qb-api.py
qb:
	@python3 testing/getTossupDiff.py
gui:
	@python3 testing/guiTest.py
clean:
	@rm -f introTossup.mp3 tossupStart.mp3 tossupEnd.mp3 answer.mp3 packet.mp3 currTossup.mp3
