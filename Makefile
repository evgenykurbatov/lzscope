
TARGET := README


.PHONY: html
html: $(TARGET).html

$(TARGET).html: $(TARGET).rst
	pandoc $< -s -o $@


.PHONY: pdf
pdf: $(TARGET).pdf

$(TARGET).pdf: $(TARGET).rst
	pandoc $< -s -o $@
