# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR1     = ../admin-ms/docs/source
BUILDDIR1      = build/credentials
SOURCEDIR2     = ../codes-ms/docs/source
BUILDDIR2      = build/codes
SOURCEDIR3     = ../sensor-ms/docs/source
BUILDDIR3      = build/sensors
SOURCEDIR4     = ../storage-ms/docs/source
BUILDDIR4      = build/users


# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR1)" "$(BUILDDIR1)" $(SPHINXOPTS) $(O)
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR2)" "$(BUILDDIR2)" $(SPHINXOPTS) $(O)
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR3)" "$(BUILDDIR3)" $(SPHINXOPTS) $(O)
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR4)" "$(BUILDDIR4)" $(SPHINXOPTS) $(O)
