# import pyhtml as ph

# t = ph.html(
#     ph.head(
#         ph.title('Hello World!')
#     ),
#     ph.body(
#         ph.h1('Hello World!'),
#         ph.div('This is some text'),
#         ph.div(ph.a('This is a link', href='https://www.google.com')),
#         ph.p('This is a paragraph'),
#     )
# )

# print(t.render())


from jinja2 import Template

# t = Template('$name is the $job of $company')
# s = t.substitute(name='Tim Cook' , job = 'CEO', company = 'Apple')
# print(s)

# t = Template("Hello {{something}}!")
# t = Template("I love these numbers {% for i in range(5) %}{{i}} {% endfor %}")
# print(t.render(something="World"))

Data = [
    {"year" : 2004, "School": "Chinmaya Vidyalaya", "name": "Shubham"},
    {"year" : 2005, "School": "Chinmaya Vidyalaya", "name": "Shubham"},
    {"year" : 2006, "School": "Chinmaya Vidyalaya", "name": "Shubham"},
    {"year" : 2007, "School": "Chinmaya Vidyalaya", "name": "Shubham"},
    {"year" : 2008, "School": "Chinmaya Vidyalaya", "name": "Shubham"},
    {"year" : 2009, "School": "Chinmaya Vidyalaya", "name": "Shubham"},
    {"year" : 2010, "School": "Chinmaya Vidyalaya", "name": "Shubham"},
    {"year" : 2011, "School": "Chinmaya Vidyalaya", "name": "Shubham"},
]

def main():
    #Read the template file content to a variable
    File  = open("template.html.jinja2", "r")
    t = File.read()
    File.close()
    #Render the template using Jinja2 with the data
    template = Template(t)
    content = template.render(Data=Data)

    #Save the rendered content to a new HTML document
    newFile = open("index.html", "w")
    newFile.write(content)
    newFile.close()
    print("File created successfully")

if __name__ == "__main__":
    main()