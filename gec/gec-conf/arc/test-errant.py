#  20-8-16
import difflib,json,spacy  #['I', '- likes', '+ like', '+ a', 'snowing', '.']
import errant		#https://github.com/chrisjbryant/errant

def docdiff(doc1, doc2):
	if not hasattr(docdiff, 'toksigns'): 
		if not 'nlp' in dir(): nlp=spacy.load('en_core_web_sm')
		d = nlp("^ - + $")
		for t in d : t.tag_ = 'LS'
		setattr(docdiff, 'toksigns', d)
	arr = [ s for s in difflib.ndiff([t.text for t in doc1], [t.text for t in doc2]) if not s.startswith('?')] #['  I', '- love', '+ like', '  you']
	i,j = 0,0
	res = [ docdiff.toksigns[0] ] #['^']
	for s in arr : 
		if s[0] == ' ':
			res.append( doc1[i])
			i+=1
			j+=1
		elif s[0] == '-':
			res.append( docdiff.toksigns[1]) #"-"
			res.append( doc1[i])
			i += 1
		elif s[0] == '+':
			res.append( docdiff.toksigns[2]) #"+")
			res.append( doc2[j])
			j += 1
	res.append(docdiff.toksigns[-1]) # "+ * $"
	return res #['^', It, '-', was, '+', is, '+', a, dog, ., '$']

tok_sign	= lambda t : t.doc == docdiff.toksigns
tok_plus	= lambda t : t.text == '+' and tok_sign(t)
tok_minus	= lambda t : t.text == '-' and tok_sign(t)
tok_start	= lambda t : t.text == '^' and tok_sign(t)
tok_end		= lambda t : t.text == '$' and tok_sign(t)
diff_markdown	= lambda arr: " ".join([ f"~~{t.text}~~" if tok_minus(arr[i-1]) else f"***{t.text}***"  if tok_plus(arr[i-1]) else t.text  for i, t in enumerate(arr) if i > 0 and  not tok_sign(t)  ]) #['English is ~~a~~ ***an*** ~~internationaly~~ ***international*** language which ***has*** ~~becomes~~ ***become*** ~~importantly~~ ***important*** for ***the*** modern world .']

def errant_diff(orig_doc1, cor_doc2):
	if not hasattr(errant_diff, 'annotator'):  
		setattr(errant_diff, 'annotator', errant.load('en', nlp=spacy.load('en_core_web_sm')))
	return errant_diff.annotator.annotate(orig_doc1, cor_doc2)

errant.annotator = errant.load('en', nlp=spacy.load('en_core_web_sm'))
	
if __name__ == '__main__':
	if not 'nlp' in dir(): nlp = spacy.load('en_core_web_sm')
	arr = docdiff( nlp("I like apple."), nlp("I likes an apple."))
	print(arr)
	print(diff_markdown(arr))
	print(errant.annotator.annotate(nlp("I like apple."), nlp("I likes an apple.")))

def test_errant():
	annotator = errant.load('en', nlp=nlp)
	orig = annotator.parse('This are gramamtical sentence .')
	cor = annotator.parse('This is a grammatical sentence .')
	edits = annotator.annotate(orig, cor)
	for e in edits:
		print(e.o_start, e.o_end, e.o_str, e.c_start, e.c_end, e.c_str, e.type) #1 2 are 1 2 is R:VERB:SVA