# PDF Text Extraction Using OpenAI

## Usage

Add OpenAI key to the .env file as such:

```
OPENAI_API_KEY="API_KEY_GOES_HERE"
```

Run `python main.py`. This assumes the PDF is in this directory under the name `memorandum.pdf`.

## Notes

The extraction takes place in two phases largely.

I'm assuming that any memorandum would have an underwrite section, though I'm not super familiar with the space. Therefore, the extraction prioritizes fetching numbers such as rent, purchase price, etc, from this section.

The extraction then goes through any pages/slides with "summary" or "memorandum" to fetch other values.

I wanted to avoid chunking the entire PDF and running every page through ChatGPT. Although that probably would have worked fine, I wanted to be cost-conscious, and also I felt like that would have been less interesting. I instead chose to find slides that had keywords that indicated that they were important.

This program also does some basic type checking. I kept it pretty bare bones for this example, I would certainly flesh it out further in a production app, but I think it's a good example of sanity checking the LLM and making sure values are logically consistent.
