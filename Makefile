.PHONY: all

audacity = $(wildcard */*.aup)
sounds = $(patsubst %.aup, %.h, $(audacity))

all: $(sounds)

%.h: %.wav wav2header.py
	python $(word 2, $^) $(notdir $*) $< $@
