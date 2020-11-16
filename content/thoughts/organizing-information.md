Title: Organizing information
Date: 2020-11-16
Tags: information, data, organization

Publishing things (as notes, code, blog posts, videos, ...) is very
powerful, because what has been done at a given point in time is not
lost. We can reuse previous work and build upon it.

Human memory has a short span and is quite inaccurate (we tend to
forget). I often refer to documents I wrote in the past (sometimes
even years earlier). It avoids me to search for the same information I
already searched for, and allows me to build upon what I did
previously (a kind of capitalization on thoughts).


## Organizing documents

Writing things down is a starting point. But a huge amount of data is
useless if we can't find the relevant information. Being able to
search is nice (as Google is promoting with its unsorted massive Gmail
inbox and the ability to search into it), but search results are
rarely exhaustive. If I get a document for some research, I have no
way to know if I found all the relevant documents or not (for
instance, they may contain variants of the keywords I searched for).

There is a limited amount of information that matters to me (at least
that I can process), as well as things I can write during my whole
life (because it takes time). So the volume of text that I can produce
is rather low and should be manageable. I should be able to organize
my content (in folders, with clear names, easy to find, ...). This is
what I recently did with my notes, and I'm impressed how much more
easy to use they are now. Organizing data should be a permanent
process.


## Types of documents

I tend to classify documents into 2 major categories:

* Living documents
* Immutable documents

### Living documents

Living documents are updated (more or less often) so that they keep
being up to date. Some ideas (for instance about the nature of humans)
don't change every day, so an article about this topic stays relevant
for a long period of time. It can be "living" while being updated very
rarely. On the other hand, a todo list needs to be updated more
often. Source code (of a maintained software) falls into this category
as well.

### Immutable documents

Immutable documents are things that never change. For instance, a
piece of art, a press or magazine article, a scientific
publication. They serve as references. Software can also fall into
this category, when it is not maintained anymore. The last version
available (or former identified versions) become an immutable
artifact.

Interestingly, blog posts usually fall into the immutable document
category, because their authors usually don't update them. On the
other hand, personal websites tend to be updated from time to time, so
they fit more in the living documents category.


## Documents structure

Documents need to be well structured, so that the relevant information
can be found quickly. [GNU Manuals][4], especially in the "Info
format", are good examples of well structured information. Organizing
documents hierarchically into sections and subsections makes it much
easier to find relevant information.

That said, throwing thoughts on a paper or in a file allows writing
ideas as they come to mind. They can be structured later. Attempting
to structure ideas too early might lead to some ideas being discarded
because they don't fit the part being written.


## How to store information

I like storing information in plain files on my filesystem. They are
actually easy to share among several computers (via NFS, or
distributed filesystems like cephfs), easy to backup, and more
generally easy to manage (delete, move, copy, ...). Also, plain files
are standard; It's not possible to loose the information because the
software required to read the files is obsolete and can't run on
modern machines. The worst case scenario is proprietary binary
blobs. Also plain files can be versioned into a [version control
system][1], like [git][2], so that we can retrieve previous versions
of the documents.


[1]: https://en.wikipedia.org/wiki/Version_control
[2]: https://en.wikipedia.org/wiki/Git
[4]: https://www.gnu.org/manual/manual.html
