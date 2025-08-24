Calibre plugin for Flibusta OPDS (flibusta.is)
===============================================

This plugin integrates the Flibusta OPDS catalog (flibusta.is) into Calibre, allowing you to search and download books directly from the Flibusta library.

## Features

- Search books by title, author, or keywords
- Direct download in multiple formats (FB2, EPUB, MOBI, PDF, TXT)
- DRM-free books
- Russian language book collection
- Simple integration with Calibre's store interface

## Installation:

Download it from [here](https://github.com/Zypresse/flibusta-calibre-opds-store/releases/tag/v1.0)

Go to: 

  ```Preferences > Advanced > Plugins > Load plugin from file```
  
Choose downloaded plugin zip archive.

## Usage

1. After installation, restart Calibre
2. Go to "Get books" and select "Флибуста" store
3. Search for books using Russian or English terms
4. Download books directly to your Calibre library

## Technical Details

- Uses flibusta.is OPDS endpoint: `https://flub.flibusta.is/opds/search`
- Supports multiple book formats
- Handles Cyrillic text encoding properly
- Compatible with modern Calibre versions (3.0+)

## Changes in v1.1

- Updated to use flibusta.is domain instead of flibusta.appspot.com
- Improved OPDS feed parsing
- Better error handling and encoding support
- Enhanced metadata extraction

