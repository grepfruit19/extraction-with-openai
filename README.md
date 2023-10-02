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
