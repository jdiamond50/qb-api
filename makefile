packet:
	@python3 makePacket.py $(ARGS)
api:
	@python3 qb-api.py
qb:
	@python3 getTossupDiff.py
clean:
	@rm -f introTossup.mp3 tossupStart.mp3 tossupEnd.mp3 answer.mp3 packet.mp3
