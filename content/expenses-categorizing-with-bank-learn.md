Title: Expenses categorizing with bank-learn
Date: 2020-08-08
Tags: expenses, categorizing, machine learning, bank, bank-learn, scikit-learn, python

Once a while, I feel the need to analyze my expenses to understand my
own costs structure (and maybe identify overspend). My bank portal
does a rude expenses categorization per account over 3 months, while I
prefer having a global view over an arbitrary long period of time,
like 1 year. Moreover, I prefer avoiding the use of a third party (i.e
fintech) tool to analyze my expenses (private data). [LibreOffice][1]
spreadsheets do a decent job at filtering and aggregating data
visually; one can generate charts as well if necessary. My bank portal
allows extracting accounts transactions in csv format, which can be
imported directly into [LibreOffice][1]. However, these extracts lack
(critical) categorization information (i.e what category each expense
belongs to).

bank-learn
----------

This is where [bank-learn][2] comes into play. Based on
[scikit-learn][4] [Python][3] module, [bank-learn][2] is a tool that
can enrich (and possibly aggregate) bank csv extracts with a
transaction category, based on a training set built either manually or
using the tool. A training set is nothing more that a chunk of csv
extract, with an additional category column that has been specified
manually (arbitrary category names can be used). In order to ease the
process of building the training set, [bank-learn][2] allows to
interactively identify transactions in wrong categories and manually
categorize them to enrich the training set, and eventually obtain a
better categorization.

### Text classifier setup

[bank-learn][2] is basically based on the [scikit-learn Working With
Text Data tutorial][5]. At the core of the tool is a text classifier
[Pipeline][8], composed of:

* a [CountVectorizer][6], to extract numerical features that
  classifiers can use from text strings
* a [MultinomialNB][7] classifier, which is a "Naive Bayes classifier
  for multinomial models"

```
self.__vectorizer = CountVectorizer(
    stop_words=STOP_WORDS,
    token_pattern= '(?u)\\b\\w[a-zA-Z0-9_\\-\\.]+\\b',
    ngram_range=(1,3),
)
self.__text_clf = Pipeline([
    ('vect', self.__vectorizer),
    ('clf', MultinomialNB()),
])
```

The `CountVectorizer` uses a custom `stop_words` list, containing
words appearing often in our bank transactions descriptions, but that
aren't relevant for our classifier to make good decisions (thus
introducing noise from the classifier point of view). These words will
be ignored by our vectorizer, when extracting the features used by the
classifier. The `stop_words` list needs to be customized according to
the country and possibly to the bank as well (depending on the words
it uses to describe its transactions). The tool may work with the
default stop_words list (or without any), but would probably need a
bigger training set than if using a good `stop_word` list.

The `token_pattern` has been customized as well to capture '.' and '-'
characters within words (bank transaction fields often use
abbreviations containing '.' and/or '-' characters, and we don't want
to split these abbreviations into one character words). This is a
[Python re][9] regular expression.

The `nrgam_range=(1,3)` setting allows considering chunks of 1, 2 and
3 words; respectively called unigrams, bigrams and trigrams. This
helps the classifier when successive words of a transaction
description taken together have a meaning that isn't conveyed by the
individual words; for instance a bar named "the little bar" can be
identified by the classifier if it considers trigrams, while "the",
"little" and "bar" words don't allow to discriminate as efficiently as
the trigram.

The classifier itself is a [multinomial Naive Bayes classifier][7],
which is the first one proposed in the [tutorial][5]. It seems to work
pretty well to classify text strings, so I didn't feel the need to
experiment with other classifiers (maybe some day).

### Text classifier usage

Once a scikit-learn classifier has been built (cf previous section),
its usage is straight forward:
    
    self.__text_clf.fit(self.__training_set_x, self.__training_set_y)
    self.__prediction = self.__text_clf.predict(self.__corpus)

The classifier `fit` method, trains it with a training set split into
(uncategorized) transactions `self.__training_set_x` and the
corresponding categories `self.__training_set_y`; both of them are
lists of strings.

Once the classifier trained, its `predict` method takes a list of
(uncategorized) transactions (the transactions that we want to
categorize, and that don't necessarily appear in our training set) and
generates the list of the corresponding categories. It then suffices
to format the data and generate the output csv file, with the
transactions together with their categories.

Results and thoughts
--------------------

With a training set of 270 transactions "manually" categorized using
the tool, it is able to automatically categorize my 1200 transactions
in a fraction of second, without any mistake (that I could see).

That said, I think that such classification could have been achieved
with a roughly equivalent set of basic rules based on strings matching
(i.e if the description contains this substring, put the transaction
into that category). That's actually how I started the implementation
of this tool, then I switched to using [scikit-learn][4] for the fun
of discovering this machine learning kit, and because writing strings
matching rules was boring.


[1]: https://www.libreoffice.org/
[2]: https://github.com/FlorentFlament/bank-learn
[3]: https://www.python.org/
[4]: https://scikit-learn.org/stable/
[5]: https://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html
[6]: https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html
[7]: https://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.MultinomialNB.html
[8]: https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html
[9]: https://docs.python.org/3/library/re.html
