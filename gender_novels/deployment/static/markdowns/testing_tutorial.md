# Markdown to HTML tutorial

This tutorial should help you to convert your markdown file into HTML and see the 
result on the website

### Step 1. Put your files in the correct location
* Place the desired markdown file in the deployment/static/markdowns directory.

* If you reference any images within your markdown make sure to place them inside of the 
deployment/static/markdowns/images directory.

Note: Don't forget to change the image source location inside of your markdown file to its new 
location in the deployment/static/markdowns/images directory. The new reference for your image 
should 
be something like 
```html
![](/static/markdowns/images/my_image.png "my_image description")
```
## Step 2. Add your filename to the markdown conversion script
* Inside of convertMarkdown.js modify the variable declaration for content_dict["test-page"] to 
the filename of your markdown. That variable declaration should now look something like
```javascript
content_dict["test-page"] = my_markdown
```
* Note: Make sure you don't include .md, just the filename is neccessary

## Step 3. Running the site
* Simply go to deployment/app.py and run the file. Your default browser will probably 
automatically open the webpage but if it doesn't, don't despair. In the terminal there will be a 
link that says
```text
Running on http://127.0.0.1:8021/ (Press CTRL+C to quit)
```
* Just click the link and you should be on a running webpage

## Step 4. That's it! You're done
* Go to the "Test Page" tab of the website and you should see your 
markdown there converted to HTML. Nice work!

### SLACK ME WITH QUESTIONS - ISAAC REDLON
