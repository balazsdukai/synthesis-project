*Pro tip: for formatting help you can always check out this README document because it is using the same Markdown syntax as the webpage,
or go to [](http://kramdown.gettalong.org/quickref.html)*

**Directory structure:**

don't mess with:

+ /css

+ Gemfile, Gemfile.lock, _config.yml, feed.xml

sub-pages live in directories and always have at least an `index.md` file which contains the content and optionally other files (e.g. figures), like:

+ 2_methodology

  + index.md
  
  + mobility.png
  
  + ...

### Add figures

the figures are referenced from the `index.md` like this:

```
![mobility](mobility.png)
{: style="text-align: center;"}
```

where `!` tells the rendering engine that this is a link, `[mobility]` is the alternative text that will be displayed if the picture cannot be displayed and `(mobility.png)` is the path to the referenced file

the line `{: style="text-align: center;"}` centers the image on the page

to add a caption you do

```
![](mobility.png)
{: style="text-align: center;"}

*Figure 2: Histogram of mobility ratio of all devices in the Wi-Fi log.*
{: style="color:gray; font-size: 80%; text-align: center;"}
```

### Add hyperlink

in-line, which will look like this:

Delft University of Technology, the [Geomatics Synthesis Project (GSP)](http://www.tudelft.nl/en/study/master-of-science/master-programmes/geomatics/programme/synthesis-project/) takes place.

`[Geomatics Synthesis Project (GSP)](http://www.tudelft.nl/en/study/master-of-science/master-programmes/geomatics/programme/synthesis-project/)`

for separate line you need and new line before and after the link

```
bla bla

![text to display](link)

bla bla
```

if you leave `[]` empty, the hyperlink itself will be printed


### Add link to a sub-page

![Methodology](/2_methodology)

`[Methodology](/2_methodology)`

### Add footnote

in the text you add the reference as `[^1]` then at the bottom you add

`[^1]: whatever`

check out [this](https://raw.githubusercontent.com/balazsdukai/synthesis-project/gh-pages/1_introduction/index.md) for an example

