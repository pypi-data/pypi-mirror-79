# PyCube Microservice Framework

## Introduction
PyCube is a framework for building the microservice which contains 3 layers, **(RegularIO, Module, Core)**. PyCube forms a pyramid structure that build from the bottom level. 

![PyCube layout](https://p9vohq.by.files.1drv.com/y4mdMoG4APIRCNX_PAwKUG7W7E-bKx72H2jbJty9VdQc7MlXEAxpIce1NHXwRAhdq2HXAaD19neG29UXTQ2M65nUOjqABPhq1hPXTSxf-ls3cFm_UTfJYuzD2K5AzLYtLw0a_s1uTgPS2KQULxk8h5YQTbmBikCBbgd4K-f0cIU4oTlufVKsp2f9_iOlqPUMyG7veNdyrNTVrsFnIHSRM1HcQ/pycube-layout.png?psid=1)

## Components
#### RegularIO  
> Serve one purpose and do it well !! 👾
<p align="center">
<img 
width="300" height="auto" src="https://qnvohq.by.files.1drv.com/y4mrmxPMRFSxqKrSw2w2Ut1O45DHJLSoRWVRuF9TofVJW6dfiHg2X3wqXsVN5xgZwBXaMNf_yamWteOXF_HKltAcShAQ6wcwBwioPNbycP7UkdS58WihvImI4b1M8_LFu_OHeElNG-C1v5NWtbqOXw19F4BcyK-51KE-dSPaTUbxNGVRRJs0-lpXuZHPQ5Ji3T9ROkQdCFIzd34CwANdy08BA/regulario-layout.png?psid=1">
</p>

#### Lifecycle
<img 
width="100%" 
height="auto" src="https://qdvohq.by.files.1drv.com/y4pL7lmUkmw8R6nTKn_e54eir2sdtVu7mptsqMxng7VBHET48_a7O4b6sxcB-5CLDIiZynWQEqKbWsRfrCBjGh0XOkfVuu7GZV3LpNZx5kbdNuuCcNuyntyzyftuo7RlvHYso_I7JpSpZ-YoJvQSRaVfe4SMZGEBACQX1JcaTmXRdyIWkc_06iC0sSredn6H1XZ4Hqn7byU6FLXq_dYaU6rQoBlCok4E3HwEiSbD3tSXPo/regulario-flow.png?psid=1">

RegularIO class can be fully customized by inheritance.
Call Seq|Method|Arguments|Description
|--|--|--|--|
|1|call_params_transformer|(self, *args, **kwargs)|Call **params_transformer**.
|2|params_transformer|(self, *args, **kwargs)|Handling params transformation, **return args** by default.
|3|call_request|(self, params,**kwargs)|Call **request_handler**.
|4|request_handler|(self, params,**kwargs)|Perform actions at request stage, **pass** by default.
|5|call_process|(self, params,**kwargs)|Call **process_handler**.
|6|process_handler|(self, params,**kwargs)|Perform actions at process stage, **pass** by default.
|7|call_response|(self, params,**kwargs)|Call **response_handler**.
|8|response_handler|(self, params,**kwargs)|Perform actions at response stage, **pass** by default.

```python
from datetime import datetime
from pycube.regulario import RegularIO

class Sum(RegularIO):
	def request_handler(self, params, **kwargs):
		# The return values will be set to kwargs['__request__']
		return {"acceptedDatetime": datetime.utcnow().isoformat()}
		
	def process_handler(self, params, **kwargs):
		# The return values will be set to kwargs['__process__']
		return {"processedDatetime": datetime.utcnow().isoformat()}

	def response_handler(self, params, **kwargs):
		'''
		The content of kwargs
		{
			'__request__': {
				'acceptedDatetime': '2020-09-13T03:50:59.297970'
			}, 
			'__process__': {
				'processedDatetime': '2020-09-13T03:50:59.298233'
			}
		}
		'''		
		return params[0] + params[1]

# Create sum instance 
s = Sum()
result = s.request(1, 2)
print(result) # Output 3
``` 
---
#### Module
> Integrate RegularIOs to get something done !! 👩🏻‍🚀🧑🏻‍🚀👨🏻‍🚀
```python
from pycube.module import Module

class MathModule(Module):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		'''
			An instance method will be added to the module 
			automatically with the class name in lower case 
			by default.
		'''
		self.add_io(Sum()) \		
			.add_io(Square()) \
			.add_io(SquareRoot(name="sqrt")) # Or specifying a name

	def pythagorean_theorem(self, a, b):
		return  self.squareroot(
			self.sum(
				self.square(a),
				self.square(b)
			)
		)
```
---
#### Core
> Handle the request from the real world !! 🚀



# Files

StackEdit stores your files in your browser, which means all your files are automatically saved locally and are accessible **offline!**

## Create files and folders

The file explorer is accessible using the button in left corner of the navigation bar. You can create a new file by clicking the **New file** button in the file explorer. You can also create folders by clicking the **New folder** button.

## Switch to another file

All your files and folders are presented as a tree in the file explorer. You can switch from one to another by clicking a file in the tree.

## Rename a file

You can rename the current file by clicking the file name in the navigation bar or by clicking the **Rename** button in the file explorer.

## Delete a file

You can delete the current file by clicking the **Remove** button in the file explorer. The file will be moved into the **Trash** folder and automatically deleted after 7 days of inactivity.

## Export a file

You can export the current file by clicking **Export to disk** in the menu. You can choose to export the file as plain Markdown, as HTML using a Handlebars template or as a PDF.


# Synchronization

Synchronization is one of the biggest features of StackEdit. It enables you to synchronize any file in your workspace with other files stored in your **Google Drive**, your **Dropbox** and your **GitHub** accounts. This allows you to keep writing on other devices, collaborate with people you share the file with, integrate easily into your workflow... The synchronization mechanism takes place every minute in the background, downloading, merging, and uploading file modifications.

There are two types of synchronization and they can complement each other:

- The workspace synchronization will sync all your files, folders and settings automatically. This will allow you to fetch your workspace on any other device.
	> To start syncing your workspace, just sign in with Google in the menu.

- The file synchronization will keep one file of the workspace synced with one or multiple files in **Google Drive**, **Dropbox** or **GitHub**.
	> Before starting to sync files, you must link an account in the **Synchronize** sub-menu.

## Open a file

You can open a file from **Google Drive**, **Dropbox** or **GitHub** by opening the **Synchronize** sub-menu and clicking **Open from**. Once opened in the workspace, any modification in the file will be automatically synced.

## Save a file

You can save any file of the workspace to **Google Drive**, **Dropbox** or **GitHub** by opening the **Synchronize** sub-menu and clicking **Save on**. Even if a file in the workspace is already synced, you can save it to another location. StackEdit can sync one file with multiple locations and accounts.

## Synchronize a file

Once your file is linked to a synchronized location, StackEdit will periodically synchronize it by downloading/uploading any modification. A merge will be performed if necessary and conflicts will be resolved.

If you just have modified your file and you want to force syncing, click the **Synchronize now** button in the navigation bar.

> **Note:** The **Synchronize now** button is disabled if you have no file to synchronize.

## Manage file synchronization

Since one file can be synced with multiple locations, you can list and manage synchronized locations by clicking **File synchronization** in the **Synchronize** sub-menu. This allows you to list and remove synchronized locations that are linked to your file.


# Publication

Publishing in StackEdit makes it simple for you to publish online your files. Once you're happy with a file, you can publish it to different hosting platforms like **Blogger**, **Dropbox**, **Gist**, **GitHub**, **Google Drive**, **WordPress** and **Zendesk**. With [Handlebars templates](http://handlebarsjs.com/), you have full control over what you export.

> Before starting to publish, you must link an account in the **Publish** sub-menu.

## Publish a File

You can publish your file by opening the **Publish** sub-menu and by clicking **Publish to**. For some locations, you can choose between the following formats:

- Markdown: publish the Markdown text on a website that can interpret it (**GitHub** for instance),
- HTML: publish the file converted to HTML via a Handlebars template (on a blog for example).

## Update a publication

After publishing, StackEdit keeps your file linked to that publication which makes it easy for you to re-publish it. Once you have modified your file and you want to update your publication, click on the **Publish now** button in the navigation bar.

> **Note:** The **Publish now** button is disabled if your file has not been published yet.

## Manage file publication

Since one file can be published to multiple locations, you can list and manage publish locations by clicking **File publication** in the **Publish** sub-menu. This allows you to list and remove publication locations that are linked to your file.


# Markdown extensions

StackEdit extends the standard Markdown syntax by adding extra **Markdown extensions**, providing you with some nice features.

> **ProTip:** You can disable any **Markdown extension** in the **File properties** dialog.


## SmartyPants

SmartyPants converts ASCII punctuation characters into "smart" typographic punctuation HTML entities. For example:

|                |ASCII                          |HTML                         |
|----------------|-------------------------------|-----------------------------|
|Single backticks|`'Isn't this fun?'`            |'Isn't this fun?'            |
|Quotes          |`"Isn't this fun?"`            |"Isn't this fun?"            |
|Dashes          |`-- is en-dash, --- is em-dash`|-- is en-dash, --- is em-dash|


## KaTeX

You can render LaTeX mathematical expressions using [KaTeX](https://khan.github.io/KaTeX/):

The *Gamma function* satisfying $\Gamma(n) = (n-1)!\quad\forall n\in\mathbb N$ is via the Euler integral

$$
\Gamma(z) = \int_0^\infty t^{z-1}e^{-t}dt\,.
$$

> You can find more information about **LaTeX** mathematical expressions [here](http://meta.math.stackexchange.com/questions/5020/mathjax-basic-tutorial-and-quick-reference).


## UML diagrams

You can render UML diagrams using [Mermaid](https://mermaidjs.github.io/). For example, this will produce a sequence diagram:

```mermaid
sequenceDiagram
Alice ->> Bob: Hello Bob, how are you?
Bob-->>John: How about you John?
Bob--x Alice: I am good thanks!
Bob-x John: I am good thanks!
Note right of John: Bob thinks a long<br/>long time, so long<br/>that the text does<br/>not fit on a row.

Bob-->Alice: Checking with John...
Alice->John: Yes... John, how are you?
```

And this will produce a flow chart:

```mermaid
graph LR
A[Square Rect] -- Link text --> B((Circle))
A --> C(Round Rect)
B --> D{Rhombus}
C --> D
```