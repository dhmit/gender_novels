**Project Groups and Roles**

_Specific groups and roles were assigned in order to
gain specialized knowledge that the team will need.
Nonetheless, all members in any role across all groups were
responsible for the success of the project.  All members were
expected to contribute code, prose, and knowledge
(technical, humanistic, and hybrid) to the project._

**Data Group** (8 members)

_Created tools for acquiring and creating corpora (collections) of novels.  Ensures the quality of data and their quantity.  Prepares metadata.  Develops Object-Oriented Models for Corpus and Novel classes.  Analyzes trends across large data collections._

Copyright and License Specialist

Metadata Specialist

Web Acquisition Specialist

Data Sanitization Engineer

Corpus Specialist (Gutenberg)

Corpus Specialist (HathiTrust)

Corpus Scout

Statistics Specialist (Data)

Visualization Specialist (Data)



**Analysis Group** (9 members)

_Created tools for low-level analysis of individual novels,
sections, sentences, and words.  Read
the literature of relevant humanities fields
in order to ask interesting and appropriate questions
and work at high levels of intellectual sophistication._

Visualization Specialist (Analysis)

Regex Specialist

Grammar Specialist

Statistics Specialist

Gender Studies Specialist

English Literature Specialist

History and Chronology Specialist

Digital Humanities Literature Specialist

Analysis Project Manager

**Deployment** (6 members)

_Ensured that knowledge from the group was disseminated
publicly by developing web interfaces, high-reliability code,
effective and beautiful visualizations,
and clear and interesting prose._

Quality Assurance Specialist

Visualization Specialist (Deployment)

Writer/Editor

Web Backend Developer

Web Frontend Developer

Javascript Developer

Development Operator (DevOps)


**Brief Role Descriptions**

Each description below gives some idea of the responsibilities
for the person in that role, in addition to responsibilities
that were shared throughout the lab.
It was each member&#39;s responsibility over the course of the
term to learn more about what they might contribute in their role
given their talents and interests and (where the role exists
outside the lab) which might be expected of them in this role
in academia, the non-profit world, or industry.

**Data Group**

**Copyright and License Specialist**

Understands the commonly used copyright and licensing formats.
Knows the copyright status of all of the novels and novel corpora
that we use. Working with Corpus Specialists and Corpus Scout,
assures that our scraped data is compliant with the requirements
defined by our sources (Gutenberg, HathiTrust etc.).
Learns the terms of service associated with digital corpora,
working closely with the Web Acquisition Specialist to shape
best practices.

**Metadata Specialist**

Coordinates the collection of metadata across our corpora.
Selects and standardizes metadata fields (e.g. place of publication,
date, author gender and nationality) to collect and analyze
for the project. Works with the Web Acquisition Specialist to
acquire missing information from Wikipedia or library APIs.
Works with the analysis team on the code to access novel metadata.


**Web Acquisition Specialist**

Uses web scraping tools to gather the corpus used in the project.
Knows how to extract data from websites and APIs with Python libraries
like Requests, Beautiful Soup, and Scrapy. Understands the commonly
used data types (json, xml, html, txt) to store texts and metadata.
Develops knowledge of the potential digital corpora available to use
and what data challenges each may present. Learns and implements web
scraping best practices.

**Data Sanitization Engineer**

Combines data from multiple sources and produces a clean and
consistent corpus for the team to use moving forward. Develops
tools to temporarily remove licensing boilerplate and introductory
information like author biographies or table of contents.
Considers how to handle outlier data and missing values.
Ensures that data is being presented in the most helpful way
and manipulate data until it is ready to be used by team members.

**Corpus Specialist** (Gutenberg)

Has a deep understanding of the holdings in the Project Gutenberg
online corpus. Coordinates with other Corpus Specialist and
Corpus Scout on building unified interfaces. Writes code aiding
the Web Acquisition Specialist for accessing text and metadata
from the corpus. Researches and selects holdings for use in our
project. Is responsible for selecting an initial corpus of 100
novels to use in our analysis. Ensures that Gutenberg access
restrictions are followed by building an &quot;rsync mirror&quot;
of the collection.

**Corpus Specialist** (HathiTrust)

