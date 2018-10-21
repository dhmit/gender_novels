window.onload = () => {
    loadPageContent();
};

function loadPageContent() {
    let content_dict = {};

    content_dict["overview"] = "gender_novels_overview";
    content_dict["copyright"] = "copyright_info";
    content_dict["topic-one"] = "gender_novels_analysis";
    content_dict["testing-tutorial"] = "testing_tutorial";
    content_dict["test-page"] = "test";

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
