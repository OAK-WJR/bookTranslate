# bookTranslate

Turns kindergarten picture-book slideshows into page-by-page translations, so that parents who are still learning English can read the same books as their children.

I wrote these scripts in February–April 2023 and cleaned them up for publication in October 2026 (see [History](#history)).

**[See it work](https://oak-wjr.github.io/bookTranslate/)** on *Denslow's Three Bears* (1903), a public-domain picture book: every page as the scripts read it, in English and 8 translations ([1-minute video](https://oak-wjr.github.io/bookTranslate/demo.mp4)). The pages were made into a slideshow and run through the three scripts below; `demo/` has the two small scripts that built the demo.

## How it works

1. `pptxTJpg.py` copies the pictures out of each `.pptx` slideshow, one folder per book.
2. `translateTest.py` reads the English text on every page with Google Cloud Vision. It keeps every line longer than eight characters and, from shorter lines, only common, correctly spelled words. Then it translates each page into Simplified and Traditional Chinese, Russian, Korean, Japanese, Spanish, German and French with the Cloud Translation API.
3. `kBsExcel.py` puts the original text and all translations side by side in an Excel file, one sheet per book.

Translations are powered by Google Translate, through the [Cloud Translation API](https://cloud.google.com/translate). Every sheet starts with the "powered by Google Translate" badge and Google's disclaimer.

## Running it

You need Python 3.10, the [Google Cloud CLI](https://cloud.google.com/sdk/docs/install) (or a key file, see below) and a Google Cloud project with billing and the Cloud Vision and Cloud Translation APIs turned on.

```sh
pip install -r requirements.txt
gcloud auth application-default login
gcloud auth application-default set-quota-project YOUR_PROJECT_ID
python pyFile/pptxTJpg.py SLIDESHOWS_FOLDER PICTURES_FOLDER
python pyFile/translateTest.py PICTURES_FOLDER
python pyFile/kBsExcel.py PICTURES_FOLDER translations.xls
```

Instead of signing in, you can set `GOOGLE_APPLICATION_CREDENTIALS` to a key file. Never commit keys or credential files.

Both APIs are paid services with free monthly amounts. Cloud Translation counts each target language separately, so a page translated into 8 languages counts 8 times. Setting a lower daily Cloud Translation quota in the Cloud console caps how much can be translated each day. If a run stops because the quota is used up, run it again the next day: finished books and languages are skipped. To redo a book, delete its `translation-*.txt` files.

## Limits

- The text read from the pictures and the machine translations should be checked by a person before they are shared.
- Only translate and share books you have the rights to.
- The first picture of each slideshow is skipped.

## History

The 2023 commits are the original work, and the next commit holds the April 2023 changes that were never committed at the time. In this public copy, private details and some code are left out, and Chinese text has been translated into English; commit dates and author names are unchanged. In October 2026 I cleaned the project up for publication: arguments instead of hard-coded paths, bug fixes, this README, the license and the demo. The free translation service the 2023 scripts used no longer works reliably, so the scripts now translate with Google's Cloud Translation API. Later I plan to add my own translation model.

## License

[PolyForm Noncommercial 1.0.0](LICENSE). Third-party material, such as the Google Translate badges and the public-domain demo book, is listed in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) and keeps its own terms.