Has a deep understanding of the holdings in the HathiTrust
Digital Library. Coordinates with other Corpus Specialist and
Corpus Scout on building unified interfaces.
Writes code aiding the Web Acquisition Specialist for
accessing text and metadata from the corpus. Researches and
selects holdings for use in our project. Creates guides for the
HathiTrust web API. Is responsible for the creation of a large
scale dataset of about 10,000 novels, though at lower quality than
the Gutenberg corpus.  Ensures that HathiTrust access restrictions
are followed. (Up to two members may hold this position.)

**Corpus Scout** (Scholarly Literature)

Actively searches for additional corpora to use in our analysis.
Coordinates with HathiTrust and Gutenberg Corpus Specialists on
building unified interfaces. Learns about the scholarly
literature in the field, especially related
to &quot;Distant Reading&quot; in the digital humanities but
also in the humanities at large. Uses this knowledge to inform
the thinking behind the project and consider ways to build on
past work and considers best practices in citing others.
Works with Copyright and License specialist to determine legal
implications of using corpora.

**Statistics Specialist** (Data)

Understands statistics and how they apply to corpora and collections.
Tests results for statistical significance and reproducibility.
Learns how to apply t-tests and interpret p-values and their pitfalls.
Creates and adapts code for statistical significance in pure
Python and, if possible, with numpy and scipy.
Works with the visualization specialists to show
statistical significance visually.

**Visualization Specialist** (Data)

Uses matplotlib or other appropriate tools to create
visualizations from results from the data group.
Works closely with Deployment Visualization Specialist
to ensure a beautiful and consistent style for results.
Studies results from data group for visualization possibilities.
Creates &quot;nutritional labels&quot; for our data that summarize
the date, country, or author gender breakdown of the
novels in our dataset.  Returns visualizations to members
of the group to aid in writing verbal descriptions of results.

**Analysis Group**

**Visualization Specialist** (Analysis)

Uses matplotlib or other appropriate tools to create
visualizations from results from the analysis group.
Works closely with Deployment Visualization Specialist to
ensure a beautiful and consistent style for results.
Studies results from analysis group for visualization possibilities.
Returns visualizations to members of the group to aid in
writing verbal descriptions of results.
Often codes in Jupyter notebook for immediate presentation.

**Regex Specialist**

Creates analysis tools using regular expressions for efficient
and effective studies of textual data.
Collaborates with the data group to share ideas and best practices.
Understands data structures to store interesting findings.
Asks questions about direct vs. indirect speech.
Plays a major role in tokenization and word stemming.
Develops interesting questions and implements solutions
together with the Gender, Literature, History, and DH Literature
specialists.

**Grammar Specialist**

Understands grammar from both linguistic and computational
perspectives.  Develops questions and solutions involving
grammar and parts of speech.  Reads, understands and begins to
implement analysis methods involving natural language processing.
Eventually becomes lab expert on NLTK (Natural Language Toolkit)
and begins to teach others about its use.

**Statistics Specialist** (Analysis)

Understands statistics and how they apply to analysis and results.
Tests results for statistical significance and reproducibility.
Learns how to apply t-tests and interpret p-values and their pitfalls.
Creates and adapts code for statistical significance in pure
Python and, if possible, with numpy and scipy.
Works with the visualization specialists to show statistical
significance visually.

**Gender Studies Specialist**

Reads relevant literature from Women and Gender Studies and
contacts at least one relevant faculty member from the department
to understand the questions and language that gender studies
professionals use in discussing gender in literature.
Translates questions into code that can be applied to individual
novels and the corpus.  Develops research questions that can be
answered computationally by analyzing individual novels or
full corpora. Ensures that all code and text fits within language
and norms established by gender studies (i.e. makes sure that
we don&#39;t embarrass ourselves through factual errors or by
using the wrong terminology).  Closely analyzes all our findings
for results that are particularly relevant to gender studies.

**English Literature Specialist**

Reads relevant literature from English Literature and contacts at
least one relevant faculty member from the Literature department
to understand the questions and language that literature professionals
use in discussing gender in literature.  Develops research
questions that can be answered computationally by analyzing
individual novels or full corpora and writes code to answer them.
Ensures that all code and text fits within language and norms
established by English literature (i.e. makes sure that we don&#39;t
embarrass ourselves through factual errors or using the wrong
terminology). Closely analyzes all our findings for results that
are particularly relevant to gender studies.

