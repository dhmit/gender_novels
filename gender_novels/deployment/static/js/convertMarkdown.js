window.onload = () => {
    /*
    If there were multiple bodies that required "variable" content
    from within local markdown files, this could be converted into a
    foreach loop or something similar
     */
  convertMarkdown("overview", "gender_novels_overview");
};

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
