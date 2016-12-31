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
ABBR_LIST=${LIB}/english-abbreviations
#PARFILE=${LIB}/multilitJune21.par
PARFILE=${LIB}/EnglishAPR28.par
#LEXFILE=${LIB}/german-lexicon-utf8.txt
LEXFILE=${LIB}/englishAPR28.lex
FILTER=${CMD}/filter-german-tags
$TOKENIZER -a $ABBR_LIST $* |
# external lexicon lookup
perl $CMD/lookup.perl $LEXFILE |
# tagging
$TAGGER $OPTIONS $PARFILE  |
# error correction
$FILTER
