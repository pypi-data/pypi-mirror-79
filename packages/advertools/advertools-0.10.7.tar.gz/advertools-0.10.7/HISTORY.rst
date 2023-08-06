=======================
Change Log - advertools
=======================

0.10.7 (2020-09-18)
-------------------

* Added
    - New function ``knowledge_graph`` for querying Google's API
    - Faster ``sitemap_to_df`` with threads
    - New parameter `max_workers` for ``sitemap_to_df`` to determine how fast
      it could go
    - New parameter `capitalize_adgroups` for ``kw_generate`` to determine
      whether or not to keep ad groups as is, or set them to title case (the
      default)

* Fixed
    - Remove restrictions on the number of URLs provided to ``crawl``,
      assuming `follow_links` is set to `False` (list mode)
    - JSON-LD issue breaking crawls when it's invalid (now skipped)

* Removed
    - Deprecate the ``youtube.guide_categories_list`` (no longer supported by
      the API)

0.10.6 (2020-06-30)
-------------------

* Added
    - JSON-LD support in crawling. If available on a page, JSON-LD items will
      have special columns, and multiple JSON-LD snippets will be numbered for
      easy filtering
* Changed
    - Stricter parsing for rel attributes, making sure they are in link
      elements as well
    - Date column names for ``robotstxt_to_df`` and ``sitemap_to_df`` unified
      as "download_date"
    - Numbering OG, Twitter, and JSON-LD where multiple elements are present in
      the same page, follows a unified approach: no numbering for the first
      element, and numbers start with "1" from the second element on. "element",
      "element_1", "element_2" etc.

0.10.5 (2020-06-14)
-------------------

* Added
    - New features for the ``crawl`` function:
        * Extract canonical tags if available
        * Extract alternate `href` and `hreflang` tags if available
        * Open Graph data "og:title", "og:type", "og:image", etc.
        * Twitter cards data "twitter:site", "twitter:title", etc.

* Fixed
    - Minor fixes to ``robotstxt_to_df``:
        * Allow whitespace in fields
        * Allow case-insensitive fields

* Changed
    - ``crawl`` now only supports `output_file` with the extension ".jl"
    - ``word_frequency`` drops `wtd_freq` and `rel_value` columns if `num_list`
      is not provided

0.10.4 (2020-06-07)
-------------------

* Added
    - New function ``url_to_df``, splitting URLs into their components and to a
      DataFrame
    - Slight speed up for ``robotstxt_test``

0.10.3 (2020-06-03)
-------------------

* Added
    - New function ``robotstxt_test``, testing URLs and whether they can be
      fetched by certain user-agents

* Changed
    - Documentation main page relayout, grouping of topics, & sidebar captions
    - Various documentation clarifications and new tests

0.10.2 (2020-05-25)
-------------------

* Added
    - User-Agent info to requests getting sitemaps and robotstxt files
    - CSS/XPath selectors support for the crawl function
    - Support for custom spider settings with a new parameter ``custom_settings``

* Fixed
    - Update changed supported search operators and values for CSE

0.10.1 (2020-05-23)
-------------------

* Changed
    - Links are better handled, and new output columns are available:
      ``links_url``, ``links_text``, ``links_fragment``, ``links_nofollow``
    - ``body_text`` extraction is improved by containing <p>, <li>, and <span>
      elements

0.10.0 (2020-05-21)
-------------------

* Added
    - New function ``crawl`` for crawling and parsing websites
    - New function ``robotstxt_to_df`` downloading robots.txt files into
      DataFrames

0.9.1 (2020-05-19)
------------------

* Added
    - Ability to specify robots.txt file for ``sitemap_to_df``
    - Ability to retreive any kind of sitemap (news, video, or images)
    - Errors column to the returnd DataFrame if any errors occur
    - A new ``sitemap_downloaded`` column showing datetime of getting the
      sitemap

* Fixed
    - Logging issue causing ``sitemap_to_df`` to log the same action twice
    - Issue preventing URLs not ending with xml or gz from being retreived
    - Correct sitemap URL showing in the ``sitemap`` column

0.9.0 (2020-04-03)
------------------

* Added
    - New function ``sitemap_to_df`` imports an XML sitemap into a
      ``DataFrame``

0.8.1 (2020-02-08)
------------------

* Changed
    - Column `query_time` is now named `queryTime` in the `youtube` functions
    - Handle json_normalize import from pandas based on pandas version

0.8.0 (2020-02-02)
------------------

* Added
    - New module `youtube` connecting to all GET requests in API
    - `extract_numbers` new function
    - `emoji_search` new function
    - `emoji_df` new variable containing all emoji as a DataFrame

* Changed
    - Emoji database updated to v13.0
    - `serp_goog` with expanded `pagemap` and metadata

* Fixed
    - `serp_goog` errors, some parameters not appearing in result
      df
    - `extract_numbers` issue when providing dash as a separator
      in the middle

