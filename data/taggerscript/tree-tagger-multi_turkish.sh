#!/bin/sh

PAR=$1

# Set these paths appropriately

BIN=../TreeTagger/bin
CMD=../TreeTagger/cmd
LIB=../TreeTagger/lib

OPTIONS="-token -lemma -sgml -pt-with-lemma"

#TOKENIZER=${CMD}/tokenize.pl
TOKENIZER=${CMD}/no-tokenize.pl
TAGGER=${BIN}/tree-tagger
ABBR_LIST=${LIB}/german-abbreviations-utf8
#PARFILE=${LIB}/multilitJune21.par
#PARFILE=${LIB}/multilitOct15.par
PARFILE=${LIB}/TurkishAPR10.par
#LEXFILE=${LIB}/german-lexicon-utf8.txt
#LEXFILE=${LIB}/October15.lex
LEXFILE=${LIB}/sancl14.lex
FILTER=${CMD}/filter-german-tags

$TOKENIZER -a $ABBR_LIST $* |
# external lexicon lookup
perl $CMD/lookup.perl $LEXFILE |
# tagging
$TAGGER $OPTIONS $PARFILE  |
# error correction
$FILTER
