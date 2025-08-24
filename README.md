Плагин Calibre для Flibusta OPDS (flibusta.is)
==============================================

Данный плагин интегрирует каталог Flibusta OPDS (flibusta.is) в Calibre, позволяя искать и скачивать книги напрямую из библиотеки Флибуста.

## Возможности

- Поиск книг по названию, автору или ключевым словам
- Прямое скачивание в нескольких форматах (FB2, EPUB, MOBI, PDF, TXT)
- Книги без DRM-защиты
- Коллекция книг на русском языке
- Простая интеграция с интерфейсом магазинов Calibre

## Установка:

Скачайте плагин [отсюда](https://github.com/Zypresse/flibusta-calibre-opds-store/releases/tag/v1.0)

Перейдите в: 

  ```Настройки > Дополнительно > Плагины > Загрузить плагин из файла```
  
Выберите скачанный zip-архив плагина.

## Использование

1. После установки перезапустите Calibre
2. Перейдите в "Получить книги" и выберите магазин "Флибуста"
3. Ищите книги, используя русские или английские термины
4. Скачивайте книги напрямую в вашу библиотеку Calibre

## Технические детали

- Использует OPDS конечную точку flibusta.is: `https://flub.flibusta.is/opds/search`
- Поддерживает несколько форматов книг
- Правильно обрабатывает кодировку кириллицы
- Совместим с современными версиями Calibre (3.0+)

## Изменения в v1.1

- Обновлено для использования домена flibusta.is вместо flibusta.appspot.com
- Улучшен парсинг OPDS-каналов
- Лучшая обработка ошибок и поддержка кодировки
- Расширенное извлечение метаданных

---

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

