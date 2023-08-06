# spaCy-ixaKat

[ixaKat](http://ixa2.si.ehu.es/ixakat/ixa-pipe-dep-eu.php) wrapper for spaCy

## Basic Usage

```py
>>> import spacy_ixakat
>>> nlp=spacy_ixakat.load()
>>> doc=nlp("Euskaldun izatea lan extra bat izatea da.")
>>> for t in doc:
...   print("\t".join([str(t.i+1),t.orth_,t.lemma_,t.pos_,t.tag_,"_",str(0 if t.head==t else t.head.i+1),t.dep_,"_","_" if t.whitespace_ else "SpaceAfter=No"]))
...
1	Euskaldun	euskaldun	PROPN	ADJ	_	2	obl	_	_
2	izatea	izan	VERB	ADI_SIN	_	7	csubj	_	_
3	lan	lan	NOUN	IZE_ARR	_	6	obl	_	_
4	extra	extra	NOUN	ADJ	_	3	nmod	_	_
5	bat	bat	NUM	DET_DZH	_	3	nummod	_	_
6	izatea	izate	VERB	IZE_ARR	_	7	ccomp	_	_
7	da	izan	VERB	ADT	_	0	ROOT	_	SpaceAfter=No
8	.	.	PUNCT	PUNT_PUNT	_	7	punct	_	_
>>> import deplacy
>>> deplacy.render(doc)
Euskaldun PROPN <╗           obl
izatea    VERB  ═╝<══════╗   csubj
lan       NOUN  ═╗═╗<╗   ║   obl
extra     NOUN  <╝ ║ ║   ║   nmod
bat       NUM   <══╝ ║   ║   nummod
izatea    VERB  ═════╝<╗ ║   ccomp
da        VERB  ═══════╝═╝═╗ ROOT
.         PUNCT <══════════╝ punct
```

`spacy_ixakat.load(convUD=True)` loads spaCy Language pipeline for ixaKat. `convUD=False` disables the conversion into Universal Dependencies and forces the pipeline to return `str` of CoNLL.

## Installation for Linux (Debian, Ubuntu, Kali)

```sh
sudo apt update
sudo apt install python3-pip python3-dev default-jre-headless git curl libncursesw5
pip3 install git+https://github.com/KoichiYasuoka/spaCy-ixaKat --user
```

