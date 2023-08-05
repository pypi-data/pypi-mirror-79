# pymsresearch

## Introduction

Microsoft Academic Research query and the entity result is very compliated with a 
lot of abbrivations. 

This package is to parse the query and the returned result to human readable results.

## Usage

```
    api_key = ""
    from researchacademic import ResearchAcademic as RA
    from researchacademic import EntityParser as EP
   
    ra = RA(api_key)

    result = ra.evaluate(query, timeout=5)
    print(result)
```


## Test

```
	MICROSOFT_API_KEY="" python researchacademic/test_fetcher.py
```