0.7.3 (2019-04-17)
------------------

* Added
    - New function `extract_exclamations` very similar to
      `extract_questions`
    - New function `extract_urls`, also counts top domains and
      top TLDs
    - New keys to `extract_emoji`; `top_emoji_categories`
      & `top_emoji_sub_categories`
    - Groups and sub-groups to `emoji db`

0.7.2 (2019-03-29)
------------------

* Changed
    - `Emoji regex` updated
    - Simpler extraction of Spanish `questions`

0.7.1 (2019-03-26)
------------------

* Fixed
    - Missing __init__ imports.

0.7.0 (2019-03-26)
------------------

* Added
    - New `extract_` functions:

      * Generic `extract` used by all others, and takes
        arbitrary regex to extract text.
      * `extract_questions` to get question mark statistics, as
        well as the text of questions asked.
      * `extract_currency` shows text that has currency symbols in it, as
        well as surrounding text.
      * `extract_intense_words` gets statistics about, and extract words with
        any character repeated three or more times, indicating an intense
        feeling (+ve or -ve).

    - New function `word_tokenize`:
      
      * Used by `word_frequency` to get tokens of
        1,2,3-word phrases (or more).
      * Split a list of text into tokens of a specified number of words each.

    - New stop-words from the ``spaCy`` package:

      **current:** Arabic, Azerbaijani, Danish, Dutch, English, Finnish,
      French, German, Greek, Hungarian, Italian, Kazakh, Nepali, Norwegian,
      Portuguese, Romanian, Russian, Spanish, Swedish, Turkish.

      **new:** Bengali, Catalan, Chinese, Croatian, Hebrew, Hindi, Indonesian,
      Irish, Japanese, Persian, Polish, Sinhala, Tagalog, Tamil, Tatar, Telugu,
      Thai, Ukrainian, Urdu, Vietnamese

* Changed
    - `word_frequency` takes new parameters:
        * `regex` defaults to words, but can be changed to anything '\S+'
          to split words and keep punctuation for example.

        * `sep` not longer used as an option, the above `regex` can
          be used instead

        * `num_list` now optional, and defaults to counts of 1 each if not
          provided. Useful for counting `abs_freq` only if data not
          available.

        * `phrase_len` the number of words in each split token. Defaults
          to 1 and can be set to 2 or higher. This helps in analyzing phrases
          as opposed to words.

    - Parameters supplied to `serp_goog` appear at the beginning
      of the result df
    - `serp_youtube` now contains `nextPageToken` to make
      paginating requests easier

0.6.0 (2019-02-11)
------------------

* New function
    - `extract_words` to extract an arbitrary set of words
* Minor updates
    - `ad_from_string` slots argument reflects new text
      ad lenghts
    - `hashtag` regex improved

0.5.3 (2019-01-31)
------------------

* Fix minor bugs
    - Handle Twitter search queries with 0 results in final request

0.5.2 (2018-12-01)
------------------

* Fix minor bugs
    - Properly handle requests for >50 items (`serp_youtube`)
    - Rewrite test for _dict_product
    - Fix issue with string printing error msg

0.5.1 (2018-11-06)
------------------

* Fix minor bugs
    - _dict_product implemented with lists
    - Missing keys in some YouTube responses

0.5.0 (2018-11-04)
------------------

* New function `serp_youtube`
    - Query YouTube API for videos, channels, or playlists
    - Multiple queries (product of parameters) in one function call
    - Reponse looping and merging handled, one DataFrame 
* `serp_goog` return Google's original error messages
* twitter responses with entities, get the entities extracted, each in a
  separate column


0.4.1 (2018-10-13)
------------------

* New function `serp_goog` (based on Google CSE)
    - Query Google search and get the result in a DataFrame
    - Make multiple queries / requests in one function call
    - All responses merged in one DataFrame
* twitter.get_place_trends results are ranked by town and country

0.4.0 (2018-10-08)
------------------

* New Twitter module based on twython
    - Wraps 20+ functions for getting Twitter API data
    - Gets data in a pands DataFrame
    - Handles looping over requests higher than the defaults
* Tested on Python 3.7

0.3.0 (2018-08-14)
------------------

* Search engine marketing cheat sheet.
* New set of extract\_ functions with summary stats for each:
    * extract_hashtags
    * extract_mentions
    * extract_emoji
* Tests and bug fixes

0.2.0 (2018-07-06)
------------------

* New set of kw_<match-type> functions.
* Full testing and coverage. 

0.1.0 (2018-07-02)
------------------

* First release on PyPI.
* Functions available:
    - ad_create: create a text ad place words in placeholders
    - ad_from_string: split a long string to shorter string that fit into
        given slots
    - kw_generate: generate keywords from lists of products and words
    - url_utm_ga: generate a UTM-tagged URL for Google Analytics tracking
    - word_frequency: measure the absolute and weighted frequency of words in
        collection of documents
