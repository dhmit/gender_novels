window.onload = () => {
    loadPageContent();
};

function loadPageContent() {
    /*
    content_dict: an object (akin to a Python dictionary) that maps HTML ID strings to markdown
    filename strings

    Result:
    Calls convertMarkdown on each value in content_dict if there is an ID in the HTML document
    of that value's key
     */

    let content_dict = {};

    content_dict["statistical-analysis"] = "statistical_analysis";
    content_dict["statistics-specialist"] = "statistics_specialist";
    content_dict["web-acquisition"] = "web_acquisition";
    content_dict["data-sanitation"] = "data_sanitation";
    content_dict["hathitrust"] = "hathitrust";
    content_dict["team-description"] = "about_team";

    for (let id in content_dict) {
        try {
            convertMarkdown(id, content_dict[id]);
        } catch {
        }
    }
}

function convertMarkdown(id, filename)
{
    /*
    Input:
    id: HTML element id (string)
    filename: markdown filename (string)

    Result:
    Converts the markdown file (filename) into HTML and loads
    the converted HTML into a particular HTML element (id)
     */

    let url = "/static/markdowns/" + filename + ".md";
    let req = new XMLHttpRequest();
    req.open("GET", url, false);
    req.send(null);

    let converter = new Remarkable();
    let html = converter.render(req.responseText);

    document.getElementById(id).innerHTML = html;
}
