from org.jsoup import Jsoup

def clean_question(html):
	"""Removes code tag and its content. Subsequently, it removes html tags"""
	doc = Jsoup.parse(html)
	doc.select("code").empty()
	return doc.text()

class PostParser:
	def __init__(self, answer):
		self.answer = answer
		self.inline = []
		self.block = []
		self.doc = Jsoup.parse(answer)

	def get_code(self):
		""" Returns all code snippets (inline and block) """
		return [c.text() for c in self.doc.select("code")]

	def block_code(self):
		""" Extract code block segments and its description """
		description = None
		for e in self.doc.select("pre>code"):
			if e.parent().previousElementSibling().tagName() == "p":
				description = e.parent().previousElementSibling().text()
			self.block.append({"code": e.text(), "description": description})
		return self.block

	def first_description(self):
		""" Extract code block segments and its description """
		description = ""
		for e in self.doc.select("pre>code"):
			previous = e.parent().previousElementSibling()
			if previous:
				if previous.tagName() == "p":
					description = previous.text()
					return description
		return description

	def inline_code(self):
		""" Extract inline code segments """
		for e in self.doc.select("p>code"):
			self.inline.append({"code": e.text(), "description": e.parent().text()})
		return self.inline



if __name__ == '__main__':
	html = """<p>I am running a Tomcat application, and I need to display some time values.  Unfortunately, the time is coming up an hour off.  I looked into it and discovered that my default TimeZone is being set to:</p>

<pre><code>sun.util.calendar.ZoneInfo[id="GMT-08:00",
    offset=-28800000,dstSavings=0,useDaylight=false,
    transitions=0,lastRule=null]
</code></pre>

<pre><code>completly differen code section
</code></pre>

<p>Rather than the Pacific time zone.  <code>Some Code</code> This is further indicated when I try to print the default time zone's <a href="http://docs.oracle.com/javase/7/docs/api/java/util/TimeZone.html#getDisplayName()" rel="nofollow">display name</a>, and it comes up "GMT-08:00", which seems to indicate to me that it is not correctly set to the US Pacific time zone.  I am running on Ubuntu Hardy Heron, upgraded from Gutsy Gibbon.</p>
	"""

	html = """<p>Just use the appropriate method: <a href="http://docs.oracle.com/javase/8/docs/api/java/lang/String.html#split-java.lang.String-"><code>String#split()</code></a>.</p>

<pre><code>String string = "004-034556";
String[] parts = string.split("-");
String part1 = parts[0]; // 004
String part2 = parts[1]; // 034556
</code></pre>

<p>Note that this takes a <a href="http://docs.oracle.com/javase/8/docs/api/java/util/regex/Pattern.html#sum">regular expression</a>, so remember to escape special characters if necessary, e.g. if you want to split on period <code>.</code> which means "any character" in regex, use either <code>split("\\.")</code> or <code>split(Pattern.quote("."))</code>.</p>

<p>To test beforehand if the string contains a <code>-</code>, just use <a href="http://docs.oracle.com/javase/8/docs/api/java/lang/String.html#contains-java.lang.CharSequence-"><code>String#contains()</code></a>.</p>

<pre><code>if (string.contains("-")) {
    // Split it.
} else {
    throw new IllegalArgumentException("String " + string + " does not contain -");
}
</code></pre>

<p>No, this does not take a regular expression.</p>
"""
	
	p = PostParser(html)
	print p.block_code()
	print p.inline_code()
	print p.get_code()