**History and Chronology Specialist**

Reads relevant literature from History, particularly historical
studies of the 19th century to understand the questions and
language that historians use in studying the period.
Develops research questions that can be answered computationally
by analyzing individual novels or full corpora and writes code
to answer them. Ensures that all code and text fits within
language and norms established by historians (i.e. makes sure
that we don&#39;t embarrass ourselves through making factual
errors or by using the wrong terminology). Closely analyzes
all our findings for results that are particularly relevant
to historians.

**Digital Humanities Literature Specialist**

Reads relevant literature from Digital Humanities to
understand the questions and language that DH professionals
might use in discussing gender in novels.
Develops research questions that can be answered
computationally by analyzing individual novels or
full corpora and writes code to answer them. Ensures
that all code and text fits within language and norms
established by the Digital Humanities (i.e. makes sure that
we don&#39;t embarrass ourselves through factual errors or
by using the wrong terminology). Closely analyzes all our
findings for results that are particularly relevant to the
Digital Humanities.

**Analysis Project Manager**

Oversees the execution of the analysis project plans,
maintaining communication across Analysis team members
and the Data and Deployment teams to gather and implement
specific requirements. Mentors other students and provides
feedback to iterate on the project effectively.
Works to determine best cadence of the administration of the
development workflow through sprints, ticket tracking, etc.


**Deployment Group**

**Quality Assurance Specialist**

Ensures that code and publication quality in the lab, across all groups, never diminishes in quality.  Reviews pull requests to ensure they have proper documentation and tests, aids Development Operator (DevOps) in setting up proper continuous integration / continuous development tools.  Adjusts test suites to changing circumstances.  Is not afraid to (politely) return code and documentation for revision.  Quickly earns Github commit permissions.

**Visualization Specialist** (Deployment)

Designs final visualizations for public presentation using Matplotlib and other visualization tools.  Learns the ins and outs of &quot;the visual display of quantitative information&quot; (reading Edward Tufte&#39;s book of the same name).  Produces beautiful visualizations, eventually learning d3.js to make animated visualizations in collaboration with the Javascript developer.  Works closely with visualization specialists in other groups.

**Writer/Editor**

Writes the first and most important texts for the website and the introduction for the publication.  Manages explanatory texts and documentation and ensures that writing flows smoothly.  Works with Frontend Developer to make sure text is appropriately displayed on website.  Codes tools for updating HTML automatically from documentation and Markdown.  (Up to two members may hold this position)

**Web Backend Developer**

Sets up first initial test servers to run locally by the Deployment team and others using SimpleHTTPServer, then, after learning Django, sets up a more robust server for later release.  Works with the FrontEnd developer to ensure that integration from front to back end is smooth, and with DevOps to help with continuous deployment.  Is responsible with staff and DevOps for the final deployment of the site online.

**Web Frontend Developer**

Creates the public interface for results and visualizations of the lab.  Develops strong HTML and CSS skills and some basic JavaScript.  Uses Bootstrap to create accessible and responsive (mobile friendly) web design.  Works closely with the Writer/Editor and Visualization Specialist to ensure writeup and results are beautifully displayed.

**JavaScript Developer**

Works on web development through modern JavaScript (ES6, 2017+), learning JavaScript best practices and becoming proficient at various JavaScript frameworks. Aims to make an interactive and accessible website based on UX principles. If time, learns how best to use JavaScript within a Django backend. Works closely with Web Developers, especially Front End, and DevOps to shape a development workflow that serves the needs of the broader team.

**Developer Operator** (DevOps)

Develops continuous integration / development (CI / CICD) tools to facilitate a rapid and stable development cycle.  Learns git (GitHub Desktop GUI, command line, and GitHub website) and is able to help with conflicts and merges.  Investigates PyCharm tools and virtual environments for developer time saving.  Releases pip installations of command line tools.

**Deployment Project Manager**

Oversees the execution of the deployment project plans, maintaining communication across Deployment team members and the Data and Analysis teams to  gather and implement specific requirements. Mentors other students and provides feedback to iterate on the project effectively. Works to determine best cadence of the administration of the development workflow through sprints, ticket tracking, etc.
