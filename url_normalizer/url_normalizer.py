"""This Code Hasn't Been Tested Yet!"""

from urllib.parse import urlparse, urlunparse, parse_qs, urlencode
import re

def normalize_url(url: str,
                  remove_trailing_slash: bool = False,
                  sort_query_params: bool = True,
                  remove_empty_query_params: bool = True,
                  lowercase_path: bool = False) -> str:
    """
    Normalizes a URL for consistent identification, especially useful for web scraping.

    Args:
        url (str): The URL string to normalize.
        remove_trailing_slash (bool): If True, removes a trailing slash from the path.
                                      Use with caution, as some servers treat /path and /path/ differently.
        sort_query_params (bool): If True, sorts query parameters alphabetically by key.
                                  e.g., ?b=2&a=1 becomes ?a=1&b=2
        remove_empty_query_params (bool): If True, removes query parameters with empty values.
                                          e.g., ?a=1&b=&c=2 becomes ?a=1&c=2
        lowercase_path (bool): If True, converts the URL path to lowercase.
                               Use with extreme caution, as paths are generally case-sensitive.
                               Only set to True if you are certain the target server is case-insensitive for paths.

    Returns:
        str: The normalized URL.
    """
    if not url:
        return ""

    parsed = urlparse(url)

    # 1. Scheme and Netloc (Domain/Port): Always lowercase
    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()

    # Remove default ports (80 for http, 443 for https)
    if (scheme == 'http' and netloc.endswith(':80')) or \
       (scheme == 'https' and netloc.endswith(':443')):
        netloc = netloc.rsplit(':', 1)[0]

    # 2. Path: Normalize and optionally lowercase
    path = parsed.path
    # Remove duplicate slashes (e.g., /path//to -> /path/to)
    path = re.sub(r'/{2,}', '/', path)

    if remove_trailing_slash and path.endswith('/') and len(path) > 1:
        path = path.rstrip('/')

    if not path: # Ensure path is at least '/' if empty
        path = '/'
    elif not path.startswith('/'): # Ensure path starts with '/'
        path = '/' + path

    if lowercase_path:
        path = path.lower()

    # 3. Query Parameters: Parse, sort, and re-encode
    query_params = parse_qs(parsed.query, keep_blank_values=True)
    if remove_empty_query_params:
        query_params = {k: [v for v in values if v] for k, values in query_params.items()}
        # Remove keys if all values are empty after filtering
        query_params = {k: v for k, v in query_params.items() if v}

    if sort_query_params:
        # Sort by key, and then by value if multiple values for a key (list comprehension to handle)
        sorted_items = []
        for key in sorted(query_params.keys()):
            values = sorted(query_params[key]) # Sort values for consistency if multiple
            for val in values:
                sorted_items.append((key, val))
        query = urlencode(sorted_items, doseq=True) # doseq=True handles multiple values for same key
    else:
        # Re-encode original order but still clean
        query = urlencode([(k, v_item) for k, v_list in query_params.items() for v_item in v_list], doseq=True)


    # 4. Fragment: Always remove for visited tracking
    fragment = "" # Always clear fragment for visited tracking

    # Reconstruct the URL
    normalized_url = urlunparse((scheme, netloc, path, parsed.params, query, fragment))

    return normalized_url

# --- Test Cases ---
if __name__ == "__main__":
    print("--- Default Normalization (Fragment removal, sorting queries) ---")
    print(f"Original: http://example.com/ProductA#section1")
    print(f"Normalized: {normalize_url('http://example.com/ProductA#section1')}\n") # Path casing preserved

    print(f"Original: HTTP://WWW.EXAMPLE.COM:80/path//to/?b=2&a=1&#fragment")
    print(f"Normalized: {normalize_url('HTTP://WWW.EXAMPLE.COM:80/path//to/?b=2&a=1&#fragment')}\n")

    print(f"Original: https://site.com/page?param1=value1&param3=&param2=value2")
    print(f"Normalized: {normalize_url('https://site.com/page?param1=value1&param3=&param2=value2')}\n")

    print(f"Original: https://site.com/page?param=&param2=value2&param1=")
    print(f"Normalized: {normalize_url('https://site.com/page?param=&param2=value2&param1=')}\n")

    print("\n--- With remove_trailing_slash=True (Use with caution!) ---")
    print(f"Original: http://example.com/path/")
    print(f"Normalized: {normalize_url('http://example.com/path/', remove_trailing_slash=True)}\n")

    print("\n--- With lowercase_path=True (Use with extreme caution!) ---")
    print(f"Original: http://example.com/ProductA")
    print(f"Normalized: {normalize_url('http://example.com/ProductA', lowercase_path=True)}\n")

    print(f"Original: http://example.com/productA")
    print(f"Normalized: {normalize_url('http://example.com/productA', lowercase_path=True)}\n")

    # Example for visited set using the normalizer
    print("\n--- Using Normalizer with a Visited Set ---")
    visited_pages = set()
    urls_to_scrape = [
        "https://example.com/Page1#top",
        "https://example.com/Page1", # Different casing
        "https://example.com/page1", # Canonical casing
        "https://example.com/products?id=123&sort=name",
        "https://example.com/products?sort=name&id=123", # Same query params, different order
        "https://example.com/products?sort=name&id=123&#frag" # Same with fragment
    ]

    for url in urls_to_scrape:
        normalized = normalize_url(url) # Using default options for path casing

        if normalized not in visited_pages:
            print(f"  Scraping: {url} -> Normalized: {normalized}")
            visited_pages.add(normalized)
            # Perform actual HTTP request and content processing here
        else:
            print(f"  Already visited (via {url}): {normalized}")

    print(f"\nFinal visited set size: {len(visited_pages)}")
    print(f"Final visited set: {visited_pages}")