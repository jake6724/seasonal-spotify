from bs4 import BeautifulSoup

# Read the HTML content from the file
with open('sample.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Find the <meta> tag where property equals "og:image"
meta_tag = soup.find('meta', {'property': 'og:image'})

# Extract the 'content' attribute from the meta tag
if meta_tag:
    image_url = meta_tag.get('content')
    print(f'Image URL: {image_url}')
else:
    print('Meta tag with property "og:image" not found.')