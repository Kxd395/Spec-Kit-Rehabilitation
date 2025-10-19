"""HTTP client configuration for Specify CLI."""

import ssl
import httpx
import truststore

ssl_context = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
client = httpx.Client(verify=ssl_context)
