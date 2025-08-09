ENGINE=pdflatex
# Name of the master LaTeX file
DOCUMENT=colm2025_conference

# Figure generation settings
PYTHON=python3
FIGURE_SCRIPTS=fig1.py fig2.py fig3.py
GENERATED_FIGURES=fig1_with_sd.pdf fig2.pdf fig3_replicated_style.pdf
CROPPED_FIGURES=fig1_with_sd-crop.pdf fig2-crop.pdf fig3_replicated_style-crop.pdf

#--------------------------------------------------
# Do NOT change anything below
#--------------------------------------------------
default: $(DOCUMENT).pdf

# Figure generation rules
fig1_with_sd.pdf: fig1.py
	$(PYTHON) fig1.py

fig2.pdf: fig2.py
	$(PYTHON) fig2.py

fig3_replicated_style.pdf: fig3.py
	$(PYTHON) fig3.py

# Figure cropping rules
fig1_with_sd-crop.pdf: fig1_with_sd.pdf
	pdfcrop fig1_with_sd.pdf fig1_with_sd-crop.pdf

fig2-crop.pdf: fig2.pdf
	pdfcrop fig2.pdf fig2-crop.pdf

fig3_replicated_style-crop.pdf: fig3_replicated_style.pdf
	pdfcrop fig3_replicated_style.pdf fig3_replicated_style-crop.pdf

# Convenience targets
figures: $(GENERATED_FIGURES)
cropped-figures: $(CROPPED_FIGURES)

$(DOCUMENT).toc: $(DOCUMENT).tex $(CROPPED_FIGURES)
	$(ENGINE) $(DOCUMENT).tex

ifeq ($(ENGINE), pdflatex)
#--------------------------------------------------
# pdflatex
#--------------------------------------------------
$(DOCUMENT).pdf: $(DOCUMENT).toc
	bibtex $(DOCUMENT)
	$(ENGINE) $(DOCUMENT).tex
	$(ENGINE) $(DOCUMENT).tex
else
#--------------------------------------------------
# latex
#--------------------------------------------------
$(DOCUMENT).dvi: $(DOCUMENT).toc
	bibtex $(DOCUMENT)
	$(ENGINE) $(DOCUMENT).tex
	$(ENGINE) $(DOCUMENT).tex
$(DOCUMENT).ps: $(DOCUMENT).dvi
	dvips -t letter -Ppdf -G0 -o $@ $<
$(DOCUMENT).pdf: $(DOCUMENT).ps
	cat $(DOCUMENT).ps | ps2pdf - > $(DOCUMENT).pdf
endif

all: $(DOCUMENT).pdf
clean:
	rm -rf $(DOCUMENT).aux $(DOCUMENT).log $(DOCUMENT).toc \
	 $(DOCUMENT).fls $(DOCUMENT).out \
     $(DOCUMENT).bbl $(DOCUMENT).blg $(DOCUMENT).pdf \
     $(DOCUMENT).ps $(DOCUMENT).dvi $(DOCUMENT).synctex.gz

clean-figures:
	rm -rf $(GENERATED_FIGURES) $(CROPPED_FIGURES)

clean-all: clean clean-figures

open:
	open $(DOCUMENT).pdf

# Help target
help:
	@echo "Available targets:"
	@echo "  all              - Build the complete document (default)"
	@echo "  $(DOCUMENT).pdf  - Build the PDF document"
	@echo "  figures          - Generate all figures from Python scripts"
	@echo "  cropped-figures  - Generate all cropped figures"
	@echo "  clean            - Clean LaTeX output files"
	@echo "  clean-figures    - Clean generated figure files"
	@echo "  clean-all        - Clean everything"
	@echo "  open             - Open the generated PDF"
	@echo "  help             - Show this help message"

.PHONY: all clean clean-figures clean-all open figures cropped-figures help
