JSON Hydrographic Profile
=========================

```javascript
{
  "type": "c", // "c" for continuous, or "d" for discrete, for ODV purposes only
  "cruise": "some cruise", // probably an expocode
  "station": "some station id",
  "cast": "some cast id"
  "lat": 0, // Decimal degs north
  "lon": 0, // decimal degs east
  "elevation": -6000, // meters above sea level (completely avoid the whole "depth" issue)

  /*
    rfc3339 is quite strict (this is desired for date times) but we
    might also want to know how precise the reported time actually is
    for use when looking at processes of differing time scales.
  */
  "date": "2016-09-19T09:53:00Z", // an rfc3339 datetime
  "date_precision": 60, // decimal seconds for the most precise time reported

  "index_parameter": "SAMPNO",
  "index_unit": nil,
  "index_type": "string",
  "index_precision": nil, // how many decimal places (for comparing)

  "data_parameter": "OXYGEN",
  "data_unit": "umol kg-1"
  "data_type": "decimal"
  "data_precision": 3, // how many decimal places

  "index": [], // required but can be empty
  "data": [], // optional key, no null values allowed
  "confidence": [], // optional key,  no null values allowed, numeric between 0 and 1 with 1 being "perfect quality" data
  /* a proposed mapping
    woce_ctd:
      1: 0.8 [0.75, 0.9)
      2: 0.95 [0.9, 1]
      3: 0.5 [0.4, 0.75)
      4: 0.3 [0, 0.4)
      5: put index value into "missing"
      6: 0.90
      7: 0.85
      8: Not used
      9: Discard the index value
    woce_discrete:
      1: put index value into "awaiting"
      2: 0.95 [0.9, 1]
      3: 0.5 (0.4, 0.9)
      4: 0.3 [0, 0.4]
      5: put index value into "missing"
      6: 0.95 
      7: ??
      8: ??
      9: discard index value
    woce_bottle:
      1: 0.8 [0.75, 0.9)
      2: 0.95 [0.9, 1]
      3: 0.5 [0.4, 0.75)
      4: 0.3 [0, 0.4)
      5: Put index value into "missing"
      9: Discard index value

      This is a somewhat continuous scale with some mappings:
      woce:
      0          0.4             0.9         1
      |-----------|---------------|----------|
          bad       questionable     good
      Oceansites:
      0          0.4        0.7    0.9        1
      |-----------|----------|-----|----------|
          bad       os:4      os:2    os:1
      ODV:
      0          0.4        0.7    0.9        1
      |-----------|----------|-----|----------|
          odv:8       odv:4   odv:1    odv:0
  */

  "awaiting": [], // optional key, contains "index" values, equivalent to woce discrete flag 1
  "missing" [], // optional key, contains "index" values, equivalent to woce discrete flag 5

  "uncertainty": [], //optional key, must be same length as "index", has the units "data_unit", has precision "data_precision", has only positive values which are ± the values in "data"

  /* Structures under consideration */

  "citation": {
    "text": "", //some citation string (probably provided by the data origionator
    "doi": "" // if the profile has some doi...
  },

  "comments": "", // optional key, for humans, applies to the entire profile, cannot change the meaning of the rest of the object
  "index_comments": {
		// this object can have as many entries as there are in "index" + "awaiting" + "missing"
    "index": "comment" // "row level" comments for humans, applied to some specific index, "index" must be a string (cast) and appear in one of "index", "awaiting" or "missing", convert numbers to strings.
  },
  "legacy": {
      "sum": ???, // sumfile representation for this "cast", format TBD
      "woce_quality": {
				// this object can have as many entries as there are in "index" + "awaiting" + "missing"
				// the "_FLAG_W" for the data column from an exchange file, no information on flag definitions (just like a normal exchange file)
        "index": "quality flag" // where "index" must be in the columns of "index", "awaiting", or "missing", convert numbers to strings
      },
    },

  /// Really crazy idea...
  "history": {
      // a collection of patches with some extra information, with a
      // datetime string as the key of the object
      "rfc3339_datetime" : {
        "comment": "", // the why of the change
        "patch": [] // the patch of the change
      }
    }
  }
```
