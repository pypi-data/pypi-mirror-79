def text_summarizer(raw_docx):
    """ usage: text_summarizer(yourtext) """
    raw_text = raw_docx
    docx = TextFrame(raw_text)
    stopwords = list(STOPWORDS)
    # Build Word Frequency # word.text is tokenization in spacy
    word_frequencies = {}  
    for word in docx.text.split(''):  
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1


    maximum_frequncy = max(word_frequencies.values())

    for word in word_frequencies.keys():  
        word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)
    # Sentence Tokens
    sentence_list = [ sentence for sentence in docx.sent_tokens() ]

    #Calculate Sentence Scores
    sentence_scores = {}  
    for sent in sentence_list:  
        for word in sent:
            if word.lower() in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word.lower()]
                    else:
                        sentence_scores[sent] += word_frequencies[word.lower()]

    # Find N Largest and Join Sentences
    summarized_sentences = nlargest(7, sentence_scores, key=sentence_scores.get)
    final_sentences = [ w for w in summarized_sentences ]
    summary = ' '.join(final_sentences)
    return summary