.SUFFIXES: .m4 .html
#
M4C     = m4 -P -I$(HOME)/public_html
.m4.html:
	rm -f $*.html
	$(M4C) $<  > $*.html

all: index.html

# 
#   $Log: Makefile,v $
#   Revision 1.1  1999/09/14 20:23:33  noonan
#   Initial revision
#
# 
