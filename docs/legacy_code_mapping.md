# Legacy Code Mapping

Historical Scopus-related workflows were reviewed only for reusable design patterns: author-affiliation parsing, author-publication indexing, city-year collection, retry/resume manifests, source comparison, and cognitive proximity over subject profiles.

New public modules reimplement those patterns in `src/scopus_toolkit/` using English module names, type annotations, synthetic fixtures, and mock transport.

Excluded content includes enterprise data, patent code, network models, mobility models, regression scripts, geospatial project stages, night-light workflows, manuscript tables, manuscript figures, private paths, credentials, real data, and API caches.
