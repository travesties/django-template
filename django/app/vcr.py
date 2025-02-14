import vcr

# VCR instance for use in tests within the app
app_vcr = vcr.VCR(
    cassette_library_dir="app/vcr_cassettes",
    filter_headers=["Vendor-API-Key"],
)
