JSON Hydrographic Profile
=========================

```javascript
{
  "type": "c", // "c" for continious, or "d" for descrete, for ODV purposes only
  "cruise": "some cruise",
  "station": "some station",
  "cast": "some cast"
  "lat": 0, // Decimal degs north
  "lon": 0, // decimal degs east

  /*
    rfc3339 is quite strict (this is desired for date times) but we
    might also want to know how precise the reported time actually is
    for use when looking at processess of differing time scales.
  */
  "date": "rfc3339",
  "date_precision": 60, // deciaml seconds for the most precise time reported

  "quality_defintions": {
    "value": "definition"
  },

  "index_parameter": "SAMPNO",
  "index_unit": nil,
  "index_type": "string",
  "data_parameter": "OXYGEN",
  "data_unit": "umol kg-1"
  "data_type": "decimal"
  "data_precision": 3, // how many decimal places

  "index": [], // required but can be empty
  "data": [], // optional key, no null values allowed
  "quality: [], // optional key,  no null values allowed

  "awaiting": [], // optional key, containins "index" values, equivalent to woce descrete flag 1
  "missing" [] // optional key, contains "index" calues, euivalent to woce discrete flag 5
  }
```
