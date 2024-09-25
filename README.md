<img src="https://bannermd.airopi.dev/banner?title=Notion%20Map&desc=Embed%20a%20google%20map%20with%20pinpoints%20from%20your%20database!&repo=AiroPi/underwater-images-color-correction" width="100%" alt="banner"/>

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fvercel%2Fexamples%2Ftree%2Fmain%2Fpython%2Fflask&demo-title=Flask%20%2B%20Vercel&demo-description=Use%20Flask%202%20on%20Vercel%20with%20Serverless%20Functions%20using%20the%20Python%20Runtime.&demo-url=https%3A%2F%2Fflask-python-template.vercel.app%2F&demo-image=https://assets.vercel.com/image/upload/v1669994156/random/flask.png)

# Notion map

Notion map allows your to embed a google maps with pinpoints from a Notion database !

 <img width="751" alt="image" src="https://github.com/user-attachments/assets/890a1780-6ade-4149-8d4b-cc16e79c2886">

## How to use it

Clone the repo.
Edit the file inside pages/index.html to setup your own Google Maps api key. Deploy the website on Vercel. Setup your environ with:
```
DATABASE_SOURCE_ID
NOTION_API_KEY
```

The program will search for a column `Longitude` and `Latitude`.

Everything should works fine 👍

### Flask + Vercel

This example shows how to use Flask 2 on Vercel with Serverless Functions using the [Python Runtime](https://vercel.com/docs/concepts/functions/serverless-functions/runtimes/python).

