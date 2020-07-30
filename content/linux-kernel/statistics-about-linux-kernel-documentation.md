Title: A couple of statistics about Linux kernel documentation
Date: 2017-03-04
Tags: Linux, Kernel, Documentation

There is a whole lot of files in the `Documentation` directory of the
[Linux kernel source][1]. Is it possible for a single person to read
the whole documentation ? Let's have a look at what's inside it.

    $ pwd
    /home/florent/src/linux/linux-4.10/Documentation

    $ find . -type f | wc -l
    5118

There are 5118 files in the Documentation directory

    $ wc  $(find . -type f) | tail -1
      661911  3175886 24210712 total

These files account for roughly 3.200.000 words spread among 660.000
lines. With a [typical novel's size][2] of 70.000 words, the Linux
documentation is equivalent to roughly 46 such novels. So the answer
is yes, it is possible to read the whole Linux documentation (though
it may take some time).

    $ find . -type f | awk -F. {'print $3'} | sort | uniq -c | sort -n | tail -5
         24 tmpl
         30 svg
         650 rst
         703
         3565 txt

Just to have an idea of the most common files' extensions. Mostly
`.txt` files, plus some extensionless and `.rst` files.

Let's consider the 3 main topics as documented in the [`index.rst`
file][4]:

    $ wc admin-guide/* | tail -1
     14131  73455 517546 total

73.000 words (1 novel) for the 'User-oriented documentation'.

    $ wc process/* dev-tools/* doc-guide/* | tail -1
     11899  72020 487333 total

72.000 words (1 novel) for the 'Introduction to kernel development'.

    $ wc $(find driver-api/ core-api/ media/ gpu/ security/ sound/ crypto/ -type f) | tail -1
     132770  516405 4740930 total

520.000 word (Roughly [equilvalent to reading 'The Lord of the
Rings'][3]) for the 'Kernel API documentation'.

[1]: https://github.com/torvalds/linux
[2]: https://en.wikipedia.org/wiki/Word_count
[3]: https://electricliterature.com/infographic-word-counts-of-famous-books-161f025a6b09
[4]: https://raw.githubusercontent.com/torvalds/linux/master/Documentation/index.rst
