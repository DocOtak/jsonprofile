JSON Hydrographic Profile
=========================

Perhaps this should just be renamed to CCHDO-IR (for internal
representation)... The citation information will be critical to the
success of this I think. So I need to put some extra thought into making
this section nice... more than one author seperately listed? support for
links in the citation, only one DOI?

```javascript
{
  "type": "d", // "c" for continuous, or "d" for discrete, for ODV purposes only
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
  "date_uncertainty": 10800, // decimal seconds for range of possible times this profile may be, for almost all CCHDO profiles this will be around 10800 seconds (±3 hours)

  // parameters names will probably just be "cchdo" ones, but can be
  // anything, the only requirement is to be "intercomparable"
  // (depenidng on units)
  "index_parameter": "SAMPNO",
  "index_unit": nil, // udunits compatable
  "index_scale": nil, // optional, a string which provides calibration information, e.g. PSS-78, ITS-90
  "index_type": "string",
  "index_precision": nil, // how many decimal places (for comparing)
  "index_standard_name": "", // optional, must have value, if available, the CF standard name

  "data_parameter": "OXYGEN",
  "data_unit": "umol kg-1" // udunits compatible requried (e.g. "PSU" Salinity has units of nothing or 1)
  "data_scale": nil, // optional, a string which provides calibration information, e.g. PSS-78, ITS-90
  "data_type": "decimal"
  "data_precision": 3, // how many decimal places
  "data_standard_name": "", // optional, must have value, if available, the CF standard name

  "index": [], // optional key, cannot be empty (must have at least one value or be omitted)
  "data": [], // optional key, no null values allowed, must be same length as "index", omitted if empty
  "masks": { // optional key, must have keys with arrays the same length as index, contains data masks to exclude points for various reasons, for space reasons, 1 and 0 vs true an false
    /// some examples (should we define what masks can be in here?):
    "oxyfit":[0,0,1,0],  // note that because it is a mask, a true value will EXCLUDE the indicated data point
    "bad": [0,0,1,0],
    "questionable": [0,1,1,0] //should probably incldue "bad" data as questionable as well
  }

  "awaiting": [], // optional key, contains "index" values, equivalent to woce discrete flag 1
  "missing" [], // optional key, contains "index" values, equivalent to woce discrete flag 5

  "uncertainty": [], //optional key, must be same length as "index", has the units "data_unit", has precision "data_precision", has only positive values which are ± the values in "data"
  "uncertainty_neg": [] // optional key, must only be present when "uncertainty" is also present, may only contain positive values which represent the unvertanty in the "minus" direction


  "citation": {
    "name": "" // The name of the person/PI responsible for this profile
    "text": "", //some citation string (probably provided by the data origionator
    "doi": "" // if the profile has some doi...
  },

  "comments": "", // optional key, for humans, applies to the entire profile, cannot change the meaning of the rest of the object
  "index_comments": {
		// this object can have as many entries as there are in "index" + "awaiting" + "missing"
    "index": "comment" // "row level" comments for humans, applied to some specific index, "index" must be a string (cast) and appear in one of "index", "awaiting" or "missing", convert numbers to strings using index_precision as a truncation length.
  },
  "legacy": {
      "sum": ???, // sumfile representation for this "cast", format TBD
      "woce_quality": {
				// this object can have as many entries as there are in "index" + "awaiting" + "missing"
				// the "_FLAG_W" for the data column from an exchange file, no information on flag definitions (just like a normal exchange file)
        "index": "quality flag" // where "index" must be in the columns of "index", "awaiting", or "missing", convert numbers to strings
      },
      "excahnge_footer": "", // anything that comes after the "END_DATA"
    },

  /// Really crazy idea...
  // probably stored seperatly in a database and populated on demand
  "history": {
      // a collection of patches with some extra information, with a
      // datetime string as the key of the object
      "rfc3339_datetime" : {
        "comment": "", // the why of the change
        "patch": [] // a reverse patch of the change (applying this patch rolls the change back)
      }
    }
  }
```
