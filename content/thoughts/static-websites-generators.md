Title: Static websites generators
Date: 2020-07-30
Tags: Website generator, Pelican, Jekyll, m.css

Recently, I have been thinking about how to organize the things I've
been doing over the last years. I happened to post a little article on
[my blog][1] from time to time, but I feel that this format becomes a
bit messy as time goes by, and that it doesn't fit well for all kind
of content. So time to think about how to improve the situation.

Tools available
---------------

Since 2013, I have been using [Pelican][2] to generate static HTML
pages from text files using the [Markdown][3] syntax. And after
looking around at what others are doing, I still very much like this
idea. All the computation required to generate the HTML documents
interpreted by our browsers is actually performed only once, during
the site/blog generation phase (and not each time a user is requesting
a page). The static files can then be uploaded anywhere, and be served
without wasting precious computing power and energy. [Vladimír Vondruš
explains a similar point of view][4] quite well, [Joanna Rutkowska][5]
as well.

I like writing (and reading) text files with [my favorite
editor][6]. And these last years, a few text formats and tools have
appeared, allowing the translation of 'easy-to-read, easy-to-write
plain text' files to HTML. [Some people][4] prefer
[reStructuredText][7], I have a (visual) preference for [Markdown][3],
though both are very good fits for the purpose of writing content for
websites.

Regarding the generation of the website/blog, a lot of tools are
available in the wild, like [Jekyll][8], [Pelican][2] and [Hugo][9],
respectively written in Ruby, Python and Go. I haven't seen any unique
feature in these tools, so any of them should work for our use
case. Well, there are some little differences though: Jekyll has a
larger community, as it seems to be the most popular static blog
generator. That is a first reason to not use Jekyll ; ). Also I'm more
familiar with Python, which naturally leads me towards Pelican. A lot
of [themes are available for Pelican][10] as well as for the other
sites generators. The choice of the theme may also influence the
choice of the tool.

Website versus Blog
-------------------

As part of the current reflection was the idea of improving the
organization of my things. I like the idea of being able to structure
my content using folders and sub-folders, like most websites are
structured, rather than a pure blog-like chronological setup. However,
most of the tools for generating static pages are primarily targeting
blogs. Jekyll documents the ability to [organize pages into
sub-folders][12] out of the box, while Pelican seems to provide that
feature through (currently not so well documented) [customization of
its configuration file][13]. That said, [Pelican exposes a notion of
category][15], that can be used to organize blog articles; filesystem
folders can be used to represent this organization. There's also the
[notion of pages][16] for non-temporal content. So by default (i.e
without customization), Pelican allows 1-level folders for articles,
plus direct access to 'special' pages. These features alone probably
cover most of my needs for the near future.

Eventually, I discovered [Vladimír Vondruš m.css Pelican
theme][11]. It has a clean and simple look and feel, is well
documented and can be extensively customized. The author uses it to
generate [his own websites][14]. This 'theme' kind of transforms
Pelican into a generic website generator, at the cost of [crafting
Pelican's configuration file][17]. I'm wondering to what extent this
customization could be simplified, by adding a better support for
sub-folders into Pelican. Anyway, [Pelican][2] + [m.css][18] is the
perfect match for my use case for the foreseeable future.

Github pages
------------

A word on [GitHub Pages][19], which is a free service from Github,
allowing to publish one static website per account; it uses Jekyll
under the hood. That is a decent place to start, but I don't really
like the idea of being too tied with a commercial organization and
provide more personal data to a [web giant][20]. Besides, this limits
the choice of the tools one can use for their personal blog or
website.

I'll rather move towards the use of commodity services, that I'll be
able to change at any moment if one of the service providers is down
or changes its policy. Two services are actually required:

* Git repository (could be [gitlab][21], [bitbucket][22],
  [github][23], or a privately hosted ssh based repository), supposing
  one would use a git repository to store their content;
* Web host (Any basic web hosting service would do).



[1]: http://www.florentflament.com/blog
[2]: https://blog.getpelican.com/
[3]: https://daringfireball.net/projects/markdown/
[4]: https://mcss.mosra.cz/why/
[5]: https://blog.invisiblethings.org/2015/02/09/my-new-git-based-blog.html
[6]: https://www.gnu.org/software/emacs/
[7]: https://docutils.sourceforge.io/rst.html
[8]: https://jekyllrb.com/
[9]: https://gohugo.io/
[10]: http://pelicanthemes.com/
[11]: https://mcss.mosra.cz/themes/pelican/
[12]: https://jekyllrb.com/docs/pages/
[13]: https://github.com/getpelican/pelican/issues/1065
[14]: https://magnum.graphics/
[15]: https://docs.getpelican.com/en/stable/content.html#file-metadata
[16]: https://docs.getpelican.com/en/stable/content.html#pages
[17]: https://github.com/mosra/m.css/blob/master/site/pelicanconf.py
[18]: https://mcss.mosra.cz
[19]: https://pages.github.com/
[20]: https://blogs.microsoft.com/blog/2018/10/26/microsoft-completes-github-acquisition/
[21]: https://about.gitlab.com/
[22]: https://bitbucket.org/
[23]: https://github.com/
