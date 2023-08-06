# dataset Creator

This package help to download multiple images in order to build an image dataset.

The used search engine is Bing Image Search API

## Usage

First you need to get an [api key](https://azure.microsoft.com/en-us/try/cognitive-services/my-apis/?api=bing-image-search-api)

Then creat an env file here an empty template

    # Api key
    API_KEY=<Your api key go here>
    # Api url
    URL="https://api.cognitive.microsoft.com/bing/v7.0/images/search"
    # Output image folder name
    OUTPUT_FOLDER=random
    # The maximum number of results for a given search
    MAX_RESULTS=100
    # How many images to download
    GROUP_SIZE=50


